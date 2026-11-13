---
pr: 60
branch: feat/59-analyzer-first-compile-check
title: "000 US1: run the analyzer before the coder on every task; compile edits before submitting"
author: Claude Code (agent session for jcbowyer)
reviewed_at: 2026-11-11
reviewer: the authoring session (the layout test was run; the competition's validator and evaluator were not available; no reviewer subagent run)
verdict: hold for the owner
---

# PR Review: 000 US1: run the analyzer before the coder on every task; compile edits before submitting

## Summary
The analyzer stops being a tool the model may call and becomes the first of two agents that always run; the coder
compiles what it edited before submitting. The reason is measured (the model called the analyzer 3 times in 20
runs); the remedy is not. Blocking: the submission has not been validated or run in this form.

## Checks
| Check | Result |
|---|---|
| Test first | `tests/test_submission_layout.py`: 6 of 8 failed on `main`'s config, 8 pass now |
| The reason is a run's number | 0 of 20, 189 tool calls, analyzer 3 times, graph tools 9, skill never; 2 syntax errors and 3 missing imports or files in 16 patches (health-transformation-lab-nlp, `data/tasks/official_agent_runs/README.md`) |
| No required prompt variable can be unset | `{code_map?}` and `{hints?}` are optional; `{problem_description}` is always set (issue 33); pinned by a test |
| One base model | both sub-agents name `gemma-4-e4b-it-qat-w4a16-ct`; the root names none |
| The analyzer cannot bloat the coder's context with file contents | graph tools only; no `read_file` |
| The submission validates | checked later the same day, below: it did not build as first written; it builds now |
| The agent runs | NOT CHECKED: no dry run, no GPU run |
| No claim of improvement | none in the PR, the ADR or the notes |
| The paper | untouched; `paper/check_rules.py --check` passes |
| Branch name and issue link | `feat/59-analyzer-first-compile-check`, `Closes #59` |

## Must fix before merge (the owner's)
1. ~~`adk_submission.validate_directory` on this branch.~~ Done, below; one line had to change.
2. A dry run of two or three tasks under the competition's evaluator; read the analyzer's share of calls and seconds.
3. Decide the timing against the paper: its runs used `main`'s configuration as of November 11.

## Check 1, run later on November 11 by a second session

With the competition's own packages (adk-submission 0.2.13, swegemma 0.2.11) on a machine with no GPU, and no model
call. The limits and model registry were built the way the evaluator's command line builds them; its nine tools were
stand-ins with the evaluator's names.

| Step | `main` at `b95b235` (the agent the paper's runs used) | This branch as first written | This branch now |
|---|---|---|---|
| `validate_directory` (files, sizes, extensions, symlinks, one root config) | passes | passes | passes |
| `compile_submission` (what the evaluator does at the start of every task) | builds one agent with 11 tools | **fails**: `Path traversal attempted in skill: ../skills/pipeline-doctor` (`sub_agents/coder.yaml`) | builds a `SequentialAgent`: `code_analyzer` (3 graph tools, `output_key` `code_map`, 2,048 output tokens, thinking 1,024), then `coder` (9 tools and the skill's, `{code_map?}` and the compile step in its instruction) |

As first written, every task would have ended before the agent's first turn. The fix is one line: a skill's path is
read from the submission's root, in a sub-agent's file too. `tests/test_submission_layout.py` now fails on a skill
path that climbs out of a folder or has no `SKILL.md` under it (9 passed; the new test failed before the change).

The two other guesses hold: `agent_class: SequentialAgent` with `sub_agents: [{config_path}]` at the root, and
`generate_content_config` on the analyzer. Checks 2 and 3 are untouched: nothing here has run on a GPU, and nothing
says the change helps.

## Should fix later
- `health-transformation-lab-nlp`'s own harness runs a single agent and fills `{hints}` only; it needs the
  two-agent order and `{code_map?}` before its numbers can be compared with the evaluator's on this branch.
- The README's layout table still says "a coder agent and a read-only analyzer"; true, but not the order.
- A compiled test file is committed under `tests/__pycache__/`. It is not part of the submission (only `agent.yaml`,
  `eval_config.yaml`, `prompts`, `sub_agents`, `configs` and `skills` are), and can be removed.

## Secrets, Real Data and Claims Scan
Secrets: none. Real data: none. Claims: none.
