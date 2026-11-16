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


def test_the_31b_time_cap_is_the_public_bundles():
    """#173: the 5-minute cap (#161) came from a timing run on our own repository's tasks (357 s a task at 8 minutes).
    On the competition's development tasks 31B-d2 at 8 minutes averaged 209 s (devset-m31b-d2, 23 tasks, 1 at the
    limit), and the public Budget-Fit bundle, which hundreds of teams score with inside 12 hours, uses 8 minutes
    (about 225 s a task measured on the scorer). So the cap is at most the public bundle's 8 minutes, and no single
    command may take most of a task."""
    import yaml
    ev = yaml.safe_load((Path(__file__).resolve().parents[1] / "eval_config.yaml").read_text())["evaluation"]
    assert ev["max_time_minutes"] <= 8.0, ev
    assert ev["timeout_seconds"] <= 120, ev


def test_31b_e8_has_the_tests_step_36_calls_and_8_minutes():
    """#173: 31B-e8 is 31B-e (#172: find.py --tests, 36 calls) at 8 minutes a task. In 31B-e's first 33 development
    tasks at 5 minutes, 13 hit the time limit and 8 ended with no patch."""
    import yaml
    ev = yaml.safe_load((Path(__file__).resolve().parents[1] / "eval_config.yaml").read_text())["evaluation"]
    assert ev["max_tool_calls"] == 36 and ev["max_time_minutes"] == 8.0, ev
    assert "find.py --tests" in PROMPT and "## Patch first" in PROMPT
