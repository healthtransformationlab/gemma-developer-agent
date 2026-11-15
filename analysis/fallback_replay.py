"""Replay the recorded edit_file calls of development-set runs on CPU, and say what the edit-fallback skill's
edit.py does with each one that failed (#122).

For each task in a run's kernel output (output/tasks/<id>/results/traces/*.json), every file starts as it is at the
task's base commit (a local clone of the public repository), and the agent's edit_file and write_file calls are
applied in order with the harness's own matcher (swegemma.edit.apply_replacement). Where a call fails, edit.py gets
the same old_string and new_string as a SEARCH/REPLACE block: once as is, once with --near the middle of the agent's
last read_file range of that file. The label, where there is one, is the agent's own later successful edit of the same
file with a similar new_string (similarity >= 0.5). Writes one row per failed call: ids, outcomes and line numbers
only, no code and no competition data.

usage: fallback_replay.py <tasks.jsonl> <dir holding clones named fastapi, rich, requests, httpx> <out.csv> <run dir>...
"""
import csv
import difflib
import glob
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

from swegemma.edit import apply_replacement  # the harness's own edit_file matcher

sys.dont_write_bytecode = True   # no __pycache__ in skills/: a .pyc in the submission is refused
_spec = importlib.util.spec_from_file_location(
    "fallback_edit", Path(__file__).resolve().parents[1] / "skills" / "edit-fallback" / "scripts" / "edit.py")
fb_edit = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fb_edit)

REPO_DIR = {"fastapi/fastapi": "fastapi", "Textualize/rich": "rich", "psf/requests": "requests",
            "encode/httpx": "httpx",
            # this organisation's repositories (the generality check; the competition's development set decides)
            "healthtransformationlab/health-transformation-lab-nlp": "health-transformation-lab-nlp",
            "healthtransformationlab/pipeline-doctor": "pipeline-doctor",
            "healthtransformationlab/gemma-developer-agent": "gemma-developer-agent",
            "getcommunityone/open-navigator": "open-navigator"}


def git_show(repo, commit, path):
    r = subprocess.run(["git", "-C", str(repo), "show", f"{commit}:{path}"], capture_output=True)
    return r.stdout.decode("utf-8", "replace") if r.returncode == 0 else None


def changed_span(before, after):
    """(first, last) 1-based lines of `before` where `after` first differs, or (None, None)."""
    if after is None:
        return None, None
    a, b = before.splitlines(), after.splitlines()
    for tag, i1, i2, _, _ in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag != "equal":
            return i1 + 1, max(i1 + 1, i2)
    return None, None


def outcome(new_content, message):
    """What edit.py did, as a code."""
    if new_content is not None:
        return "applied"
    if "already in the file" in message or "already matches" in message or "nothing to change" in message:
        return "already_done"
    if message.startswith("SEARCH occurs at lines"):
        return "lists_lines"
    if message.startswith("SEARCH has "):
        return "refused_long"
    if "leaves out" in message or "differ where" in message:
        return "refused_conflict"
    return "refused_closest"


def _path(args):
    p = str(args.get("filepath", "")).lstrip("/")
    return p[len("workspace/"):] if p.startswith("workspace/") else p


def _obs(text):
    try:
        return json.loads(text) if text else {}
    except ValueError:
        return {}


def replay_task(trace_path, task, repo):
    events = []
    for step in json.load(open(trace_path))["steps"]:
        obs = (step.get("observation") or {}).get("content") or ""
        for tc in step.get("tool_calls") or []:
            events.append((tc.get("function_name"), tc.get("arguments") or {}, obs))
    files, last_read, rows = {}, {}, []
    for i, (fn, args, obs) in enumerate(events):
        path = _path(args)
        if fn == "read_file" and path:
            try:
                s = int(args.get("start_line") or 1)
                e = int(args.get("end_line") or s + 149)
            except (TypeError, ValueError):
                s, e = 1, 150
            last_read[path] = (s, e)
        if fn == "write_file" and path and _obs(obs).get("status") == "ok":
            files[path] = args.get("content") or ""
        if fn != "edit_file" or not path or "old_string" not in args:
            continue
        if path not in files:
            files[path] = git_show(repo, task["base_commit"], path)
        content = files[path]
        if content is None:
            continue
        old, new = args.get("old_string") or "", args.get("new_string") or ""
        try:
            multi = str(args.get("allow_multiple")).lower() == "true"
            files[path] = apply_replacement(content, old, new, filepath=path, allow_multiple=multi).new_content
            continue
        except Exception as ex:  # the harness's failure: the case edit.py is for
            failure = "multiple" if ("occurs" in str(ex) or "flexibly matches" in str(ex)) else "not_found"
        row = dict(instance_id=task["instance_id"], repo_name=task["repo"], call_num=i, file_name=path,
                   recorded_status_code=_obs(obs).get("status"), replay_failure_code=failure,
                   search_line_count=len(fb_edit.core(old.splitlines(), debris=True)))
        new_c, msg = fb_edit.apply(content, old, new)
        row["edit_py_outcome_code"] = outcome(new_c, msg)
        row["edit_py_start_num"], row["edit_py_end_num"] = changed_span(content, new_c)
        near = last_read.get(path)
        if near:
            new_n, msg_n = fb_edit.apply(content, old, new, (near[0] + near[1]) // 2)
            row["edit_py_near_outcome_code"] = outcome(new_n, msg_n)
            row["edit_py_near_start_num"], row["edit_py_near_end_num"] = changed_span(content, new_n)
        else:
            row["edit_py_near_outcome_code"] = row["edit_py_near_start_num"] = row["edit_py_near_end_num"] = None
        row["later_fix_start_num"] = row["later_fix_end_num"] = None
        for fn2, a2, obs2 in events[i + 1:]:
            if fn2 != "edit_file" or _path(a2) != path or _obs(obs2).get("status") != "ok":
                continue
            if difflib.SequenceMatcher(None, new, a2.get("new_string") or "").ratio() < 0.5:
                continue
            try:
                later = apply_replacement(content, a2.get("old_string") or "", a2.get("new_string") or "",
                                          allow_multiple=str(a2.get("allow_multiple")).lower() == "true")
                row["later_fix_start_num"], row["later_fix_end_num"] = changed_span(content, later.new_content)
            except Exception:
                pass
            break
        rows.append(row)
    return rows


def main(tasks_path, repos_dir, out_path, runs):
    tasks = {json.loads(line)["instance_id"]: json.loads(line) for line in open(tasks_path)}
    rows = []
    for run in runs:
        for trace in sorted(glob.glob(f"{run}/output/tasks/*/results/traces/*.json")):
            task = tasks[trace.split("/tasks/")[1].split("/")[0]]
            for row in replay_task(trace, task, Path(repos_dir) / REPO_DIR[task["repo"]]):
                rows.append(dict(run_name=Path(run).name, **row))
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(len(rows), "failed edits")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:])
