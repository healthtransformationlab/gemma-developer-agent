---
pr: 20
branch: docs/19-published-93-verified
title: "000 DOCS5: the published set is 93 tasks, verified with the competition's evaluator as published"
author: Claude Code (agent session for jcbowyer)
reviewed_at: 2026-11-10
reviewer: the authoring session (every changed figure was recomputed from the other repository's committed tables; no reviewer subagent run)
verdict: approve
---

# PR Review: 000 DOCS5: the published set is 93 tasks, verified with the competition's evaluator as published

## Summary
The writeup, its sources and the two README files now describe dataset version 4: 93 tasks, verified with the
competition's evaluator on the files as published. The baseline is recounted over the published tasks. Nothing
blocking.

## Checks
| Check | Result |
|---|---|
| 93 of 93 reference patches, 0 of 93 empty patches, on the published files | `health-transformation-lab-nlp` `data/tasks/official_verifier/published_verification.csv` (its pull request 647): 93 `reference` rows resolved, 93 `empty` rows not |
| The published set is the 93 verified | the published `tasks.jsonl` has 93 rows whose ids equal the verified ids |
| 48 scorable attempts, 38 with a patch, 5 resolved (10.4%, 4.5 to 22.2) | the run table restricted to the 93: 48 rows, 38 with `agent_patch_bytes` above zero, 5 resolved; Wilson interval recomputed |
| 31 and 17; 26 and 12; 5 and 0 | the same split by `run_ts` as before, over the 48 |
| 0.55 against 0.27 GPU-hours | means 0.555 and 0.266 over the rows of each group that record it |
| Tiers 4 of 24, 1 of 19, 0 of 5 | joined to the manifest |
| 43 unresolved: 33 failing patches (28 failing tests, 5 errors), 10 empty; 4 with no tool call | `verify_exit_code` and `tool_call_count` over the 48 |
| Five empty patches among the last 17: four at the token limit, one without an edit | the six read earlier, less `htlnlp_122`, which is one of the ten set aside |
| De-identification: 5 attempted among those published, none resolved | 16 candidates by the title match, 12 of them published, 5 attempted |
| The two conditions are not presented as a designed experiment | the text says they were not planned and names the fault; the paragraph after the table still says they are not a comparison of the graph tools |
| No stale figure left | no "51", "33 of", "18 later", "needs a fix" or "version 3" remains in the writeup; "113" remains only where it is the count before the evaluator's check |
| README agrees with the writeup | 93 tasks; 48 run, 5 resolved (10.4%, 4.5 to 22.2); 38 patches; 31 and 17 |
| Word count | 2,989 without references |
| Branch name and issue link | `docs/19-published-93-verified`, `Closes #19` |

## Should fix later
- If the rerun of the early tasks on the fixed harness finishes before the deadline, Section 6 gets a paired
  comparison and the "not planned" clause can go. That is a separate change for the owner to read first.

## Secrets, Real Data and Claims Scan
Secrets: none. Real data: none. Claims: one added (the published files verify), from a committed table; one
limitation removed because it no longer holds.
