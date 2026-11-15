# PR 157 review: 31B-d goes before E4B-all; E4B-all waits on the skill-use check (#156)

Reviewed by the author session against `AGENTS.md`, `.conventions/AGENTS-common.md`, ADR 0002 and the plan's rules.

| Check | Result |
|---|---|
| Branch `docs/156-31b-first-e4b-all-check`, `Closes #156`, issue with its four parts before the first commit | ok |
| Test first: the order, queued-list and new `test_e4b_all_waits_on_the_skill_use_check` tests failed on main (4 failures) | ok |
| The order matches the owner's "31b needs to be second slot" and the approved recommendation ("when the timing run clears, submit 31B-d first") | ok |
| The colab-skill result is named at its source (Kaggle dataset `jcblearning/htlnlp-colab-official-colab-skill`, read in this session): 0 of 10 installed | ok |
| ADR 0002 is amended with a dated section, not rewritten | ok |
| Every row keeps 13 cells, a three-task case and a kill criterion | ok |
| Secrets, data, claims | none |

## Findings

None blocking.

- **Risk, accepted.** Only entry 5 is queued now. If neither the timing run nor the skill-use check has reported when
  entry 5 is scored (about 12:00 UTC, November 16), the slot sits idle. Both are planned for tonight on Modal, under
  ADR 0008's $5 cap, and the November 17 check-in reads them.
- **Noted.** 31B-d's prompt still has the install at step 2, where the 31B smoke test skipped it (0 of 3). Moving the
  calls into 31B-d would change the commit the timing run is measuring. If 31B-d is rebuilt for a repeat, it gets #154
  and the compile check together.

## Verdict

Approve. It starts no run, publishes nothing and changes no submission file. It changes the queue order and which
commit E4B-all names, as #156 sets out. Merge when the checks are green.
