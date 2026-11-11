# ADR 0001: the analyzer runs before the coder on every task

Date: 2026-11-11 · Status: proposed · Issue: #59

## Context

Under the competition's own evaluator on November 10, the agent resolved 0 of 20 sampled tasks
(health-transformation-lab-nlp, `data/tasks/official_agent_runs/README.md`). The coder had three graph tools, an
analyzer it could call as a tool, and a skill. Over 189 tool calls it called a graph tool 9 times in 4 runs, the
analyzer 3 times in 3 runs, and the skill never. Offering Gemma 4 E4B a tool did not make it use the tool. Of the
16 patches, 2 had syntax errors in the model's own code and 3 lacked an import or file the tests need.

The submission is declarative YAML, so nothing of ours can run between the model's turns. The schema does allow a
`SequentialAgent`, an `output_key` that saves an agent's final answer to session state, and state variables in a
later agent's instruction (`docs/rulebook-notes.md`).

## Decision

The root is a `SequentialAgent`: `code_analyzer`, then `coder`. The analyzer has the three graph tools only, at
most five calls by its prompt, and a twelve-line answer saved as `code_map`. The coder's prompt carries
`{code_map?}` (optional, so an analyzer that fails cannot end the run: issue 33) and no longer has the analyzer as
a tool. The coder compiles every Python file it edited before `submit_patch`.

Not done: no new tool, no trace of a failing test (the agent has no failing test until it writes one), no adapter.

## Consequences

- The code map costs tool calls and seconds on every task, including those where it is wrong or not needed. All
  budgets are per task, so they come out of the coder's 40 calls and five minutes.
- The analyzer's tool results stay in the session the coder reads. It has no `read_file`, so those are names and
  edges, not file contents. Whether the coder's context still grows too much is for the dry run to show.
- A prompt limit of five calls is a request, not a cap. A looping analyzer is stopped only by the task's budget.
- Checked on November 11 with the competition's own packages (adk-submission 0.2.13, swegemma 0.2.11), with no
  GPU and no model call: `validate_directory` accepts the files, and `compile_submission`, given the evaluator's
  limits and its nine tool names, builds a `SequentialAgent` of `code_analyzer` (the three graph tools,
  `output_key: code_map`, its own sampling settings) then `coder` (`{code_map?}` in its instruction, the skill's
  tools). As first written it did not build: `skills: ../skills/pipeline-doctor` in `sub_agents/coder.yaml` was
  refused as path traversal, which would have ended every task before it started. A skill's path is written from
  the submission's root in whichever file names it (`skills/pipeline-doctor`); a test pins that.
- Still unverified until a run on a GPU: that `code_map` reaches the coder's prompt, what share of the 40 calls and
  five minutes the analyzer uses, and that the evaluator's turn and nudge counts treat the analyzer's final answer
  as the end of its part and not as an idle turn of the session.

## Revisit when

The same 20 tasks have been rerun. Keep it if more runs reach the right file or resolve; go back to the single
agent (the state before this change) if the analyzer uses more than a quarter of the budget or the submission does
not validate. If it does not validate, the fallback that needs no schema change is one prompt line: the coder's
first tool call is always `code_analyzer`.
