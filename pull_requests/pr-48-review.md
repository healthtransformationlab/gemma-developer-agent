# PR 48 review: say how the 48 were sampled wherever the 5 of 48 appears; three points from a fourth review (#47)

| Check | Result |
|---|---|
| Branch `docs/47-...`, `Closes #47` | ok |
| Held for the owner: the abstract changes | held |
| The abstract gives the interval beside 5 of 48 (4.5 to 22.2%, the Wilson interval already in Section 6) and says the graph-tool calls are over three runs | ok |
| Section 6 says no rate here is an unbiased estimate for the 93; the conclusion says "cheapest-first" | ok |
| The larger-budget sentence, which one review found confusing, now reads "with eight times the output budget it resolved 2 of the 23 cheapest tasks, against 2 before" | ok |
| Section 4.3: "It misses the fix in 42 of the 93 tasks": 31 + 11 = 42, and 42 + 51 = 93 | ok |
| Section 7 says the cloud agent was not rerun on the statements alone, which is the honest answer to a review's point that the title's comparison has no cloud baseline | ok |
| `sources.md`: the second screen rates the statement 2 or 3 in 19 tasks, not 20 (one rating was lowered by its rater before it finished; no verdict changed) | ok |
| Not taken from the reviews, with reasons in `sources.md`: a new title, "Overfitting risk" as a heading, a claim that SWE-bench's screening skews outcomes | ok |
| No number changes; no first person | ok |
| Word count: 2,812 before the references (2,810 before); the pasted text with its references is 2,976 | ok |
| `check_rules.py --check` exits 0: 15 rows PASS, none FAIL | ok |
| PDF rebuilt: 6 pages, Figure 1 on page 1 | ok |
| No secrets, no real data, no organisation names | ok |

## Notes
- Four reviews by other models, all with the same strict prompt, scored the paper 3.2 and 3.0 before today's
  additions and 3.1 and 3.2 after. Verifiability rose (3.0 and 3.5 to 4.0 and 4.5); novelty and quality did not
  move, and what holds them down is not wording: one repository, a known mining recipe, small samples.

## Blocking
None. Waits for the owner's "merge".
