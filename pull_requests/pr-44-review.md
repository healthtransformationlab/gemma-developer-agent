# PR 44 review: lead the abstract with the fifteen days of commits; frame it by what can leave the loop (#43)

| Check | Result |
|---|---|
| Branch `docs/43-...`, `Closes #43` | ok |
| Held for the owner: the abstract changes (each change here is one the owner asked for) | held |
| The lead's figures each have a row in `sources.md`: fifteen days (October 25 to November 8, 2026, both ends counted), 960 commits, 775 marked as agent-authored (710 + 65) | ok |
| "from nothing to 960 commits": the first commit is GitHub's initial commit of October 25; 960 counts every commit on `main`, and the sentence gives the 775 beside it, so merges and bot commits are not passed off as the agent's | ok |
| "without typing code": the four commits by the owner alone are three documentation edits and one merge | ok |
| "a record of issues, pull requests and reviews": says what the record holds, not that every change has all three (the issue rule was adopted partway through, Section 4.2) | ok |
| The three headings in bold are a reading, and `sources.md` says so; under each heading the figures are the measured ones, unchanged: 5 of 48, 2 of 23 against 2, 0 of 20, 25 of 30, 22 of 93, 20 of 473 | ok |
| "Some small upkeep can leave it" says "some": five small tasks were resolved, not small tasks in general | ok |
| No claim is left about who maintains other benchmarks' sources; none was measured | ok |
| No first person is left in the paper (checked by a search for "I", "my", "me") | ok |
| No result changes | ok |
| Word count does not grow: 2,803 before the references (2,805 before this pull request); the pasted text with its references is 2,969 | ok |
| `check_rules.py --check` exits 0: 15 rows PASS, none FAIL | ok |
| PDF rebuilt: 6 pages, page 1 read by eye, the new abstract is in its text | ok |
| No secrets, no real data, no organisation names | ok |

## Notes
- The framing (what can leave a person's loop, and what the person gains for the rest) is the owner's. The paper
  does not measure what organisations want; it reports what one model resolved unattended and what the task set
  records. The abstract keeps to that.
- Cut to make room, each listed in `sources.md`: the masking-defect example in Section 1, the dollar estimate in
  Section 6, the conclusion's sentence on whether graphs help, and several short phrases.
- "The rest stays with a person" rests on small samples (48 tasks cheapest first, a random 20). Section 7 says so.

## Blocking
None. Waits for the owner's "merge".
