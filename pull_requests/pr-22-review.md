---
pr: 22
branch: docs/21-paired-rerun
title: "000 DOCS6: report the paired rerun in Section 6 (held for the owner)"
author: Claude Code (agent session for jcbowyer)
reviewed_at: 2026-11-10
reviewer: the authoring session (every changed figure was recomputed from the other repository's tables on its pull request 648; no reviewer subagent run)
verdict: approve, held for the owner
---

# PR Review: 000 DOCS6: report the paired rerun in Section 6 (held for the owner)

## Summary
Section 6 reports the paired rerun in place of a split it had itself called confounded. The headline is unchanged
(5 of 48). Nothing blocking in the text. It waits for the owner because it changes the results section, and for
`health-transformation-lab-nlp` pull request 648, whose tables it cites.

## Checks
| Check | Result |
|---|---|
| 48 tasks, a patch for 40, 5 resolved (10.4%, 4.5 to 22.2) | the run table on pull request 648 restricted to the 93 published tasks; Wilson interval recomputed |
| Tiers 4 of 24, 1 of 19, 0 of 5 | unchanged: the task lost and the task gained are both tier A |
| Paired: 23 tasks, resolved 2 and 2, patches 18 and 20 | the paired table's published rows; lost `htlnlp_144`, gained `htlnlp_226`, both `htlnlp_pr63` |
| 8.7% (2.4 to 26.8) | Wilson, 2 of 23 |
| A graph tool in 4 of 23 runs, 6 calls among 145 | `rerun_graph_tool_call_count` and `rerun_tool_call_count`, published rows |
| 35 failing patches (30 failing tests, 5 errors), 8 empty | `verify_exit_code` and `agent_patch_bytes` over the 48 |
| Eight empty patches: four, three, one | the eight transcripts: `htlnlp_206`, `236`, `cfa7c008`, `pr23` have a turn at 2,048 output tokens; `htlnlp_120`, `152`, `230` submit without an edit; `htlnlp_71` makes four `edit_file` calls the tool rejects |
| 20.6 + 9.6 = 30.2 GPU-hours; about $21; 6.0 per resolved task | 20.56 and 9.64; 14.19 + 6.65 = 20.84; 30.2 / 5 = 6.04 |
| Median 0.39 GPU-hours, 7 tool calls, about 91,000 prompt tokens | the run table's 58 rows: 0.387, 7, 91,489 |
| 48 agent patches compared, none where the verifiers differ | 25 earlier and 23 from the rerun |
| The resolved tasks' descriptions | titles of `htlnlp_116`, `143`, `174`, `226`, `pr63` in the manifest |
| The claim is hedged as far as the evidence goes | "no measurable difference" is not in the text as a law: it gives the counts, says the transcripts "suggest why", and the limitation says one task flipping moves the result |
| Nothing else changed a number | the trims were read line by line |
| Word count | 2,988 without references |
| Branch name and issue link | `docs/21-paired-rerun`, `Closes #21` |

## Should fix
- Do not merge before `health-transformation-lab-nlp` pull request 648: until then the tables this cites are on a
  branch.
- "Runs with the tools took longer (0.35 against 0.21 GPU-hours)" was drafted and cut: the cause is not known, so it
  is left to the paired table.

## Secrets, Real Data and Claims Scan
Secrets: none. Real data: none. Claims: two added (the paired result, the tool-use count), both from committed
tables; one sentence that promised an experiment is replaced by its result.
