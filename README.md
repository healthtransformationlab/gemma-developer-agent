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
| The competition's development set, same evaluator | 4 × L4 on Kaggle | not run yet (129 tasks) | | |

- **Controls.** On the published files the competition's evaluator resolves 93 of 93 reference patches and 0 of
  93 empty patches, and gives the same verdict as the local harness on all 48 agent patches.
- **Cost of a fix.** 1.80 hours of agent time a fix across the 48. The 13 attempted tasks whose statements say
  what their tests check (an AI screen of all 93; a person checked 30) gave 4 of the 5 fixes for 17% of that
  time: 0.38 hours a fix.
- **What the graph could tell it.** By name, call edge or embedding search (first ten results), the code graph
  leads from statement to fix in 42 of the 51 tasks that edit existing code. The model asked a graph tool in 20 of
  its 473 tool calls, and a paired rerun of 23 tasks resolved 2 with the graph tools and 2 without.

Sources, at the commit the paper used: the [local harness](https://github.com/healthtransformationlab/health-transformation-lab-nlp/blob/254c44c4a19fae5ffae1fb9661692aa2f390e034/data/tasks/agent_runs/gemma-4-e4b-it_kaggle.csv)
table (its 48 rows of published tasks; tokens over the 46 that logged them), the
[larger budget](https://github.com/healthtransformationlab/health-transformation-lab-nlp/blob/254c44c4a19fae5ffae1fb9661692aa2f390e034/data/tasks/agent_reruns/gemma-4-e4b-it_larger_budget.csv),
[official evaluator](https://github.com/healthtransformationlab/health-transformation-lab-nlp/blob/254c44c4a19fae5ffae1fb9661692aa2f390e034/data/tasks/official_agent_runs/gemma-4-e4b-it-qat-w4a16-ct_swegemma.csv) (the 20 in
its sample) and [routing](https://github.com/healthtransformationlab/health-transformation-lab-nlp/blob/254c44c4a19fae5ffae1fb9661692aa2f390e034/data/tasks/screening/screen_routing.csv) tables. The Kaggle kernels run with
internet off, so they send no telemetry: the harness writes each task's timing, tokens and tool calls into these
tables instead. The source repo's pipelines send theirs to Azure Application Insights
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
development set (129 tasks) and this task set (93). Only this task set without the skill has been run (above), so
this repo does not yet say whether the skill, or a well-run repo, helps. The local harness re-implements the
competition's documented harness; the competition's own evaluator then checked the task set and the agent's
patches. Ten more attempts were on tasks since left out of the published set. Details and limits:
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
  the skill never.
- **Not run:** the competition's development set; a comparison with and without the pipeline-doctor skill.
- **Dates:** paper deadline November 12, 2026; entry deadline November 25; final submission December 2.

</details>
