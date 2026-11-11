# Where each number in the writeup comes from

`AGENTS.md`: no number is a result until a run produced it, and a figure names the run it came from. Paths are in
[health-transformation-lab-nlp](https://github.com/healthtransformationlab/health-transformation-lab-nlp) (`NLP/`)
unless another repository is named. Checked on November 10, 2026 against `NLP` main at `b12e2e0`; the rows on the competition's development set, on what a failing test's report adds, on the cost in dollars and on the pre-registered experiment were added on November 11, 2026.

Every agent number was measured with `htlnlp-harness-v1`, that repository's re-implementation of the competition's
documented harness, except the 20 tasks of "the agent under the competition's evaluator", the three arms of "the pre-registered
experiment" and the 40 development tasks of "beside the competition's own tasks" below. None is a
leaderboard score. The word limit excludes references (the host's
reply in the competition's "Word Count" discussion, October 27, 2026).

## The title block, Figure 1 and the PDF

| Figure | Source |
|---|---|
| "Gemma 4 Developer Agent Competition, Paper Track [14]" and reference 14 (17 until three references were cut on November 10, 2026) | the "Citation" block of the competition's Overview page (kaggle.com/competitions/gemma-4-developer-agent), as the owner pasted it on November 10, 2026. The reference gives the ten authors' surnames, the title, Kaggle and 2026 as that block does |
| "Topic: Tasks & Benchmarks (resource paper)" | the same page's list of paper topics: "Tasks & Benchmarks: Development of new tasks, evaluation datasets, or resources targeting code structure, graphs, and structured code generation". "Resource paper" is the author's own description: the main contribution is the released task set |
| "Data and code": three links and their licences | the same three releases the closing paragraph named until November 10, 2026: the Kaggle dataset (CC BY 4.0), `NLP` (Apache 2.0) and this repository (Apache 2.0). All three answered on November 10, 2026 |
| "Quickstart notebook" | `kaggle.com/code/jcblearning/coding-agent-tasks-quickstart`: public (`is_private` false in its kernel metadata, read through Kaggle's API on November 10, 2026), last run November 10, 2026; its source is `NLP/notebooks/agent_tasks_quickstart.ipynb`, pushed by `NLP/kaggle/prepare_kernel.py`. It loads a task, its snapshot, graph and embeddings ("Using the set", Section 8) |
| Figure 1: 197, 116, 113, 93 | Section 4.1 (a table until November 11, 2026). "Built, pass both gates, licensed" is the 113 left after one task was withdrawn, one failed a gate and one was withheld |
| Figure 1: 48, 40, 5 | Section 6, "Results": 48 scored, a patch for 40, 5 resolved |
| Figure 1: 0, 4, 5 | Section 6, "A pre-registered experiment": resolved as published (of the 21 tasks that arm ran), with graph retrieval (of 93) and with the failing test's report (of 93); rows below. Until November 11, 2026 this group showed the first sample of 20 (20, 16, 0) |
| Figure 1: 93, 76, 17 | Section 6, "Task fairness": the second screen of all 93, 76 whose tests need a name or text the statement never gives (`test_rating_num` 2 or 3), 17 that pass (the core split). Until November 11, 2026 this group showed the first screen of 30 (30, 25, 5) |

Figure 1 adds no number. `paper/figures/make_figure1.py` holds its thirteen counts and draws `figure1.svg`;
`paper/build_pdf.js` makes `figure1.png` from it and lays `small-local-agent-redo-cloud-agent-work.md` out as `small-local-agent-redo-cloud-agent-work.pdf` without changing a word.

## The abstract

Each figure is in a section below; these rows say which. The five headings in bold sort the results (what the model
did unattended, what more context did, where the fixes were, what the graph could tell it, where its time went); the figures under each are the measurements.
The framing by a person's loop, and the wish to show what the graph is worth, are the owner's (November 10, 2026).

| Figure | Source |
|---|---|
| "In fifteen days, one person in the loop with a cloud coding agent ... from nothing to 960 commits and 2,269 tests" (the tests: Section 3's row below; "775 marked as agent-authored" is in Section 3, not in the abstract since November 11, 2026) | Section 3 (rows below): 960 commits on `main` from GitHub's initial commit on October 25 to November 8, 2026, fifteen days counting both ends; 775 = 710 with the agent's co-author trailer + 65 authored as the agent. The other 185 are 175 merge commits GitHub made for pull requests, 5 by an automation bot, 4 by the owner alone and the initial commit. The owner asked on November 10, 2026 for the abstract to lead with this |
| "without typing code" | the four commits by the owner alone are three documentation edits and one merge of `main` into a branch (Section 3, the row on the 250 commits without a trailer); every other change came through a coding-agent session's pull request |
| "one person in the loop"; "that loop" | Section 1 and Section 3: every change was made by a coding-agent session the owner directed in chat; `NLP/AGENTS.md` ("Branches and issues", rule 6) keeps limited-compute runs, publishing, deletions and rule changes for the owner's word |
| "Scripts turn its CI-enforced record into 93 ... tasks" (the record: issues, pull requests and reviews) | Section 1's row on the scripts, and Section 3: `NLP/AGENTS.md` requires an issue per user story and a pull request tied to it, CI rejects a pull request without an issue link, and 240 reviews are committed as files. The issue rule was adopted partway through (Section 4.2's tiers B and C: no issue existed), so this says what the record holds, not that every change has all three |
| "health-data modelling tasks" | Section 1's row on the kinds of work, below |
| "by the competition's own mining rule, format and evaluator" | Section 4.1 (a candidate touches both non-test code and test files, the competition's own mining rule), Section 5 (its evaluator on all 93) and Section 4.3: the format check against the competition's own files (snapshot layout, graph keys, embedding shape) |
| "the 17 whose statements say what their tests check form a core split" | Section 6, "Task fairness" (rows below): the 17 tasks that pass the second screen, listed in `NLP/data/tasks/screening/core_split.csv` |
| "unattended" | each task ran from the prompt to a submitted patch with no person acting: the harness loop of `NLP` spec 035, one task per offline Kaggle notebook |
| "5 of the 48 tasks it ran, cheapest first" ("95% CI 4.5–22.2%" and "all small": not in the abstract since November 11, 2026; Section 6, "Results", has both) | Section 6, "Setup", "Results" (the Wilson interval of 5 of 48) and "How it fails" (a CI rule, a warning message, a label parser and two settings) |
| "With eight times the output budget it resolved 2 of the 23 cheapest, against 2" (not in the abstract since November 11, 2026; Section 6, "A larger budget", has it) | Section 6, "A larger budget": 16,384 output tokens a turn against 2,048, with thinking on |
| "Under the competition's evaluator it resolved none of a random 20" (not in the abstract since November 11, 2026; Section 6 has "A first seeded sample of 20 resolved none") | Section 6, "A pre-registered experiment" and the rows of "the agent under the competition's evaluator" below |
| "in a pre-registered experiment under that evaluator: with graph retrieval done for it, 4 of 93; with a failing test's report (from the hidden test: not a benchmark condition), 5 of 93" | Section 6, "A pre-registered experiment" (rows below). The report is built by running the task's `test_patch`, which no arm gives the agent |
| "The baseline arm's server failed after 21 tasks (none resolved), so neither context could be tested" | Section 6, "A pre-registered experiment" (rows below): the `statement` arm ran 21 of 93 tasks and resolved 0; each paired test has 21 pairs and no discordant one |
| "7 of those arms' 8 resolved tasks are in the core split" | Section 6, the sentence under the experiment's table (rows below). A description the plan names, not a test |
| "under the competition's evaluator, 3 of 23 verifiable tasks of the competition's own" (its development set) | Section 6, "Beside the competition's own tasks" (rows below): the same agent, settings and evaluator on a seeded 40 of the competition's 129 development tasks, of which 23 are verifiable in a Kaggle notebook |
| "it holds the edited code in 51 of the 93 tasks (114 of 129 in the competition's)" | Section 4.3 (`edited_node_count` above 0 in 51 rows of `graph_coverage.csv`) and the Section 6 table (114 of the 129 rows of `devset_graph_reach.csv`, rows below) |
| "leads from statement to fix in 42 of the 51" (by name, call edge or embedding search's first ten results) | Section 4.3 (rows below): 20 by a name, 2 more by call edges, and an edited node in the first ten by embedding similarity for 20 of the 29 that neither reaches; 51 tasks have a fix that edits a function, class or method the graph holds |
| Not in the abstract since November 11, 2026: "embedding search ranks an edited function first in 15 (0.6 by chance)" | Section 4.3 still has it, as "puts an edited one first in 15 of the 51 (0.6 expected by chance)" (rows below) |
| Not in the writeup since November 11, 2026: "The model asked a graph tool in only 20 of 473 tool calls" | 6 of 145 in the paired rerun, 5 of 139 with the larger budget and 9 of 189 in the first sample of 20. The Section 6 table now has "Tool calls to a graph tool, as published" for this set and the development set (rows below) |
| "66–83% of a task was model calls, by its OpenTelemetry spans" | Section 6, "Time, GPUs and cost" (rows below) |
| Not in the abstract since November 11, 2026 (Section 6 has both counts): "only 17 of 93 statements say what their tests check (an AI screen, matching all 30 a person checked), against 20 of 40 of the competition's" (the 20 of 40: "Beside the competition's own tasks", rows below) | Section 6, "Task fairness" (rows below): 17 pass the second screen; "say what their tests check" is the screen's pass, both ratings 0 or 1 |
| Not in the abstract since November 11, 2026 (Section 6, "Time, GPUs and cost", has it): "the 13 of those 17 it ran gave 4 of its 5 fixes for 17% of its time" (the tasks a name or call edge reaches, 3 for 20%: not in the writeup since november 11, 2026) | Section 6, "Cost, and what to send" (rows below) |

## Section 1, the introduction

| Figure | Source |
|---|---|
| "adds one repository that is both, set beside the competition's four by its mining rule, format and evaluator, and compared with its own tasks" (the comparison: Section 6, "Beside the competition's own tasks") | "four" is the count Section 1 already gives for the competition's development set, two sentences earlier; this change adds no count. The set is not part of the competition's data and the paper does not say it is: "beside", not "in". The rule, format and evaluator are the rows of Sections 4.1, 4.3 and 5. The owner's point of November 10, 2026: the method is the competition's and is already run on several repositories; this set adds one of a different kind |
| "its tasks are real changes to application code: de-identification, record checks, model scoring, pipelines" | the 93 reference patches by the package modules they change, read from `NLP/data/tasks/graph_coverage.csv` (`edited_node_text`) and the manifest's titles: de-identification (`deid`, `deid_eval`, `phi_challenge`), record plausibility and data-quality checks (`plausibility`, `grader_tables`), model scoring and reliability (`judge`, `reliability`, `rungs`, `mlflow_judge`), and pipelines, tracking and dashboards (`runlog`, `tracking`, `telemetry`, `dashboards`). A description, not a count |
| Not in the writeup since November 11, 2026 (cut to leave a margin under the word limit; the abstract's "Scripts turn its CI-enforced record into 93 ... tasks" rests on this row): "Coding-agent sessions made every change, and scripts make every step from merged change to published task" (the sessions: Section 3's rows) | mining `NLP/python/health_transformation_lab_nlp/task_mine.py`; building tasks, snapshots, graphs and embeddings `python/scripts/55_build_tasks.py`; gates `57_gate_tasks.py`; publishing `kaggle/publish_tasks.py` and `.github/workflows/kaggle-publish-tasks.yml`; the evaluator's controls `kaggle/official_verify.py`. The set was mined as of October 29, 2026; rebuilding it on later history has not been done |
| "with a person in the loop" ("what does the person need for the rest?": not in the writeup since november 11, 2026) | the abstract's rows above: the owner directed every session; the question is the paper's framing |
| Every record is synthetic | `NLP/DISCLAIMER.md`; stated in the title block and in "synthetic dental records" |
| The contributions as reworded on November 11, 2026: "with a 17-task core split"; "A baseline and a pre-registered experiment"; "all 93 tasks with graph retrieval or a failing test's report added"; "Checks on the recipe" | Section 6 (rows below): the core split, the development-set run and the two arms that ran all 93 tasks; Sections 4.3 and 6 for the two checks. No new count |

## Section 2, related work

| Figure | Source |
|---|---|
| MLOps-Bench: 212 tasks with fail-to-pass tests from 31 public ML repositories | Tran et al., arXiv:2610.23506 (October 16, 2026), abstract: "212 validated tasks from 31 public ML repositories, with 636 fail-to-pass tests and 856 pass-to-pass tests"; each task has "a natural-language requirement, oracle patch, plausible buggy baseline, fail-to-pass tests, pass-to-pass tests, and provenance metadata". Read November 10, 2026 |
| data-eng-bench scores a produced artefact (dbt models) | the README and `CITATION.cff` of [`Snowflake-Labs/data-eng-bench`](https://github.com/Snowflake-Labs/data-eng-bench), version 1.0.0, released July 29, 2026: 103 dbt tasks on a retail warehouse, each scored by "a `pytest` verifier that checks the materialized tables row by row against a reference solution"; 16 of the 103 are bug fixes. Read November 10, 2026 |
| RepoGraph and LocAgent "lead an agent to the code to edit by finding an issue's terms in a code graph and walking its edges" | Ouyang et al., ICLR 2025 (arXiv:2410.14684): a repository-level graph of definitions and references, searched for terms from the issue and expanded to their neighbours, plugged into existing agents. Chen et al., ACL 2025 (aclanthology.org/2025.acl-long.426): a graph of files, classes and functions with contain, import, invoke and inherit edges, and tools to search it by keyword and traverse it. Both checked against their abstracts on November 10, 2026. They replace Defects4J and BugsInPy as references 3 and 4, so no other reference number changes |
| "labelled with its statement's source" (contribution 1) | It replaced "a field the others lack": SWE-bench takes every statement from an issue, so it has no need of such a field; the claim kept is what this set records, not what others lack |
| "Section 6 runs the agent with the walk done for it" | the `graph` arm of the experiment (Section 6 rows below): the retrieval is given to the agent in its task text. The arm ran; whether it helps is not tested (the baseline arm ran 21 tasks) |
| "one entry counts such signals on the competition's 129 tasks [15], close to the counts here" | Ali Hassan, "Model-free localization benchmark on the 129 public tasks", Paper Track discussion 748395 (October 11, 2026) and its notebook (`kaggle.com/code/alikalwar`), read November 11, 2026: 117 tasks have an edit site in the graph, "Only 28% of reports name the exact function", and the edit site is "within 2 hops of a symbol mentioned in the report in 47.9% of tasks". Here, on the same 129 (the Section 6 table): 114 tasks edit a node the graph holds; the statement names one in 29 of them (25%) and a name or one call edge reaches one in 52 (46%). His rules and script 63's differ (keywords and two hops against names and one edge), so "close", not equal |
| Not in the writeup since November 12, 2026 (cut for length, with its reference): "another finds that test feedback lifts this model on planted bugs and asks whether that holds on real issues" | Anisha Mehajabin, "Localizing Gemma 4 Agents via AST-Guided Retrieval" (a Writeup in this track) and Paper Track discussion 756473 (November 6, 2026), read November 11, 2026: on 50 single-operator bugs planted in each of two libraries, showing the failing test output and retrying took Gemma 4 E4B from 26% to 42% (p = 0.008) and from 22% to 36% (p = 0.016), exact McNemar; the post asks "whether this holds for bigger models, or for real issues rather than planted bugs". Section 6's `report` arm gives a failing test's report once, with no retry, on real changes; it does not answer that question (no baseline for most tasks) |
| Reference 15 | Hassan's notebook, two rows above: cited by its author's name as shown on Kaggle, its title and the year. It is not peer-reviewed: another entry's own account |

## Section 3, the source repository

| Figure | Source |
|---|---|
| 960 commits, October 25 to November 8, 2026 | `git rev-list --count origin/main`; first and last commit dates |
| "On November 8 it held 2,269 tests in 126 files, run by CI on every pull request" | `python -m pytest --collect-only -q tests` in `NLP/python` at `b12e2e0` (November 8, 09:52 Central), the commit where `git rev-list --count` reaches 960: 2,269 tests collected (1,547 test functions; each parametrized case counts once) in 126 `test_*.py` files. At `254c44c` (November 10), the commit the analyses use, 2,355 in 133. `NLP/.github/workflows/ci.yml` runs on every pull request and every push to `main`; its R parity job runs when a changed file can reach it, and in full every Monday |
| 710 with a co-author trailer | `git log origin/main -i --grep='Co-authored-by: Claude'` |
| "the rest are merge commits (175), a bot's (5), the author's (4) and the initial one" (65 of the 250 were authored as the agent) | the 250 commits without a trailer, grouped by author, committer and subject: 175 "Merge pull request #n" commits made by GitHub, 4 by the owner alone (three documentation edits and one merge of `main` into a branch), and GitHub's "Initial commit". 710 + 65 + 175 + 5 + 4 + 1 = 960. Squash merges carry the trailer and are among the 710 |
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
| Not in the writeup since November 12, 2026: 67 backfilled issue records | the tier B and C candidates (45 + 22), each with an `issue_number` in the manifest |
| 115 built, 114 pass both gates | `NLP/data/tasks/task_gates.csv` (`is_valid`) |
| The three tasks left out, with reasons | `NLP/data/tasks/tasks_excluded.csv` |
| 113 after one is withheld; median 488 nodes and 397 `calls` edges; the format check | `NLP/specs/028-dataops-task-set/tasks.md` (T009 to T011) |
| In 31 of the 93 tasks the reference patch touches no module the graph covers | `NLP/data/tasks/graph_coverage.csv` (`is_fix_in_graph` false for 31, true for 62), written by `NLP/python/scripts/63_graph_coverage.py` from dataset version 4 as downloaded on November 10, 2026 (`NLP` pull request 660). A changed file counts when it is `python/<module path>.py` and that module holds a node of the task's graph; a module the patch adds is not in the base commit's graph. 155 of the 1,173 files the 93 patches change are such modules (not in the writeup: a patch carries documents and data too) |
| Not in the writeup since November 11, 2026: "new modules, scripts, notebooks, configuration or documents" (what those 31 patches touch instead) | the changed files of those 31 patches, grouped by path and extension (my grouping, approximate): documents in 29 of the 31, configuration, CI or pipeline files in 20, notebooks in 12, a package module that is not in the base graph in 9, data or figures in 7, scripts in 6 |
| "The graph misses the fix in 42 of the 93 tasks": 31 + 11 | the two rows around this one: `is_fix_in_graph` false in 31 rows, and true with `edited_node_count` 0 in 11 |
| "11 change no existing function or class" | the same table: `is_fix_in_graph` true and `edited_node_count` 0 in 11 rows. The patch changes a module the graph covers, but only at module level, in a decorator, or by adding new functions; no changed line falls inside a function, class or method the base commit already had |
| "In the other 51": the fix edits a function or class the graph holds | `edited_node_count` above 0 in 51 rows. An edited node is the innermost function, class or method that holds a line the patch removes or replaces, or that holds both neighbours of lines it only inserts, read from the task's snapshot with the graph builder's own naming (`edited_nodes`); `edited_node_text` lists them. Counting inserted lines for the def above gives 54 |
| The statement names an edited function or class in 20 | `statement_to_fix_edge_count` 0 in 20 rows. A node is named when the last part of its id is a whole identifier in the problem statement or hints of five characters or more with an underscore or a capital, or when an inline code span is exactly that name, optionally qualified or called (`named_nodes`); `statement_node_text` lists them. A fixed rule, not a judgement: a statement that describes a function without its name names nothing, so the count is a lower bound. Thirteen of the 20 are named by the identifier rule alone; the other seven by a code span (`runlog.run`, `telemetry.setup()`, `track()`, `fit`, `readme_results.breakdown`, `rungs.HFEncoder.fit`), each read by hand |
| Call edges lead from a named one to an edited one in 2 more | `statement_to_fix_edge_count` 1 (`htlnlp_143`) and 3 (`htlnlp_235`): the fewest `calls` edges, followed in either direction, from any named node to any edited node (`call_distance`) |
| "call edges lead there from one it names" | the same two rows: "there" is an edited function or class |
| "in 29 neither does" | the column is blank in 29 of the 51 rows: the statement names no node of the graph in 25 of them and names only nodes with no path to an edit in 4 (`dental_omop_nlp.judge.Verdict` and `labels.Status` match as plain capitalised words in three of the four; without them the split is 27 and 2, and the 20, 2 and 29 do not change) |
| 22 of 93 (the abstract and the conclusion) | 20 + 2. In the other 71 tasks nothing joins statement and fix by names and call edges: the 29 above, and the 42 whose fix edits no node the graph holds (31 + 11) |
| "a node for each function, class and method with its source text, and a `calls` edge where one calls another" | `NLP/python/health_transformation_lab_nlp/task_graph.py` (`build_graph`): node keys `id`, `name`, `text`; edges `source`, `target`, `type` (always `calls`), `key`; calls are resolved through same-module names, imports, `self.<method>` and `<Class>.<method>` |
| Embedding search: an edited node "in the first ten in 30 (5.4 by chance), 20 of them among those 29"; "median 398" nodes | `NLP/data/tasks/statement_search.csv`, written by `NLP/python/scripts/64_statement_search.py` (`NLP` pull request 663): each task's statement and hints embedded with EmbeddingGemma at the nodes' pinned revision (query prompt; the nodes use the document prompt), cut to 256 dimensions and renormalised; nodes ranked by cosine similarity; `edited_node_best_rank_num` at most 10 in 30 of the 51 rows with an edited node and in 20 of the 29 where `is_named_or_called` is false. First in 15 and 11; in the first five in 23 and 17. The median `graph_node_count` of the 51 is 398. Run twice from separately written code with the same rank on all 93 tasks |
| "first in 15 of the 51 (0.6 expected by chance) and in the first ten in 30 (5.4 by chance)" | the chance that a random ranking of a task's nodes puts at least one edited node in the first k, summed over the 51 tasks: 0.6 for the first place, 2.9 for the first five, 5.4 for the first ten (`chance_top` in `NLP/python/scripts/64_statement_search.py`, `NLP` pull request 665; for the 29 that names and call edges miss: 0.5, 2.4 and 4.3 against 11, 17 and 20 observed) |
| "by name, call edge or embedding search the graph leads to the fix in 42 of the 51" | 20 + 2 + 20. The other 9 have an edited node that none of the three reaches (`unreached` in `NLP/data/tasks/cost_by_graph_reach.csv`) |
| Not in the writeup since November 11, 2026 as a sentence (the next paragraph says "not a result an agent achieved"): "counts from the published files, not agent runs" | the ranking says where the edited code sits in what a similarity search returns for the statement; no run here had the model make that search with the statement as its query |
| How the 93 rows were checked | two implementations written separately (their own diff parsers and AST walks) give the same edited nodes, named nodes and distance on all 93 tasks; all 1,926 definitions in the 159 modified package files are graph nodes whose text equals the snapshot's source (`NLP/pull_requests/pr-660-review.md`) |
| 93 published | `NLP/data/tasks/official_verifier/swegemma_verification.csv`: the tasks whose reference patch the competition's evaluator resolves and whose empty patch it does not (`task_gate.evaluator_verified`). The 20 left out, each with its reason, are in `NLP/data/tasks/tasks_excluded.csv` |
| The former Section 4.5, cut on November 11, 2026 when the competition's development set took its place (Section 6). Second repository: 1,320 first-parent commits, 133 candidates (commits that touch non-test Python and Python tests), 22 tied to a pull request, none linking an issue | `git log --first-parent` on [`getcommunityone/open-navigator`](https://github.com/getcommunityone/open-navigator) (Apache 2.0) main at `6fa4943`; its README describes it as an "AI-powered civic engagement platform", and its owner confirmed on November 10, 2026 that it may be cited. A change counts when its diff has a non-test `.py` file and a test `.py` file (under `tests/`, or named `test_*.py` or `*_test.py`). Tied to a pull request: the commit subject ends in `(#n)` or starts with "Merge pull request". Linking an issue: the message has `closes`, `fixes`, `resolves` or `refs` followed by `#n`. Not gated |
| 169 merged pull requests (of 204: 15 open, 20 closed without merging) | GitHub's search API, read November 10, 2026. 33 of the 169 left no `(#n)` subject on `main` (14 fast-forwarded, 18 squashed or rebased under another subject or merged elsewhere, 1 through a merge commit with another subject), so 22 is a lower bound |

## Section 4.3, what a failing test's report adds

Added on November 11, 2026 (this repository's issue 61). All from `NLP/data/tasks/trace_reach.csv`, written by
`NLP/python/scripts/68_trace_reach.py` (`NLP` pull requests 671 and 673; spec 028 T023): each of the 51 tasks'
snapshot as published, its test patch applied, and its test files run under the pytest plugin `_trace_plugin.py`,
which records names only.

| Figure | Source |
|---|---|
| "the tests of 23 of the 51 tasks call an edited function, but only 1 in a task those three miss" ("among a median of 7 public functions": not in the writeup since November 12, 2026) | `is_edited_in_trace` true in 23 rows; median `traced_node_count` 7 (public: no part of the name starts with an underscore). "Those three" are the name, the call edge and the embedding search of the paragraph above, which reach 42 of the 51. Of the 23, one is outside the 42: `htlnlp_pr21`. A failure's traceback holds an edited function in 7, all among the 23 (not in the writeup) |
| Not in the writeup since November 12, 2026: "which its OpenTelemetry spans would record" | `NLP/AGENTS.md`: every public function or method in the package gets `@traced` (`telemetry.py`, spec 014), and a test fails without it. The functions were recorded by a profiler, not read from exported spans; the span cap per caller (`MAX_SPANS_PER_CALLER`) limits repeated calls, not distinct functions |
| "In 15 the tests fail at import, and 13 of those errors name a module the fix changes, 5 in tasks those three miss" | `is_import_error` in 15 rows; `is_error_module_changed_by_fix` in 13 (the error's module is one the reference patch changes); outside the 42: `htlnlp_c5e54000`, `htlnlp_c7c49998`, `htlnlp_ca9964a0`, `htlnlp_cb988381`, `htlnlp_pr6`. In 9 the error names a name the patch defines on an added line (`is_missing_name_added_by_fix`), 3 of them outside the 42 and all among the 5 (not in the writeup) |
| "with the report, 48 of the 51" (it adds 6 to the 42) | the script's summary on the committed table: `statement_count` 42, `trace_not_statement_count` 1, `import_error_not_statement_count` 5, `report_not_statement_count` 6, `statement_or_report_count` 48. The report leads to the fix when an edited function is called by the tests or on a failure's traceback, or an import error names a name the fix adds or a module it changes (36 of the 51). Reached by neither: `htlnlp_109`, `htlnlp_cc73f4cf`, `htlnlp_pr8`. The review of `NLP` pull request 671 had credited all 6 to the functions called; a second session's check found they add 1 and the import errors 5, and `NLP` pull request 673 corrected the record |
| "uses the hidden test and the reference fix" (Section 4.3); "which uses the hidden test" (Section 6) | the test patch is the task's `test_patch`, which the agent is never given; 68's docstring says the same. Section 4.3's counts are from files; Section 6's `report` arm is the run that gave an agent the report |
| "An oracle-assisted analysis"; "This analysis uses the hidden test and the reference fix, so it is not a result an agent achieved; Section 6 gives an agent the report" | the counts need the task's hidden test (to make the report) and its reference patch (to know which node the fix edits). An outside review asked on November 11, 2026 that the 48 of 51 be labelled so. The `report` arm of Section 6 is the run that gives an agent the report |

## Section 5, the controls

| Figure | Source |
|---|---|
| The competition's evaluator: 93 of 113 reference patches, 0 of 113 empty patches, the same verdict as the author's harness on 25 of 25 saved patches | `NLP/data/tasks/official_verifier/swegemma_verification.csv` and its `README.md` (`NLP` pull request 642). `swegemma` 0.2.11 from the Kaggle dataset `metric/gemma-4-developer-agent-wheelhouse`, its `harness.verification.verify_task` unmodified, subprocess sandbox, run November 10, 2026 on copies of the first release's snapshots (dataset version 3) with a `conftest.py` added at the root, the text that `task_graph.EVALUATOR_CONFTEST_TEXT` now writes into every snapshot |
| The corrected release as published: 93 of 93 reference patches, 0 of 93 empty patches | `NLP/data/tasks/official_verifier/published_verification.csv` (`NLP` pull request 647): the same driver on dataset version 4, downloaded from Kaggle on November 10, 2026, with nothing added. Its 93 task ids are the 93 the first table vouches for, and each published snapshot's head matches `NLP/data/tasks/snapshot_index.csv` |
| The rerun's patches: the same verdict as the author's harness on 23 of 23; 48 agent patches compared in all | the `gemma-4-e4b-it` rows of `NLP/data/tasks/official_verifier/published_verification.csv` against `is_rerun_resolved` in `NLP/data/tasks/agent_reruns/gemma-4-e4b-it_graph_tools.csv` (`NLP` pull request 648); 25 + 23 = 48 |
| The first release as published: all 3 tasks tried fail at import (not in the writeup since november 11, 2026; the text keeps "no task could be scored") | the evaluator's own command line (`python -m swegemma eval --sandbox subprocess --skip-agent-patch`) on `htlnlp_116`, `htlnlp_143` and `htlnlp_174`: `ModuleNotFoundError` for the package during collection |
| The 20 tasks left out: 12, 6 and 2 | the `reason_text` column of the same table; each was rerun with full output and grouped by its error |
| What was tried before the harness was re-implemented | an install in a cloud session (`NLP/pull_requests/pr-421-review.md`), PyPI (`NLP/specs/035-local-agent-harness/spec.md`), and the competition's file list (`NLP` pull request 449). None tried the wheelhouse dataset |
| The author's control: reference patch resolves 111 of 113 | `NLP/data/tasks/agent_runs/oracle_tasks_gated.csv`. It ran from the repository's history, not from the published snapshots, which is why it did not see the withheld files |
| Empty patch resolves 0 of 113 | `NLP/data/tasks/agent_runs/null_tasks_gated.csv` |
| The review that found commands ran on the host (cut from the writeup on November 10, 2026, see the end) | `NLP/pull_requests/pr-549-review.md` |
| Known differences from the competition's harness | `NLP/specs/035-local-agent-harness/spec.md` |

## Section 6, the baseline

All from `NLP/data/tasks/agent_runs/gemma-4-e4b-it_kaggle.csv` (58 rows) and its settings file
`gemma-4-e4b-it_kaggle_settings.json`, as merged by pull requests 620, 623, 630 and 648. Pull request 648 is the
rerun of November 10, 2026 (workflow run 42742256439): it replaced 28 rows, and the rows it replaced are kept
beside the new ones in `NLP/data/tasks/agent_reruns/gemma-4-e4b-it_graph_tools.csv` (the paired table).

| Figure | Source |
|---|---|
| 58 tasks attempted; 10 excluded from the set (set aside); 48 scorable with 40 non-empty patches and 5 resolved (35 fail the tests and 8 are empty: both follow from those counts, and their sentence is not in the writeup since November 11, 2026) | `is_resolved`, `agent_patch_bytes`, `reason_text`, each task's latest run. The 10 set aside are the attempted tasks among the 20 left out of the published set: `htlnlp_pr38`, `pr39`, `pr40`, `pr41`, `pr44`, `pr49`, `pr61` (tests read withheld files) and `htlnlp_122`, `172`, `185` (`PYTHONSAFEPATH`) |
| Not in the writeup since November 11, 2026 (Section 6's graph arm gives graph retrieval to the agent on all 93): the paired rerun, 23 published tasks; resolved 2 and 2, one in common | the paired table, rows with `is_published`: `is_first_resolved`, `is_rerun_resolved`, `first_patch_bytes`, `rerun_patch_bytes`. The first run is the run table's row at `NLP` commit `db0a29d`, before the harness fault of `NLP/specs/035-local-agent-harness/tasks.md` (T005) was fixed. 28 tasks were rerun; five are not in the published set. Lost `htlnlp_144`, gained `htlnlp_226`, both `htlnlp_pr63` |
| Not in the writeup since November 11, 2026: 6 graph-tool calls among 145, in 4 of 23 runs | `rerun_graph_tool_call_count` and `rerun_tool_call_count` in the paired table, published rows. The calls are counted from each run's transcript; all six are `search_similar_code` |
| By tier: 4 of 24, 1 of 19, 0 of 5 (not in the writeup since november 11, 2026) | joined to `tier_code` in the manifest, over the 48 |
| 30 with failing tests, 5 with errors | `verify_exit_code` 1 and 2, over the 48 |
| Eight empty patches: four hit the token limit, three submit without an edit, one calls the edit tool with an argument it does not take | each run's `result.json`, downloaded from its Kaggle notebook output on November 10, 2026. `htlnlp_206`, `236`, `cfa7c008` and `pr23` each have a turn at exactly 2,048 output tokens; `htlnlp_120`, `152` and `230` call `submit_patch` without an edit; `htlnlp_71` calls `edit_file` four times with `start_line`, which the tool rejects. `NLP/pull_requests/pr-630-review.md` had attributed the first five to the limit |
| 20.6 GPU-hours for the 58 first attempts, 9.6 for the 28 reruns, 30.2 in all; median 0.39 GPU-hours, 7 tool calls, about 91,000 prompt tokens | `gpu_hours` summed over the run table at `NLP` commit `db0a29d` (20.56) and `rerun_gpu_hours` over the paired table (9.64); the medians are over the run table's 58 rows as they are now |
| Not in the writeup since November 10, 2026: about $21 at $0.69 per T4-hour (an estimate) | `estimated_cost_usd`: 14.19 for the first attempts, 6.65 for the reruns; `price_basis_text` |
| The first screen: "a random 30" (5 pass, 25 with tests that need a name or text the statement never gives: not in the writeup since November 12, 2026; the screen of all 93 gives 17 and 76) | `NLP/data/tasks/screening/agent_screen.csv` and its `README.md` (`NLP` pull request 653): drawn with seed 20261110 within each statement source (13 of 39, 11 of 34, 6 of 20); `is_pass` is both ratings 0 or 1, the rule of SWE-bench Verified [2]; `test_rating_num` is 2 or 3 for 25. An AI reviewer made both passes; the second agrees with the first on all 30 but had read the first's ratings |
| "Two AI screens"; the second "rated all 93", "blind to the first", "17 of 93 pass" | `NLP/data/tasks/screening/agent_screen_all.csv` and the second part of its `README.md` (`NLP` pull request 665): eight AI raters, each given a random share of the 93 tasks, the task files and the written protocol, and none of the first screen's ratings; the same two questions and scales. 17 pass (both ratings 0 or 1), 76 fail; the tests are rated 2 or 3 in 76 and the statement in 19 (20 until the last rater lowered one rating before it finished; no verdict changed). An AI reviewer's rating in one pass, not checked by a person outside the 30 |
| "the same verdict on all 30" | `is_same_as_checked` true in all 30 rows where `is_owner_checked` is true: 25 fail and 5 pass in both screens |
| "Those 17 are the set's core split; the other 76 stay as a collection of real statements that leave out what their tests need" | `NLP/data/tasks/screening/core_split.csv` and the "core split" part of that folder's `README.md` (`NLP` pull request 682): the 17 rows of `agent_screen_all.csv` with `is_pass` true (both ratings 0 or 1), tiers A 11 and B 6; the author checked 5 of them in the first screen (`is_owner_checked`). Named a split on November 11, 2026 after an outside review asked for a core subset for benchmark quality that keeps the broader collection. The 76 are the tasks whose tests need a name or text the statement never gives (`test_rating_num` 2 or 3). The split is a list of ids in the source repository; the Kaggle dataset's files are unchanged |
| No longer in the writeup: "26 tasks rated twice by different raters got the same verdict" | stand-in raters were started on two raters' tasks when those two had written nothing for nine minutes; all the first eight then finished, so 26 tasks have two ratings from raters who did not see each other's. Pass or fail is the same on all 26; the table keeps the first eight raters' ratings (`NLP/pull_requests/pr-665-review.md`) |
| Not in the writeup since November 11, 2026 as a sentence ("Time, GPUs and cost" keeps the 13 and the 4 of 5): "it resolved 4 of the 13 that pass and 1 of the 35 that fail" | the same table, `is_attempted` and `is_resolved` (from the Gemma 4 E4B run table, each task's latest run): 48 attempted, 13 of them pass the second screen with 4 resolved, 35 fail with 1 resolved (`htlnlp_116`). On the first screen's 30: 16 attempted, 1 of 3 passing resolved and 0 of 13 failing (no longer in the writeup) |
| Not in the writeup since November 11, 2026: "Seventeen of the 20 fail the second screen" | the 20 rows with `is_in_sample` in `NLP/data/tasks/official_agent_runs/gemma-4-e4b-it-qat-w4a16-ct_swegemma.csv` against `is_pass` in `agent_screen_all.csv`: 3 pass, 17 fail. On the first screen: 13 of the 20 were in it and 11 of those fail (no longer in the writeup) |
| Not in the writeup since November 11, 2026 (the core split's sentence took its place): "Each verdict and its reason are in the repository" | `NLP/data/tasks/screening/agent_screen.csv`: one row per screened task with both ratings, the reason for each, what the tests need that the statement lacks, the second check and the owner's answer; the protocol is in its `README.md` |
| SWE-bench's human screen "filtered out 68.3% of 1,699 annotated samples" (not in the writeup since november 11, 2026: the development set's 20 of 40 is the closer comparison) | Chowdhury et al. (OpenAI, August 2024): 1,699 randomly drawn samples annotated by software developers; 68.3% filtered out for underspecified issue descriptions, tests that reject valid solutions, or other issues. The method was read from the announcement and the 68.3% confirmed through a summary of it on November 10, 2026. The comparison is of kind, not of rate: theirs is a human screen of a random sample of twelve libraries, this one an AI reviewer's of 30 tasks |
| "the author checked its findings in summary and agreed with all 30" | the same table, `owner_fair_code` and `owner_note_text`: on November 10, 2026 the author answered one question per task (is the test fair) from two plain-language sentences, with the AI's verdict already selected: fair 5, unfair 25, cannot tell 0. The author did not read the test code. It is a check of the AI's findings, not an independent rating, which is what Section 7 says |
| Of 16 screened tasks the model attempted: 1 of the 3 that pass resolved, 0 of the 13 that fail | the same table, `is_attempted` and `is_resolved` against `is_pass`; the resolved one is `htlnlp_pr63` |
| Not in the writeup from the same table | 10 of 30 statements rated vague or worse; 4 fixes, 14 features, 12 maintenance changes; the statement names the fix fully in 10 and partly in 17 |
| Confidence intervals | Wilson, 95%; named once in the text since an outside review took them for Clopper-Pearson (which would give 3.5 to 22.7 for 5 of 48) |
| Not in the writeup since November 11, 2026 (cut to leave a margin under the word limit; Section 6's "Setup" says "Tasks ran cheapest first under a GPU-hour cap, so no rate here estimates the 93"): "The first baseline covers 48 of 93 tasks, cheapest first" (Section 7) | the setup's own sentence: tasks were run cheapest first under a GPU-hour cap, so the 48 are not a sample of the 93 and 5 of 48 is not a rate for the set |
| No longer in the writeup: "No human screening" (Section 7 now says "AI screens") | no annotation pass over the tasks exists in `NLP/data/tasks/`: the checks are the two gates and the evaluator's reference-patch and empty-patch controls. SWE-bench Verified's screening, of whether a statement specifies what its tests require, was not done |

## Section 6, cost by graph reach

| Figure | Source |
|---|---|
| The agent's 9.0 hours on the 48 tasks | `agent_seconds` summed over the 48 published rows of `NLP/data/tasks/agent_runs/gemma-4-e4b-it_kaggle.csv` (each task's latest run): 32,472 seconds, 9.02 hours, on two T4s. It is the agent's own time (the model's turns and its tool calls), which every run records; the session's GPU-hours are missing for the three earliest runs, two of them resolved, so they are not used here |
| Not in the writeup since November 11, 2026: 20% on the 12 a name or call edge reaches (3 of the 5 resolved); 43% on the 19 whose fix is outside the graph (2); 20% on the 9 only embedding search reaches (none) | `NLP/data/tasks/cost_by_graph_reach.csv`, written by `NLP/python/scripts/65_cost_by_graph_reach.py` (`NLP` pull request 663): `named_or_called` 12 run, 3 resolved, 20.2%; `outside_graph` 19, 2, 43.1%; `embedding_top10` 9, 0, 20.0%. "17% on the other 8 (none)" is the other two kinds together: `no_existing_node` 7 run, 0 resolved, 15.9%; `unreached` 1, 0, 0.7%. Every published task has exactly one kind (31 + 11 + 22 + 20 + 9 = 93) |
| No longer in the writeup: "a fifth of the agent's time and ... three of its five fixes" (the abstract) | the `named_or_called` row: 20.2% and 3 of 5. A count from one run of 48 tasks, cheapest first, not a rate to generalise from |

## Section 6, what to send

| Figure | Source |
|---|---|
| "the 13 core-split tasks it ran took 17% of its 9.0 hours and gave 4 of its 5 fixes: 0.38 hours a fix against 1.80 overall" | `NLP/data/tasks/screening/screen_routing.csv`, written by `NLP/python/scripts/66_screen_routing.py` (`NLP` pull request 665): the 13 attempted tasks that pass took 1.53 of the agent's 9.01 hours (17.0%) with 4 resolved, 0.38 hours each; all 48 took 9.01 hours with 5 resolved, 1.80 each; the 35 that fail took 83.0% with 1 resolved. A what-if on the one run, not a new run |
| "about $0.53 against $2.49 at a median rental of $0.69 a T4-hour (Kaggle's were free)" | an estimate, not anything paid. `NLP/ops/cost_settings.yaml` declares `t4_usd_per_gpu_hour` 0.69: the median on-demand price of a T4 across the providers listed at getdeploying.com/gpus/nvidia-t4 on October 26, 2026, read November 4 (`NLP` spec 036). The baseline ran on two T4s (Section 6, "Setup"), so an agent hour is two GPU-hours: 1.53 hours for 4 fixes is 1.53 × 2 × 0.69 / 4 = 0.53 dollars a fix; 9.01 hours for 5 is 9.01 × 2 × 0.69 / 5 = 2.49. It prices the agent's own time only: loading the model and starting each notebook are not in the 9.0 hours |
| "0.61 hours a fix" for the 12 a name or call edge reaches (not in the writeup since november 11, 2026) | `named_or_called` in `cost_by_graph_reach.csv`: 1.82 hours, 3 resolved |
| Not in the writeup since November 11, 2026: "The screen reads the tests, which a test-first workflow has before the fix" | the screen's second question compares the statement with the test patch; `NLP/AGENTS.md` requires the failing test before the code, so in this repository's own process the test exists when the fix is assigned. Whether routing by the screen works in advance was not run |
| "graph reach here uses the reference fix, so it is not yet a routing rule" (not in the writeup since november 11, 2026) | `named_or_called` is computed from the nodes the reference patch edits. The one graph signal known in advance, whether the statement names any node, sends 31 of the 48 tasks for 67% of the time and 4 of the 5 fixes (not in the writeup) |

## Section 6, the larger budget

All from `NLP/data/tasks/agent_reruns/gemma-4-e4b-it_larger_budget.csv` (23 rows on November 10, 2026) and its
`README.md`, written by `NLP/python/scripts/62_colab_agent.py score` (`NLP` issue 656). Each row sets a task's run
under the tight limits (its row in the Section 6 run table) beside its run with the larger budget.

| Figure | Source |
|---|---|
| "eight times the output tokens, thinking on and 100 tool calls" (16,384 a turn against 2,048; "20 minutes": not in the writeup since november 11, 2026) | `MODEL_CFG` and `BUDGET` in `62_colab_agent.py` (also 500 turns and 300 seconds a command, the rulebook's values); the same harness, `htlnlp-harness-v1` |
| "thinking on" | `gemma_agent.GemmaModel` passes `enable_thinking` to the model's chat template, which then opens the system turn with `<|think|>` (`chat_template.jinja` of `google/gemma-4/transformers/gemma-4-e4b-it/1`, read November 10, 2026) |
| "one Colab L4" ("a 20,000-token context"; 1 run reached it: not in the writeup since november 11, 2026) | `larger_gpu_name` in every row; `MAX_CONTEXT` in `NLP/kaggle/colab_agent.ipynb` (32,768 on a 40 GB card, 20,000 on an L4's 24 GB; the tight run's two T4s held 24,576). `larger_over_context_turn_count` above zero in 1 of the 23 rows: turns the model could not take because the prompt was past the limit |
| the 23 cheapest of the 48 | the notebook's `IDS`: the 48 scored tasks ordered by `session_seconds` in the tight run's table, so the first to finish are the cheapest. The run was read while still going: 23 had finished |
| Resolved 2 of 23 against 2; a patch for 20 against 19 | `is_larger_resolved` and `is_tight_resolved`; `larger_patch_bytes` and `tight_patch_bytes` above zero. Each patch was verified by `agent_harness.score_patch` in the sandbox, as in the baseline |
| 1 of the 23 runs with a turn above 2,048 output tokens; the longest turn, 3,335 | `larger_max_output_token_count`, the largest output of any turn of each run |
| Not in the writeup since November 11, 2026: 5 of 139 tool calls to a graph tool | `larger_graph_tool_call_count` and `larger_tool_call_count` summed (`submit_patch` and `get_status` are free and not counted); a graph tool was called in 4 of the 23 runs |
| "no command in the transcripts used it" (not in the writeup since november 11, 2026) | each run's `result.json` in the private Kaggle dataset `jcblearning/htlnlp-colab-results`: every `run_command` argument searched for `curl`, `wget`, `git clone`, `git fetch`, `git pull`, `pip install`, `http://`, `https://`, `github.com` and `kaggle`: none in 23 runs. A command also sees only an allow-listed environment (`agent_harness._env`), not the notebook's Kaggle token |
| 2.1 L4 GPU-hours | `larger_task_seconds` summed (each task's time on the one GPU, its bundle download included; the model's load is not) |

## Section 6, the agent under the competition's evaluator

All from `NLP/data/tasks/official_agent_runs/gemma-4-e4b-it-qat-w4a16-ct_swegemma.csv` (21 rows), its
`_settings.json` and its `README.md` (`NLP` pull request 658). The run was made on November 10, 2026 with the owner's
go-ahead: `NLP/kaggle/official_agent_run.py --sample 20 --seed 20261110`.

| Figure | Source |
|---|---|
| The harness, server and hardware | `_settings.json`: `swegemma` 0.2.11 (`Evaluator.evaluate_task`, subprocess sandbox), vLLM 0.19.1, four NVIDIA L4 per kernel (`gpu_count`, `gpu_name` in every row), tensor parallel 4, bfloat16 |
| 16,384 output tokens, 4,096 thinking budget, 40 tool calls, 5 minutes | `budgets` and `generation_defaults` in `_settings.json`; they are this repository's `eval_config.yaml` and `configs/sampling.yaml`. `differences_from_competition_defaults` lists the four that differ (120 s per command against 300, 40 tool calls against 100, 5 minutes against 60, 60 turns against no limit) |
| "A first seeded sample of 20" (of the 93, stratified by tier) | `sample` in `_settings.json`: seed 20261110, the 20 ids, and the method (`official_agent_run.sample`: proportional to each tier's size, largest remainder; A 9, B 7, C 4). The rows with `is_in_sample` true |
| Each task alone, without its patch or tests; verified by the same evaluator | `NLP/kaggle/official_agent_bundle.py` (the bundle's `tasks.jsonl` has no `patch` and no `test_patch`; a test checks it) and `official_agent_run._verify`, which calls `NLP/kaggle/official_verify.py` on the published snapshot |
| "resolved none" (0 of 20; "95% CI 0–16.1": not in the writeup since november 11, 2026) | `is_resolved` over the 20 `is_in_sample` rows; Wilson |
| Not in the writeup since November 11, 2026: 16 patches fail, 4 runs submit nothing | `reason_text`: 11 "tests fail with the agent's patch", 5 "errors before any test ran", 4 "empty patch" |
| Not in the writeup since November 10, 2026: no run reached a budget | `agent_seconds` at most 238.4 of 300; `tool_call_count` at most 22 of 40 |
| Not in the writeup since November 11, 2026: 189 tool calls, 9 to a graph tool, 3 sub-agent and 0 skill calls | `tool_call_count`, `graph_tool_call_count`, `sub_agent_call_count`, `skill_call_count` summed over the 20; counted from the evaluator's own trace of each task |
| 13 of the 20 are in the screen; 11 of them fail it | joined on `instance_id` to `NLP/data/tasks/screening/agent_screen.csv` (`is_pass`): 13 rows, 2 pass, 11 fail |
| Not in the writeup since November 10, 2026: the prompt defect, and "half the tasks" | `_hints_defect.csv`: three sampled tasks, 0 model calls, "Context variable not found: `hints`". Fixed in this repository's pull request 34 (`{hints?}`). 48 of the 93 published tasks have an empty `hints_text`. The settings' notes say which tasks ran on which side of the fix |
| 12.8 L4 GPU-hours for the evaluator's runs (21 of them) | `script_seconds` summed over the 21 rows (11,524 s, 3.2 hours) times four GPUs. The 21st row is the pilot, `htlnlp_143`, outside the sample and in no rate; it resolved |

## Section 6, the pre-registered experiment

All from `NLP/data/tasks/official_agent_runs/` (`NLP` pull request 682): the three arms' tables (`gemma-4-e4b-it-qat-w4a16-ct_swegemma_statement.csv`, `gemma-4-e4b-it-qat-w4a16-ct_swegemma_graph.csv`,
`gemma-4-e4b-it-qat-w4a16-ct_swegemma_report.csv`), each with its `_settings.json`, the paired tables `context_pairs_graph.csv` and
`context_pairs_report.csv` written by `NLP/python/scripts/70_context_pairs.py`, and the last section of the
folder's `README.md`, which is written from those tables. Run on November 11, 2026 with the owner's go-ahead; the
owner asked for the experiment, and an outside review for a controlled test of graph retrieval.

| Figure | Source |
|---|---|
| "under a plan hashed before any result (source repository, issue 674)" | `NLP/specs/028-dataops-task-set/preregistration-failing-test-report.md` (SHA-256 `1b517ae1bb96d84d670ac6891542278275a0802a33ac57dae43c0c715e43d7c4`), in a comment on `NLP` issue 674 at 14:39 UTC on November 11, 2026, before the first kernel started (14:42 UTC); and its addendum for the graph arm, `preregistration-graph-retrieval-arm.md` (SHA-256 `7121f14cd2c28baaa63af5bbcc35d668edb1fe8843f0351005673819393a0f29`), in a comment at 14:56 UTC, while the first two kernels were running and before any outcome was read (the graph arm's kernel started at 17:10 UTC). GitHub sets the comments' times. The owner posted both hashes on the Paper Track forum that afternoon |
| "all 93 were to run three times" | three kernels, one per arm, each given all 93 published tasks in one seeded order (seed 20261110); every `_settings.json` names the same agent commit (`b95b235`), model, harness and budgets, and gives its context file's SHA-256 and size, never its text. "Were to": the `statement` arm did not finish (rows below) |
| "its competition settings (16,384 output tokens, a 4,096-token thinking budget, 40 tool calls, 5 minutes), each task alone, without patch or tests" | `budgets` and `generation_defaults` in each `_settings.json`, the same as the first sample's (rows above); the bundle's `tasks.jsonl` has no `patch` and no `test_patch` |
| "graph retrieval done for the agent (named nodes, their call neighbours and the ten nearest by embedding search, from statement and graph alone)" | `NLP/python/scripts/72_graph_context.py`: up to 5 nodes the statement names (script 63's rule), up to 8 nodes one `calls` edge from those, and the 10 nearest by script 64's EmbeddingGemma search, each with its file. `NLP/data/tasks/graph_context_shape.csv`: 93 contexts, 54 name a node, median 1,203 characters, and an edited node listed in 41 of the 51 tasks whose fix edits code the graph holds. Nothing in it comes from the reference patch or the tests. The kernel's trace of every task in the arm holds the retrieval's first line |
| "the failing test's report (its errors and the public functions it called), which uses the hidden test: a test-first workflow's context, not a benchmark condition" | `NLP/python/scripts/69_failure_report.py`: up to 10 distinct errors, each with its first test and the first line of the error, then up to 15 public functions the tests called. `NLP/data/tasks/failure_report_shape.csv`: 93 reports, 32 with an import error, median 868 characters. The report is made by running the task's `test_patch` at its base commit; the plan and every table's settings say so |
| Table: "As published": 21 run; 0 (0–15.5%); core 0 (of 1 run) | the 21 rows of `gemma-4-e4b-it-qat-w4a16-ct_swegemma_statement.csv`: `is_resolved` summed; Wilson, 95%; 1 of the 21 is in `core_split.csv`. 14 of the 21 runs wrote a patch |
| Table: "With graph retrieval": 93 run; 4 (1.7–10.5%); core 4 | the 93 rows of `gemma-4-e4b-it-qat-w4a16-ct_swegemma_graph.csv`; 62 runs wrote a patch. The four resolved tasks are all among the 17 of `core_split.csv` |
| Table: "With the failing test's report": 93 run; 5 (2.3–12%); core 4 | the 93 rows of `gemma-4-e4b-it-qat-w4a16-ct_swegemma_report.csv`; 70 runs wrote a patch. Four of the five resolved tasks are in `core_split.csv`; the fifth is `htlnlp_116` |
| "The baseline arm's model server stopped answering after 21 tasks. The other 72 count as not run under the plan" | the plan's rule: "A task a kernel did not reach, or whose agent phase did not start, is 'not run' in that arm." `gemma-4-e4b-it-qat-w4a16-ct_swegemma_statement_settings.json`, `not_run`: 60 tasks made no model call (they ended at the 5-minute limit, then on connection errors) and 12 were not reached before the kernel's deadline. Recorded on `NLP` issue 674 at 19:01 UTC from the kernel's live log, before the kernel ended and before any of its patches was verified. `NLP/kaggle/official_agent_run.py` applies the rule (`not_run_reasons`), with a test |
| "Kaggle refused the one rerun it allows (the weekly GPU allowance was spent)" | the plan: "Such tasks are run in one more kernel for that arm, once, with the same settings and order." The kernel was pushed at 19:30 and 19:33 UTC; Kaggle's answer: "Maximum weekly GPU quota of 30.00 hours reached." Kaggle's own count stood at 33.69 of 30 hours, with the reset on November 14, 2026. Recorded on issue 674 at 19:34 UTC; the rerun is `NLP` issue 681 |
| "On the 21 tasks every arm ran, no arm resolved any (exact McNemar p = 1.00 for each context), so no difference is claimed and none is ruled out" | `context_pairs_graph.csv` and `context_pairs_report.csv`: 21 pairs each with both sides run, 72 left out, and no pair where either side resolved; the exact McNemar test, two-sided, is a binomial test at one half on the discordant pairs (`70_context_pairs.mcnemar_exact`), which is 1.0 when there are none. The plan claims a difference only at p < 0.05 |
| "counting the 72 as baseline failures would give p = 0.125 and 0.0625" | the other reading of "not run": if each task the baseline did not run were a task it failed, `graph` would have 4 discordant pairs and `report` 5, all one way, and the exact test gives 2 × 0.5^4 and 2 × 0.5^5. Given because the rule "no model call, ended at the time limit or on a server error" was written into the runner at 19:00 UTC, after the `report` arm had been collected; under either reading nothing is claimed |
| "Described, not tested: 7 of the 8 tasks the two full arms resolved are in the core split" | the resolved ids of the two tables against `core_split.csv`: `graph` `htlnlp_111`, `144`, `226`, `pr31`; `report` `htlnlp_116`, `143`, `144`, `174`, `187`; 8 different tasks, all but `htlnlp_116` in the core split. The addendum names the core split's counts as a description. Of the other 76 tasks `graph` resolved 0 and `report` 1 |
| "6 of the 8 had been resolved from the statement alone in an earlier run" | `htlnlp_116`, `143`, `174` and `226` in the T4 baseline (`NLP/data/tasks/agent_runs/gemma-4-e4b-it_kaggle.csv`), `htlnlp_144` in the first run of the paired graph-tools table (`agent_reruns/gemma-4-e4b-it_graph_tools.csv`, `is_first_resolved`), `htlnlp_187` with the larger budget (`agent_reruns/gemma-4-e4b-it_larger_budget.csv`), and `htlnlp_143` again in the evaluator's pilot of November 10. Those runs used another harness, budget or checkpoint (the first three tables ran `gemma-4-e4b-it` on the local harness); none had either context. So a task resolved in an arm is not shown to be one its context was needed for. The other 2 (`htlnlp_111`, `htlnlp_pr31`) had not been resolved before |
| Each patch's verdict | the competition's own `verify_task` on the published snapshot with the task's tests (`NLP/kaggle/official_verify.py`), on the machine that collected the kernels. Before any patch was scored, both controls ran there on the published files: the reference patch resolved 93 of 93 and an empty patch 0 of 93 (`context_run_controls.csv`), the verdicts of Section 5's table in all 186 rows |
| Not in the writeup: every `statement` run under these settings | the first sample's 20 tasks (0 resolved, November 10) and the arm's 21 (0 resolved) are 41 runs over 37 tasks (4 in both), which hold 4 of the core split's 17. On those 37 tasks `graph` resolved 1 and `report` 0. Two days are not one run, so this is not a paired test |

## Section 6, time, GPUs and cost

| Figure | Source |
|---|---|
| "The kernels' OpenTelemetry spans put 66–83% of a task's time in model calls, 14–15% in context compaction and under 0.1% in the graph tools" | `gemma-4-e4b-it-qat-w4a16-ct_swegemma_<arm>_sections.csv` (`time_share_pct`), written by `NLP/python/scripts/71_run_telemetry.py` from the spans each kernel kept (names, counts and seconds; no prompt or reply). Model call: `statement` 82.8, `graph` 76.5, `report` 66.3; context compaction 13.8, 14.6, 15.4; the three graph tools together 0.02, 0.02, 0.02. A section's time is its spans' self time, so each second of a task is counted once. The `statement` figures are over its 21 tasks |
| "45 of 207 runs ended at the model's context window" | `error_text` holding `ContextWindowExceededError` in the three tables: 3 of 21, 24 of 93 and 18 of 93. The server's window is 32,768 tokens with 16,384 kept for output |
| "A task took 297–419 GPU-seconds on the four L4s and 4.8–6.7 Wh" | `gemma-4-e4b-it-qat-w4a16-ct_swegemma_<arm>_gpu.csv`: the mean of `task_seconds` times `gpu_count` (297 `graph`, 350 `report`, 419 `statement`) and the mean of `gpu_energy_wh` (4.8, 5.5, 6.7), from each kernel's reading of its GPUs every five seconds. Loading the model is not in it |
| "a fix 1.9 GPU-hours with graph retrieval and 1.8 with the report" | `gpu_hours` summed over each arm's tasks, divided by the tasks it resolved: 7.67 / 4 and 9.04 / 5. No dollar figure: `NLP/ops/cost_settings.yaml` declares a price for a T4 and none for an L4 |

## Section 6, beside the competition's own tasks

The development set is the competition's own (`gemma-4-developer-agent`: 129 tasks from fastapi 67, rich 48,
requests 13 and httpx 1), read inside the competition's terms and never redistributed: the tables hold task ids,
counts, ranks and ratings only. The host has said that labels derived from the task data may be published (Paper Track discussion 749803: "Yes, publishing derived labels is okay").

| Figure | Source |
|---|---|
| "The graph counts were repeated on its 129 development tasks" (each changed file read from GitHub at its base commit) | `NLP/data/tasks/devset/devset_graph_reach.csv` and its `README.md`, written by `NLP/python/scripts/67_devset_graph_reach.py` (`NLP` pull request 676) from the competition's `tasks.jsonl`, graphs and embeddings, downloaded November 11, 2026. The snapshots (21.5 GB) were not downloaded: each changed file of a reference patch is read once from GitHub at the task's base commit, the only source the edited nodes need. The rules are those of Section 4.3, reused from scripts 63 and 64 (`changed_files`, `edited_nodes`, `named_nodes`, `call_distance`, `chance_top`); the competition's patches have plain `--- a/` headers, so `git_headers` adds the `diff --git` line those rules read (a test checks it) |
| "The fix edits a function the graph holds": 51 of 93; 114 of 129 | `edited_node_count` above 0: 51 rows of `graph_coverage.csv`; 114 rows of `devset_graph_reach.csv`. Of the other 15 development tasks, 5 change no module the graph covers and 10 change no existing function, class or method |
| "Of those: a name or call edge reaches it; with embedding search too": 22; 42 and 52; 66 | `statement_to_fix_edge_count` 0 (named) in 29 and above 0 (call edges) in 23 of the 114: 52. With an edited node in the first ten of the embedding search as well: 20 + 2 + 20 = 42 of the 51 (Section 4.3), and `reached_count` 66 of the 114 in the script's summary |
| Not in the writeup: embedding search alone on the development set | `edited_node_best_rank_num` at most 10 in 34 of the 114 (1.5 by chance) and first in 6 (0.1 by chance); this set, 30 (5.4) and 15 (0.6) of 51. The competition's provided embeddings are 256-dimensional but are not EmbeddingGemma document vectors (on one graph the cosine between the two vectors of a node averages 0.05), so the script embeds each graph's nodes with EmbeddingGemma at the same revision as this set's (document prompt) and the statement with its query prompt, cut to 256 dimensions. Chance: `chance_top` summed over the 114 (0.148 and 1.453); the graphs are larger than this set's (a median of 3,256 nodes against 398), so chance is lower |
| Not in the writeup: the competition's own embeddings | by the provided vectors, a named symbol's ten nearest nodes include an edited one in 6 development tasks beyond the 29 whose statement names one, all already reached by call edges (`provided_edited_node_best_rank_num`; the README of `NLP/data/tasks/devset/`) |
| "Statement vague or worse (AI screen)": 19 of 93; 11 of 40 | `statement_rating_num` 2 or 3: `agent_screen_all.csv` and `NLP/data/tasks/screening/devset_screen.csv` (the same protocol and raters' instructions as the second screen, blind, one AI pass, no person's check) |
| "Tests need a name or text the statement never gives": 76 of 93; 14 of 40 | `test_rating_num` 2 or 3 in the same two tables |
| "the screen passes half" (Section 8; "20 of 40 of the competition's" is not in the abstract since November 11, 2026) | `is_pass` (both ratings 0 or 1) in 20 of the 40 rows of `devset_screen.csv`. By repository: requests 4 of 4, fastapi 10 of 21, rich 6 of 15 (not in the writeup) |
| "a seeded 40, stratified by repository" (fastapi 21, rich 15, requests 4) | `official_agent_run.strata` with seed 20261110: proportional to each repository's share of the 129, largest remainder; httpx's one task gets no place. The 40 ids are in the run table and in `devset_controls.csv` |
| "In a Kaggle notebook the evaluator's sandbox has no pip to install test dependencies, so the reference patch fails 16 of the 40 and one passes with an empty patch, leaving 23" (rich 15, fastapi 8) | `NLP/data/tasks/official_agent_runs/devset_controls.csv` and its `README.md`, written by `NLP/kaggle/official_controls_run.py` in a CPU notebook with the competition attached and the same pinned image as the agent's run (`htlnlp-offrun-devset-controls`): the competition's own `verify_task` with the reference patch resolves 24 of 40 and with an empty patch 1 (`fastapi_14851`); 24 − 1 = 23, of which 15 rich and 8 fastapi. The sandbox: `swegemma.sandbox.subprocess` logged "ensurepip unavailable ... creating venv without pip" for every task, and the competition's `sandbox/setup.py` installs a task's dependencies with pip. Of the 16: 12 fastapi tasks stop while collecting tests (exit code 2; the 7 whose output shows a cause name a missing test library), 3 requests tasks pass 135 or 136 tests and error in 185 to 187, and 1 fails one assertion. The cause is read from the log for the sandbox and from the output for 7 tasks; for the other 9 it is inferred |
| The development-set run's settings ("with the same settings": not in the writeup since november 11, 2026) | the run table's `_settings.json`: the same agent directory and `eval_config.yaml` as the 20 (16,384 output tokens, a 4,096-token thinking budget, 40 tool calls, 5 minutes), `swegemma` 0.2.11, vLLM on four L4 GPUs, all 40 tasks in one kernel (`htlnlp-offrun-devset`), run November 11, 2026 with the owner's go-ahead (`NLP` pull request 675) |
| "Resolved as published": 0 of 21 (the `statement` arm, rows above; the first sample's 0 of 20 is not in the table since November 11, 2026); 3 of 23 | `is_resolved` in `NLP/data/tasks/official_agent_runs/gemma-4-e4b-it-qat-w4a16-ct_swegemma_devset.csv` over the 23 tasks whose reference patch resolves and whose empty patch does not in `devset_controls.csv`; each patch was verified in the kernel by the competition's own `verify_task` with the task's tests. The 0 of 20 is the row above |
| "Tool calls to a graph tool, as published": 17 of 207; 83 of 439 | `graph_tool_call_count` and `tool_call_count` summed over the 21 rows of `gemma-4-e4b-it-qat-w4a16-ct_swegemma_statement.csv` and over the 40 rows of `gemma-4-e4b-it-qat-w4a16-ct_swegemma_devset.csv`, counted from the evaluator's own trace of each task. With added context: 61 of 710 (`graph`) and 48 of 707 (`report`), not in the writeup |
| "On the competition's tasks the graph holds more fixes and the screen passes half"; "the two sets differ in their tests more than their statements" (Section 8) | the table: 114 of 129 against 51 of 93; 20 of 40 pass against 17 of 93; statements vague or worse 11 of 40 against 19 of 93, tests that need an unstated name 14 of 40 against 76 of 93. A reading of AI ratings, not a test |

## Section 8, the conclusion

| Figure | Source |
|---|---|
| "3 of 23 of the competition's own under its evaluator"; "the graph holds more fixes and the screen passes half" | Section 6, "Beside the competition's own tasks" (rows above) |
| "With graph retrieval done for it, it resolved 4 of all 93, and with a failing test's report (from the hidden test) 5, in an experiment registered before it ran; its baseline arm failed after 21 tasks, so whether either context helps is still open" | Section 6, "A pre-registered experiment" (rows above) |
| "Over every run, 8 of the 9 tasks this model has resolved are in the core split of 17" | every resolved row of the four run tables and the larger-budget table: the T4 baseline (`htlnlp_116`, `143`, `174`, `226`, `pr63`), the larger budget (`187`, `pr63`), the evaluator's pilot (`143`), `graph` (`111`, `144`, `226`, `pr31`) and `report` (`116`, `143`, `144`, `174`, `187`): 9 different tasks, all but `htlnlp_116` in `core_split.csv`. A description over runs with different harnesses, budgets and contexts, not a test; the last section of the runs' `README.md` gives the same count |
| "which is where a result on this set should be quoted" | a recommendation, not a measurement: the 17 tasks whose statements say what their tests check (Section 6, "Task fairness") |
| "One new repository, compared with the competition's development set" (Section 7) | the Section 6 table above. The second repository (former Section 4.5) is cut |
| "No baseline for 72 tasks. The experiment's baseline arm ran 21 of 93, so neither context is tested against it; the rerun is owed (source repository, issue 681)" (Section 7) | Section 6, "A pre-registered experiment" (rows above); `NLP` issue 681 is the action item for the rerun, which needs the owner's word and the allowance |
| "Every run under the competition's evaluator used 5 minutes and 40 tool calls, not 60 and 100, once per arm at temperature 0.2" (Section 7) | `differences_from_competition_defaults` in the settings file of each run table (the first sample, the three arms, the development set); each task ran once in each arm; the agent's `configs/sampling.yaml` sets the temperature. Not in the writeup since November 11, 2026: "20 of our tasks and 40 of its own" |
| "The report arm's context comes from the hidden test, so it is not a benchmark condition" (Section 7) | Section 6, "A pre-registered experiment" (rows above) |
| "63 of ours, 12 of the core split's 17 and all 40 development tasks have AI ratings only" (Section 7) | `devset_screen.csv` has no person's check; 93 − 30 = 63 of ours; `is_owner_checked` is true for 5 of the 17 rows of `core_split.csv`, so 12 are not |
| "5 of 48 cheapest-first tasks" ("2 of 23 with a larger budget" and "none of a random 20": not in the writeup since november 11, 2026 in Section 8; Section 6 has both) | Section 6: "Results", "A larger budget" and "Under the competition's evaluator" |
| Not in the writeup since November 11, 2026: "Five small tasks left the loop and the rest stayed in it" | Section 6: the 5 resolved of 48, each a small change, and the 43 unresolved, which the cloud agent and the owner had done |
| Not in the writeup since November 11, 2026 in Section 8 (Section 4.3 has it): "and a failing test's report in 6 more" | Section 4.3, "what a failing test's report adds" (rows above) |
| Not in the writeup since November 11, 2026 in Section 8: "The graph could have told it where to look in 42 of the 51 tasks that edit existing code"; "that signal is there to be used, its benefit to an agent untested" (still untested: Section 6) | Section 4.3 for the count; the second phrase is a reading: the tools to ask the graph exist and were called in 20 of 473 tool calls |
| "Sending the model only the tasks that pass the screen would have kept 4 of its 5 fixes for 17% of its time" (not in the writeup since november 11, 2026 in Section 8; in Section 6 and the abstract) | Section 6, "Cost, and what to send" |
| "its evaluator runs on it as published" | Section 5: `NLP/data/tasks/official_verifier/published_verification.csv`, 93 of 93 reference patches and 0 of 93 empty patches on dataset version 4 with no file added |
| `kaggle/official_verify.py` "replays the two controls" | `NLP/kaggle/official_verify.py` runs the competition's verification with a chosen patch per task: none, the reference patch, or patches from a file |
| Not in the writeup since November 11, 2026 (cut to leave a margin under the word limit; the source repository's README lists the scripts): "scripts 63 to 72 rebuild the graph, cost, failing-test, experiment and telemetry tables" (63 to 68: the graph, search, cost, routing and failing-test counts, 67 on the competition's tasks) | `NLP/python/scripts/63_graph_coverage.py --published <the downloaded dataset>` (about ten seconds, no model), `64_statement_search.py --published <the same>` (the gated embedding model, about three minutes on a CPU) and `65_cost_by_graph_reach.py` (no model) |
| Scripts 69 to 72 of those | `NLP/python/scripts/69_failure_report.py` (the report), `72_graph_context.py` (the retrieval), `70_context_pairs.py` (the paired tables and the test) and `71_run_telemetry.py` (time by code section, GPU-hours and energy). The arms' tables themselves need the kernels' output, which is not public |
| "the quickstart notebook loads a task" (with its snapshot, graph and embeddings) | the "Quickstart notebook" row under the title block above |

## The former Section 7 (cut on November 10, 2026)

None of its three cases is in the paper now. The rows below are for what was cut.

| Figure | Source |
|---|---|
| De-identification rules: 1.00 and 0.27 (`regex_v2`, hard and unseen tiers) | `NLP/data/deid/scores.csv` (`entity_recall`). In Section 1 for part of November 10, 2026, then cut for length |
| The masking defect: about a quarter of charted teeth without measures while every test passed | `NLP/docs/tooth_loss.md`, "After the tooth-table fixes of #631"; fixed by pull request 632. In Section 1 for part of November 10, 2026, then cut for length |
| Tooth-loss AUC 0.89 to 0.90 and 0.59 to 0.63 | `NLP/docs/tooth_loss.md`, "After the tooth-table fixes of #631" (completed-extraction models) |
| 16 de-identification candidates; 5 scorable attempts, none resolved | a keyword match on `title_text` in the manifest (`de-id`, `phi`, `maccrobat`, `presidio`, `redact`, `mask`), joined to the run table. Three more were attempted but are among the 10 set aside. The match is mine and approximate |

## Not in the writeup, and why

- The switch-off test in `pipeline-doctor`: its rules were written from the same nine incidents it is scored on, its
  trailing runs are simulated, and its "no conventions" condition blanks five data columns.
- Any comparison with and without the pipeline-doctor skill or the analyzer sub-agent: not run. Both were
  available in the evaluator's 20 runs (Section 6): the sub-agent was called 3 times, the skill never.
- A score on all 129 of the competition's development tasks: not run. Section 6 has a seeded 40, of which 23 can be
  verified in a Kaggle notebook.
- A test of graph retrieval, or of a failing test's report, against the agent as published: not made. The
  experiment's baseline arm ran 21 of 93 tasks (Section 6); `NLP` issue 681 is the rerun.
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
- "A growing share of code is written by agents under a person's direction" (Section 1): cut on November 10, 2026.
  An outside review of version 6 pointed out that nothing in the paper measures or cites it. The sentence now
  describes this repository only. The same review prompted "The released tasks let others measure that gap" to become
  "... test other models and settings": the paper does not score the cloud agent on the same statements, so it shows
  no gap between two measured systems.
- Cut on November 10, 2026 (pull request for issue 41) to lead with the findings, report the larger-budget rerun
  and stay well under the word limit by any way of counting; the owner asked for the margin:
  - Section 7, "What these tasks contain that web-library tasks do not": two of its three cases moved into Section
    1; the tooth-loss case (AUC 0.89 to 0.90 against 0.59 to 0.63) is cut. The limitation "Synthetic health data"
    became a clause of that sentence. Sections 8 and 9 became 7 and 8.
  - Section 2's "Health-data quality" paragraph and its three references (Kahn et al.; Stubbs and Uzuner; Caufield
    et al., then 12 to 14): about the source repository's own checks, not about coding agents. References 15 to 17
    became 12 to 14.
  - Section 3: "Of the 192 [reviews] with a structured verdict, all approve (64 with minor findings, 9 with
    conditions)" and "CI rejects a pull request from an agent's own session branch". Their rows are in the Section 3
    table above. (Earlier the same day, pull request 38 cut "more than half of my time went into three things a
    person reads" and "better health starts with accurate health information"; their rows are above too.)
  - Section 4.2: a backfilled record "carries a `backfilled` label and is closed on creation". Section 4.5: "67 of
    this paper's 116 candidates got their issue record afterwards" (Section 4.2 gives the 67).
  - Section 5: the seven-row table became two rows with the same counts; "all three tasks tried fail at import"
    moved into the sentence under it. Cut: "The prompt, nudge messages and budget warning follow the guide's
    wording"; the review that found an earlier version ran the model's commands on the host; "user, mount, network
    and pid" before "namespaces".
  - Section 6: "30 with failing tests, 5 with errors before any test ran"; "the figures use each task's latest run;
    eight tasks have none with the tools"; the split of the 30.2 GPU-hours into 20.6 and 9.6 and the median of 0.39
    per task; "each task ran alone ... the same evaluator then verified the patch on the published snapshot" became
    "each task ran alone, without its patch or tests". Their rows are in the Section 6 tables above.
  - Section 7 (limitations): "My harness ran the baseline" and "Constrained settings" became "No leaderboard score".
  - The abstract's "labelled with where its problem statement came from" (now in contribution 1) and its last
    sentence, "I report how the model fails and what each task costs".
- Cut later on November 10, 2026 (the same pull request) to make room for the graph result of Section 4.3 without
  the paper growing:
  - The abstract: "Building and running the set gave three findings" (there are now four, each in bold) and "and
    exposed a prompt defect my harness had hidden" (still in Section 6).
  - Section 1: the de-identification case (1.00 and 0.27; row under the former Section 7 above).
  - Section 2: "Defects4J and BugsInPy did the same for Java and Python bugs before language models" and their
    two references; RepoGraph and LocAgent take the numbers 3 and 4.
  - Section 3: "Agents merge their own green pull requests; limited-compute runs, publishing, deletions and rule
    changes wait for me" (row "The four cases reserved for the owner" above).
  - Section 4.5: "To see whether the recipe transfers" and "touch non-test Python and Python tests" (now
    "are candidates"; the row above gives the rule).
  - Section 5: "(prompt, multi-turn loop, nine tools, budgets, patch extraction and verification)".
  - Section 6: "a training setting, a notebook setting" became "two settings"; "drawn with a fixed seed" became
    "seeded".
  - Section 8: "Across the paired rerun, the larger budget and the evaluator's run" before the graph-tool count
    (the abstract's row gives the three), and the list of the dataset's four parts (`tasks.jsonl`, `snapshots/`,
    `graphs/`, `embeddings/`; Section 4.3 and the dataset's card describe them).
  - The abstract again: "The official evaluator also rejected 20 tasks my own gates had passed" (Section 4.1 and
    Section 5: 113 tasks passed both gates and were published first; the evaluator resolves the reference patch
    of 93).
  - Section 6: "(Kaggle's GPUs are free)" after the cost estimate (the abstract says "two free T4 GPUs"); the
    prompt-defect sentence shortened, with "the half of tasks with none" as before (row above).
- Cut on November 10, 2026 (pull request for issue 43) so that the abstract could lead with the fifteen days of
  commits without the paper growing: the abstract's first two sentences ("Coding-agent benchmarks are mined from
  mature web libraries maintained by people. I release a task set mined from a different source ..."), now one
  clause after the lead; "on its hardware" after the evaluator's run in the abstract; "I typed no code:" in
  Section 1 (now in the abstract); and Section 5's "Elsewhere the two verifiers agree on every reference patch"
  (the table's counts say it: the evaluator resolves 93 of 113, and the 20 it rejects are listed with their
  reasons).
- Changed later on November 10, 2026 (the same pull request), at the owner's direction:
  - Voice: "I" and "my" became "this paper", "this work", "the author" or "the local harness" throughout.
  - The claim that other benchmarks' sources are "maintained by people" (the abstract) or "human-maintained"
    (Section 2) is gone: nothing here measured who maintains them. Section 2 now says they "draw on public
    open-source projects".
  - The abstract and the conclusion are framed by what can leave a person's loop and what the person gains for
    the rest. Cut to make room: the abstract's "Can a small local model redo that work?" and its clause on
    existing benchmarks; "with thinking on" and "run end to end" in the abstract (Section 6 has both); the
    masking-defect example and "(synthetic records throughout)" in Section 1; "about $21 at an estimated $0.69
    per hour" in Section 6; "One task was resolved only without the tools, one only with them, one both times"
    became "Only one task was resolved both times"; "To see whether the tight limits decide the result" became
    "To test the tight limits"; "which ships in" became "in"; and the conclusion's "Whether graphs help a small
    model on a data repository cannot be told until the model asks them and they cover more than its package"
    (Section 4.3 says the graph covers the package only).
- Another model's review, November 10, 2026 (the owner gave it the Paper Track's rubric and the PDF). It scored the
  paper 3.2 of 5 as a strict judge (novelty 3.0, quality 2.0, relevance 3.5, verifiability 3.5, clarity 4.0) and
  proposed five wording changes. Acted on:
  - Its finding that "The rest stays with a person" says more than the experiments show: the heading is now "The
    rest stays in the loop for now", in the abstract and the conclusion.
  - Its reading of the 25 of 30 as a weakness of this set alone: the abstract and Section 6 now say what the
    screen is modelled on and what SWE-bench's own screen found, and Section 6 says where each verdict is.
  - Its reading of "2 more by call edges" as a small result: Section 4.3 now says what it means for a graph tool.
  - Two of its five wordings, in part: "can leave it" became "can leave the loop", and Section 6 gives the larger
    budget's settings as one list.
  Not taken, because the paper cannot support them or a reader needs what they remove: dropping "Some", the
  model's name and the five tasks' examples from the abstract; "the first benchmark derived specifically from an
  agent-built health data repository" (no source for "first"); "full verification requires extensive manual test
  screening" in place of the conclusion's recipe (the screen was an AI reviewer's, checked in summary); a sentence
  on data repositories in place of "Two kinds of repository are scarce"; and a shorter larger-budget sentence
  without "of the 48", "on the same harness", "per turn" and the 20,000-token context.
  Cut to make room: Section 1's "part of the author's open health-data benchmarks"; Section 6's sentence on the
  prompt defect the evaluator's run exposed (its row is above), "58 first attempts and 28 reruns" and "6.0 for
  each task resolved" in the cost line, and the detail of how eight runs submitted nothing (shortened); the
  conclusion's "A cloud agent built this repository in fifteen days" and "all of them small" (both in the
  abstract). The abstract's "resolves every reference patch and no empty patch" became "each verified with
  the competition's own evaluator" (Section 5 has the counts). In Section 7, "One task flipping moves a paired
  result" is cut and four bullets are shortened without losing a figure. Reference 13 no longer gives the
  version (1.0.0; its row is under Section 2). What the review marked down and no wording can change: one repository, 63 tasks unscreened, a
  screen checked only in summary.
- A second model's review the same day scored the paper 3.0 of 5 (novelty 2.5, quality 2.5, relevance 3.5,
  verifiability 3.0, clarity 3.0). Both reviews named the abstract's headings as its costliest sentences: they
  read as claims ("Some small upkeep can leave it", "The rest stays with a person") that five resolved tasks and
  an unresolved remainder do not establish. Acted on:
  - The headings now only sort the results ("What it did unattended", "What stayed in the loop", "What the person
    in the loop can now see"), and the abstract says the 48 were run cheapest first.
  - Both asked why embedding search was untested and whether edges do better than search. It is now tested from
    the published files (Section 4.3), and Section 4.3 gives the graph's node and edge types.
  - "21 runs" for 20 tasks is no longer in the text (the extra run is the pilot; its row is under Section 6).
  - The conclusion's recipe no longer says it "should transfer"; it says it was run in full on one repository.
  - Related work names what the set adds (statement-source labels, counts of graph and embedding reach).
  Not taken: cutting the graph-tool call count from the abstract (the same review called it the most memorable
  sentence), and replacing the abstract with caveats only.
- A third model's review the same day, of the version with the embedding search and the full screen, scored it 3.1
  of 5 (novelty 2.5, quality 2.0, relevance 3.5, verifiability 4.0, clarity 3.5) and named "5 of the 48 tasks it
  ran, cheapest first" as the sentence most likely to cost points, because the ordering is easy to miss. Acted on:
  the abstract gives the interval beside the count and says the graph-tool calls are over three runs; Section 6
  says no rate here is an unbiased estimate for the 93; the conclusion says "cheapest-first". Cut to make room:
  "(Section 7)" after the cap, "committed as a file" became "committed", "than a person's" in Section 7, and three
  small rewordings. What it marked down and no wording can change: one repository, one model, a standard mining
  recipe.
- A fourth model's review the same day scored it 3.2 of 5 (novelty 3.0, quality 2.0, relevance 3.5, verifiability
  4.5, clarity 3.0). Acted on: the abstract's sentence on the larger budget, which it found confusing, now reads
  "with eight times the output budget it resolved 2 of the 23 cheapest tasks, against 2 before"; Section 4.3 says
  outright that the graph misses the fix in 42 of the 93 tasks; and Section 7 says the cloud agent was not rerun
  on the statements alone, which answers its point that the title's comparison has no cloud baseline (every
  reference patch is the cloud agent's own change, made with a person in the loop and with the tests written
  beside it). Not taken: a new title (it called the repository synthetic, which only its data are), "Overfitting
  risk" as a heading, and a sentence saying SWE-bench's screening skews outcomes. Cut to make room: "The local
  harness ran the baseline and the larger-budget rerun" in Section 7 (Sections 5 and 6 say it), "two" before
  "free T4 GPUs" in the abstract (Section 6 has it), and the last bullet of Section 7 is shorter.
- Last change of November 10, 2026, at the owner's direction (show what the graph is worth; tie cost to it): the
  abstract's second heading is now "What the graph could tell it" and leads with the 42 of 51; Section 4.3 gives
  the chance baseline; Section 6 gives the hours a fix by screen verdict and by graph reach, and says what each
  can and cannot be used for. The paired rerun still shows no difference with the tools available (2 and 2 on
  23 tasks), and the paper still says so. Cut to make room: the abstract's "each task's statement source" and its
  "What stayed in the loop" heading (its two figures moved under the first heading); Section 2's "the competition
  fixes it"; Section 5's "and a notebook can read every attached file"; Section 6's interval for the paired rerun
  (2.4 to 26.8% each), how the eight empty runs ended (four at the 2,048-token limit, three without an edit, one
  misusing the edit tool), "26 tasks rated twice by different raters got the same verdict", the 43% of the
  agent's time on the 19 tasks whose fix is outside the graph (2 resolved) and the other rows of the cost split;
  the conclusion's list of what the person in the loop can see; and the GPU-hour totals (30.2 T4 GPU-hours for the
  baseline and its reruns, 12.8 L4 for the evaluator's runs, 2.1 for the larger budget; their rows are under
  Section 6 above).
- At the owner's request (November 11), the abstract's first sentence and Section 3 give the number of tests, at
  the same cut-off as the 960 commits.
  Cut to keep the count flat: "and its embeddings" in Related work, "public under CC BY 4.0" in the first
  contribution (the licence is in the Data and code line), and "which Kaggle's notebooks did not" (Section 6 says
  Kaggle ran with internet off).
- The abstract's longest sentence, three results joined by semicolons, is now three sentences (a review gave
  Clarity 2.5 and named it the sentence most likely to cost points). "cheapest first", "all small", "against 2
  before" and "random" stay. Four words left the abstract to keep it at 229: "of them" after 775, "expected"
  before "by chance" (Section 4.3 keeps it and says how it is worked out), and "tool" in "473 tool calls".
- Two more from a further review, the same day: the first row of Section 5's table reads "First release, with the
  import fix below" (the review found "one file added per snapshot" at odds with "As first published, no task
  could be scored"), and the conclusion's "that value is there to be used" became "that signal is there to be
  used, its benefit to an agent untested", because reaching the fix is not repairing it.
- Three more wording fixes from a review, the same day. That review read the task set as "heavily synthesized":
  the patient records are synthetic, the tasks are real merged changes, so Section 1 now says "its tasks are real
  changes to application code". The second screen's sentence reads "An independent second pass, blind to the
  first, rated all 93: the same verdict on all 30, and 17 of 93 pass" (it had a stray semicolon). Section 4.5 ends
  "Gating and releasing them is future work": the same fact as "The 133 are not gated or released". Not taken:
  "All five resolved tasks required trivial configuration or string edits" (one is a label parser), "This isolates
  the boundary between local agent capabilities and human intervention" (a cheapest-first sample does not), and
  "Data repositories expose critical coverage gaps in standard AST graphs" (one repository).
- Four wording fixes from reviews, the same day: the withheld candidate's row reads "unlicensed third-party files"
  (its patch adds third-party files with no stated licence); "The model made only 6 graph-tool calls among 145, in 4
  of the 23 runs" (the denominator stays, because the abstract's 473 is its sum with two others); "Ten of the 58
  tasks attempted were excluded from the set (Section 5)"; and Section 4.3 now says how chance is worked out: for
  each task, the probability that a random ranking of its graph's nodes puts an edited one in the first k (one
  minus a hypergeometric zero term, `chance_top` in `64_statement_search.py`), summed over the tasks.
- Every review marked the paper down for "one repository". At the owner's direction the paper now says which parts
  are the competition's own and already run on its four development repositories (the mining rule, the format, the
  evaluator) and which this paper added and ran on one (statement sources, controls on the published files, the
  screens, the graph counts): in the abstract, Section 1, Section 7's first bullet and the conclusion's recipe.
  "The second repository tests only the mining rule" left Section 7; Section 4.5 still says the 133 candidates are
  not gated or released (from the next change on, as "Gating and releasing them is future work"). Cut to make room: the larger-budget paragraph's sentence on output tokens and the context
  limit (its rows are under Section 6 above), "it reads and edits files and rarely searches", and "of issues,
  pull requests and reviews" in the abstract (Section 3 has it).
- Added the same day at the owner's direction: what the task set is made of and how (application work in health
  data; every step a script; the competition's exact format), the embedding-search count, the split of the
  agent's time by graph reach, and an automated screen of all 93 tasks beside the 30 the owner checked.
  Cut to make room: the paired rerun's table and its non-empty-patch counts (18 and 20); "the analyzer sub-agent
  3 times and the skill never" and "No run reached a budget" (Section 6); "(the local control ran from the
  repository's history and missed this)" (Section 5); the reasons in two rows of Section 4.1's table (one task
  withdrawn because its patch names an organisation the repository's rules forbid; one withheld because its
  patch adds third-party files with no stated licence); "by commit subject to one of its 169 merged pull
  requests" and "Candidates are everywhere" (Section 4.5); "The best coding agents today run on large models in
  the cloud", "a table is written" and "written by agents under a person's direction" (Section 1); the five
  resolved tasks' examples in the abstract (Section 6 has them); the sentence on what this graph lacks.
- Added on November 11, 2026 (this repository's issue 61): what a failing test's report adds to the graph's reach
  (Section 4.3), and the cost of a fix in dollars (Section 6). Cut to make room: the introduction's question
  ("Which changes can a small local agent take out of the person's loop, and what does the person need for the
  rest?"; the abstract asks it); "directed in chat and merged after an automated review" (Section 3 has the rules);
  Related work's clause on what the set adds (the contributions list has it); in Section 5, "before finding its
  evaluator in a separate Kaggle dataset", "Two scripted models bound it", "(the other two need Postgres and R)",
  "(all three tried fail at import)", "and the local harness allows", and the detail of the namespaces (an
  allow-listed environment; Kaggle does not allow them); "ADK" and "are not run" in the known differences; "is an
  unbiased estimate for" became "estimates"; and the results by statement source (4 of 24, 1 of 19, 0 of 5).
- Added later on November 11, 2026 (issue 62): the competition's own development set beside this set, in one table
  in Section 6, with the agent's result on it; the abstract, Section 1, Section 7 and Section 8 say what the
  comparison shows. Every review had marked the paper down for "one repository". Cut to make room: Section 4.5 (the
  second repository, mined only; its row stays under Section 4 above); SWE-bench's 68.3% (the development set's 20
  of 40 is the closer comparison); the time split and the hours a fix by graph reach, and "graph reach here uses
  the reference fix, so it is not yet a routing rule" (Section 6; rows above); "embedding search ranks an edited
  function first in 15 (0.6 by chance)" in the abstract (Section 4.3 has it); the conclusion's sentence on sending
  only the tasks that pass the screen (Section 6 and the abstract have it) and the recipe's bracket; "Colab had
  network access; no command used it"; the larger budget's patch counts; "in 4 of the 23 runs" and "after the
  fix, 28 were rerun with the same settings"; "end to end"; "renormalised" and "the competition does not name its
  embedding model" (Section 4.3); "(by its identifier)"; the wording of two table headers and two table rows; and
  the competition reference's author list became "Markowitz et al.".
- Added on November 11 and 12, 2026 (issue 62): a pre-registered experiment under the competition's evaluator, with
  graph retrieval and a failing test's report as added context on all 93 tasks and a baseline arm that ran
  21 (Section 6, the abstract, Sections 1, 7 and 8); the core split of 17 tasks; time by code section,
  GPU-seconds and energy from the kernels' OpenTelemetry spans; two citations to other entries of this track
  [15, 16]; and the label "oracle-assisted" on Section 4.3's 48 of 51. An outside review asked for the core split,
  the label and a controlled test of graph retrieval; the test could not be made, and the text says so. Cut to make
  room: the paired rerun of the graph tools ("Do the graph tools help?"); the first sample's interval, patch counts
  and tool calls, and "Seventeen of the 20 fail the second screen"; the larger budget's 20 minutes, context size
  and graph-tool count; "Each verdict and its reason are in the repository"; "The screen reads the tests, which a
  test-first workflow has before the fix"; "it resolved 4 of the 13 that pass and 1 of the 35 that fail, so the
  baseline may measure the tasks more than the model"; the Section 4.1 table (now a sentence); "These are counts
  from the published files, not agent runs"; the closing paragraph on the recipe; from the abstract, "775 marked
  as agent-authored", the baseline's interval, the larger budget, the count of graph-tool calls over three runs,
  the screen's two counts and the routing sentence; from Section 8, the larger budget, the first sample, "Five
  small tasks left the loop and the rest stayed in it" and the sentence on what the graph could have told the
  model; and wording in Sections 2, 4.3, 5, 6 and 7. Figure 1's third and fourth groups now show the experiment's
  arms and the screen of all 93. Then, to keep the pasted text under 3,000 words with its references as every
  earlier version was: the second track entry and its reference (test feedback on planted bugs); "among a median
  of 7 public functions, which its OpenTelemetry spans would record"; the first screen's 5 and 25; "for those 67
  candidates a backfilled issue record quotes the original text"; "so no later history comes along"; "(rich 15,
  fastapi 8)"; and the conclusion's opening clause.
- Cut later on November 11, 2026, when the owner asked for a wider margin under the word limit than 6 words: the pasted
  text went from 2,994 words with its references to 2,899 (2,678 before them; the rule counts the words before them). No number
  changed. Cut: "These draw on open-source libraries; this set comes from an agent-built data repository" (Section 2);
  "Tiers B and C exist because the issue rule was adopted partway through" (Section 4.2: the table's brackets say
  it); "The graph reaches only part of what a data repository changes" (Section 4.3); "Of the other 43, 35 submitted a
  patch that fails the target tests and 8 submitted nothing" (Section 6: 40 patches and 5 resolved give both); the
  list of scripts in Section 8; "Coding-agent sessions made every change, and scripts make every step from merged
  change to published task" (Section 1: the abstract and Section 3 say it); "The first baseline covers 48 of 93
  tasks, cheapest first" (Section 7: Section 6 and the abstract say it); and wording in contribution 3 and Section
  2. Added: "(from the hidden test)" beside the failing test's report in Section 8, so the report is labelled
  wherever a result of it is given.
- An independent human screen of task quality: not done. Both screens are AI reviewers'; a person checked the
  first screen's 30 verdicts in summary (Section 6 above). The second screen's 63 other verdicts have no person's
  check.
- A split of all 93 tasks into fixes, features and maintenance: not done; the screen classifies its 30. The mining
  rule keeps any change that touches code and tests, so the set is not only bug fixes.
