# Where each number in the writeup comes from

`AGENTS.md`: no number is a result until a run produced it, and a figure names the run it came from. Paths are in
[health-transformation-lab-nlp](https://github.com/healthtransformationlab/health-transformation-lab-nlp) (`NLP/`)
unless another repository is named. Checked on November 10, 2026 against `NLP` main at `b12e2e0`.

Every agent number was measured with `htlnlp-harness-v1`, that repository's re-implementation of the competition's
documented harness. None is a score from the competition's evaluator. The word limit excludes references (the host's
reply in the competition's "Word Count" discussion, October 27, 2026).

## The title block, Figure 1 and the PDF

| Figure | Source |
|---|---|
| "Gemma 4 Developer Agent Competition, Paper Track [17]" and reference 17 | the "Citation" block of the competition's Overview page (kaggle.com/competitions/gemma-4-developer-agent), as the owner pasted it on November 10, 2026. Reference 17 gives the ten authors' surnames, the title, Kaggle and 2026 as that block does |
| "Topic: Tasks & Benchmarks" | the same page's list of paper topics: "Tasks & Benchmarks: Development of new tasks, evaluation datasets, or resources targeting code structure, graphs, and structured code generation" |
| "Data and code": three links and their licences | the same three releases the closing paragraph named until November 10, 2026: the Kaggle dataset (CC BY 4.0), `NLP` (Apache 2.0) and this repository (Apache 2.0). All three answered on November 10, 2026 |
| Figure 1: 197, 116, 113, 93 | the Section 4.1 table. "Built, pass both gates, licensed" is the 113 left after one task was withdrawn, one failed a gate and one was withheld |
| Figure 1: 48, 40, 5 | Section 6, "Results": 48 scored, a patch for 40, 5 resolved |
| Figure 1: 30, 25, 5 | Section 6, "Task fairness": 30 screened, 25 whose tests need a name or text the statement never gives, 5 that pass |

Figure 1 adds no number. `paper/figures/make_figure1.py` holds its ten counts and draws `figure1.svg`;
`paper/build_pdf.js` makes `figure1.png` from it and lays `writeup.md` out as `writeup.pdf` without changing a word.

## Section 1, the introduction

| Figure | Source |
|---|---|
| "Better health starts with accurate health information" | the headline of [healthtransformationlab.org](https://healthtransformationlab.org) and the `NLP` repository's description on GitHub |

## Section 2, related work

| Figure | Source |
|---|---|
| MLOps-Bench: 212 tasks with fail-to-pass tests from 31 public ML repositories | Tran et al., arXiv:2610.23506 (October 16, 2026), abstract: "212 validated tasks from 31 public ML repositories, with 636 fail-to-pass tests and 856 pass-to-pass tests"; each task has "a natural-language requirement, oracle patch, plausible buggy baseline, fail-to-pass tests, pass-to-pass tests, and provenance metadata". Read November 10, 2026 |
| data-eng-bench scores a produced artefact (dbt models) | the README and `CITATION.cff` of [`Snowflake-Labs/data-eng-bench`](https://github.com/Snowflake-Labs/data-eng-bench), version 1.0.0, released July 29, 2026: 103 dbt tasks on a retail warehouse, each scored by "a `pytest` verifier that checks the materialized tables row by row against a reference solution"; 16 of the 103 are bug fixes. Read November 10, 2026 |
| "labels each statement's source" in place of "a field the others lack" | SWE-bench takes every statement from an issue, so it has no need of such a field; the claim kept is what this set records, not what others lack |

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
| The 81 changes that are not candidates: 49 touch no Python file, 19 change tests without code, 13 change code without tests | the same manifest, `is_code_changed` and `is_tests_changed` (`NLP/python/health_transformation_lab_nlp/task_mine.py`, `classify_files`: code is a `.py` file that is not a test; a test is a `.py` file under `tests/` or named `test_*`). 49 + 19 + 13 = 81 = 197 − 116. The 49 are documentation, specs, decks and data. Not in the writeup, which gives the rule and both totals |
| Of the 93 published: 39 / 34 / 20 | the 93 task ids of `NLP/data/tasks/official_verifier/published_verification.csv` joined to `tier_code` in the manifest (`NLP` main at `d876fa6`); 39 + 34 + 20 = 93 |
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
| The rerun's patches: the same verdict as the author's harness on 23 of 23; 48 agent patches compared in all | the `gemma-4-e4b-it` rows of `NLP/data/tasks/official_verifier/published_verification.csv` against `is_rerun_resolved` in `NLP/data/tasks/agent_reruns/gemma-4-e4b-it_graph_tools.csv` (`NLP` pull request 648); 25 + 23 = 48 |
| The first release as published: all 3 tasks tried fail at import | the evaluator's own command line (`python -m swegemma eval --sandbox subprocess --skip-agent-patch`) on `htlnlp_116`, `htlnlp_143` and `htlnlp_174`: `ModuleNotFoundError` for the package during collection |
| The 20 tasks left out: 12, 6 and 2 | the `reason_text` column of the same table; each was rerun with full output and grouped by its error |
| What was tried before the harness was re-implemented | an install in a cloud session (`NLP/pull_requests/pr-421-review.md`), PyPI (`NLP/specs/035-local-agent-harness/spec.md`), and the competition's file list (`NLP` pull request 449). None tried the wheelhouse dataset |
| The author's control: reference patch resolves 111 of 113 | `NLP/data/tasks/agent_runs/oracle_tasks_gated.csv`. It ran from the repository's history, not from the published snapshots, which is why it did not see the withheld files |
| Empty patch resolves 0 of 113 | `NLP/data/tasks/agent_runs/null_tasks_gated.csv` |
| The review that found commands ran on the host | `NLP/pull_requests/pr-549-review.md` |
| Known differences from the competition's harness | `NLP/specs/035-local-agent-harness/spec.md` |

## Section 6, the baseline

All from `NLP/data/tasks/agent_runs/gemma-4-e4b-it_kaggle.csv` (58 rows) and its settings file
`gemma-4-e4b-it_kaggle_settings.json`, as merged by pull requests 620, 623, 630 and 648. Pull request 648 is the
rerun of November 10, 2026 (workflow run 42742256439): it replaced 28 rows, and the rows it replaced are kept
beside the new ones in `NLP/data/tasks/agent_reruns/gemma-4-e4b-it_graph_tools.csv` (the paired table).

| Figure | Source |
|---|---|
| 58 tasks attempted; 10 set aside; 48 scorable with 40 non-empty patches and 5 resolved; 35 fail the tests, 8 empty | `is_resolved`, `agent_patch_bytes`, `reason_text`, each task's latest run. The 10 set aside are the attempted tasks among the 20 left out of the published set: `htlnlp_pr38`, `pr39`, `pr40`, `pr41`, `pr44`, `pr49`, `pr61` (tests read withheld files) and `htlnlp_122`, `172`, `185` (`PYTHONSAFEPATH`) |
| The paired rerun: 23 published tasks; resolved 2 and 2; patches 18 and 20; one task lost, one gained, one both | the paired table, rows with `is_published`: `is_first_resolved`, `is_rerun_resolved`, `first_patch_bytes`, `rerun_patch_bytes`. The first run is the run table's row at `NLP` commit `db0a29d`, before the harness fault of `NLP/specs/035-local-agent-harness/tasks.md` (T005) was fixed. 28 tasks were rerun; five are not in the published set. Lost `htlnlp_144`, gained `htlnlp_226`, both `htlnlp_pr63` |
| A graph tool called in 4 of 23 runs, 6 calls among 145 | `rerun_graph_tool_call_count` and `rerun_tool_call_count` in the paired table, published rows. The calls are counted from each run's transcript; all six are `search_similar_code` |
| By tier: 4 of 24, 1 of 19, 0 of 5 | joined to `tier_code` in the manifest, over the 48 |
| 30 with failing tests, 5 with errors | `verify_exit_code` 1 and 2, over the 48 |
| Eight empty patches: four hit the token limit, three submit without an edit, one calls the edit tool with an argument it does not take | each run's `result.json`, downloaded from its Kaggle notebook output on November 10, 2026. `htlnlp_206`, `236`, `cfa7c008` and `pr23` each have a turn at exactly 2,048 output tokens; `htlnlp_120`, `152` and `230` call `submit_patch` without an edit; `htlnlp_71` calls `edit_file` four times with `start_line`, which the tool rejects. `NLP/pull_requests/pr-630-review.md` had attributed the first five to the limit |
| 20.6 GPU-hours for the 58 first attempts, 9.6 for the 28 reruns, 30.2 in all; median 0.39 GPU-hours, 7 tool calls, about 91,000 prompt tokens | `gpu_hours` summed over the run table at `NLP` commit `db0a29d` (20.56) and `rerun_gpu_hours` over the paired table (9.64); the medians are over the run table's 58 rows as they are now |
| About $21 at $0.69 per T4-hour (an estimate) | `estimated_cost_usd`: 14.19 for the first attempts, 6.65 for the reruns; `price_basis_text` |
| The screen: 30 of the 93, 5 pass, 25 with tests that need a name or text the statement never gives | `NLP/data/tasks/screening/agent_screen.csv` and its `README.md` (`NLP` pull request 653): drawn with seed 20261110 within each statement source (13 of 39, 11 of 34, 6 of 20); `is_pass` is both ratings 0 or 1, the rule of SWE-bench Verified [2]; `test_rating_num` is 2 or 3 for 25. An AI reviewer made both passes; the second agrees with the first on all 30 but had read the first's ratings |
| "I checked its findings in summary and agreed with all 30" | the same table, `owner_fair_code` and `owner_note_text`: on November 10, 2026 the author answered one question per task (is the test fair) from two plain-language sentences, with the AI's verdict already selected: fair 5, unfair 25, cannot tell 0. The author did not read the test code. It is a check of the AI's findings, not an independent rating, which is what Section 8 says |
| Of 16 screened tasks the model attempted: 1 of the 3 that pass resolved, 0 of the 13 that fail | the same table, `is_attempted` and `is_resolved` against `is_pass`; the resolved one is `htlnlp_pr63` |
| Not in the writeup from the same table | 10 of 30 statements rated vague or worse; 4 fixes, 14 features, 12 maintenance changes; the statement names the fix fully in 10 and partly in 17 |
| Confidence intervals | Wilson, 95%; named once in the text since an outside review took them for Clopper-Pearson (which would give 3.5 to 22.7 for 5 of 48) |
| "48 of 93 tasks, cheapest first" (Section 8) | the setup's own sentence: tasks were run cheapest first under a GPU-hour cap, so the 48 are not a sample of the 93 and 5 of 48 is not a rate for the set |
| "No human screening" (Section 8) | no annotation pass over the tasks exists in `NLP/data/tasks/`: the checks are the two gates and the evaluator's reference-patch and empty-patch controls. SWE-bench Verified's screening, of whether a statement specifies what its tests require, was not done |

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
- Why most of the second repository's candidates cannot be tied to a pull request (fast-forwarded and squashed
  merges): cut from Section 4.5 on November 10, 2026 to make room for the limits two outside reviews asked for.
  The counts are in the Section 4 table above.
- Why the repository's issue count is not the task count. On November 10, 2026 the repository had 313 closed issues
  and 312 merged pull requests (GitHub's search API). The task set mines merged changes on `main` as of October 29,
  2026 (197), so nothing merged later is in it: 114 of the 313 closed issues were opened after that date. 67 of the
  313 are the backfilled records of Section 4.2.
- The two health-AI studies that opened Section 1 (GlobalDentBench, arXiv:2605.24636v2: twelve models averaged 81.34% on
  multiple-choice and 22.34% on case-based questions; First, do NOHARM, arXiv:2512.01241v4: omissions are more than 80%
  of severe errors on a 1,100-task benchmark): cut on November 10, 2026 to make room for the screen. Two outside
  reviews had called them peripheral to coding agents. They were references 15 and 16; MLOps-Bench and data-eng-bench
  took those numbers.
- The keyword count of de-identification tasks that closed Section 7 (16 of 116 candidates; 5 attempted, none
  resolved): cut the same day for the same reason. Its row is in the Section 7 table above.
- "38 of 305 merged pull requests" from Section 3 (a keyword count of the pull requests that touch the three artifacts):
  cut on November 10, 2026 to make room for the author's check. Its row is in the Section 3 table above.
- "Data, harness and run tables are public." (the abstract's last sentence) and the closing paragraph that listed the
  three releases: replaced on November 10, 2026 by the "Data and code" paragraph under the abstract, which names the
  same three releases and licences as links a reader can open from page 1. "Where each number comes from is listed
  in `paper/sources.md`" became "each number's source" beside this repository's link.
- An independent human screen of task quality: not done. The screen of 30 is an AI reviewer's, checked by the
  author in summary (Section 6 above).
- A split of all 93 tasks into fixes, features and maintenance: not done; the screen classifies its 30. The mining
  rule keeps any change that touches code and tests, so the set is not only bug fixes.
