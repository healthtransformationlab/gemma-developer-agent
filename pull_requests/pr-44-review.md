# PR 44 review: lead the abstract with the fifteen days of commits (#43)

| Check | Result |
|---|---|
| Branch `docs/43-...`, `Closes #43` | ok |
| Held for the owner: the abstract changes (the owner asked for this lead) | held |
| The lead's figures each have a row in `sources.md`: fifteen days (October 25 to November 8, 2026, both ends counted), 960 commits, 775 marked as agent-authored (710 + 65) | ok |
| "took a health-data repository from nothing to 960 commits": the first commit is GitHub's initial commit of October 25; 960 counts every commit on `main`, and the sentence gives the 775 beside it, so merges and bot commits are not passed off as the agent's | ok |
| "I typed no code": the four commits by the owner alone are three documentation edits and one merge | ok |
| No result changes; the four findings and every number after the lead are as merged in pull request 42 | ok |
| Word count does not grow: 2,806 before the references (2,805 before); the pasted text with its references is 2,972 | ok |
| `check_rules.py --check` exits 0: 15 rows PASS, none FAIL | ok |
| PDF rebuilt: 6 pages, page 1 read by eye, the lead is in its text | ok |
| No secrets, no real data, no organisation names | ok |

## Notes
- The claim that existing benchmarks come from human-maintained libraries is now one clause; Section 1 and Section 2
  still carry it in full.
- Section 5 loses "Elsewhere the two verifiers agree on every reference patch". The table beside it gives the
  counts, and the paragraph above lists the 20 tasks where they differ or both fail.

## Blocking
None. Waits for the owner's "merge".
