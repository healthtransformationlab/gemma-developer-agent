# Where each number in the writeup comes from

`AGENTS.md`: no number is a result until a run produced it, and a figure names the run it came from. Paths are in
[health-transformation-lab-nlp](https://github.com/healthtransformationlab/health-transformation-lab-nlp) (`NLP/`)
unless another repository is named. Checked on November 10, 2026 against `NLP` main at `b12e2e0`.

Every agent number was measured with `htlnlp-harness-v1`, that repository's re-implementation of the competition's
documented harness. None is a score from the competition's evaluator. The word limit excludes references (the host's
reply in the competition's "Word Count" discussion, October 27, 2026).

## Section 1, the introduction

| Figure | Source |
|---|---|
| Twelve models: 81% on dental licensing-exam questions, 22% on questions from published patient cases | Zhao et al., *GlobalDentBench*, arXiv:2605.24636v2, abstract: accuracy "plummeted from 81.34% on multiple-choice to 64.53% on short-answer and 22.34% on case-based questions" across "12 frontier LLMs". Read November 10, 2026; also in `NLP/docs/claims.yaml` |
| Omissions are more than 80% of severe errors on 1,100 medical consultation cases | Wu et al., *First, do NOHARM*, arXiv:2512.01241v4, abstract: "a 1,100-task benchmark of primary care-to-specialist consultation cases" and "errors of omission accounting for more than 80% of severe errors" across 20 models and 4 retrieval tools. A preprint, in general medicine, with no oral-health cases. Read November 10, 2026 |
| "Better health starts with accurate health information" | the headline of [healthtransformationlab.org](https://healthtransformationlab.org) and the `NLP` repository's description on GitHub |

## Section 3, the source repository

| Figure | Source |
|---|---|
| 960 commits, October 25 to November 8, 2026 | `git rev-list --count origin/main`; first and last commit dates |
| 710 with a co-author trailer | `git log origin/main -i --grep='Co-authored-by: Claude'` |
| 65 authored as the agent, 175 merge commits, 5 bot, 4 owner only, 1 initial commit | the 250 commits without a trailer, grouped by author, committer and subject: 175 "Merge pull request #n" commits made by GitHub, 4 by the owner alone (three documentation edits and one merge of `main` into a branch), and GitHub's "Initial commit". 710 + 65 + 175 + 5 + 4 + 1 = 960. Squash merges carry the trailer and are among the 710 |
| 240 review files, pull requests up to 634 | `NLP/pull_requests/pr-*-review.md` |
| 192 with a verdict: 119 approve, 64 approve with minor findings, 9 other approve forms, 0 request changes | the `verdict:` line of each review's front matter |
| The four cases reserved for the owner | `NLP/AGENTS.md`, "Branches and issues", rule 6 |
| More than half of the author's time on three artifacts | the author's own estimate; not measured |
| 38 of 305 merged pull requests touch those artifacts | titles of the merged pull requests in `NLP` from GitHub's search API (November 10, 2026), matched for the entity diagram and data dictionary (5), the results tables, metric display and SHAP (22), and the data-quality page and dashboards (11). The match is by keyword and approximate |

## Section 4, the task set

| Figure | Source |
|---|---|
| 197 changes, 116 candidates, tiers 49 / 45 / 22 | `NLP/data/tasks/task_manifest.csv` (`is_candidate`, `tier_code`) |
| 67 backfilled issue records | the tier B and C candidates (45 + 22), each with an `issue_number` in the manifest |
| 115 built, 114 pass both gates | `NLP/data/tasks/task_gates.csv` (`is_valid`) |
| The three tasks left out, with reasons | `NLP/data/tasks/tasks_excluded.csv` |
| 113 after one is withheld; median 488 nodes and 397 `calls` edges; the format check | `NLP/specs/028-dataops-task-set/tasks.md` (T009 to T011) |
| 93 published | `NLP/data/tasks/official_verifier/swegemma_verification.csv`: the tasks whose reference patch the competition's evaluator resolves and whose empty patch it does not (`task_gate.evaluator_verified`). The 20 left out, each with its reason, are in `NLP/data/tasks/tasks_excluded.csv` |
| Second repository: 1,320 first-parent commits, 133 candidates, 22 tied to a pull request, none linking an issue | `git log --first-parent` on [`getcommunityone/open-navigator`](https://github.com/getcommunityone/open-navigator) (Apache 2.0) main at `6fa4943`; its README describes it as an "AI-powered civic engagement platform", and its owner confirmed on November 10, 2026 that it may be cited. A change counts when its diff has a non-test `.py` file and a test `.py` file (under `tests/`, or named `test_*.py` or `*_test.py`). Tied to a pull request: the commit subject ends in `(#n)` or starts with "Merge pull request". Linking an issue: the message has `closes`, `fixes`, `resolves` or `refs` followed by `#n`. Not gated |
| 169 merged pull requests (of 204: 15 open, 20 closed without merging) | GitHub's search API, read November 10, 2026. 33 of the 169 left no `(#n)` subject on `main` (14 fast-forwarded, 18 squashed or rebased under another subject or merged elsewhere, 1 through a merge commit with another subject), so 22 is a lower bound |

## Section 5, the controls

| Figure | Source |
|---|---|
| The competition's evaluator: 93 of 113 reference patches, 0 of 113 empty patches, the same verdict as the author's harness on 25 of 25 saved patches | `NLP/data/tasks/official_verifier/swegemma_verification.csv` and its `README.md` (`NLP` pull request 642). `swegemma` 0.2.11 from the Kaggle dataset `metric/gemma-4-developer-agent-wheelhouse`, its `harness.verification.verify_task` unmodified, subprocess sandbox, run November 10, 2026 on copies of the first release's snapshots (dataset version 3) with a `conftest.py` added at the root, the text that `task_graph.EVALUATOR_CONFTEST_TEXT` now writes into every snapshot |
| The corrected release as published: 93 of 93 reference patches, 0 of 93 empty patches | `NLP/data/tasks/official_verifier/published_verification.csv` (`NLP` pull request 647): the same driver on dataset version 4, downloaded from Kaggle on November 10, 2026, with nothing added. Its 93 task ids are the 93 the first table vouches for, and each published snapshot's head matches `NLP/data/tasks/snapshot_index.csv` |
| The first release as published: all 3 tasks tried fail at import | the evaluator's own command line (`python -m swegemma eval --sandbox subprocess --skip-agent-patch`) on `htlnlp_116`, `htlnlp_143` and `htlnlp_174`: `ModuleNotFoundError` for the package during collection |
| The 20 tasks left out: 12, 6 and 2 | the `reason_text` column of the same table; each was rerun with full output and grouped by its error |
| What was tried before the harness was re-implemented | an install in a cloud session (`NLP/pull_requests/pr-421-review.md`), PyPI (`NLP/specs/035-local-agent-harness/spec.md`), and the competition's file list (`NLP` pull request 449). None tried the wheelhouse dataset |
| The author's control: reference patch resolves 111 of 113 | `NLP/data/tasks/agent_runs/oracle_tasks_gated.csv`. It ran from the repository's history, not from the published snapshots, which is why it did not see the withheld files |
| Empty patch resolves 0 of 113 | `NLP/data/tasks/agent_runs/null_tasks_gated.csv` |
| The review that found commands ran on the host | `NLP/pull_requests/pr-549-review.md` |
| Known differences from the competition's harness | `NLP/specs/035-local-agent-harness/spec.md` |

## Section 6, the baseline

All from `NLP/data/tasks/agent_runs/gemma-4-e4b-it_kaggle.csv` (58 rows) and its settings file
`gemma-4-e4b-it_kaggle_settings.json`, as merged by pull requests 620, 623 and 630.

| Figure | Source |
|---|---|
| 58 attempts; 10 set aside; 48 scorable with 38 non-empty patches and 5 resolved; 33 fail the tests, 10 empty | `is_resolved`, `agent_patch_bytes`, `reason_text`. The 10 set aside are the attempted tasks among the 20 left out of the published set: `htlnlp_pr38`, `pr39`, `pr40`, `pr41`, `pr44`, `pr49`, `pr61` (tests read withheld files) and `htlnlp_122`, `172`, `185` (`PYTHONSAFEPATH`) |
| 31 scorable tasks without the code graph, 17 on the fixed harness | `NLP/specs/035-local-agent-harness/tasks.md` (T005) for the fault; the split is by `run_ts` before and after 2026-11-06 12:00 UTC, with the three pilot rows (no `run_ts`) in the first group. The table has no batch column, so this split is mine |
| 26 and 12 non-empty patches; 5 and 0 resolved | the same split |
| 0.55 against 0.27 GPU-hours per task | `gpu_hours` averaged over the rows of each group that record it |
| By tier: 4 of 24, 1 of 19, 0 of 5 | joined to `tier_code` in the manifest, over the 48 |
| 28 with failing tests, 5 with errors | `verify_exit_code` 1 and 2, over the 48 |
| Four empty patches with no tool call | `tool_call_count` 0 among the empty-patch rows, over the 48 |
| Five empty patches on the fixed harness: four hit the token limit, one submitted without editing | the `turns[].output_tokens` of each run's `result.json`, downloaded from its Kaggle notebook output on November 10, 2026: `htlnlp_206`, `236`, `cfa7c008` and `pr23` each have a turn at exactly 2,048; `htlnlp_120` ends in two turns (so does `htlnlp_122`, one of the 10 set aside). `NLP/pull_requests/pr-630-review.md` had attributed all of them to the limit |
| 20.6 GPU-hours, 10.3 allowance hours, median 0.32 GPU-hours, 6 tool calls, about 74,000 prompt tokens | `gpu_hours`, `gpu_hours / gpu_count`, `tool_call_count`, `prompt_token_count` |
| $14.19 at $0.69 per T4-hour (an estimate) | `estimated_cost_usd`, `price_basis_text` |
| Confidence intervals | Wilson, 95% |

## Section 7, the three cases

| Figure | Source |
|---|---|
| De-identification 1.00 and 0.27 (`regex_v2`, hard and unseen tiers) | `NLP/data/deid/scores.csv` (`entity_recall`) |
| Tooth-loss AUC 0.89 to 0.90 and 0.59 to 0.63 | `NLP/docs/tooth_loss.md`, "After the tooth-table fixes of #631" (completed-extraction models) |
| The masking defect | the same section; fixed by pull request 632 |
| 16 de-identification candidates; 5 scorable attempts, none resolved | a keyword match on `title_text` in the manifest (`de-id`, `phi`, `maccrobat`, `presidio`, `redact`, `mask`), joined to the run table. Three more were attempted but are among the 10 set aside. The match is mine and approximate |

## Not in the writeup, and why

- The switch-off test in `pipeline-doctor`: its rules were written from the same nine incidents it is scored on, its
  trailing runs are simulated, and its "no conventions" condition blanks five data columns.
- Any result for the pipeline-doctor skill or the analyzer sub-agent: neither has been run.
- Any score on the competition's development set: not run.
