# PR 58 review: say how many tests the source repository has (#57)

| Check | Result |
|---|---|
| Branch `docs/57-test-count`, `Closes #57` | ok |
| Held for the owner: the abstract changes, and the Writeup is already submitted, so it needs pasting again | held |
| The abstract's first sentence: "960 commits (775 marked as agent-authored) and 2,269 tests, without typing code" | ok |
| Section 3: "On November 8 it held 2,269 tests in 126 files, run by CI on every pull request." | ok |
| The count is at the same cut-off as the 960 commits: `b12e2e0`, where `git rev-list --count` reaches 960; `pytest --collect-only -q tests` collects 2,269 there (1,547 test functions, 126 files). At `254c44c`, the commit the analyses use, it is 2,355 in 133 files; `sources.md` gives both | ok |
| "run by CI on every pull request": `NLP/.github/workflows/ci.yml` runs on every pull request and every push to `main`; `sources.md` says its R parity job runs when a changed file can reach it | ok |
| Cut to keep the count flat: "and its embeddings" in Related work, "public under CC BY 4.0" in the first contribution (the licence is in the Data and code line), "which Kaggle's notebooks did not" in Section 6 (its Setup says Kaggle ran with internet off) | ok |
| Word count: 2,812 before the references by the rules check (2,805 before); the pasted text is 2,762 before the references and 2,976 with them | ok |
| The abstract is 232 words; Figure 1 stays on page 1; the PDF is 6 pages | ok |
| `check_rules.py --check` exits 0: 15 rows PASS, none FAIL | ok |
| No other number changes; no first person, secrets, real data or organisation names | ok |

Nothing blocking. Held for the owner's "merge".
