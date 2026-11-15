# PR 137 review: the 31B comes second, and 31B-b gives it the Budget-Fit budget (#136)

Reviewed by the author session against `AGENTS.md`, `.conventions/AGENTS-common.md` and the plan's own rules.

| Check | Result |
|---|---|
| Branch `docs/136-31b-second-and-budget-fit`, `Closes #136`, issue with its four parts before the first commit | ok |
| Test first: `test_the_31b_comes_second_and_31b_b_waits_on_its_timing`, and 31B-b in `QUEUED` and `BRANCH`, failed on main (3 failed) and pass here (79 passed) | ok |
| The owner's word for the reorder: "31b needs to be second slot … can't win only through small model" (November 15, 2026) | ok |
| One change per entry: 31B-b (`c75c619`) differs from the 31B entry (`ed11c15`) only in `eval_config.yaml` | ok: `git diff ed11c15 c75c619 --stat` shows one file |
| Evidence cited for the budget: the public "Budget-Fit Single Agent" (8 minutes, 28 calls, 80 turns, 300 s), forum reports of normal scores and about 225 s a task including setup | ok; no number is ours, each is attributed |
| Risk: an entry over 12 hours scores nothing | gated: 31B-b goes only if the 31B entry finished inside 12 hours |
| Secrets, data, claims | none |

## Findings

None blocking.

- **Nit, left as is.** The 225-second figure is one team's measurement of the Budget-Fit bundle, not of ours. Ours adds
  the install call and `find.py`, and its prompt differs. The gate on the 31B entry's own timing is what protects the
  entry.
- **Nit, left as is.** The plan's row pattern now allows a hyphen (`31B-b`). No existing entry name changes how it's
  read.

## Verdict

Approve. It starts no run and publishes nothing: the queue submits files to the host's machines, which use no GPU
hours of ours, and the owner gave the order. Merge when the checks are green.
