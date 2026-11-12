# gemma-developer-agent

**Paper Track submission:** [Can a small local agent redo a cloud agent's work?](https://kaggle.com/competitions/gemma-4-developer-agent-paper/writeups/can-a-small-local-agent-redo-a-cloud-agents-work)

A coding agent for the Gemma 4 Developer Agent Competition, and the question behind it:

**Does a well-run data repo make a small AI coding agent better at fixing bugs?**

The idea is that five things a well-run repo has do part of the agent's thinking for it. What has been measured and run is a baseline (below).

| Ingredient | In one line |
|---|---|
| Metadata-driven | The pipelines, runs, lineage and runbook are tables, not logs |
| Conventions | Typed names; every change traced to an issue |
| Configuration management | One place per setting; credentials and dependencies with expiry dates |
| Telemetry | Every call records timing and cost |
| Forecasting | Because of the four above, failures are predicted with a date |

> Personal learning project. Not affiliated with or endorsed by any employer, institution or vendor.

Licence: [Apache 2.0](LICENSE), the licence type the competition names for winning submissions.

## What has been run, and what it cost

Gemma 4 E4B on the 93 tasks built from
[`health-transformation-lab-nlp`](https://github.com/healthtransformationlab/health-transformation-lab-nlp)'s history.
One row per run. Time and tokens are averages for one task, from each run's own log.

| Run | Hardware and budget | Resolved | Agent time a task | Tokens a task |
|---|---|---|---|---|
| Local harness, cheapest tasks first | 2 × T4 on Kaggle; 2,048 output tokens a turn | **5 of 48** (10.4%, 95% CI 4.5–22.2) | 11.3 min | 112k in, 4.4k out |
| The same, larger budget | 1 × L4 on Colab; 16,384 output tokens a turn, thinking on | 2 of the 23 cheapest (2 before) | 5.4 min | not logged |
| The competition's own evaluator, end to end | 4 × L4 on Kaggle; the competition's 5-minute budget | 0 of a random 20 (95% CI 0–16.1) | 1.7 min, plus 5.9 min to load the model | 124k in, 6.7k out |
| The competition's development set, same evaluator | 4 × L4 on Kaggle; the same 5-minute budget; a seeded 40 of its 129 tasks | 3 of the 23 a Kaggle notebook can verify (95% CI 4.5–32.1) | 1.8 min | 121k in, 6.9k out |
| Pre-registered experiment: as published (the baseline arm) | 4 × L4 on Kaggle; the same 5-minute budget; all 93 tasks | 0 of the 21 tasks run before its model server failed; 72 not run | 1.7 min | 125k in, 6.2k out |
| The same, with graph retrieval done for the agent | the same | **4 of 93** (95% CI 1.7–10.5) | 1.2 min | 103k in, 4.7k out |
| The same, with the failing test's report (from the hidden test: not a benchmark condition) | the same | **5 of 93** (95% CI 2.3–12) | 1.5 min | 101k in, 4.9k out |

- **Controls.** On the published files the competition's evaluator resolves 93 of 93 reference patches and 0 of
  93 empty patches, and gives the same verdict as the local harness on all 48 agent patches compared: 25 saved
  from the baseline run, on the first release, and 23 from a rerun, on the corrected release (the two rows of the
  table in the paper's Section 5).
- **Cost of a fix.** 1.80 hours of agent time a fix across the 48. The 13 attempted tasks whose statements say
  what their tests check (an AI screen of all 93; a person checked 30) gave 4 of the 5 fixes for 17% of that
  time: 0.38 hours a fix.
- **With more context.** A pre-registered experiment gave the agent graph retrieval, or a failing test's report,
  on all 93 tasks. Its baseline arm lost its model server after 21 tasks, none of which any arm resolved, and
  Kaggle's weekly GPU allowance ran out before the rerun the plan allows, so neither context has been tested
  against the baseline
  ([the rerun](https://github.com/healthtransformationlab/health-transformation-lab-nlp/issues/681) is owed).
  7 of the 8 tasks those two arms resolved are in the 17-task core split (statements that an AI
  screen finds say what their tests check), and 6 of the 8 had been resolved from the statement alone in an earlier run.
- **Where the time went.** The kernels kept OpenTelemetry spans (names, counts and seconds). In the experiment's
  three arms, 66–83% of a task's time was model calls and 14–15% context compaction;
  45 of 207 runs ended when a prompt passed the model's context window. A fix cost 1.9 L4 GPU-hours
  with graph retrieval and 1.8 with the report: about 1.59 and 1.50 US dollars at a median rental of 0.83 an L4
  GPU-hour (an estimate; Kaggle's GPUs were free).
- **Tests.** The source repository had 2,269 tests in 126 files on November 8, when its 960 commits end, and 2,355
  in 133 at the commit the paper's analyses use; CI runs them on every pull request.
- **What the graph could tell it.** By name, call edge or embedding search (first ten results), the code graph
  leads from statement to fix in 42 of the 51 tasks that edit existing code. The model asked a graph tool in 20 of
  its 473 tool calls, and a paired rerun of 23 tasks resolved 2 with the graph tools and 2 without.

Sources, at the commits the paper used: the [local harness](https://github.com/healthtransformationlab/health-transformation-lab-nlp/blob/254c44c4a19fae5ffae1fb9661692aa2f390e034/data/tasks/agent_runs/gemma-4-e4b-it_kaggle.csv)
table (its 48 rows of published tasks; tokens over the 46 that logged them), the
[larger budget](https://github.com/healthtransformationlab/health-transformation-lab-nlp/blob/254c44c4a19fae5ffae1fb9661692aa2f390e034/data/tasks/agent_reruns/gemma-4-e4b-it_larger_budget.csv),
[first official-evaluator sample](https://github.com/healthtransformationlab/health-transformation-lab-nlp/blob/254c44c4a19fae5ffae1fb9661692aa2f390e034/data/tasks/official_agent_runs/gemma-4-e4b-it-qat-w4a16-ct_swegemma.csv) (the 20 in
its sample), [development-set](https://github.com/healthtransformationlab/health-transformation-lab-nlp/blob/4ce2170983add8aabe15ad1cf7cc303ad300bf04/data/tasks/official_agent_runs/gemma-4-e4b-it-qat-w4a16-ct_swegemma_devset.csv), [pre-registered experiment](https://github.com/healthtransformationlab/health-transformation-lab-nlp/blob/4ce2170983add8aabe15ad1cf7cc303ad300bf04/data/tasks/official_agent_runs/README.md) and [routing](https://github.com/healthtransformationlab/health-transformation-lab-nlp/blob/254c44c4a19fae5ffae1fb9661692aa2f390e034/data/tasks/screening/screen_routing.csv) tables. The Kaggle kernels run with
internet off, so they send no telemetry: each task's timing, tokens and tool calls are written into these
tables, and the evaluator's kernels keep their spans in a file that is rolled up beside them. The source repo's pipelines send theirs to Azure Application Insights
([`docs/telemetry.md`](https://github.com/healthtransformationlab/health-transformation-lab-nlp/blob/254c44c4a19fae5ffae1fb9661692aa2f390e034/docs/telemetry.md)). Every number in the paper is traced in
[`paper/sources.md`](paper/sources.md).

<details>
<summary><b>What's in this repo</b></summary>

| Folder | What |
|---|---|
| `agent.yaml`, `prompts/`, `sub_agents/`, `configs/`, `eval_config.yaml` | the competition entry (`submission.zip` layout): a coder agent and a read-only analyzer, on Gemma 4 E4B for the small-model bonus; to be rebased on the dataset's `sample_submission/` |
| `skills/pipeline-doctor/` | the [pipeline-doctor](https://github.com/healthtransformationlab/pipeline-doctor) method as a skill: classify the issue from the repo's tables before reading code |
| `tasks/` | a note on the task set: 93 tasks in the competition's format, each verified with the competition's own evaluator, built from a real repo's history. The tasks themselves are [on Kaggle](https://www.kaggle.com/datasets/jcblearning/health-transformation-lab-coding-agent-tasks); the builders and run tables are in [health-transformation-lab-nlp](https://github.com/healthtransformationlab/health-transformation-lab-nlp) (`data/tasks/`) |
| `paper/` | the paper-track writeup ([`small-local-agent-redo-cloud-agent-work.md`](paper/small-local-agent-redo-cloud-agent-work.md), under 3,000 words, due November 12, 2026), the same text laid out as a paper ([`small-local-agent-redo-cloud-agent-work.pdf`](paper/small-local-agent-redo-cloud-agent-work.pdf), rebuilt with `node paper/build_pdf.js`) where each of its numbers comes from ([`sources.md`](paper/sources.md)), and how it meets each competition rule ([`rules_check.md`](paper/rules_check.md), written by `python paper/check_rules.py`, checked in CI) |
| `docs/` | what the rules, the dataset format and the starter notebook tell us |

</details>

<details>
<summary><b>The plan, and what is still to run</b></summary>

The plan is the same agent on two task sets, with and without the pipeline-doctor skill: the competition's
development set (129 tasks) and this task set (93). This task set has been run under two harnesses (above): a
local re-implementation of the competition's documented harness, and the competition's own evaluator, end to end.
The development set has been run on a seeded 40 of its tasks under that evaluator.
The comparison with and without the skill has not been run: in the evaluator's run the skill was available and the
model never called it, so this repo does not yet say whether the skill, or a well-run repo, helps. Ten more
attempts were on tasks since left out of the published set. Details and limits:
[`paper/small-local-agent-redo-cloud-agent-work.md`](paper/small-local-agent-redo-cloud-agent-work.md).

The offline switch-off test in pipeline-doctor is not evidence for the ingredients above: its rules were written
from the nine incidents it is scored on, and its "no conventions" condition blanks five data columns.

</details>

<details>
<summary><b>Where the task set comes from</b></summary>

The source repo's own history: every merged change that touched code and tests (the competition's own
mining rule). 116 candidates; 114 pass both gates; 93 are published, the ones whose reference patch the
competition's own evaluator resolves. Each candidate carries a fidelity tier for its
problem statement: A, from an
issue (49); B, from a PR description (45); C, from a commit message (22). Every one is now traced to an
issue; 67 of those issues are backfilled records that quote the original text verbatim and say so. Format:
[`docs/dataset-format.md`](docs/dataset-format.md).

</details>

<details>
<summary><b>Status and dates</b></summary>

- **Run:** the task set (built, gated, verified with the competition's evaluator, published), the harness controls, and Gemma 4 E4B on 58 tasks, 28 of them twice and 23 a third time with a larger budget. Every number
  is in `paper/sources.md` with the file it came from.
- **Run under the competition's own evaluator:** this `agent.yaml`, end to end, on a seeded sample of 20 published tasks
  (0 resolved). The analyzer sub-agent and the skill were available there; the model called the sub-agent 3 times and
  the skill never. Then a seeded 40 of the competition's development tasks (3 resolved of the 23 a Kaggle notebook can
  verify), and a pre-registered experiment on all 93 with two kinds of added context (above), whose baseline arm ran
  21 tasks.
- **Not run:** the experiment's baseline for the other 72 tasks ([issue 681](https://github.com/healthtransformationlab/health-transformation-lab-nlp/issues/681));
  the other 89 development tasks; a comparison with and without the pipeline-doctor skill.
- **Dates:** paper deadline November 12, 2026; entry deadline November 25; final submission December 2.

</details>
