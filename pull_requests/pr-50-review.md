# PR 50 review: the recipe is the competition's own; this repository sits beside its four (#49)

| Check | Result |
|---|---|
| Branch `docs/49-fifth-repository`, `Closes #49` | ok |
| Held for the owner: the abstract changes by one sentence | held |
| The abstract says the tasks are "made the way the competition's own are: its mining rule, its format, its evaluator on every task" | ok |
| Section 1: "This paper adds one repository that is both, set beside the competition's four by the competition's mining rule, format and evaluator" | ok |
| Section 7's first bullet says what is shared with the competition's four (rule, format, evaluator) and what was run on this repository alone (the screens, the graph counts) | ok |
| The conclusion's recipe separates the competition's steps from the four this paper adds | ok |
| Nothing says the set is part of the competition's data: "beside", "made the way", never "in" or "official" | ok |
| "Four" is the count Section 1 already gave for the competition's development set; no new number | ok |
| Still stated: one author's set, cheapest-first sample, no rate an unbiased estimate, the 133 second-repository candidates not gated or released (Section 4.5) | ok |
| Four wording fixes from reviews: "unlicensed third-party files"; "The model made only 6 graph-tool calls among 145, in 4 of the 23 runs" (the denominator stays: the abstract's 473 is its sum with two others); "Ten of the 58 tasks attempted were excluded from the set (Section 5)"; Section 4.3 says how chance is worked out (each graph's nodes ranked at random, hypergeometric, summed over tasks), which is what `chance_top` in the source repository's `64_statement_search.py` computes | ok |
| Cut to keep the count flat, each listed in `sources.md`: the larger-budget paragraph's sentence on output tokens and the context limit, "it reads and edits files and rarely searches", "of issues, pull requests and reviews" in the abstract | ok |
| Word count: 2,800 before the references (2,800 before); the pasted text with its references is 2,964; the abstract is 229 words | ok |
| `check_rules.py --check` exits 0: 15 rows PASS, none FAIL | ok |
| PDF rebuilt: 6 pages, Figure 1 on page 1 | ok |
| No first person, no secrets, no real data, no organisation names | ok |

## Not taken

From the same day's review by another model, with reasons: dropping "(first ten results)" from the abstract (the
42 of 51 depends on it); "What fraction of this loop's changes can a small local model resolve unattended?" (the
paper says no rate here is an unbiased estimate, so it should not promise a fraction); shortening the sentence on
silent defects (it is the point of the domain).

Nothing blocking. Held for the owner's "merge".
