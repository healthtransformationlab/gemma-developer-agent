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
- Measured on November 14, 2026, with the owner's go-ahead: the competition's evaluator end to end on the 23
  development tasks that pass both controls (seed 20261110), one Kaggle kernel on four L4 GPUs, the same settings as
  the November 11 baseline. Resolved 4 of 23 (old prompt 3 of 23); both resolved `fastapi_14301` and `rich_3454`,
  only this prompt `fastapi_14873` and `rich_3905`, only the old one `rich_3535`; exact McNemar p = 1.0, so no
  difference can be claimed. Empty patches fell from 5 to 2; 21 of 23 runs started with `run_command`, 17 of them
  the localization grep; no skill calls. The rows are recorded in health-transformation-lab-nlp's official agent runs.
- The grep example's placeholder was copied in none of the 23 runs' first calls.
- Draft PR #60 also edits `prompts/system.md`; whichever merges second needs a small merge.
