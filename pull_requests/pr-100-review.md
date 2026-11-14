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
