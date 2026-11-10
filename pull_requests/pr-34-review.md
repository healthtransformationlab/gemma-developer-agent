---
pr: 34
branch: fix/33-optional-hints
title: "000 BUG5: make the hints variable optional in the agent's prompt"
author: Claude Code (agent session for jcbowyer)
reviewed_at: 2026-11-10
reviewer: the authoring session (the framework's template code was read, and the fix was dry-run through the competition's evaluator; no reviewer subagent run)
verdict: approve
---

# PR Review: 000 BUG5: make the hints variable optional in the agent's prompt

## Summary
One character in `prompts/system.md`. Without it the agent ends before its first model call on any task that has no
hints, under the competition's own evaluator. Nothing blocking.

## Checks
| Check | Result |
|---|---|
| The failure is real and is this | three sampled tasks under the competition's evaluator on Kaggle: `agent_error` "Context variable not found: `hints`", 0 model calls, 1.2 to 1.4 seconds |
| The cause | `swegemma`'s agent runner sets `session_state['hints']` only when the task's hints are not empty; `google.adk.utils.instructions_utils` raises `KeyError` for a name that is not in the state |
| The fix is the framework's own form | the same function treats a name ending in `?` as optional and returns an empty string |
| The prompt is unchanged for a task with hints | both forms are replaced by the hint text when it is set |
| Dry run | the competition's evaluator against a stand-in endpoint on `htlnlp_c95eedd3` (no hints): 3 model calls and a patch, where there were none |
| The submission still validates | `adk_submission.validate_directory` accepts it |
| Other variables | `{problem_description}` is always set by the evaluator; no other variable is used in `prompts/` or the YAML files |
| Branch name and issue link | `fix/33-optional-hints`, `Closes #33` |

## Should fix later
- `health-transformation-lab-nlp`'s `agent_harness.fill_instruction` fills `{hints}` only. It should fill `{hints?}`
  the same way, or that harness will pass the literal text to the model.

## Secrets, Real Data and Claims Scan
Secrets: none. Real data: none. Claims: none.
