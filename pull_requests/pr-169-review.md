# PR 169 review: find.py and the agent's tests in use, from the Kaggle E4B-all run (#168)

| Check | Result |
|---|---|
| Branch `docs/168-find-and-tests-in-use`, `Closes #168`, issue with its four parts before the first commit | ok |
| Test first: `tests/test_devset_traces.py` failed on import before `analysis/devset_traces.py` existed | ok |
| No competition data committed: the CSVs hold ids, codes and counts; the traces stay out of the repository | ok |
| Every number in the new study section comes from `devset_e4b_all_k.csv`, `find_ranks.csv` or `find_ranks_docs_src_as_code.csv` | ok; recomputed |
| Mechanism, not effect: one run of 23 tasks; the rank and resolve link is called association | ok |

## Findings

None blocking.

- **Noted.** `is_test_file_run` counts a pytest call whose arguments name `tests/…` or `test_*.py`, so a call naming
  an unrelated test file also counts. With only 4 such calls in 23 tasks, it can't have inflated the finding.
- **Noted.** The `docs_src/` comparison ran on CPU against `find_eval.py`'s extracted names, not the model's own names.
  That's the same basis as the committed `find_ranks.csv`.

## Verdict

Approve. It changes no submission file and starts no run. Merge when the checks are green.
