# gemma-developer-agent

An entry for the Gemma 4 Developer Agent Competition and its paper track, and the experiment behind it:
**do five ingredients — a metadata-driven framework, consistent conventions with every change traced to an
issue, configuration management (a credential register, a dependency inventory, one declaration per
setting), OpenTelemetry on every call with timing and cost, and the forecasting those four enable — make a
small local coding agent better at fixing data-pipeline bugs?** Each ingredient is switched off in turn and
its contribution measured; nothing is asserted.

> Personal learning project. Not affiliated with or endorsed by any employer, institution or vendor.

## What's here

| Folder | What |
|---|---|
| `agent.yaml`, `prompts/`, `sub_agents/`, `configs/`, `eval_config.yaml` | the `submission.zip` layout: a root coder agent and a read-only analyzer, on `gemma-4-e4b` (small-model bonus); to be rebased on the dataset's `sample_submission/` once copied in |
| `skills/pipeline-doctor/` | the [pipeline-doctor](https://github.com/healthtransformationlab/pipeline-doctor) method as an ADK skill: classify the issue from the repository's metadata tables before reading code |
| `tasks/` | the DataOps task set in the competition's format, built from a real project's incident history |
| `paper/` | the paper-track writeup (3,000 words, due November 12, 2026) |
| `docs/` | what the starter notebook and the rules tell us about the evaluation |

## The experiment

Same agent, two task sets, two conditions:

|  | Competition dev set (129 tasks, web libraries) | DataOps task set (data-pipeline repo) |
|---|---|---|
| Agent without the skill | pass rate | pass rate |
| Agent with the pipeline-doctor skill | pass rate | pass rate |

Plus the offline switch-off test from pipeline-doctor on the same incidents: what each of the five
ingredients contributes (hide the config table, the naming conventions, lineage, the telemetry metrics, or
the run history, and measure what the rules can still do). If the skill helps on the DataOps set and not on
the web libraries, the ingredients are doing the work, not the prompt.

## Status

Scaffold. Nothing has been run yet; no number here is a result until `paper/` says so with its interval.
Deadlines: paper November 12, 2026; agent entry November 25; final submission December 2.
