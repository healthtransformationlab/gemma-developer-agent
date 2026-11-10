# PR 52 review: three wording fixes from a review (#51)

| Check | Result |
|---|---|
| Branch `docs/51-review-wording-fixes`, `Closes #51` | ok |
| Held for the owner: the Writeup is being submitted today, and the repository's copy should match what is submitted | held |
| Section 1: "so its tasks are real changes to application code". A review read the set as "heavily synthesized"; the patient records are synthetic, the tasks are merged changes | ok |
| Section 6: "An independent second pass, blind to the first, rated all 93: the same verdict on all 30, and 17 of 93 pass." The old sentence had a stray semicolon before "Each" | ok |
| Section 4.5: "Gating and releasing them is future work." The same fact as "The 133 are not gated or released": they are still neither | ok |
| No number changes; the abstract is untouched (229 words) | ok |
| Word count: 2,799 before the references (2,800 before); the pasted text with its references is 2,963 | ok |
| `check_rules.py --check` exits 0: 15 rows PASS, none FAIL | ok |
| PDF rebuilt: 6 pages, Figure 1 on page 1 | ok |
| No first person, no secrets, no real data, no organisation names | ok |

## Not taken, with reasons

- "All five resolved tasks required trivial configuration or string edits": one of the five is a label parser.
- "This isolates the boundary between local agent capabilities and human intervention": a cheapest-first sample
  of 48 does not isolate a boundary, and the paper says so.
- "Data repositories expose critical coverage gaps in standard AST graphs": one repository.
- "the 10.4% rate is a lower-bound estimate": cheapest-first tasks are more likely easier than harder, so the
  rate is not a lower bound. "No rate here is an unbiased estimate" stays.
- "computed on the released graphs before any agent run": the counts were made after the runs.
- A longer question in the abstract: the abstract is at the length that keeps Figure 1 on page 1.

Nothing blocking. Held for the owner's "merge".
