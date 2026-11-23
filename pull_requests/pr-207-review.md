
# PR 207 review: find.py shows the top functions' code, and reads several ranges in one call

Closes #206. Branch `feat/206-find-show`. Files: `skills/edit-fallback/scripts/find.py`, `skills/edit-fallback/SKILL.md`,
`tests/test_find_show.py` (new).

| Check | Result |
|---|---|
| Tests written first: 6 of 7 new tests failed before the change (the unchanged-output test passed) | ok |
| Without `--show` or `--read` the output is byte-for-byte the old path (existing find tests pass) | ok |
| Output stays under run_command's 5,000 characters: `SHOW_TOTAL_CHARS` 4,900, ranking capped at 1,800 with `--show` | ok |
| A long function is cut at 40 lines with the exact `--read` range to get the rest | ok |
| Standard library only, Python 3.8+, no install change (both options live in find.py) | ok |
| `python -m pytest -q tests`: 120 passed, 1 skipped | ok |
| No submission or run; the agent package is unchanged until a separate build | ok |

## Findings, not blocking

- Whether the agent uses `--show` depends on the prompt line added in the next build; the mechanism check
  (private repo) estimates the calls saved from recorded runs.

## Verdict

Ready to merge once CI is green.
