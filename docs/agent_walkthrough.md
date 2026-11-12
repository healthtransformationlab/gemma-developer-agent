# The agent, file by file

What the competition entry is made of and why each part is set the way it is. The entry is declarative: YAML and
prompts, compiled by the competition's harness, with no code of its own
([the rules as read here](rulebook-notes.md)). What the agent did when it ran is in
[the paper](../paper/small-local-agent-redo-cloud-agent-work.md) and the
[README's run table](../README.md#what-has-been-run-and-what-it-cost).

## The files

| File | What it is |
|---|---|
| [`agent.yaml`](../agent.yaml) | the root agent, `data_pipeline_fixer`: its model, the tools it may call, a sub-agent and a skill |
| [`prompts/system.md`](../prompts/system.md) | its instructions: submit a patch before the budget runs out, then the order of work |
| [`sub_agents/code_analyzer.yaml`](../sub_agents/code_analyzer.yaml), [`prompts/analyzer.md`](../prompts/analyzer.md) | a read-only analyst the coder can hand a question to |
| [`configs/sampling.yaml`](../configs/sampling.yaml) | sampling and the thinking budget |
| [`eval_config.yaml`](../eval_config.yaml) | the budgets for one task |
| [`skills/pipeline-doctor/`](../skills/pipeline-doctor/SKILL.md) | the [pipeline-doctor](https://github.com/healthtransformationlab/pipeline-doctor) method as a skill |

## The model

Every agent in the entry names the same base model, `gemma-4-e4b-it-qat-w4a16-ct`, which is Gemma 4 E4B: the
competition allows one base model across all agents, and gives a bonus for the small one. To run the larger model,
change every `model:` line together.

## The root agent: `agent.yaml`

It may call the harness's nine tools: `run_command`, `read_file`, `edit_file`, `write_file`, `get_status`,
`submit_patch`, and the three graph tools `get_code_neighbors`, `search_similar_code` and `get_code_subgraph`.
`submit_patch` and `get_status` do not count against the tool-call budget.

The analyzer is attached as a tool (`agent_tool`) with `skip_summarization: true`, not as a sub-agent the
conversation moves into: that keeps what the analyzer reads out of the coder's context.

## The instructions: `prompts/system.md`

In the order the prompt gives them:

1. **Submit before the budget runs out.** A missing patch scores zero; a partial one may pass. The harness adds a
   `budget_warning` to every tool response when ten calls or fewer remain: the prompt says to stop exploring then,
   make the smallest edit and submit.
2. **Budget discipline.** Read line ranges, never a whole file, and never the same file twice; keep each thought
   short; keep edits small.
3. **What the grader strips.** Changes to test files and to the test runner's configuration are removed from a
   patch before grading, so the prompt says to fix the library code and to keep scratch files out of the workspace.
4. **The order of work.** Say what test would prove the fix; read the repository's conventions before its code;
   find the named symbols with the graph tools, or hand that to the analyzer; reproduce when it is cheap; make the
   smallest change, following the repository's naming rules; run the targeted tests; submit.

The prompt takes `{problem_description}` and `{hints?}` from the harness. The question mark matters: the evaluator
sets `hints` only for a task that has some, and a required variable that is not set ends the agent before its first
model call.

## The analyzer: `sub_agents/code_analyzer.yaml`

A second agent on the same model, with four tools, all of them read-only: `read_file` and the three graph tools.
Given an issue, it returns the symbols the issue names, their neighbours one hop away, the tests that refer to them
and the configuration that governs them, as paths and line ranges. It proposes no fix. `include_contents: none`
means it starts from the question alone, without the coder's history.

## Sampling: `configs/sampling.yaml`

| Setting | Value |
|---|---|
| `temperature`, `top_p` | 0.2, 0.95 |
| `max_output_tokens` | 16,384 |
| `thinking_config.thinking_budget` | 4,096, with `include_thoughts` |

The file's own note gives the reasons for the last two: a bounded thinking budget keeps a tool call from being cut
off behind a long thought, and the output limit leaves room for an `edit_file` payload.

## Budgets: `eval_config.yaml`

| Setting | Value | The harness's default |
|---|---|---|
| `max_time_minutes` | 5 | 60 |
| `max_tool_calls` | 40 | 100 |
| `max_turns` | 60 | 500 |
| `timeout_seconds` (one command) | 120 | 300 |

The whole evaluation has 12 hours for about 120 tasks, sandbox setup included, so about 5 minutes of agent time a
task is the real ceiling. The competition's sample submission used 1 minute and 10 calls, and wrote no patch on two
tasks. Every run of this agent under the competition's evaluator used the values above, which is one reason the
paper gives no leaderboard score.

## The skill: `skills/pipeline-doctor/`

For a repository that keeps its pipeline metadata as tables (a pipeline configuration, a run log, lineage, a
runbook), the skill classifies an issue from those tables before any code is read: a credential that expired, a
deprecation, a setting that drifted, a schema that changed. Only an issue it cannot classify needs reasoning from
the code. It reads names, counts, durations, error types and check results, never note text or rows of data.

## What the runs showed about these parts

- In the first sample of 20 tasks under the competition's evaluator, the sub-agent and the skill were both
  available: the model called the sub-agent 3 times and the skill never. So nothing here says whether the skill
  helps: the comparison with and without it has not been run.
- Across three runs (a paired rerun, the larger budget and the evaluator's first sample), the model called a
  graph tool in 20 of its 473 tool calls.
- In the experiment's three Kaggle arms, 45 of 207 runs ended when a prompt passed the model's context window.

Each of these is in the [README](../README.md#what-has-been-run-and-what-it-cost) or the
[paper](../paper/small-local-agent-redo-cloud-agent-work.md), with its source in
[`paper/sources.md`](../paper/sources.md).

## Running it

The agent runs inside the competition's evaluator, which this repository does not hold: the competition's files
are not redistributed. What runs it is in the source repository,
[health-transformation-lab-nlp](https://github.com/healthtransformationlab/health-transformation-lab-nlp):

| To | Use |
|---|---|
| run the agent under the competition's evaluator, in a Kaggle notebook | `kaggle/official_agent_run.py` |
| replay the evaluator's two controls on the task set (reference patch, empty patch) | `kaggle/official_verify.py` |
| run an agent under the local harness | `python/scripts/59_run_agent.py`, and `60_kaggle_agent.py` on Kaggle's GPUs |
| read the run tables | `data/tasks/agent_runs/`, `data/tasks/official_agent_runs/` |

The tasks themselves are
[on Kaggle](https://www.kaggle.com/datasets/jcblearning/health-transformation-lab-coding-agent-tasks), in the
competition's layout ([format](dataset-format.md)).

## Checks in this repository

```bash
pip install pypdf && python paper/check_rules.py --check   # the paper against the competition's rules
python docs/build_decks.py --check                         # the deck is up to date, and its numbers are the paper's
```

CI runs both, and checks each pull request's branch name and issue link.
