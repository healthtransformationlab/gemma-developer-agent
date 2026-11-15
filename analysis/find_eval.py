"""Score the edit-fallback skill's find.py against the prompt's grep | head -40 on the competition's development
tasks, per repository (#122). CPU only.

Each task's repository is checked out at its base commit from a local clone of the public repository
(fastapi/fastapi, Textualize/rich, psf/requests, encode/httpx). The query is the issue's first five identifiers, as
analysis/localize.py extracts them (the prompt asks for two to five); the answer is the reference patch's non-test
files. Writes one row per task, ids and ranks only, no competition data.

usage: find_eval.py <tasks.jsonl> <dir holding clones named fastapi, rich, requests, httpx> <out.csv>
"""
import csv
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_DIR = {"fastapi/fastapi": "fastapi", "Textualize/rich": "rich", "psf/requests": "requests",
            "encode/httpx": "httpx",
            # this organisation's repositories (the generality check; the competition's development set decides)
            "healthtransformationlab/health-transformation-lab-nlp": "health-transformation-lab-nlp",
            "healthtransformationlab/pipeline-doctor": "pipeline-doctor",
            "healthtransformationlab/gemma-developer-agent": "gemma-developer-agent",
            "getcommunityone/open-navigator": "open-navigator"}
TEST = re.compile(r"(^|/)(tests?|testing)/|(^|/)test_[^/]*\.py$|_test\.py$|(^|/)conftest\.py$")


sys.dont_write_bytecode = True   # no __pycache__ in skills/: a .pyc in the submission is refused


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


find = _load("fallback_find", ROOT / "skills" / "edit-fallback" / "scripts" / "find.py")
identifiers = _load("localize", ROOT / "analysis" / "localize.py").identifiers


def grep_files(root, words):
    """The prompt's step 2: grep for the names, tests left out, first 40 lines; files in order of appearance."""
    cmd = ["grep", "-rnE", "--include=*.py", "--exclude-dir=.git", "--exclude-dir=tests", "--exclude=test_*.py",
           "|".join(words), root]
    out = subprocess.run(cmd, capture_output=True, text=True).stdout.splitlines()[:40]
    files = []
    for line in out:
        f = os.path.relpath(line.split(":", 1)[0], root)
        if f not in files:
            files.append(f)
    return files, sum(len(line) for line in out)


def rank(files, gold):
    """1-based rank of the first answer file in files, or None."""
    return next((k for k, f in enumerate(files, 1) if f in gold), None)


def main(tasks_path, repos_dir, out_path):
    rows, skipped = [], 0
    for line in open(tasks_path):
        t = json.loads(line)
        gold = {f for f in re.findall(r"^\+\+\+ b/(\S+)", t["patch"], re.M) if f.endswith(".py") and not TEST.search(f)}
        if not gold:
            continue
        words = identifiers(t["problem_statement"])[:5]
        td = tempfile.mkdtemp()
        try:
            archive = subprocess.run(["git", "-C", str(Path(repos_dir) / REPO_DIR[t["repo"]]), "archive",
                                      t["base_commit"], "--", ":(glob)**/*.py"],  # both searches read .py only
                                     capture_output=True)
            if archive.returncode != 0:  # base commit not in the local clone: skipped, and counted
                skipped += 1
                continue
            subprocess.run(["tar", "-x", "-C", td], input=archive.stdout, check=True)
            g_files, g_chars, f_files, secs = [], 0, [], 0.0
            if words:
                g_files, g_chars = grep_files(td, words)
                t0 = time.perf_counter()
                found = find.scan(td, words)
                secs = time.perf_counter() - t0
                main_files = [r for r in found if not r[0]]
                f_files = [r[2] for r in (main_files or found)][:find.MAX_FILES]
            rows.append(dict(instance_id=t["instance_id"], repo_name=t["repo"], query_word_count=len(words),
                             gold_file_count=len(gold), grep_file_rank_num=rank(g_files, gold),
                             find_file_rank_num=rank(f_files, gold), grep_output_char_count=g_chars,
                             find_seconds=round(secs, 3)))
        finally:
            shutil.rmtree(td, ignore_errors=True)
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(len(rows), "tasks;", skipped, "skipped (base commit not in the local clone)")


if __name__ == "__main__":
    main(*sys.argv[1:4])
