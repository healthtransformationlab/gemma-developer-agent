# gemma-developer-agent

A coding agent for the Gemma 4 Developer Agent Competition, and the question behind it:

**Does a well-run data repo make a small AI coding agent better at fixing bugs?**

We test five things a well-run repo has. Each one is switched off in turn and the drop is measured.

| Ingredient | In one line |
|---|---|
| Metadata-driven | The pipelines, runs, lineage and runbook are tables, not logs |
| Conventions | Typed names; every change traced to an issue |
| Configuration management | One place per setting; credentials and dependencies with expiry dates |
| Telemetry | Every call records timing and cost |
| Forecasting | Because of the four above, failures are predicted with a date |

> Personal learning project. Not affiliated with or endorsed by any employer, institution or vendor.

<details>
<summary><b>What's in this repo</b></summary>

| Folder | What |
|---|---|
| `agent.yaml`, `prompts/`, `sub_agents/`, `configs/`, `eval_config.yaml` | the competition entry (`submission.zip` layout): a coder agent and a read-only analyzer, on Gemma 4 E4B for the small-model bonus; to be rebased on the dataset's `sample_submission/` |
| `skills/pipeline-doctor/` | the [pipeline-doctor](https://github.com/healthtransformationlab/pipeline-doctor) method as a skill: classify the issue from the repo's tables before reading code |
| `tasks/` | the DataOps task set, in the competition's format, built from a real repo's history |
| `paper/` | the paper-track writeup (3,000 words, due November 12, 2026) |
| `docs/` | what the rules, the dataset format and the starter notebook tell us |

</details>

<details>
<summary><b>The experiment</b></summary>

Same agent, two task sets, two conditions:

|  | Competition dev set (129 tasks, web libraries) | DataOps task set (a data-pipeline repo) |
|---|---|---|
| Agent without the skill | pass rate | pass rate |
| Agent with the pipeline-doctor skill | pass rate | pass rate |

If the skill helps on the DataOps set and not on the web libraries, the repo's ingredients are doing the
work, not the prompt. Alongside: the offline switch-off test from pipeline-doctor, which hides one
ingredient at a time (the config table, the naming conventions, lineage, the telemetry metrics, the run
history) and measures what the rules can still do.

</details>

<details>
<summary><b>Where the task set comes from</b></summary>

The source repo's own history: every merged change that touched code and tests (the competition's own
mining rule). 116 candidates so far. Each carries a fidelity tier for its problem statement: A, from an
issue (49); B, from a PR description (45); C, from a commit message (22). Every one is now traced to an
issue; 67 of those issues are backfilled records that quote the original text verbatim and say so. Format:
[`docs/dataset-format.md`](docs/dataset-format.md).

</details>

<details>
<summary><b>Status and dates</b></summary>

Scaffold. No run has happened; no number here is a result until `paper/` says so with its interval.
Paper deadline November 12, 2026; entry deadline November 25; final submission December 2.

</details>
