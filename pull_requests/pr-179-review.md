# PR 179 review: the November 18 slot goes to 31B-e8, which beat the public bundle on unseen code (#178)

Reviewed by the author session against `AGENTS.md`, `.conventions/AGENTS-common.md` and the submission rules
(`docs/rulebook-notes.md`).

| Check | Result |
|---|---|
| Branch `docs/178-31b-e8-tonight`, `Closes #178`, issue with its four parts before the first commit | ok |
| Test first: the changed and new tests failed on main's plan (6 failed); then 103 passed, 1 skipped | ok |
| The owner's choice is quoted with its time ("Switch to our agent, 8 min", November 17, about 13:10 UTC) | ok |
| Practice: 36 against 31 of 129, 6 against 1, recounted here from the runs' `result.json` on the same task ids | ok |
| Our repository: 17, 12 and 12 of 25 are the other analysis session's grading with the verifier on CPU, not recounted here; the row says who graded | noted |
| The commit is `af1e006` on `feat/173-31b-e8`; its only change from 31B-e (`f5f35cc`) is `max_time_minutes` 8.0 (and its test) | ok |
| Time risk: 248 s a task on the practice set and about 300 s on ours, against the bundle's 202 s, both on an A100; the kill criterion says what happens past 12 hours | noted |
| One pending at a time: if 31B-public (58448837) is still pending at 00:00 UTC, the slot can't be used | noted |
| No secrets, no task text | ok |

## Verdict

Ready to merge once CI is green.
