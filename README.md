# gemma-developer-agent

A coding agent for the Gemma 4 Developer Agent Competition, and the question behind it:

View submission: [Kaggle Submission: Can a small local agent redo a cloud agents work](https://kaggle.com/competitions/gemma-4-developer-agent-paper/writeups/can-a-small-local-agent-redo-a-cloud-agents-work)

**Does a well-run data repo make a small AI coding agent better at fixing bugs?**

The idea is that five things a well-run repo has do part of the agent's thinking for it. That has not been measured
here yet: what has been run is a baseline (below).

| Ingredient | In one line |
|---|---|
| Metadata-driven | The pipelines, runs, lineage and runbook are tables, not logs |
| Conventions | Typed names; every change traced to an issue |
| Configuration management | One place per setting; credentials and dependencies with expiry dates |
| Telemetry | Every call records timing and cost |
| Forecasting | Because of the four above, failures are predicted with a date |

> Personal learning project. Not affiliated with or endorsed by any employer, institution or vendor.

Licence: [Apache 2.0](LICENSE), the licence type the competition names for winning submissions.

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
<summary><b>The experiment, and what has been run</b></summary>

The plan was the same agent on two task sets under two conditions:

|  | Competition dev set (129 tasks) | DataOps task set (93 tasks) |
|---|---|---|
| Agent without the skill | not run | **48 tasks run, 5 resolved** (10.4%, 95% CI 4.5 to 22.2) |
| Agent with the pipeline-doctor skill | not run | not run |

One cell has been run, so this repo does not yet say whether the skill, or a well-run repo, helps. What the run
does give is a baseline and its controls. The agent ran on a local re-implementation of the competition's
documented harness, not the competition's evaluator. The competition's evaluator then checked the task set and the
patches: on the published files it resolves 93 of 93 reference patches and 0 of 93 empty patches, and it gives
the same verdict as the local harness on all 48 agent patches compared. Gemma 4 E4B on two T4 GPUs wrote a patch
for 40 of the 48 published tasks it attempted and resolved 5. A paired rerun of 23 of them, with and without the
code-graph tools, resolved 2 either way; with the tools available the model called one in 4 of the 23 runs. Ten
more attempts were on tasks since left out of the published set. Run end to end by the competition's own evaluator
(four L4 GPUs, this repo's competition settings) on a seeded sample of 20 tasks, the agent resolved none. A rerun of
the 23 cheapest of the 48 with eight times the output budget and thinking on (one L4 GPU on Colab, the local harness) resolved
2, against 2 under the tight limits. By names and call edges, a task's code graph leads from its statement to
its fix in 22 of the 93 tasks. Details and limits: [`paper/small-local-agent-redo-cloud-agent-work.md`](paper/small-local-agent-redo-cloud-agent-work.md).

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
