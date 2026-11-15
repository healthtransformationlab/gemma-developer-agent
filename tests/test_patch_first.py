"""31B-d (#145): the prompt makes the agent edit early and look at the clock. In the 31B smoke test two of three tasks
ran out of time without an edit, and only 7 of 118 recorded task-runs ever called get_status."""
from pathlib import Path

PROMPT = (Path(__file__).resolve().parents[1] / "prompts" / "system.md").read_text()


def test_the_prompt_has_a_patch_first_rule():
    assert "## Patch first" in PROMPT
    section = PROMPT.split("## Patch first", 1)[1].split("\n## ", 1)[0]
    assert "10th tool call" in section
    assert "after your 6th tool call" in section and "time_seconds_remaining" in section
    assert "half" in section and "quarter" in section


def test_the_old_every_five_calls_line_is_replaced():
    assert "Call `get_status` after every five tool calls." not in PROMPT


def test_the_first_two_calls_come_before_patch_first():
    """#158: 31B-d2 is 31B-d on main, so the install and find.py (#154) come first and the patch-first rule after them;
    the two calls count towards the 10th-call edit."""
    order = [PROMPT.index(h) for h in ("## The one rule above all others", "## Your first two tool calls",
                                       "## Patch first", "## Budget discipline")]
    assert order == sorted(order), order


def test_the_31b_budget_fits_120_tasks_in_12_hours():
    """#161: at 8 minutes the 31B timing run averaged 357 s a task (13.4 hours for 120), past the 12-hour limit. The
    per-task budget must fit 120 tasks even if every one uses all of it, with about 45 s of setup each; and no single
    command may take most of a task."""
    import yaml
    ev = yaml.safe_load((Path(__file__).resolve().parents[1] / "eval_config.yaml").read_text())["evaluation"]
    assert 120 * (ev["max_time_minutes"] * 60 + 45) <= 12 * 3600, ev
    assert ev["timeout_seconds"] <= 120, ev
