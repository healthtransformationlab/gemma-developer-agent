# PR 153 review: the remaining slots go to stacked final candidates, E4B-all and 31B-d (#152)

Reviewed by the author session against `AGENTS.md`, `.conventions/AGENTS-common.md`, nlp ADR 0007 and the plan's own
rules.

| Check | Result |
|---|---|
| Branch `docs/152-stacked-final-candidates`, `Closes #152`, issue with its four parts before the first commit | ok |
| Test first: `test_the_final_candidates_are_the_stacks` and the changed order tests failed on main (6 failures) before the plan changed | ok |
| A decision is an ADR, not only a PR description (`AGENTS-common.md`, "Decisions and action items"): ADR 0002 with context, decision, consequences and when to revisit | ok |
| The owner's approval: asked "Do you want me to make this switch?" and answered "Do what you recommend" (November 15, 2026) | ok; this is the switch that was proposed |
| Every queued or held row keeps 13 cells, a three-task case and a kill criterion (#142) | ok; `test_every_entry_names_its_kill_criterion` passes |
| The timing hold (#150) still holds 31B-d until nlp #821 reports | ok |
| No submission file changes; E4B-all is main at `204216e`, already checked (87 tests, compiler, harness check with a scripted, simulated model) | ok |
| Every number cites its run or source; nothing simulated is presented as a result | ok |
| Secrets, data, claims | none |

## Findings

None blocking.

- **Noted, left as is.** 31B-d's skill predates the compile check (#144: on the development set, wrong edits 62 → 42 of
  about 4,400). A 31B-d rebuilt on main would carry it, but the 31B timing run (nlp #821) is measuring `31df2c0`, and
  the check changes refusals, not running time. The row and the ADR say so. If 31B-d is rebuilt for a repeat, rebase
  it on main.
- **Noted.** The old gate "If 31B-b runs past the 12-hour limit …" stays because a test pins it. It is conditional on a
  31B-b entry that won't now run unless 31B-d is split, and the timing rule covers 31B-d's time.
- **Risk accepted by the decision.** A stack's score can't be split among its changes. The kill criteria say which part
  comes out first: 5b for E4B-all; patch first for 31B-d.

## Verdict

Approve. It starts no run, publishes nothing and changes no submission file. It changes the queue's order (5b is
replaced by E4B-all), as the owner approved. Merge when the checks are green.
