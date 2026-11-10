# Can a small local agent redo a cloud agent's work?

**113 issue-traced tasks from a health-data repository, with a calibrated open harness and a Gemma 4 E4B baseline**

*A personal learning project, not affiliated with or endorsed by any employer, institution or vendor. Every patient record in the source repository is synthetic.*

## Abstract

Coding-agent benchmarks are mined from mature web libraries maintained by people. I release a task set mined from a different kind of repository: a health-data benchmark built by cloud coding-agent sessions under written rules that CI enforces (960 commits in fifteen days, 775 of them marked as agent-authored), where every pull request has a committed review. From 197 merged changes I derive 116 candidate tasks and publish 113 in the competition's format, each with a one-commit snapshot, a code graph, embeddings, and a tier recording whether its problem statement came from an issue, a pull request or a commit message. No statement was written after the fact. Scores come from my sandboxed re-implementation of the competition's documented harness, not from the official evaluator, which I did not run. Two controls bound it: the reference patch resolves 111 of 113 tasks and an empty patch resolves none. Gemma 4 E4B on two free T4 GPUs produced a patch for 45 of 58 tasks and resolved 5. I report how it fails, what each task costs, and what a second repository shows about why issue-traced history matters. Data, harness and run tables are public.

## 1. Introduction

The best coding agents today run on large models in the cloud. This competition asks whether a model that fits on one accelerator can do the same work. Answering that needs tasks, and the tasks available come from a narrow place: SWE-bench draws on twelve popular Python libraries [1], and the competition's development set on four (FastAPI, Requests, Rich and HTTPX).

Two kinds of repository are missing from that picture.

The first is the **data repository**. In a web library a bug usually announces itself: a request fails, a test goes red. In health data the costly defect is the one that raises nothing. A pipeline finishes, a table is written, and a number in it is wrong. Section 7 gives three cases, including a model whose AUC is 0.89 where it was built and 0.59 on the realistic set.

The second is the **agent-built repository**. A growing share of code is written by agents under a person's direction. Such a repository leaves an unusually complete record: an issue for each change, a pull request, a review. It also poses the competition's question in its plainest form. A large cloud agent did this work. How much of it can a small local agent redo from the same problem statements?

I study one repository that is both. `health-transformation-lab-nlp` is a public benchmark for finding gum disease in synthetic dental records. I typed no code: every change was made by coding-agent sessions I directed in chat and merged after an automated review.

Contributions:

1. **A task set** of 113 tasks in the competition's format, public on Kaggle under CC BY 4.0, with snapshots, code graphs, embeddings and a fidelity tier per task (Section 4).
2. **An open, calibrated harness**: a sandboxed re-implementation of the competition's documented harness, bounded by a reference-patch control and an empty-patch control, with a design that keeps answers away from the model on shared GPUs (Section 5).
3. **A baseline** for Gemma 4 E4B with a failure breakdown and cost per task (Section 6).
4. **Evidence that the tracing rule is what makes a history minable**: the same mining rule on a second repository without that rule yields candidates but almost no usable problem statements (Section 4.5).

## 2. Related work

**Task sets from repository history.** SWE-bench pairs GitHub issues with the pull requests that closed them and scores a patch by the repository's tests [1]; SWE-bench Verified adds human screening of task quality [2]. Defects4J [3] and BugsInPy [4] did the same for Java and Python bugs before language models. SWE-Gym [5], SWE-smith [6] and SWE-rebench [7] scale task collection for training and for contamination-free evaluation. All draw on human-maintained open-source libraries. This one follows the same recipe (a change that touches code and tests, a statement, fail-to-pass and pass-to-pass gates) on an agent-built data repository, and adds a field the others lack: where each statement came from.

**Agents.** SWE-agent showed that the interface given to a model matters as much as the model [8]. The competition fixes that interface (nine tools, including three over a precomputed code graph), so this work re-implements it.

**Data work.** DS-1000 tests data-science code generation [9], and Spider 2.0 [10] and ELT-Bench [11] test agents on enterprise SQL and pipeline construction. They score a produced artefact. These tasks score a repair to an existing, tested data codebase.

