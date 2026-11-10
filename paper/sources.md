# Where each number in the writeup comes from

`AGENTS.md`: no number is a result until a run produced it, and a figure names the run it came from. Paths are in
[health-transformation-lab-nlp](https://github.com/healthtransformationlab/health-transformation-lab-nlp) (`NLP/`)
unless another repository is named. Checked on November 10, 2026 against `NLP` main at `b12e2e0`.

Every agent number was measured with `htlnlp-harness-v1`, that repository's re-implementation of the competition's
documented harness. None is a score from the competition's evaluator.

## Section 3, the source repository

| Figure | Source |
|---|---|
| 960 commits, October 25 to November 8, 2026 | `git rev-list --count origin/main`; first and last commit dates |
| 710 with a co-author trailer | `git log origin/main -i --grep='Co-authored-by: Claude'` |
| 65 authored as the agent, 175 squash merges, 5 bot, 4 owner only | the 250 commits without a trailer, grouped by author, committer and a `(#n)` subject |
| 240 review files, pull requests up to 634 | `NLP/pull_requests/pr-*-review.md` |
| 192 with a verdict: 119 approve, 64 approve with minor findings, 9 other approve forms, 0 request changes | the `verdict:` line of each review's front matter |
| The four cases reserved for the owner | `NLP/AGENTS.md`, "Branches and issues", rule 6 |

## Section 4, the task set

| Figure | Source |
|---|---|
| 197 changes, 116 candidates, tiers 49 / 45 / 22 | `NLP/data/tasks/task_manifest.csv` (`is_candidate`, `tier_code`) |
| 67 backfilled issue records | the tier B and C candidates (45 + 22), each with an `issue_number` in the manifest |
| 115 built, 114 pass both gates | `NLP/data/tasks/task_gates.csv` (`is_valid`) |
| The three tasks left out, with reasons | `NLP/data/tasks/tasks_excluded.csv` |
| 113 published; median 488 nodes and 397 `calls` edges; the format check | `NLP/specs/028-dataops-task-set/tasks.md` (T009 to T011) |
| Second repository: 1,320 first-parent commits, 133 candidates (all committed by the author), 22 through a pull request | `git log --first-parent` on [`getcommunityone/open-navigator`](https://github.com/getcommunityone/open-navigator) (Apache 2.0) main at `6fa4943`; its README describes it as an "AI-powered civic engagement platform", and its owner confirmed on November 10, 2026 that it may be cited; a change counts when its diff has a non-test `.py` file and a test `.py` file (under `tests/`, or named `test_*.py` or `*_test.py`). Not gated |

## Section 5, the controls

| Figure | Source |
|---|---|
| Reference patch resolves 111 of 113 | `NLP/data/tasks/agent_runs/oracle_tasks_gated.csv` |
| Empty patch resolves 0 of 113 | `NLP/data/tasks/agent_runs/null_tasks_gated.csv` |
| The review that found commands ran on the host | `NLP/pull_requests/pr-549-review.md` |
| Known differences from the competition's harness | `NLP/specs/035-local-agent-harness/spec.md` |

## Section 6, the baseline

All from `NLP/data/tasks/agent_runs/gemma-4-e4b-it_kaggle.csv` (58 rows) and its settings file
`gemma-4-e4b-it_kaggle_settings.json`, as merged by pull requests 620, 623 and 630.

| Figure | Source |
|---|---|
| 58 tasks, 45 non-empty patches, 5 resolved, 40 fail the tests, 13 empty | `is_resolved`, `agent_patch_bytes`, `reason_text` |
| 36 tasks without the code graph, 22 on the fixed harness | `NLP/specs/035-local-agent-harness/tasks.md` (T005) for the fault; the split is by `run_ts` before and after 2026-11-06 12:00 UTC, with the three pilot rows (no `run_ts`) in the first group. The table has no batch column, so this split is mine |
| 30 and 15 non-empty patches; 5 and 0 resolved | the same split |
| 0.53 against 0.27 GPU-hours per task | `gpu_hours` summed over each group (11.75 over 22; 8.81 over the 33 rows that record it) |
| By tier: 4 of 27, 1 of 26, 0 of 5 | joined to `tier_code` in the manifest |
| 35 with failing tests, 5 with errors | `verify_exit_code` 1 and 2 |
| Six empty patches with no tool call | `tool_call_count` 0 among the empty-patch rows |
| Empty patches traced to the 2,048-token limit | `NLP/pull_requests/pr-630-review.md`. I did not re-read the transcripts |
| 20.6 GPU-hours, 10.3 allowance hours, median 0.32 GPU-hours, 6 tool calls, about 74,000 prompt tokens | `gpu_hours`, `gpu_hours / gpu_count`, `tool_call_count`, `prompt_token_count` |
| $14.19 at $0.69 per T4-hour (an estimate) | `estimated_cost_usd`, `price_basis_text` |
| Confidence intervals | Wilson, 95% |

## Section 7, the three cases

| Figure | Source |
|---|---|
| De-identification 1.00 and 0.27 (`regex_v2`, hard and unseen tiers) | `NLP/data/deid/scores.csv` (`entity_recall`) |
| Tooth-loss AUC 0.89 to 0.90 and 0.59 to 0.63 | `NLP/docs/tooth_loss.md`, "After the tooth-table fixes of #631" (completed-extraction models) |
| The masking defect | the same section; fixed by pull request 632 |
| 16 de-identification candidates, 8 attempted, none resolved | a keyword match on `title_text` in the manifest (`de-id`, `phi`, `maccrobat`, `presidio`, `redact`, `mask`), joined to the run table. The match is mine and approximate |

## Not in the writeup, and why

- The switch-off test in `pipeline-doctor`: its rules were written from the same nine incidents it is scored on, its
  trailing runs are simulated, and its "no conventions" condition blanks five data columns.
- Any result for the pipeline-doctor skill or the analyzer sub-agent: neither has been run.
- Any score on the competition's development set: not run.
