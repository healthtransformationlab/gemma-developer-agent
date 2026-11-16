# PR 171 review: find.py --tests names the test files for the file changed; step 7 runs those (#170)

| Check | Result |
|---|---|
| Branch `feat/170-find-tests-to-run`, `Closes #170`, issue with its four parts before the first commit, a dated "Changed" line for the redesign | ok |
| Test first: the ranking, `--tests` and step 7 tests failed before the change | ok |
| The measurement is honest: the first design was measured against the reference file the agent doesn't know (61/71), re-measured as shipped (30/45), and redesigned to use the file the agent changed (59/66, the reference file standing in) | ok; all three in the PR and the issue |
| The normal output is unchanged; `find_ranks.csv`'s file and grep ranks are unchanged task by task | ok |
| Python 3.8, standard library only, no compiled files under `skills/` | ok |
| No leaderboard entry changes: E4B-all is pinned to a09e97e; the PR says a development-set run comes first | ok |

## Findings

None blocking.

- **Risk, open.** The agent must pass the file it changed to `--tests`. The 59 of 129 assumes the right file; when it
  edited a wrong file, the tests named are that file's, so they still show a hang or a broken import in its own
  module. Only a development-set run shows whether E4B makes the call at all.
- **Risk, accepted.** FastAPI's tests need `inline_snapshot`, which the sandbox lacks, so a FastAPI test file can fail
  on collection whatever the patch. `-x` stops at the first failure, so it fails in seconds. The agent then submits
  as before.
- **Noted.** `-x -q` with `timeout 120` bounds the cost to two calls and two minutes at most. The run will show
  whether that's worth it for E4B within its 300 s.

## Verdict

Approve. It changes main's skill and prompt, but no queued entry. Merge when the checks are green; the plan names
the entries.
