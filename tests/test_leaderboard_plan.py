"""One leaderboard plan (#126): every queued entry's commit and change in one table, and the edit-failure analysis kept."""

import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs" / "leaderboard-plan.md"
QUEUED = {"5": "9c9cd3a", "31B-d2-5m": "27d3020", "E4B-all": "a09e97e", "5b": "80d23e8", "31B": "ed11c15", "31B-b": "c75c619", "31B-c": "2b1c444", "31B-d": "31df2c0", "5c": "0b7c63b",
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


BRANCH = {"5": "main", "31B-d2-5m": "feat/161-31b-d2-5-minutes", "E4B-all": "main", "5b": "feat/122-skill-on-copyfix", "31B": "feat/124-31b-entry",
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
    order = [e for e, line in _rows().items() if line.rstrip().endswith("| queued |")]
    assert order == ["31B-public"], order   # 31B-d2-5m scored 0.12; the 31B gets the slots, E4B-all is held (#174)
    text = PLAN.read_text()
    assert re.search(r"\| 31B \|[^\n]*\| held: replaced by 31B-b", text), "the 5-minute 31B row is marked held"
    assert "#818" in text, "cite the smoke test"
    assert re.search(r"If 31B-b runs past the 12-hour limit, its per-task\s+budget is shortened", text)


def test_31b_c_is_compared_with_31b_b_and_shares_its_gate():
    """#140: 31B-c is 31B-b without the code_analyzer sub-agent, so it is measured against 31B-b, and with the same
    8-minute budget it goes only if 31B-b finished inside 12 hours."""
    row = _rows()["31B-c"]
    assert "| 31B-b |" in row, "31B-c is compared with 31B-b"
    assert re.search(r"31B-c and 31B-d[^.]*do not go", PLAN.read_text()), "gate 31B-c and 31B-d on 31B-b finishing inside 12 hours"


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
    assert _cells(_rows()["5"])[-1].startswith("held: skipped by the owner"), "entry 5 is skipped (#159)"
    rows = [e for e in _rows() if e in QUEUED]
    assert rows.index("5c") > rows.index("8"), "5c is last in line"


def test_the_31b_entries_wait_on_the_timing_run():
    """#150: no 31B entry goes until a 10-task run measures the average time a task (nlp #821); since #152 only the
    stack, 31B-d, goes back to queued."""
    rows = _rows()
    assert _cells(rows["31B-d"])[-1].startswith("held: over 12 hours at 8 minutes"), "the timing run decided (#162)"
    assert "about 11 hours" in PLAN.read_text()


def test_the_final_candidates_are_the_stacks():
    """#152 (ADR 0002): with about 6 slots and ±2–3 tasks of noise, the slots go to the stacks, E4B-all (main: copyfix,
    the skill with its compile check, no graph tools, short anchors, scratch cleanup, 12,288) and 31B-d (Budget-Fit
    budget, single agent, patch first); their parts are held, and a freed slot repeats the candidate nearer its line."""
    rows = [e for e in _rows() if e in QUEUED]
    assert rows[:4] == ["5", "31B-d2-5m", "31B-d", "E4B-all"], rows   # the 31B second (#156, #162)
    for part, stack in (("5b", "E4B-all"), ("31B-b", "31B-d"), ("31B-c", "31B-d")):
        assert _cells(_rows()[part])[-1].startswith(f"held: part of {stack}"), part
    assert (ROOT / "docs" / "adr" / "0002-stack-changes-for-the-final-candidates.md").is_file()
    assert "ADR 0002" in (ROOT / "AGENTS.md").read_text()
    assert "Stacked final candidates" in PLAN.read_text()


def test_e4b_all_passed_its_check_at_a09e97e():
    """#166: the skill-use check (#156) passed: on the Kaggle run devset-e4b-all-k every one of 23 tasks called
    run_skill_script first and find.py second, so E4B-all's commit is a09e97e, the one that merged #154. Since #174 it
    is held behind the 31B, not queued."""
    cells = _cells(_rows()["E4B-all"])
    assert "a09e97e" in cells[2], "E4B-all names the commit that merged #154"
    assert cells[-1].startswith("held: the owner wants the 31B competitive first"), cells[-1]
    assert "204216e" in _rows()["E4B-all"], "the kill criterion still names the fallback commit"
    text = PLAN.read_text()
    assert "jcblearning/htlnlp-colab-official-colab-skill" in text, "name the colab-skill run"
    assert "devset-e4b-all-k" in text and "23 of 23" in text, "name the check that passed"
    assert "0 of 10" in _rows()["5b"], "5b's row records the colab-skill result"

def test_entry_5_is_skipped_and_31b_d_goes_second():
    """#159: entry 5 would hold the one slot for about 12 hours to check what E4B-all checks too (it carries copyfix),
    so the owner skipped it; 31B-d goes when its timing run clears, and E4B-all at 204216e if not by 02:00 UTC."""
    assert _cells(_rows()["5"])[-1].startswith("held: skipped by the owner (#159)")
    text = PLAN.read_text()
    assert re.search(r"02:00 UTC[^.]*204216e", text), "the fallback names 02:00 UTC and 204216e"
    e4b_all = _cells(_rows()["E4B-all"])
    header = _cells(next(line for line in text.splitlines() if line.startswith("| Entry |")))
    assert e4b_all[header.index("Compared with")].startswith("4"), "E4B-all compares with entry 4, since 5 won't score"


def test_31b_d2_5m_is_queued_second():
    """#162: the timing run put 31B-d at 8 minutes past 12 hours (357 s a task); the owner chose 31B-d2 at 5 minutes
    (#161) for the open slot, ahead of the 02:00 UTC fallback."""
    rows = _rows()
    assert _cells(rows["31B-d2-5m"])[-1] in ("queued", "submitted 2026-11-16 00:08 UTC, pending", "**0.12**")
    assert _cells(rows["31B-d"])[-1].startswith("held: over 12 hours at 8 minutes")
    assert "357" in rows["31B-d"] and "#821" in rows["31B-d"]
    assert "31B-d2-5m replaces the 02:00 UTC fallback" in PLAN.read_text()


def test_31b_d2_5m_scored_012():
    """#164: 31B-d2-5m went in as ref 58406723 at 00:08 UTC on November 16. #174: it scored 0.12, and the row says so,
    so no queue takes it again."""
    cells = _cells(_rows()["31B-d2-5m"])
    assert cells[1] == "58406723" and cells[-1] == "**0.12**", cells


def test_31b_e8_r2_and_50calls_timed_out():
    """#202: refs 58575084 (exact 31B-e8 repeat) and 58622854 (50 calls) both ended with the notebook runtime
    limit, so neither has a score."""
    rows = _rows()
    header = _cells(next(line for line in PLAN.read_text().splitlines() if line.startswith("| Entry |")))
    r2 = _cells(rows["31B-e8-r2"])
    c50 = _cells(rows["31B-e8-50calls"])
    assert r2[header.index("Ref")] == "58575084"
    assert c50[header.index("Ref")] == "58622854"
    assert r2[-1].startswith("timed out:") and "exceeded the allowed runtime" in r2[-1]
    assert c50[-1].startswith("timed out:") and "exceeded the allowed runtime" in c50[-1]


def test_31b_e8_fix_c32t6_is_pending():
    """#202: ref 58685342 is 31B-e8-fix with max_tool_calls 32 and max_time_minutes 6.0, Score pending."""
    rows, text = _rows(), PLAN.read_text()
    header = _cells(next(line for line in text.splitlines() if line.startswith("| Entry |")))
    cells = _cells(rows["31B-e8-fix-c32t6"])
    assert cells[header.index("Ref")] == "58685342"
    assert cells[-1] == "pending", cells[-1]
    assert "6f7ff699" in rows["31B-e8-fix-c32t6"] and "e532e35a" in rows["31B-e8-fix-c32t6"]
    assert "Two post-0.17 entries timed out" in text
    assert "31B-e8-fix-c32t6 went in" in text


PUBLIC_FILES = {"agent.yaml": "680799291cc7", "configs/sampling.yaml": "571a934e8991",
                "eval_config.yaml": "916cf6cb34a6", "prompts/system.md": "475cc9b7fcc0"}


def test_31b_public_is_queued_and_e4b_all_is_held():
    """#174: 0.12 is below the pack (about 2,200 teams at 0.17-0.18, about 620 at 0.20-0.22), most of it on the public
    Budget-Fit bundle, which we have never scored on our own account. The owner (November 16): "don't score the small
    model let's get the big one competitive first". So the bundle goes next, exactly as published, and E4B-all waits."""
    rows, text = _rows(), PLAN.read_text()
    header = _cells(next(line for line in text.splitlines() if line.startswith("| Entry |")))
    cells = _cells(rows["31B-public"])
    assert len(cells) == len(header), f"31B-public has {len(cells)} cells, the header {len(header)}"
    assert cells[-1] == "queued", cells[-1]
    row = rows["31B-public"]
    assert "verracodeguacas/gemma-4-agent-budget-fit-single-agent" in row, "name the notebook"
    assert "exactly as published" in row
    for name, sha in PUBLIC_FILES.items():
        assert name in row and sha in row, f"give {name}'s hash, {sha}"
    assert cells[header.index("Model")] == "**31B**"
    assert cells[header.index("Compared with")].startswith("31B-d2-5m"), "its score is read against our 0.12"
    assert cells[header.index("≥3 tasks plausible?")] and cells[header.index("Kill criterion")]
    names = [e for e in rows if e in QUEUED or e == "31B-public"]
    assert names.index("31B-public") == names.index("31B-d2-5m") + 1, "it goes right after 31B-d2-5m"
    assert _cells(rows["E4B-all"])[-1].startswith("held: the owner wants the 31B competitive first (November 16")
    assert "**The 31B gets every slot until it is competitive**" in text
    assert "don't score the small model let's get the big one competitive first" in " ".join(text.split()), \
        "quote the owner"
    adr = (ROOT / "docs" / "adr" / "0002-stack-changes-for-the-final-candidates.md").read_text()
    assert "#174" in adr and "31B-public" in adr, "the ADR records the change of which candidate a slot goes to"
