---
pr: 28
branch: docs/27-title-and-abstract-caveats
title: "000 DOCS9: return to the earlier title and put the baseline's caveats in the abstract (held for the owner)"
author: Claude Code (agent session for jcbowyer)
reviewed_at: 2026-11-10
reviewer: the authoring session (each changed sentence was read against the section it summarises; no reviewer subagent run)
verdict: approve, held for the owner
---

# PR Review: 000 DOCS9: return to the earlier title and put the baseline's caveats in the abstract

## Summary
Six sentences change and no number does. The title goes back to the one the writeup had before pull request 16;
the abstract's two sentences about the baseline carry the settings, the order the tasks were run in and the fact
that the evaluator did not run the agent; contribution 4 and two sentences of the conclusion claim less. Three of
four outside reviews asked for the first, and the latest named the rest. Nothing blocking. Held for the owner: the
title is the owner's choice, made the other way one day earlier.

## Checks
| Check | Result |
|---|---|
| The title | the text of `paper/writeup.md` at `60843bd`, before pull request 16 added "Silent defects in health data:" |
| The subtitle still says what the paper is | unchanged: 93 evaluator-verified tasks, an open harness, a Gemma 4 E4B baseline |
| "Under tight limits (2,048 output tokens, thinking off)" | Section 6, Setup |
| "5 of 48 tasks, run cheapest first" | Section 6: 48 scorable tasks, 5 resolved; "Tasks were run cheapest first under a GPU-hour cap" |
| "the official evaluator, which did not run the agent, gives the same verdict on all 48 patches compared" | Section 5's table (25 of 25 and 23 of 23) and Section 8, "My harness ran the agent" |
| Contribution 4 says what Section 4.5 shows | 133 candidates, none linking an issue; the second repository was not gated or released, so "evidence that the rule makes a history minable" claimed more |
| "The released tasks let others measure that gap" | the set is public (Section 9); the sentence no longer says the gap has been measured against the standard sets |
| "should transfer" | one repository where the recipe ran and one mining check on a second |
| The silent-defect motivation is still in the paper | Section 1's second paragraph, Section 7 and the limit "The tasks are not silent" are unchanged |
| No number changed | the diff is six lines; no digit differs except those newly quoted from Section 6 |
| Word count | 2,996 without references by `wc` (2,997 before); limit 3,000 |
| Nothing else names the old title | `README.md`, `paper/sources.md` and `paper/outline.md` do not quote it |
| Branch name and issue link | `docs/27-title-and-abstract-caveats`, `Closes #27` |

## Should fix
- The owner decides the title. If "silent defects" should stay in it, the other five edits stand on their own.
- Drafts outside this repository that carry the title (the Kaggle post drafts, the review prompts) need the same
  change if this is merged.
- Not taken up from the same reviews: shrinking Sections 4.5 and 7, a split of the tasks by kind of defect, and
  running the agent under the competition's evaluator, which every review ranks first and which is a GPU run.

## Secrets, Real Data and Claims Scan
Secrets: none. Real data: none. Claims: none added; four are narrowed and two caveats move forward into the
abstract.
