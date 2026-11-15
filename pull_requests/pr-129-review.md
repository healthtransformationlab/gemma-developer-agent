# PR 129 review: name each entry's repository and branch in the leaderboard plan (#128)

| Check | Result |
|---|---|
| Branch `docs/128-plan-repo-branch`, `Closes #128`, issue with its four parts first | ok |
| Test first: `test_every_queued_entry_names_its_repository_and_branch` failed, then passed; 74 pass | ok |
| A `Code` column links each entry's commit and branch (`main`, or `feat/122-skill-on-copyfix`, `feat/124-31b-entry`, `feat/125-distilled-adapter`); every row has 11 cells | ok |
| Evidence links name their repository (this one's studies, health-transformation-lab-nlp's ledger, dev-set tables and ADR 0007) | ok |
| Docs only; not part of the submission | ok |

Nothing blocking. Merge when CI is green.
