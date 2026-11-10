---
pr: 40
branch: docs/39-official-evaluator-run
title: "000 DOCS12: report the agent run by the competition's own evaluator (held for the owner)"
author: Claude Code (agent session for jcbowyer)
reviewed_at: 2026-11-10
reviewer: the authoring session (every new figure was recomputed from the run's table on health-transformation-lab-nlp pull request 658; no reviewer subagent run)
verdict: approve, held for the owner
---

# PR Review: 000 DOCS12: report the agent run by the competition's own evaluator (held for the owner)

## Summary
The paper reports the agent run end to end by the competition's evaluator on a seeded sample of 20 tasks: none
resolved. Nothing blocking in the text. Held because it changes the abstract and the results, and until the rows it
cites are on the other repository's `main`.

## Checks
| Check | Result |
|---|---|
| 0 of 20; 0 to 16.1 | `is_resolved` over the 20 `is_in_sample` rows; Wilson for 0 of 20 |
| 16 fail, 4 submit nothing | `reason_text`: 11 + 5 with a patch, 4 empty |
| No run reached a budget | longest agent phase 238.4 s of 300; most tool calls 22 of 40 |
| 189 tool calls: 9, 3, 0 | the four count columns summed over the sample |
| Settings named in the text | `_settings.json`: 16,384 output tokens, thinking budget 4,096, 40 tool calls, 5.0 minutes; four NVIDIA L4 in every row |
| "drawn with a fixed seed and stratified by tier, not by cost" | `sample` in `_settings.json` and `official_agent_run.sample` |
| 13 in the screen, 11 fail it | joined to `data/tasks/screening/agent_screen.csv`: 13 rows, `is_pass` true for 2 |
| "half of the tasks have no hints" | 48 of 93 published rows have an empty `hints_text` |
| "I fixed it before those tasks ran" | the three first-pass rows are in `_hints_defect.csv`; the table's rows for those tasks are the rerun; the nine with hints render the same prompt under both forms |
| 12.8 L4 GPU-hours for 21 runs | `script_seconds` sums to 11,524 s; times four GPUs |
| The abstract claims no more than the section | "a seeded sample of 20", "resolved none"; the interval is in Section 6 |
| "the competition's hardware and my competition settings" | four L4s is the competition's machine; the settings are this repository's, and the limitation says where they differ from the defaults |
| The limitation that no score is a leaderboard score is kept | "no score here is comparable to the leaderboard"; `check_rules.py` still passes its "Honest reporting" row |
| Figure 1 | 20, 16, 0 match the text; the zero is drawn as a label with no bar; read in the PNG |
| PDF | rebuilt; the new paragraph is on page 6; 8 pages |
| Rules table | regenerated; `--check` passes; 2,980 words |
| Other sessions' text | unchanged: title block, Sections 1 to 5, "Task fairness", the screen's limitation |
| Branch name and issue link | `docs/39-official-evaluator-run`, `Closes #39` |

## Should fix
- Do not merge before `health-transformation-lab-nlp` pull request 658.
- The cut from Section 6's cost line (median tool calls and prompt tokens of the baseline) is the one thing removed
  that a reader might miss; it is still in `sources.md`.

## Secrets, Real Data and Claims Scan
Secrets: none. Real data: none. Claims: one added (0 of 20 under the competition's evaluator), with its interval and
its limits; one limitation removed because it no longer holds.
