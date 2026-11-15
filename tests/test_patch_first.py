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
