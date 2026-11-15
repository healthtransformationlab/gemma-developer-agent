"""Synthetic copy-error test of the edit-fallback skill's edit.py across the development set's four repositories
(#122). CPU only.

For each reference-patch hunk in a non-test .py file: SEARCH = the hunk's old lines (removed lines plus up to two
context lines each side), REPLACE = its new lines; the expected file is the base file with that hunk applied. Each
SEARCH/REPLACE is then damaged the ways real failed edits were, and both edit_file's matcher
(swegemma.edit.apply_replacement) and edit.py are scored: correct (file == expected), wrong (changed, not expected),
refused (unchanged).

Needs the harness's swegemma package (for edit_file's matcher) and local clones of the four public repositories. Set
MAX_FUZZY_LINES to override edit.py's length check (the study ran 8, the default, and 1000, none). Writes one row per
damaged hunk: ids, counts and outcomes only, no competition data.

usage: fallback_synth.py <tasks.jsonl> <dir holding clones named fastapi, rich, requests, httpx> <out.csv>
"""
import csv
import importlib.util
import json
import os
import random
import re
import subprocess
import sys
import time
from pathlib import Path

from swegemma.edit import apply_replacement  # the harness's own edit_file matcher

sys.dont_write_bytecode = True   # no __pycache__ in skills/: a .pyc in the submission is refused
_spec = importlib.util.spec_from_file_location(
    "fallback_edit", Path(__file__).resolve().parents[1] / "skills" / "edit-fallback" / "scripts" / "edit.py")
fb_edit = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fb_edit)
fb_edit.MAX_FUZZY_LINES = int(os.environ.get("MAX_FUZZY_LINES", fb_edit.MAX_FUZZY_LINES))

REPO_DIR = {"fastapi/fastapi": "fastapi", "Textualize/rich": "rich", "psf/requests": "requests",
            "encode/httpx": "httpx",
            # this organisation's repositories (the generality check; the competition's development set decides)
            "healthtransformationlab/health-transformation-lab-nlp": "health-transformation-lab-nlp",
            "healthtransformationlab/pipeline-doctor": "pipeline-doctor",
            "healthtransformationlab/gemma-developer-agent": "gemma-developer-agent",
            "getcommunityone/open-navigator": "open-navigator"}
TEST = re.compile(r"(^|/)(tests?|testing)/|(^|/)test_[^/]*\.py$|_test\.py$|(^|/)conftest\.py$")


def git_show(repo, commit, path):
    r = subprocess.run(["git", "-C", str(repo), "show", f"{commit}:{path}"], capture_output=True)
    return r.stdout.decode("utf-8", "replace") if r.returncode == 0 else None


def hunks(patch):
    """(path, old_lines, new_lines, old_start) per hunk, trimmed to at most 2 context lines around the change."""
    out, path = [], None
    lines = patch.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r"^\+\+\+ b/(\S+)", line)
        if m:
            path = m.group(1)
            i += 1
            continue
        m = re.match(r"^@@ -(\d+)", line)
        if m and path and path.endswith(".py") and not TEST.search(path):
            start = int(m.group(1))
            body = []
            i += 1
            while i < len(lines) and not lines[i].startswith(("@@", "diff ", "--- ", "+++ ")):
                body.append(lines[i])
                i += 1
            body = [b for b in body if not b.startswith("\\")]
            changed = [k for k, b in enumerate(body) if b[:1] in "+-"]
            if not changed:
                continue
            lo, hi = max(0, changed[0] - 2), min(len(body), changed[-1] + 3)
            seg = body[lo:hi]
            old = [b[1:] for b in seg if b[:1] in " -"]
            new = [b[1:] for b in seg if b[:1] in " +"]
            skipped_old = sum(1 for b in body[:lo] if b[:1] in " -")
            out.append((path, old, new, start + skipped_old))
            continue
        i += 1
    return out


