---
pr: 30
branch: docs/29-report-task-screen
title: "000 DOCS10: report the screen of 30 tasks and what it means for the baseline (held for the owner)"
author: Claude Code (agent session for jcbowyer)
reviewed_at: 2026-11-10
reviewer: the authoring session (every figure recomputed from the screening table; no reviewer subagent run)
verdict: approve, held for the owner
---

# PR Review: 000 DOCS10: report the screen of 30 tasks and what it means for the baseline

## Summary
The writeup gains one finding and loses four passages to make room. The finding: of 30 published tasks screened,
5 pass, and in 25 the tests need a name or text the statement never gives; the model resolved 1 of the 3 passing
tasks it attempted and none of the 13 failing ones. The text says who made the screen (an AI reviewer) and what the
author's part was (a check of its findings from summaries, not a reading of the tests). Nothing blocking. Held for
the owner: it changes how the paper's headline result reads and cuts the two health-AI studies from the
introduction.

## Checks
| Check | Result |
|---|---|
| 30 screened, 5 pass, 25 with tests rated 2 or 3 | `NLP/data/tasks/screening/agent_screen.csv` (pull request 653): `is_pass` true for 5; `test_rating_num` of 2 or 3 for 25 |
| "I checked its findings in summary and agreed with all 30" | `owner_fair_code`: fair 5, unfair 25, cannot tell 0; `is_owner_agree` true for 30; pasted by the owner on November 10, 2026 |
| 16 attempted; 1 of 3 and 0 of 13 | `is_attempted`, `is_resolved` against `is_pass`; the resolved one is `htlnlp_pr63` |
| "the baseline may measure the tasks more than the model" | hedged as "may": 16 tasks, three of them passing, cannot show more |
| Section 8 says what the check was | "I did not read the tests; the AI's verdict was shown first", which is how the sheet worked |
| "63 tasks are unscreened" | 93 - 30 |
| Each cut loses no figure the rest of the paper uses | references 15 and 16 were cited only in the cut sentences; "38 of 305" and the de-identification count appear nowhere else |
| Citations and references agree | [1] to [16]: each cited, each listed; MLOps-Bench and data-eng-bench renumbered 15 and 16 in Section 2 |
| Word count | 2,992 without references by `wc` (2,996 before); limit 3,000 |
| `paper/sources.md` | a row for the screen, one for the author's check, one for what is not in the writeup from the same table; each cut recorded under "Not in the writeup" |
| Branch name and issue link | `docs/29-report-task-screen`, `Closes #29` |

## Should fix
- Do not merge before `health-transformation-lab-nlp` pull request 653: until then the table this cites is on a
  branch.
- The cut from Section 1 is the owner's to accept: the two health-AI studies were the paper's link to why the
  source repository exists. "In health data the costly defect is silent" and Section 7 remain.
- The screen covers 30 of 93. A judge may ask for the other 63; the same method would take them.
- If the paper session adds a result from the competition's evaluator, it will need words: the count stands eight
  under the limit.

## Secrets, Real Data and Claims Scan
Secrets: none. Real data: none. Claims: one finding added, from a committed table, with who made it stated in the
abstract, Section 6 and Section 8; three sentences that cited outside studies or keyword counts removed.
