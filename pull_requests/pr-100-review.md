# PR 100 review: keep a quarter of the context window for output, not half (#99)

| Check | Result |
|---|---|
| Branch `fix/99-context-window-output-reservation`, `Closes #99`; issue 99 has its Problem, Done when, Contract and Read first | ok |
| Test first: `tests/test_sampling.py` was written before the config changed and failed on 16,384 (input room 16,384 < 24,576); its 3 tests pass on 8,192 | ok |
| The counts in the issue and description are committed ones: 45 of 207 (`paper/sources.md`, from the three run tables) and 8 of 40 (`gemma-4-e4b-it-qat-w4a16-ct_swegemma_devset.csv` in `health-transformation-lab-nlp`, `error_text` holding `ContextWindowExceededError`); the 8 task ids were read from that table | ok |
| The window is the server's 32,768 tokens (`paper/sources.md`; `build_submission_limits` in `swegemma/config.py` bounds `max_output_tokens` to 1–32,768, so 8,192 is accepted) | ok |
| `adk_submission.validate_directory` on `agent.yaml`, `eval_config.yaml`, `prompts`, `sub_agents`, `configs`, `skills`: passes | ok |
| Only `configs/sampling.yaml`, `docs/rulebook-notes.md` and a new test change; no file that PR 98 or draft PR 60 changes, so the three merge in any order | ok |
| `paper/check_rules.py --check` exits 0; the paper and its sources are untouched | ok |
| Every submission file keeps an allowed extension; the test sits in `tests/`, outside the agent's bundle | ok |
| No secrets, real data or organisation names | ok |

Nothing blocking. Held as a draft until it is measured.

## Notes
- Unmeasured. Halving the output room could cut a long `write_file` short (with 2,048 tokens, edits were cut off in
  the first runs); 4,096 after thinking is twice that, but only a run can say whether more patches are lost to it
  than are saved from the window. Compare with 16,384 on the same tasks, after PR 98's run, so the two changes are
  not mixed.
- `compile_submission` was not run here: it needs the evaluator's tool and model registries. The value is checked
  only against the range above, which the source shows.
- The evaluator also puts a tree of `/workspace` into the prompt; on large repositories that is part of what fills
  the window. Not changed here.
- No workflow runs `tests/` on this repository until PR 98 adds `submission-check.yml`; until then the test is run by
  hand.

## Measured 2026-11-15
- The run the notes asked for was made on November 14 with the owner's approval: this branch's agent (before `main`
  was merged in) on the same 23 verifiable development tasks as the November 11 run, under the competition's
  evaluator, one Kaggle kernel on four L4 GPUs. Record: `health-transformation-lab-nlp` pull request 745,
  `data/tasks/official_agent_runs/gemma-4-e4b-it-qat-w4a16-ct_swegemma_devset-max-output-8192.csv`.
- Resolved 3 against 3 (one gained, one lost; exact McNemar p = 1.0): no change in resolved tasks is claimed.
- Ended at the context window: 0 against 3. One call's prompt was 17,155 tokens (`rich_3930`), which 16,384 would have
  refused.
- The worry in the first note did not happen: the largest of 418 answers was 4,813 tokens and none reached 8,000.
- `main` (pull request 98's prompt and its `submission-check.yml`) merged in without conflict; 9 tests pass, the
  competition's `validate_directory` passes, `paper/check_rules.py --check` exits 0. The two changes together are not
  measured.

Nothing blocking. Ready to merge once the record (`health-transformation-lab-nlp` pull request 745) is on its `main`.
