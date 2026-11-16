"""How find.py and the agent's own tests were used, per task of a development run (#168).

For each trace under a run folder, against the files the task's reference patch changes (test files left out):
the failure stage (analysis/failure_stages.py), find.py's rank of a reference file in its first output, whether
the first file the agent read was find.py's top file, how many pytest calls it made and whether any named a test
file, the evaluator's test exit code (0 pass, 1 tests fail, 2 collection error, 124 timeout), and the agent's seconds.
Ids, codes and counts only: the traces hold the competition's tasks, which are never written out.

    python analysis/devset_traces.py <run dir> --tasks <tasks.jsonl> --out analysis/devset_<run>.csv
"""
from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True
_spec = importlib.util.spec_from_file_location("failure_stages", Path(__file__).with_name("failure_stages.py"))
fs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fs)

COLUMNS = ["instance_id", "failure_stage_code", "find_gold_rank_num", "is_top_read_first", "pytest_call_count",
           "is_test_file_run", "test_exit_code", "agent_seconds"]
_LISTED = re.compile(r"^\s*([\w./-]+\.py)\s+\(names", re.M)   # find.py's file lines: "path  (names N, defines M)"
_TEST_FILE = re.compile(r"(^|[\s/])(tests?/\S*|test_\w+\.py)")


def _text(out) -> str:
    if not isinstance(out, str):
        out = json.dumps(out)
    try:
        d = json.loads(out)
        if isinstance(d, dict):
            return str(d.get("stdout") or d.get("content") or d.get("output") or out)
    except (ValueError, TypeError):
        pass
    return out


def _path(p: str) -> str:
    return str(p or "").replace("/workspace/", "").lstrip("/")


def task_row(trace: dict, result: dict, gold: set[str], instance_id: str, stage: str) -> dict:
    calls = [(c.get("function_name"), c.get("arguments") or {}, (s.get("observation") or {}).get("content", ""))
             for s in trace.get("steps", []) for c in (s.get("tool_calls") or [])]
    listed = next((_LISTED.findall(_text(o)) for n, a, o in calls
                   if n == "run_command" and "find.py" in str(a.get("command", ""))), None)
    rank = next((i + 1 for i, f in enumerate(listed or []) if any(f.endswith(g) or g.endswith(f) for g in gold)), None)
    reads = [_path(a.get("filepath")) for n, a, o in calls if n == "read_file"]
    top_first = None if listed is None else bool(listed and reads and reads[0].endswith(listed[0]))
    pytest = [str(a.get("command", "")) for n, a, o in calls if n == "run_command" and "pytest" in str(a.get("command", ""))]
    verification = result.get("verification") or {}
    return {"instance_id": instance_id, "failure_stage_code": stage, "find_gold_rank_num": rank,
            "is_top_read_first": top_first, "pytest_call_count": len(pytest),
            "is_test_file_run": any(_TEST_FILE.search(c.split("pytest", 1)[1]) for c in pytest),
            "test_exit_code": verification.get("test_exit_code") if isinstance(verification, dict) else None,
            "agent_seconds": round(float(result.get("agent_phase_seconds") or 0), 1)}


def rows(run_dir: Path, tasks_path: Path) -> list[dict]:
    tasks = {json.loads(line)["instance_id"]: json.loads(line) for line in open(tasks_path) if line.strip()}
    stages = {r["instance_id"]: r["failure_stage_code"] for r in fs.stages([Path(run_dir)], Path(tasks_path))}
    out = []
    for trace_path in sorted(Path(run_dir).rglob("trace_*.json")):
        iid = trace_path.stem.removeprefix("trace_")
        if iid not in tasks:
            continue
        result_path = trace_path.parents[2] / "result.json"
        result = json.loads(result_path.read_text()) if result_path.exists() else {}
        out.append(task_row(json.loads(trace_path.read_text()), result, fs.gold_files(tasks[iid]["patch"]), iid,
                            stages.get(iid)))
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("run_dir", type=Path)
    ap.add_argument("--tasks", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args(argv)
    found = rows(a.run_dir, a.tasks)
    with open(a.out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS, lineterminator="\n")
        w.writeheader()
        w.writerows(found)
    print(f"{len(found)} tasks -> {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
