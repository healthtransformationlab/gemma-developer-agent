# PR 127 review: one leaderboard plan and the edit-failure analysis (#126)

| Check | Result |
|---|---|
| Branch `docs/126-leaderboard-plan`, `Closes #126`, issue with its four parts first | ok |
| Test first: `tests/test_leaderboard_plan.py` failed (no plan, no module), then passed; 73 pass | ok |
| Every queued entry's commit in its row (5 9c9cd3a, 5b 80d23e8, 31B ed11c15, 5c 0b7c63b, 6 d265a78, 7 7153a87, 8 5d68ce8), checked by test against the zips built from them | ok |
| Evidence cited matches its sources: fallback study, localization study, PR 117's statistics, the dev-set tables, write-ups by number | ok |
| `analysis/edit_failures.csv`: 119 rows of ids, counts and classes; no task text or code (the traces hold the competition's tasks) | ok |
| Reproduces: the script run on the five runs' downloaded traces gives the committed counts | ok |
| Not part of the submission: `docs/`, `analysis/`, `tests/` are outside the bundle | ok |

## Findings

- Minor: with exact matching (`autojunk=False`) the near-copy, paraphrase and not-read counts differ a little from the first, quicker classification reported in chat (33, 36, 22 against 30, 29, 32); the committed figures are these.
- Minor: the scheduled queue still carries its own copy of the order; it now reads this page first and keeps the copy as a fallback.

## Verdict

Nothing blocking. Merge when CI is green.
