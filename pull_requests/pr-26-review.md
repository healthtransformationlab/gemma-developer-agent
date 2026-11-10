---
pr: 26
branch: docs/25-sources-non-candidates
title: "000 DOCS8: record where the 81 non-candidate changes went, and why issues are not tasks"
author: Claude Code (agent session for jcbowyer)
reviewed_at: 2026-11-10
reviewer: the authoring session (each figure recomputed from the manifest or read from GitHub's search API; no reviewer subagent run)
verdict: approve
---

# PR Review: 000 DOCS8: record where the 81 non-candidate changes went, and why issues are not tasks

## Summary
Five lines in `paper/sources.md`. The writeup gives 197 merged changes and 116 candidates; this records what the
other 81 were, and says why the repository's issue count is not the task count. The owner chose to keep both out of
the writeup, which is three words under its limit. Nothing blocking.

## Checks
| Check | Result |
|---|---|
| 49 touch no Python file, 19 tests without code, 13 code without tests | `task_manifest.csv` on `NLP` main, 197 rows: `is_code_changed` and `is_tests_changed`; 49 + 19 + 13 = 81 = 197 − 116 |
| What counts as code and as a test | `task_mine.classify_files`: a `.py` file that is not a test; a `.py` file under `tests/` or named `test_*` |
| "The 49 are documentation, specs, decks and data" | the 49 titles read: deck and landing-page text, specs, review files, data refreshes; none changes a `.py` file by the rule above |
| 313 closed issues, 114 opened after October 29, 67 backfilled; 312 merged pull requests | GitHub's search API, November 10, 2026 |
| The writeup is unchanged | `git diff origin/main -- paper/writeup.md` is empty; 2,997 words without references |
| Branch name and issue link | `docs/25-sources-non-candidates`, `Closes #25` |

## Should fix
Nothing.

## Secrets, Real Data and Claims Scan
Secrets: none. Real data: none. Claims: none added to the writeup; the sources file gains two records.
