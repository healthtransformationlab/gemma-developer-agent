# PR 163 review: 31B-d2-5m is queued second; 31B-d is held as over 12 hours at 8 minutes (#162)

Reviewed by the author session against `AGENTS.md`, ADR 0002 and the plan's rules.

| Check | Result |
|---|---|
| Branch `docs/162-31b-d2-5m-queued`, `Closes #162`, issue with its four parts before the first commit | ok |
| Test first: `test_31b_d2_5m_is_queued_second` and the changed order tests failed on main (7 failures) | ok |
| The owner's choice is quoted: "31B-d2, 5 min (Recommended)" | ok |
| The timing figures come from the other session's report of the Modal run (nlp #821): 8 of 10 tasks, mean 357 s, maximum 483 s, 7 of 8 patched | ok; that run's own record lands in nlp |
| The new row has 13 cells, a three-task case and a kill criterion | ok |
| Secrets, data, claims | none |

## Findings

None blocking.

- **Risk, accepted.** 31B-d2-5m hasn't been timed at 5 minutes, but its worst case is bounded: 120 × (300 + 45) s is
  about 11.5 hours, even if every task uses all of its budget, and commands get 120 s. The 45 s of setup a task is an
  estimate; if the scorer's setup is much longer, the margin narrows. The kill criterion says to cut to 4 minutes if
  it runs past 12 hours.
- **Risk, accepted.** Only one task of evidence shows the first two calls working on the 31B. The Colab run
  devset-31b-d2 (23 tasks, at 8 minutes) will show the rest while this entry is scored.

## Verdict

Approve. It changes which entry the queue submits next, as the owner chose. The plan PR itself starts no run. Merge
when the checks are green.
