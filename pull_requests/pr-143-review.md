# PR 143 review: each plan row names its three-task case and kill criterion; 6, 7, 8 and 5c are held (#142)

Reviewed by the author session against `AGENTS.md`, `.conventions/AGENTS-common.md` and the plan's own rules.

| Check | Result |
|---|---|
| Branch `docs/142-three-task-rule`, `Closes #142`, issue with its four parts before the first commit | ok |
| Test first: `test_every_entry_names_its_kill_criterion` and `test_small_entries_are_held_under_the_three_task_rule` failed on main and pass here (82 passed) | ok |
| The owner's word: the four questions and the holds ("do what you recommend", November 15, 2026) | ok |
| The holds are reversible: rows stay in the table with their commits, and the rule says when a held entry goes (no three-task candidate or repeat ready) | ok |
| Each "≥3 tasks plausible?" cell cites its evidence (write-ups, our CPU studies, spans), and none is presented as a measured gain | ok |
| Secrets, data, claims | none |

## Findings

None blocking.

- **Should know.** Entries 6, 7 and 8 are the other session's. It is told in the same hour, and its queue reads this
  page, so it skips held rows as it already skips the 5-minute 31B.
- **Nit, left as is.** The repeats that the freed slots are for are not rows yet. Which entry to repeat depends on the
  first scores, so the next check-in proposes them to the owner.

## Verdict

Approve. It starts no run and publishes nothing. Merge when the checks are green.
