# PR 133 review: the edit-failure analysis reads the tool's own error

Closes #132. Reviewed against `.conventions/AGENTS-common.md` and this repository's `AGENTS.md`.

## What changed

- `analysis/edit_failures.py`: `error_kind()` reads the failed call's `error_message` (`ambiguous` for "occurs N times",
  `not_found`, else `other`); only `not_found` rows go through the similarity classifier. New column
  `error_kind_code` (a coded value, `_code` suffix as the data-name rules ask).
- `analysis/edit_failures.csv`: regenerated from the same five runs; still ids, counts and codes only, no task text.
- `docs/leaderboard-plan.md`: the cause table and entry 7's evidence corrected.
- `tests/test_leaderboard_plan.py`: two new tests, written first and seen failing (3 failed before the change).

## Checks

- Tests first: yes. `pytest tests`: 77 passed, 1 skipped.
- Numbers come from a run in the repo: the table matches the regenerated CSV (119 = 90 + 25 + 4).
- No secrets, no competition task text, no `__pycache__` committed.
- No GPU run, no submission, no change to agent rules: an agent may merge it when green.

## Findings

- Not blocking: `error_kind` matches English substrings of the harness's messages; if the harness rewords them, rows
  fall to `other` rather than being misclassified, which the table would show.

Nothing blocking.
