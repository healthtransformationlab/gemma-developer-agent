"""#147: each development task-run gets the stage it failed at."""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("failure_stages", ROOT / "analysis" / "failure_stages.py")
fs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fs)
GOLD = {"pkg/core.py"}


def test_each_stage():
    assert fs.stage_of(GOLD, set(), set(), set(), False) == "localize"
    assert fs.stage_of(GOLD, {"pkg/core.py"}, set(), set(), False) == "edit"
    assert fs.stage_of(GOLD, {"pkg/core.py"}, {"pkg/core.py"}, set(), False) == "complete"
    assert fs.stage_of(GOLD, {"pkg/core.py"}, {"pkg/other.py"}, {"pkg/other.py"}, False) == "patch_wrong_file"
    assert fs.stage_of(GOLD, {"pkg/core.py"}, {"pkg/core.py"}, {"pkg/core.py"}, False) == "patch_right_file"
    assert fs.stage_of(GOLD, {"pkg/core.py"}, {"pkg/core.py"}, {"pkg/core.py"}, True) == "resolved"


def test_a_run_folder_is_read_end_to_end(tmp_path):
    tasks = tmp_path / "tasks.jsonl"
    tasks.write_text(json.dumps({"instance_id": "t1", "patch": "+++ b/pkg/core.py\n+++ b/tests/test_core.py\n"}) + "\n")
    task = tmp_path / "run1" / "tasks" / "t1"
    (task / "results" / "traces").mkdir(parents=True)
    steps = [{"tool_calls": [{"function_name": "read_file", "arguments": {"filepath": "/workspace/pkg/core.py"}}],
              "observation": {"content": json.dumps({"content": "x = 1"})}},
             {"tool_calls": [{"function_name": "edit_file", "arguments": {"filepath": "/workspace/pkg/core.py"}}],
              "observation": {"content": json.dumps({"status": "ok"})}}]
    (task / "results" / "traces" / "trace_t1.json").write_text(json.dumps({"steps": steps}))
    (task / "result.json").write_text(json.dumps({"patch": "+++ b/pkg/core.py\n", "verification": {"is_resolved": True}}))
    rows = fs.stages([tmp_path / "run1"], tasks)
    assert rows == [{"run_name": "run1", "instance_id": "t1", "failure_stage_code": "resolved", "tool_call_count": 2,
                     "first_edit_call_num": 2}]
