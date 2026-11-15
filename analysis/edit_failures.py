"""Why did each failed edit_file call fail? (#126)

For every `edit_file` call that failed with "old_string not found" in a set of trace folders, compare its `old_string`
with everything the agent had seen of the repository in that trace so far (`read_file` output, `run_command` output,
with its earlier successful edits applied) and give one cause:

    seen_yet_failed   the exact text was in what it read (the file changed since, or a tool quirk)
    whitespace_only   it matches once runs of whitespace are made equal
    backslash_only    it matches once doubled backslashes are undone (or done)
    near_copy         a block it read is at least 95% alike: characters dropped or changed in copying
    paraphrase        a block it read is 80% to 95% alike: lines rewritten from memory
    not_read          nothing it read is that close: invented, or never read

The result holds ids, counts and causes only, never task text or code, since the traces hold the competition's tasks.

    python analysis/edit_failures.py <trace dirs...> --out analysis/edit_failures.csv
"""

from __future__ import annotations

import argparse
import csv
import difflib
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

CLASSES = ("seen_yet_failed", "whitespace_only", "backslash_only", "near_copy", "paraphrase", "not_read")
NEAR, CLOSE = 0.95, 0.80


def _ws(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def _best_ratio(old: str, seen: str) -> float:
    """The highest similarity between old and any block of seen with the same number of lines."""
    lines = seen.splitlines()
    n = max(1, old.count("\n") + 1)
    best = 0.0
    for i in range(max(1, len(lines) - n + 1)):
        sm = difflib.SequenceMatcher(None, old, "\n".join(lines[i:i + n]), autojunk=False)
        if sm.real_quick_ratio() > best and sm.quick_ratio() > best:
            best = max(best, sm.ratio())
    return best


def classify(old_string: str, seen: str) -> str:
    """One of CLASSES for a failed edit's old_string against what the agent had seen."""
    if not seen.strip():
        return "not_read"
    if old_string in seen:
        return "seen_yet_failed"
    if _ws(old_string) and _ws(old_string) in _ws(seen):
        return "whitespace_only"
    if "\\" in old_string and (old_string.replace("\\\\", "\\") in seen or old_string.replace("\\", "\\\\") in seen):
        return "backslash_only"
    r = _best_ratio(old_string, seen)
    return "near_copy" if r >= NEAR else "paraphrase" if r >= CLOSE else "not_read"


def _content(observation) -> dict:
    c = observation.get("content") if isinstance(observation, dict) else None
    if isinstance(c, str):
        try:
            d = json.loads(c)
            return d if isinstance(d, dict) else {"content": c}
        except ValueError:
            return {"content": c}
    return {}


def failures(trace_dirs: list[Path]) -> list[dict]:
    """One row per failed edit_file call in the traces (trace_*.json) under the given folders; a trace found twice is
    counted once."""
    seen_hashes, rows = set(), []
    for root in trace_dirs:
        for p in sorted(Path(root).rglob("trace_*.json")):
            h = hashlib.sha256(p.read_bytes()).hexdigest()
            if h in seen_hashes:
                continue
            seen_hashes.add(h)
            instance_id = p.stem.removeprefix("trace_")
            files: dict[str, str] = {}
            pool = ""
            for step in json.loads(p.read_text())["steps"]:
                for call in step.get("tool_calls") or []:
                    fn, args = call.get("function_name"), call.get("arguments") or {}
                    out = _content(step.get("observation") or {})
                    path = str(args.get("filepath") or "")
                    if fn == "read_file":
                        files[path] = files.get(path, "") + "\n" + str(out.get("content", ""))
                    elif fn == "run_command":
                        pool += "\n" + str(out.get("stdout") or out.get("output") or out.get("content") or "")
                    elif fn == "edit_file":
                        old = args.get("old_string") or ""
                        failed = "old_string not found" in json.dumps(out) or "FileEditError" in json.dumps(out)
                        if not failed:
                            if path in files and old:
                                files[path] = files[path].replace(old, args.get("new_string", ""), 1)
                            continue
                        text = files.get(path) or next((v for k, v in files.items()
                                                        if k.endswith(path) or path.endswith(k)), "")
                        rows.append({"run_name": Path(root).name, "instance_id": instance_id,
                                     "old_string_line_count": old.count("\n") + 1 if old else 0,
                                     "has_backslash": "\\" in old,
                                     "failure_class_code": classify(old, text + "\n" + pool)})
    return rows


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("trace_dirs", nargs="+", type=Path)
    ap.add_argument("--out", type=Path)
    a = ap.parse_args(argv)
    rows = failures(a.trace_dirs)
    if a.out:
        with open(a.out, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["run_name", "instance_id", "old_string_line_count", "has_backslash",
                                              "failure_class_code"])
            w.writeheader()
            w.writerows(rows)
    counts = Counter(r["failure_class_code"] for r in rows)
    print(f"{len(rows)} failed edits")
    for c in CLASSES:
        print(f"  {counts[c]:4d}  {c}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
