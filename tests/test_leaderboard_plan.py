"""One leaderboard plan (#126): every queued entry's commit and change in one table, and the edit-failure analysis kept."""

import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs" / "leaderboard-plan.md"
QUEUED = {"5": "9c9cd3a", "5b": "80d23e8", "31B": "ed11c15", "5c": "0b7c63b", "6": "d265a78", "7": "7153a87",
          "8": "5d68ce8"}

_spec = importlib.util.spec_from_file_location("edit_failures", ROOT / "analysis" / "edit_failures.py")
ef = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ef)


def _rows() -> dict[str, str]:
    rows = {}
    for line in PLAN.read_text().splitlines():
        m = re.match(r"\|\s*\*{0,2}(\w+)\*{0,2}\s*\|", line)
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
    assert lines[0] == "run_name,instance_id,old_string_line_count,has_backslash,failure_class_code"
    assert len(lines) > 100
    classes = {line.rsplit(",", 1)[1] for line in lines[1:]}
    assert classes <= set(ef.CLASSES)


BRANCH = {"5": "main", "5b": "feat/122-skill-on-copyfix", "31B": "feat/124-31b-entry",
          "5c": "feat/125-distilled-adapter", "6": "main", "7": "main", "8": "main"}


def test_every_queued_entry_names_its_repository_and_branch():
    rows = _rows()
    for entry, branch in BRANCH.items():
        assert "healthtransformationlab/gemma-developer-agent" in rows[entry], f"entry {entry}: name the repository"
        assert f"/tree/{branch}" in rows[entry] or (branch == "main" and "/commit/" in rows[entry]), \
            f"entry {entry}: link its branch {branch} or its commit on main"
