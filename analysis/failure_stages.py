"""Where did each development task-run fail? (#147)

For each trace under the given run folders, against the files the task's reference patch changes (test files left
out), one stage:

    localize          never read a file the fix changes
    edit              read one, but no edit went through
    complete          an edit went through, but the submitted patch is empty
    patch_wrong_file  a patch that touches none of the files the fix changes
    patch_right_file  a patch on a file the fix changes, tests still fail
    resolved          the evaluator's tests pass

The result holds ids, run names, stages and counts only, never task text or code (the traces hold the competition's
tasks).

    python analysis/failure_stages.py <run dirs...> --tasks <tasks.jsonl> --out analysis/failure_stages.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path

STAGES = ("localize", "edit", "complete", "patch_wrong_file", "patch_right_file", "resolved")
_FILE = re.compile(r"^\+\+\+ b/(\S+)", re.M)
_TEST = re.compile(r"(^|/)(tests?/|test_)")


def gold_files(patch: str) -> set[str]:
    return {f for f in _FILE.findall(patch) if not _TEST.search(f)}


def _hit(gold: set[str], paths: set[str]) -> bool:
    return any(p and (g.endswith(p) or p.endswith(g)) for g in gold for p in paths)


def stage_of(gold: set[str], read: set[str], edited: set[str], patch_files: set[str], resolved: bool) -> str:
    """One of STAGES for one task-run."""
    if resolved:
        return "resolved"
    if patch_files:
        return "patch_right_file" if _hit(gold, patch_files) else "patch_wrong_file"
    if edited:
        return "complete"
    return "edit" if _hit(gold, read) else "localize"


def _observation(step: dict) -> str:
    return json.dumps((step.get("observation") or {}).get("content"))


def stages(run_dirs: list[Path], tasks_path: Path) -> list[dict]:
    tasks = {json.loads(line)["instance_id"]: json.loads(line) for line in open(tasks_path) if line.strip()}
    rows = []
    for run in run_dirs:
        for trace in sorted(Path(run).rglob("trace_*.json")):
            iid = trace.stem.removeprefix("trace_")
            if iid not in tasks:
                continue
            gold = gold_files(tasks[iid]["patch"])
            read, edited, n, first_edit = set(), set(), 0, None
            for step in json.loads(trace.read_text())["steps"]:
                obs = _observation(step)
                for call in step.get("tool_calls") or []:
                    n += 1
                    fn, args = call.get("function_name"), call.get("arguments") or {}
                    path = str(args.get("filepath") or args.get("path") or "").replace("/workspace/", "")
                    if fn == "read_file":
                        read.add(path)
                    elif fn == "run_command":
                        read |= {g for g in gold if g in json.dumps(args)}
                    elif fn in ("edit_file", "write_file") and not any(
                            s in obs for s in ("Error", "not found", "occurs")):
                        edited.add(path)
                        first_edit = first_edit or n
            result_path = trace.parents[2] / "result.json"
            result = json.loads(result_path.read_text()) if result_path.exists() else {}
            verification = result.get("verification") or {}
            resolved = bool(isinstance(verification, dict) and verification.get("is_resolved"))
            rows.append({"run_name": Path(run).name, "instance_id": iid,
                         "failure_stage_code": stage_of(gold, read, edited,
                                                        set(_FILE.findall(result.get("patch") or "")), resolved),
                         "tool_call_count": n, "first_edit_call_num": first_edit})
    return rows


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("run_dirs", nargs="+", type=Path)
    ap.add_argument("--tasks", type=Path, required=True)
    ap.add_argument("--out", type=Path)
    a = ap.parse_args(argv)
    rows = stages(a.run_dirs, a.tasks)
    if a.out:
        with open(a.out, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]) if rows else ["run_name"])
            w.writeheader()
            w.writerows(rows)
    by_run: dict[str, Counter] = {}
    for r in rows:
        by_run.setdefault(r["run_name"], Counter())[r["failure_stage_code"]] += 1
    total = sum(by_run.values(), Counter())
    print("run".ljust(24) + "".join(s.rjust(18) for s in STAGES))
    for name, c in list(by_run.items()) + [("ALL", total)]:
        print(name.ljust(24) + "".join(str(c[s]).rjust(18) for s in STAGES))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
