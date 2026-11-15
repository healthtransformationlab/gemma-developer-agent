# PR 106 review: delete scratch files before submitting, checked with git status (#104)

| Check | Result |
|---|---|
| Branch `fix/104-scratch-files-git-status`, `Closes #104` | ok |
| Test first: `test_scratch_files_are_removed_before_submitting` fails on main's prompt (checked by stashing the prompt change: 1 failed, 9 passed) and passes with it (10 passed) | ok |
| The issue's Done when: the step before `submit_patch` names `git status --short` and says to delete every file made only to try or check the fix | ok |
| No extra tool call: the listing is appended to the test command step 7 already runs (`pytest ...; git status --short`) | ok |
| No change to tools, budgets or sampling (Contract) | ok |
| The grader's rules (`docs/rulebook-notes.md`): untracked files are diffed into the patch, so removing scratch files changes only what the patch carries | ok |
| Secrets, real data, claims | none |
| CI (`check`, `conventions / check`) on 5962b54 | green |

## Findings

- Minor: the step tells the agent to `rm` untracked files it made. A task whose fix is a new file keeps it ("either
  part of the fix or removed"), so the wording doesn't push it to delete a needed file. Whether the model follows
  that distinction is for the run to show.
- Not measured: the issue says no score change is claimed until a paired GPU run against main on the 23 development
  tasks. That run waits on the owner's go-ahead.

## Verdict

Nothing blocking. Hold the merge until the paired run, since main is what the next leaderboard entry is built from.