def damage(kind, old, new, rng, other):
    """(search, replace) damaged as `kind`; None when the damage does not apply to this hunk."""
    s, r = "\n".join(old), "\n".join(new)
    if kind == "exact":
        return s, r
    if kind == "escaped":  # the whole block written as one JSON-escaped line
        esc = lambda t: t.replace("\\", "\\\\").replace("\n", "\\n").replace('"', '\\"')  # noqa: E731
        return esc(s), esc(r)
    if kind == "copy_s":  # the QAT copy defect: a word's final "s" dropped, in SEARCH and in REPLACE's copy of it
        ctx = [k for k, x in enumerate(old) if re.search(r"[a-z]s\b", x) and x in new]
        if not ctx:
            return None
        k = rng.choice(ctx)
        bad = re.sub(r"([a-z])s\b", r"\1", old[k], count=1)
        o2 = old[:k] + [bad] + old[k + 1:]
        n2 = [bad if x == old[k] else x for x in new]
        return "\n".join(o2), "\n".join(n2)
    if kind == "indent":  # the block written 4 spaces shallower
        if not all(x.startswith("    ") or not x.strip() for x in old + new):
            return None
        return "\n".join(x[4:] for x in old), "\n".join(x[4:] for x in new)
    if kind == "drop_line":  # one context line left out of SEARCH and REPLACE
        ctx = [k for k, x in enumerate(old) if x.strip() and x in new and 0 < k < len(old) - 1]
        if len(old) < 4 or not ctx:
            return None
        k = rng.choice(ctx)
        n2 = list(new)
        n2.remove(old[k])
        return "\n".join(old[:k] + old[k + 1:]), "\n".join(n2)
    if kind == "junk_tail":  # tool-call parser debris after the last line
        return s + '",', r
    if kind == "not_in_file":  # SEARCH from another file: must be refused
        return "\n".join(other), r
    if kind == "already_done":  # the change is already in the file: must change nothing
        return s, r
    raise ValueError(kind)


KINDS = ["exact", "escaped", "copy_s", "indent", "drop_line", "junk_tail", "not_in_file", "already_done"]


def score(before, after, expected):
    if after is None or after == before:
        return "refused"
    return "correct" if after == expected else "wrong"


def main():
    tasks = [json.loads(line) for line in open(sys.argv[1])]
    repos = Path(sys.argv[2])
    rng = random.Random(20261115)
    rows = []
    all_hunks = []
    for t in tasks:
        for h in hunks(t["patch"]):
            all_hunks.append((t, h))
    for t, (path, old, new, start) in all_hunks:
        repo = repos / REPO_DIR[t["repo"]]
        base = git_show(repo, t["base_commit"], path)
        if base is None or not old:
            continue
        s0, r0 = "\n".join(old), "\n".join(new)
        try:
            expected = apply_replacement(base, s0, r0).new_content
        except Exception:
            continue  # hunk not uniquely locatable even exactly: skip (the agent would need --near)
        if expected == base:
            continue
        other_t, (op, oold, _, _) = all_hunks[rng.randrange(len(all_hunks))]
        if op == path or not oold:
            oold = ["def _unrelated_helper(value):", "    return value * 2 + 1"]
        for kind in KINDS:
            d = damage(kind, old, new, rng, oold)
            if d is None:
                continue
            s, r = d
            content = expected if kind == "already_done" else base
            target = expected
            try:
                b_after = apply_replacement(content, s, r).new_content
            except Exception:
                b_after = None
            t0 = time.perf_counter()
            try:
                e_after, _ = fb_edit.apply(content, s, r)
            except Exception:  # a crash counts as refused (unchanged); none happened in the committed run
                e_after = None
            secs = time.perf_counter() - t0
            if kind == "not_in_file":
                b = "correct" if b_after is None or b_after == content else "wrong"
                e = "correct" if e_after is None or e_after == content else "wrong"
            elif kind == "already_done":
                b = "correct" if b_after is None or b_after == content else "wrong"
                e = "correct" if e_after is None or e_after == content else "wrong"
            else:
                b = score(content, b_after, target)
                e = score(content, e_after, target)
            rows.append(dict(instance_id=t["instance_id"], repo_name=t["repo"], file_name=path, hunk_start_num=start,
                             search_line_count=len(old), damage_code=kind, edit_file_outcome_code=b,
                             edit_py_outcome_code=e, edit_py_seconds=round(secs, 3),
                             file_line_count=base.count("\n") + 1))
    with open(sys.argv[3], "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(len(rows), "rows from", len(all_hunks), "hunks")


if __name__ == "__main__":
    main()