**Health-data quality.** The repository's checks follow the harmonized data-quality terms of Kahn et al. [12]; its de-identification tests follow the i2b2/UTHealth categories [13] and use MACCROBAT [14].

## 3. The source repository

The repository holds a Python package, its tests, an R twin kept in numerical parity, SQL and Databricks pipelines, and documentation. It was written between October 25 and November 8, 2026.

**Who wrote it.** Of 960 commits on `main`, 775 are marked as agent-authored (710 carry a co-author trailer; 65 are authored directly as the agent), 175 are squash merges of agent pull requests made through GitHub, 5 come from an automation bot, and 4 carry only my name (one merge and three documentation edits). I specified the work and directed the sessions in chat.

**Rules the agents work under.** A checked-in `AGENTS.md` requires one issue per user story, a branch named for its issue, a pull request that closes it, and a test written before the code. CI rejects a pull request from an agent's own session branch or without an issue link. Prose rules are tests too: one fails the build on a banned phrase, another on a benchmark listed out of order, another when a public function lacks its tracing decorator.

**Reviews.** Every pull request has a review committed as a file: 240 of them, for pull requests numbered up to 634. Of the 192 with a structured verdict, 119 approve, 64 approve with minor findings, 9 approve with conditions, and none request changes; blocking findings are fixed on the branch before the verdict is written. Agents merge their own green pull requests except in four cases reserved for me: runs on limited compute, publishing outside the repository, deletions, and changes to the rules.

## 4. Building the task set

### 4.1 Mining

The mining script reads every merged pull request and every first-parent commit on `main` as of October 29, 2026: 197 changes. A change is a **candidate** when its diff touches both non-test code and test files, which is the competition's own mining rule.

