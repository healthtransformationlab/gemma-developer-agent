"""One leaderboard plan (#126): every queued entry's commit and change in one table, and the edit-failure analysis kept."""

import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs" / "leaderboard-plan.md"
QUEUED = {"5": "9c9cd3a", "5b": "80d23e8", "31B": "ed11c15", "31B-b": "c75c619", "31B-c": "2b1c444", "5c": "0b7c63b",
          "6": "d265a78", "7": "7153a87", "8": "5d68ce8"}

_spec = importlib.util.spec_from_file_location("edit_failures", ROOT / "analysis" / "edit_failures.py")
ef = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ef)


def _rows() -> dict[str, str]:
    rows = {}
    for line in PLAN.read_text().splitlines():
        m = re.match(r"\|\s*\*{0,2}([\w-]+)\*{0,2}\s*\|", line)
        if m:
            rows[m.group(1)] = line
    return rows


def test_the_plan_names_every_queued_entry_with_its_commit_and_evidence():
    rows = _rows()
    for entry, commit in QUEUED.items():
        assert entry in rows, f"entry {entry} is missing from docs/leaderboard-plan.md"
        assert commit in rows[entry], f"entry {entry}'s row doesn't name commit {commit}"
    assert "one pending" in PLAN.read_text().lower() and "one change per entry" in PLAN.read_text().lower()


def test_classify_tells_the_failure_causes_apart():
    seen = "def total(items):\n    return sum(i.price for i in items)\n"
    assert ef.classify("    return sum(i.price for i in items)", seen) == "seen_yet_failed"
    assert ef.classify("return  sum(i.price  for i in items)", seen) == "whitespace_only"
    assert ef.classify("    return sum(i.pric for i in items)", seen) == "near_copy"
    assert ef.classify("    return sum(i.prices for each in items)", seen) == "paraphrase"
    assert ef.classify("class Basket:\n    pass", seen) == "not_read"
    assert ef.classify("x = 1", "") == "not_read"
    assert ef.classify('    pattern = "a\\\\nb"', '    pattern = "a\\nb"') == "backslash_only"


def test_the_committed_result_holds_ids_and_classes_only():
    lines = (ROOT / "analysis" / "edit_failures.csv").read_text().splitlines()
    assert lines[0] == "run_name,instance_id,old_string_line_count,has_backslash,error_kind_code,failure_class_code"
    assert len(lines) > 100
    classes = {line.rsplit(",", 1)[1] for line in lines[1:]}
    assert classes <= set(ef.CLASSES)


BRANCH = {"5": "main", "5b": "feat/122-skill-on-copyfix", "31B": "feat/124-31b-entry",
          "31B-b": "feat/136-31b-budget-fit", "31B-c": "feat/140-31b-single-agent", "5c": "feat/125-distilled-adapter",
          "6": "main", "7": "main", "8": "main"}


def test_every_queued_entry_names_its_repository_and_branch():
    rows = _rows()
    for entry, branch in BRANCH.items():
        assert "healthtransformationlab/gemma-developer-agent" in rows[entry], f"entry {entry}: name the repository"
        assert f"/tree/{branch}" in rows[entry] or (branch == "main" and "/commit/" in rows[entry]), \
            f"entry {entry}: link its branch {branch} or its commit on main"


def test_entry_5b_cites_the_wider_check_with_open_navigator():
    row = _rows()["5b"]
    assert "getcommunityone/open-navigator" in row and "255 tasks" in row, "cite the 255-task check and open-navigator"
    assert "one repository" in row, "state the study's caveat: most of the check is one repository"


def test_error_kinds_come_from_the_tools_own_message():
    assert ef.error_kind("Failed to replace: old_string not found. Ensure you're not escaping content") == "not_found"
    assert ef.error_kind("Target string occurs 2 times in rich/table.py. Please provide more surrounding context.") \
        == "ambiguous"
    assert ef.error_kind("old_string cannot be empty.") == "other"
    assert "ambiguous" in ef.CLASSES


def test_the_committed_result_records_the_error_kind():
    header = (ROOT / "analysis" / "edit_failures.csv").read_text().splitlines()[0]
    assert "error_kind_code" in header


def test_31b_b_takes_the_second_slot_and_the_5_minute_31b_is_held():
    """#136 put the 31B right after entry 5; #138 gave that slot to 31B-b (8 minutes, 28 calls), since the 5-minute 31B
    entry ran out of time on all 3 tasks of its smoke test (health-transformation-lab-nlp #818). A 31B-b that runs past
    the 12-hour limit gets a shorter budget."""
    order = [e for e, line in _rows().items() if e in QUEUED and line.rstrip().endswith("| queued |")]
    assert order == ["5", "31B-b", "5b", "31B-c"], order   # 6, 7, 8 and 5c held under the three-task rule (#142)
    text = PLAN.read_text()
    assert re.search(r"\| 31B \|[^\n]*\| held: replaced by 31B-b", text), "the 5-minute 31B row is marked held"
    assert "#818" in text, "cite the smoke test"
    assert re.search(r"If 31B-b runs past the 12-hour limit, its per-task\s+budget is shortened", text)


def test_31b_c_is_compared_with_31b_b_and_shares_its_gate():
    """#140: 31B-c is 31B-b without the code_analyzer sub-agent, so it is measured against 31B-b, and with the same
    8-minute budget it goes only if 31B-b finished inside 12 hours."""
    row = _rows()["31B-c"]
    assert "| 31B-b |" in row, "31B-c is compared with 31B-b"
    assert re.search(r"31B-c[^.]*does not go", PLAN.read_text()), "gate 31B-c on 31B-b finishing inside 12 hours"


def _cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def test_every_entry_names_its_kill_criterion():
    """#142: every queued or held entry says whether three tasks are plausible and what result stops it."""
    header = next(line for line in PLAN.read_text().splitlines() if line.startswith("| Entry |"))
    cols = _cells(header)
    assert "≥3 tasks plausible?" in cols and "Kill criterion" in cols, cols
    i3, ik = cols.index("≥3 tasks plausible?"), cols.index("Kill criterion")
    for entry in QUEUED:
        cells = _cells(_rows()[entry])
        assert len(cells) == len(cols), f"entry {entry} has {len(cells)} cells, the header {len(cols)}"
        assert cells[i3] and cells[ik], f"entry {entry}: fill both new columns"


def test_small_entries_are_held_under_the_three_task_rule():
    """#142: the noise is ±2-3 tasks, so an entry likely worth one or two is held; the slot goes to a three-task
    candidate or a repeat of a final candidate."""
    text = PLAN.read_text()
    assert "Three tasks or a repeat" in text
    for entry in ("6", "7", "8", "5c"):
        assert _cells(_rows()[entry])[-1].startswith("held:"), f"entry {entry} is not held"
    for entry in ("5", "31B-b", "5b", "31B-c"):
        assert _cells(_rows()[entry])[-1] == "queued", f"entry {entry} should still be queued"
    rows = [e for e in _rows() if e in QUEUED]
    assert rows.index("5c") > rows.index("8"), "5c is last in line"
