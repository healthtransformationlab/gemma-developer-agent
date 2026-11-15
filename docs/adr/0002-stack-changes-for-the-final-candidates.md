# ADR 0002: the remaining slots go to stacked final candidates, not one change at a time

Date: 2026-11-15 · Status: accepted · Issue: #152

## Context

Since #126 the leaderboard plan has submitted one change per entry, as health-transformation-lab-nlp ADR 0007 decided:
each entry differs from the one it is compared with by one change, so the score difference is that change's effect.

By the evening of November 15 that rule had stopped serving the goal, for three reasons.

- **Few slots.** Kaggle allows one pending entry per team, and scoring takes 12 or more hours. About 6 slots remain
  before December 2.
- **Noise.** The same submission varies by about ±2–3 of the 58 public tasks (write-ups 91230 and 93326). A single
  change worth one or two tasks can't be told apart from noise, which is why entries 6, 7 and 8 were held (#142).
- **The goal is to win, not to measure.** Two prizes are open: the main prizes, which in practice need the 31B, and the
  $10k small-model bonus. Submitting one change at a time means the combination with the most evidence behind it may
  never be submitted at all.

The builds already stack:

- **31B-d** (`31df2c0`): the 31B with the Budget-Fit budget (31B-b), a single agent (31B-c) and the patch-first rule.
  Its skill predates the compile check (#144). The commit is left as it is, because the 31B timing run (nlp #821) is
  measuring it.
- **Main** (`204216e`), E4B:
  - copyfix;
  - the edit-fallback skill with its compile check;
  - no graph tools;
  - short anchors;
  - scratch cleanup;
  - the 12,288-token budget.

  Entry 5b has only copyfix and the skill.

A reviewing model made the same argument, and the owner agreed ("do what you recommend", November 15, 2026).

## Decision

- **The final candidates are the stacks:**
  - E4B-all (main at `204216e`) for the small-model bonus;
  - 31B-d for the main prizes.

  Each goes in as one entry. E4B-all comes right after entry 5. 31B-d goes once the 31B timing run (nlp #821) clears
  its budget, or at the capped budget that run calls for.
- **Their parts are held:** 5b (part of E4B-all), and 31B-b and 31B-c (parts of 31B-d). Their rows and commits stay.
- **A freed slot repeats whichever candidate is closer to its prize's line.** One repeat checks that the score isn't a
  one-off and, for the 31B, that it stays inside 12 hours. Finals are chosen on reproducibility, running time and
  failure modes, not on one public score.
- **The one-change rule still holds for any new single change,** which must also pass the three-task rule (#142).
  Entry 5 (copyfix alone) still goes first, as the check that the adapter serves on the scorer.

## Consequences

- **Easier:** our strongest combinations reach the leaderboard about two slots sooner, and the repeats give the final
  choice something to stand on.
- **Harder:** a stack's score can't be split among its changes. If E4B-all or 31B-d scores worse than expected, which
  change hurt is not known from the leaderboard. Traces (the colab-skill run, the 31B timing run) and the CPU studies
  are what remain for that.
- **The other session's queue reads the plan**, so the switch takes effect through `docs/leaderboard-plan.md`.

## Revisit when

- **A stack scores clearly below its best part's evidence:** E4B-all under entry 5, or 31B-d under 0.12. Then split it,
  starting with the part whose evidence is weakest.
- **More slots open:** Kaggle's pending limit changes, or scoring speeds up.
- **A new single change** passes the three-task rule with evidence strong enough to be worth a slot of its own.

## Amended

- **2026-11-15 (#156):**
  - **Order.** 31B-d goes before E4B-all once the timing run clears it, as the owner set ("31b needs to be second slot")
    and as the approved recommendation said ("when the timing run clears, submit 31B-d first"). The rows had E4B-all
    first.
  - **E4B-all's commit.** It moves from `204216e` to `a09e97e` (#154), which makes the install and `find.py` the first
    two calls. In the Modal colab-skill run, 0 of 10 tasks installed the skill on the previous prompt. E4B-all is held
    until a 5-task E4B run on Modal shows `run_skill_script` in at least half the tasks. If it doesn't, E4B-all goes at
    `204216e`.
- **2026-11-15, about 23:40 UTC (#159):** entry 5 (copyfix alone) is skipped, the owner's choice. It would have held the
  one slot for about 12 hours to check what E4B-all checks too, since it carries copyfix. 31B-d goes as soon as its
  timing run clears it; if it isn't cleared and submitted by 02:00 UTC on November 16, E4B-all goes at `204216e`.
