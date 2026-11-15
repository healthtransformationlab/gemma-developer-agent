"""The model call's token budget (configs/sampling.yaml), issue 99.

The competition's model server has a 32,768-token window (paper/sources.md, the row for "45 of 207 runs ended at
the model's context window"). Whatever max_output_tokens keeps for output is taken from the input, and a run whose
conversation outgrows the rest ends with ContextWindowExceededError and no patch.
"""

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
WINDOW_TOKENS = 32768


def _sampling() -> dict:
    return yaml.safe_load((ROOT / "configs" / "sampling.yaml").read_text())


def test_the_input_has_room_for_the_largest_prompt_seen():
    """Issue 105: the largest prompt in the two 8,192 runs on the 23 development tasks was 17,426 tokens."""
    assert WINDOW_TOKENS - _sampling()["max_output_tokens"] >= 20480


def test_an_answer_still_has_room_after_thinking():
    s = _sampling()
    # issue 105: at 8,192 (4,096 after thinking) one edit was cut off before its tool call closed
    assert s["max_output_tokens"] - s["thinking_config"]["thinking_budget"] >= 8192


def test_the_rulebook_notes_state_the_configured_output_tokens():
    notes = (ROOT / "docs" / "rulebook-notes.md").read_text()
    line = next(l for l in notes.splitlines() if l.startswith("- `configs/sampling.yaml`"))
    stated = int(re.search(r"`max_output_tokens` ([\d,]+)", line).group(1).replace(",", ""))
    assert stated == _sampling()["max_output_tokens"]
