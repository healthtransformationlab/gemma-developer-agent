"""#168: per task, how find.py and the agent's own tests were used in a run (analysis/devset_traces.py)."""
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("devset_traces", ROOT / "analysis" / "devset_traces.py")
dt = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(dt)


def _call(name, args, out):
    return {"tool_calls": [{"function_name": name, "arguments": args}], "observation": {"content": out}}


def _run(tmp_path, steps, exit_code=1, seconds=88.5):
    tasks = tmp_path / "tasks.jsonl"
    tasks.write_text(json.dumps({"instance_id": "t1", "patch": "+++ b/pkg/core.py\n+++ b/tests/test_core.py\n"}) + "\n")
    task = tmp_path / "run" / "tasks" / "t1"
    (task / "results" / "traces").mkdir(parents=True)
    (task / "results" / "traces" / "trace_t1.json").write_text(json.dumps({"steps": steps}))
    (task / "result.json").write_text(json.dumps({"patch": "+++ b/pkg/core.py\n", "agent_phase_seconds": seconds,
                                                  "verification": {"is_resolved": False, "test_exit_code": exit_code}}))
    return dt.rows(tmp_path / "run", tasks)


def test_find_rank_top_read_and_a_real_test_file(tmp_path):
    steps = [_call("run_skill_script", {"skill_name": "edit-fallback", "file_path": "scripts/install.py"}, "ok"),
             _call("run_command", {"command": "python3 /tmp/h/find.py total"},
                   "pkg/util.py  (names 1, defines 0)\n  3: total\npkg/core.py  (names 1, defines 1)\n  9: def total"),
             _call("read_file", {"filepath": "pkg/util.py"}, "{}"),
             _call("edit_file", {"filepath": "pkg/core.py"}, '{"status": "ok"}'),
             _call("run_command", {"command": "cd /workspace && python3 -m pytest pkg/core.py"}, "no tests ran"),
             _call("run_command", {"command": "python3 -m pytest tests/test_core.py -q"}, "3 passed in 0.1s")]
    (row,) = _run(tmp_path, steps)
    assert list(row) == dt.COLUMNS
    assert row["find_gold_rank_num"] == 2, "the reference file is find.py's second"
    assert row["is_top_read_first"] is True, "the first file read was find.py's top file"
    assert row["pytest_call_count"] == 2 and row["is_test_file_run"] is True
    assert row["failure_stage_code"] == "patch_right_file"
    assert (row["test_exit_code"], row["agent_seconds"]) == (1, 88.5)


def test_no_find_call_and_pytest_on_source_only(tmp_path):
    steps = [_call("read_file", {"filepath": "pkg/core.py"}, "{}"),
             _call("run_command", {"command": "pytest pkg/core.py"}, "no tests ran"),
             _call("run_command", {"command": "pytest -q"}, "ModuleNotFoundError: No module named 'inline_snapshot'")]
    (row,) = _run(tmp_path, steps, exit_code=124)
    assert row["find_gold_rank_num"] is None and row["is_top_read_first"] is None
    assert row["pytest_call_count"] == 2 and row["is_test_file_run"] is False, "neither call names a test file"
    assert row["test_exit_code"] == 124
