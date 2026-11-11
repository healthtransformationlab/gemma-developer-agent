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
| The submission validates | NOT CHECKED: `adk_submission.validate_directory` was not available |
| The agent runs | NOT CHECKED: no dry run, no GPU run |
| No claim of improvement | none in the PR, the ADR or the notes |
| The paper | untouched; `paper/check_rules.py --check` passes |
| Branch name and issue link | `feat/59-analyzer-first-compile-check`, `Closes #59` |

## Must fix before merge (the owner's)
1. `adk_submission.validate_directory` on this branch.
2. A dry run of two or three tasks under the competition's evaluator; read the analyzer's share of calls and seconds.
3. Decide the timing against the paper: its runs used `main`'s configuration as of November 11.

## Should fix later
- `health-transformation-lab-nlp`'s own harness runs a single agent and fills `{hints}` only; it needs the
  two-agent order and `{code_map?}` before its numbers can be compared with the evaluator's on this branch.
- The README's layout table still says "a coder agent and a read-only analyzer"; true, but not the order.

## Secrets, Real Data and Claims Scan
Secrets: none. Real data: none. Claims: none.
