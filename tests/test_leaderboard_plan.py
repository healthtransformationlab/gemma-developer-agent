"""One leaderboard plan (#126): every queued entry's commit and change in one table, and the edit-failure analysis kept."""

import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs" / "leaderboard-plan.md"
QUEUED = {"5": "9c9cd3a", "5b": "80d23e8", "31B": "ed11c15", "31B-b": "c75c619", "5c": "0b7c63b", "6": "d265a78",
          "7": "7153a87", "8": "5d68ce8"}

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
          "31B-b": "feat/136-31b-budget-fit", "5c": "feat/125-distilled-adapter", "6": "main", "7": "main", "8": "main"}


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


def test_the_31b_comes_second_and_31b_b_waits_on_its_timing():
    """#136: the owner put the 31B right after entry 5 (the main prizes can only be won with it); 31B-b, a longer
    budget, goes only if the 31B entry finished inside 12 hours."""
    order = [e for e in _rows() if e in QUEUED]
    assert order == ["5", "31B", "5b", "31B-b", "5c", "6", "7", "8"], order
    text = PLAN.read_text()
    assert re.search(r"31B-b[^.]*does not go", text), "gate 31B-b on the 31B entry finishing inside 12 hours"