| Step | Tasks |
|---|---|
| Merged changes | 197 |
| Touch code and tests (candidates) | 116 |
| Built (one withdrawn: its patch names an organisation the repository's rules forbid) | 115 |
| Pass both gates | 114 |
| Published (one withheld: its patch adds third-party files with no stated licence) | 113 |

### 4.2 Fidelity tiers

Each task records where its `problem_statement` came from.

| Tier | Statement source | Candidates |
|---|---|---|
| A | the issue body | 49 |
| B | the pull request's title and body (no issue existed) | 45 |
| C | the commit message (no pull request existed) | 22 |

Tiers B and C exist because the issue rule was adopted partway through the history. For those 67 candidates a **backfilled issue record** quotes the original text verbatim, carries a `backfilled` label and is closed on creation.

### 4.3 Snapshots, graphs, embeddings

A snapshot is the tree at `base_commit` as a single commit, so no later history comes along. The code graph is an AST walk over the package into NetworkX node-link JSON with the competition's keys (median 488 nodes and 397 `calls` edges). Embeddings come from EmbeddingGemma, cut to 256 dimensions and renormalised. The competition does not name its embedding model, so similarity to its vectors is unverified. A format check against the competition's own files matched on the snapshot layout, the graph keys and the embedding shape.

### 4.4 Gates

A task is kept only if its tests fail at `base_commit` with the test patch alone, and pass once the reference patch is applied with the files the grader strips removed (test files and runner configuration). All 115 fail without the fix; 114 pass with it. The one failure is a package rename whose fix lives in a stripped file.

### 4.5 A second repository

To see whether the recipe transfers, I applied the mining rule unchanged to a second public repository: Open Navigator, an open-source civic engagement platform (FastAPI, dbt, React) run by a nonprofit I lead, with several human contributors and no issue-tracing rule. Of 1,320 first-parent commits, 133 touch non-test Python and Python tests. None links an issue. Only 22 can be tied by commit subject to one of the repository's 169 merged pull requests; others came in pull requests fast-forwarded onto `main`, which history alone cannot tell from direct commits.

So the rule finds candidates anywhere, but the problem statements come from the convention. In the source repository every candidate traces to an issue, 49 natively and 67 through backfilled records. These 133 candidates are not gated and are not part of the release.

## 5. Harness and controls

The competition's evaluator, `swegemma`, is available to participants as wheels in a separate Kaggle dataset that the starter notebook attaches. I looked for it only among the competition's own files, did not find it, and built a re-implementation from its guide. That was a mistake, and it shapes everything below: every score here comes from the re-implementation, and scoring this task set with the official evaluator is the first thing to do next.

The guide documents the initial prompt, the multi-turn loop, the nine tools with their limits, the budgets, patch extraction and verification. The harness implements those sections. The prompt, nudge messages and budget warning follow the guide's wording; the guide itself is not redistributed.

**Controls.** Two scripted models bound the harness. One replays each reference patch and should resolve every task; it resolves 111 of 113. The two misses need a Postgres server and an R runtime that the sandbox lacks, and are excluded from any real model's denominator. The other submits nothing and resolves 0 of 113.

**Keeping answers from the model.** This repository's history contains every fix, and later snapshots contain earlier tasks' fixes. Commands and verification run in Linux user, mount, network and pid namespaces: a read-only system, no network, and an allow-listed environment. A review before the first pull request found that an earlier version ran the model's commands on the host, where it could read the repository's history, every reference patch and the host's credentials.

Kaggle GPUs do not allow namespaces, and anything a notebook runs can read every attached file. So each task runs alone in its own private, offline notebook beside a private dataset holding that task only: the prompt fields, a snapshot refused if it holds more than one commit, its graph and embeddings. The patch comes back and is verified locally in the sandbox.

**Known differences.** Namespaces instead of a container; no ADK context compaction or prefix caching; sub-agents and skills are not run; packages come from the host Python. Every row records the harness name and its settings, and no number here is a competition score.

## 6. Baseline

**Setup.** `gemma-4-e4b-it` in fp16 with transformers on two T4 GPUs, internet off, thinking off, at most 2,048 new tokens per turn, a 24,576-token context, 40 tool calls, 60 turns and 30 minutes per task. Generation runs at about 8 tokens a second, hence 30 minutes, not the 5 my competition configuration uses. Tasks were run cheapest first under a GPU-hour cap.

**Results.** The runs span a harness fault: the first 36 tasks were served without their code graph and embeddings, so the three graph tools had nothing to query.

| Condition | Tasks | Non-empty patch | Resolved (95% CI) |
|---|---|---|---|
| Code graph missing (harness fault) | 36 | 30 | 5 (13.9%, 6.1–28.7) |
| Fixed harness | 22 | 15 | 0 (0%, 0–14.9) |
| All | 58 | 45 | 5 (8.6%, 3.7–18.6) |

The two conditions are not a comparison of the graph tools. The 22 later tasks are the costlier ones (0.53 against 0.27 GPU-hours per task), so they are also harder. A paired rerun of the first tasks on the fixed harness is the experiment that would isolate the tools.

By tier, the model resolved 4 of 27 tasks whose statement is an issue, 1 of 26 from a pull request and 0 of 5 from a commit message. The intervals overlap.

**How it fails.** Of the 53 unresolved tasks, 40 submitted a patch that fails the target tests (35 with failing tests, 5 with errors before any test ran) and 13 submitted nothing. Six of those 13 ended within two turns without a single tool call. On the fixed harness, a review of the transcripts traced the empty patches to the 2,048-token limit cutting off whole-file writes, not to the harness. The five resolved tasks are small: a CI rule, a warning message, a renumbered script, a label parser, a notebook setting.

**Cost.** The 58 tasks used 20.6 GPU-hours (10.3 hours of Kaggle's weekly allowance), a median of 0.32 GPU-hours, 6 tool calls and about 74,000 prompt tokens per task. At an estimated $0.69 per T4-hour that is $14.19 in total; Kaggle's GPUs are free, so this is an equivalent, not a spend. Five resolved tasks cost 4.1 GPU-hours each.

## 7. What these tasks contain that web-library tasks do not

Three cases from the repository show the defect class that motivates it. In each, everything ran and a number was wrong.

| Case | Score on what it was built against | Score on what it was not |
|---|---|---|
| De-identification rules, share of identifiers removed | 1.00 (the tier the rules were written beside) | 0.27 (a tier written after the rules were frozen) |
| Tooth-loss model, AUC | 0.89–0.90 (held-out labelled extractions) | 0.59–0.63 (teeth missing at the first visit) |
| A masking defect in the feature table | every test passed | the measures of about a quarter of charted teeth were blank in every earlier run |

All three are on synthetic data and are documented in the repository. Its response each time was a table to look things up in, not more inference: a held-out tier of identifier shapes, named ranges for the charted measurements, and a list of generator parameters each marked with a published source or the word "placeholder".

A keyword match on titles puts 16 of the 116 candidates in de-identification. The baseline attempted 8 and resolved none.

## 8. Limitations

- **One repository, one author's rules.** The second repository tests the mining rule only, not the agent.
- **Agent-written statements.** The issue text was largely written by a cloud agent at my direction. Following a large model's problem statements may be easier or harder than following a person's.
- **My harness, not the official evaluator, which was available.** Section 5 says how that happened and lists the known differences. No score here is comparable to the leaderboard.
- **Constrained settings.** The baseline caps output at 2,048 tokens with thinking off on T4 GPUs. My competition configuration allows 16,384 output tokens and a 4,096-token thinking budget on four L4s. The baseline is a floor for this setup, not a measure of the model.
- **Small and partial.** 58 of 111 scorable tasks, one sampled run each at temperature 0.2, and 36 of them without the graph tools.
- **Untested components.** The submission's analyzer sub-agent and its skill were not run.
- **Synthetic health data.** The cases in Section 7 are agreement with a synthetic answer key, not findings about any patient or practice.

## 9. Conclusion and release

A cloud agent built this repository in fifteen days. From the same problem statements, a model that runs on free GPUs resolved 5 of 58 tasks, all of them small. That gap is what this competition is trying to close, and it is now measurable on a kind of repository the standard sets miss.

The recipe generalises to any repository that traces its changes to issues: mine the changes that touch code and tests, record where each statement came from, gate, and calibrate the harness with a reference-patch control and an empty-patch control before trusting any model's score.

Where each number comes from is listed in `paper/sources.md`. Released: the task set (Kaggle, `jcblearning/health-transformation-lab-coding-agent-tasks`, CC BY 4.0), the harness and builders (`healthtransformationlab/health-transformation-lab-nlp`, MIT), the agent configuration (`healthtransformationlab/gemma-developer-agent`, Apache 2.0), and every run table cited here.

## References

1. Jimenez et al. SWE-bench: Can Language Models Resolve Real-World GitHub Issues? ICLR 2024.
2. Chowdhury et al. Introducing SWE-bench Verified. OpenAI, 2024.
3. Just, Jalali, Ernst. Defects4J: A Database of Existing Faults to Enable Controlled Testing Studies for Java Programs. ISSTA 2014.
4. Widyasari et al. BugsInPy: A Database of Existing Bugs in Python Programs. ESEC/FSE 2020.
5. Pan et al. Training Software Engineering Agents and Verifiers with SWE-Gym. ICML 2025.
6. Yang et al. SWE-smith: Scaling Data for Software Engineering Agents. NeurIPS 2025.
7. Badertdinov et al. SWE-rebench: An Automated Pipeline for Task Collection and Decontaminated Evaluation of Software Engineering Agents. NeurIPS 2025.
8. Yang et al. SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering. NeurIPS 2024.
9. Lai et al. DS-1000: A Natural and Reliable Benchmark for Data Science Code Generation. ICML 2023.
10. Lei et al. Spider 2.0: Evaluating Language Models on Real-World Enterprise Text-to-SQL Workflows. ICLR 2025.
11. Jin, Zhu, Kang. ELT-Bench: An End-to-End Benchmark for Evaluating AI Agents on ELT Pipelines. PVLDB, 2026.
12. Kahn et al. A Harmonized Data Quality Assessment Terminology and Framework for the Secondary Use of Electronic Health Record Data. eGEMs, 2016.
13. Stubbs, Uzuner. Annotating longitudinal clinical narratives for de-identification: the 2014 i2b2/UTHealth corpus. Journal of Biomedical Informatics, 2015.
14. Caufield et al. A Comprehensive Typing System for Information Extraction from Clinical Narratives (MACCROBAT). 2019.
