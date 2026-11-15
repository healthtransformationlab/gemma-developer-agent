# PR 135 review: untrack the compiled .pyc under paper/

Closes #134. Reviewed against `.conventions/AGENTS-common.md` and `AGENTS.md`.

- **Change:** removes one tracked `.pyc` from the index; adds `tests/test_no_compiled_files.py` over `git ls-files`.
- **Test first:** the new test failed with the file tracked, passes without it. Full suite: 78 passed, 1 skipped.
- **Submission:** none of `agent.yaml`, `prompts/`, `sub_agents/`, `configs/`, `eval_config.yaml`, `skills/` changes; the
  queued zips are unaffected (they were already free of compiled files).
- **Rules:** no GPU, no submission, no rule change: an agent may merge it when green.

Nothing blocking.
