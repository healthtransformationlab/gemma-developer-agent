# PR 98 review: localize first and give edit_file's arguments, for any repository (#97)

| Check | Result |
|---|---|
| Branch `fix/97-prompt-localize-first-edit-args`, `Closes #97` | ok |
| Test first: `tests/test_submission.py` was written before the prompt changed and failed on the old prompt (3 failed: no localization step, conventions read unconditionally, `edit_file`'s arguments not named); 6 pass on the new one | ok |
| `edit_file`'s arguments (`filepath`, `old_string`, `new_string`, `allow_multiple`) match the tool declaration as reproduced in `health-transformation-lab-nlp/python/health_transformation_lab_nlp/agent_harness.py` | ok |
| The localization command uses only `ls` and `grep` inside `/workspace`, which every task sandbox has; no network, no `pip install`, nothing written to `/workspace` | ok |
| Conventions files and `pipeline-doctor` are still used on repositories that have them (this repository's own DataOps tasks), only not on every task | ok |
| No change to the model, tools, budgets (`eval_config.yaml`) or sampling (`configs/sampling.yaml`); the prompt keeps `{problem_description}` and `{hints?}` | ok |
| Every submission file has an allowed extension; the new test sits in `tests/`, outside the agent's bundle | ok |
| CI: the new workflow pins `pytest` and `pyyaml` and runs only on changes to the submission or the test | ok |
| No secrets, real data or organisation names | ok |

Nothing blocking.

## Notes
- Unmeasured: no evaluation was run. Whether this raises the score needs a GPU run on the public development set,
  compared with the current prompt over repeated runs, since leaderboard noise is about ±0.03–0.04. The owner
  approves each GPU run.
- The grep example could be copied literally by a small model; the prompt says to put the issue's own strings in
  place of the placeholder. Worth checking in the first run's traces.
- Draft PR #60 also edits `prompts/system.md`; whichever merges second needs a small merge.
