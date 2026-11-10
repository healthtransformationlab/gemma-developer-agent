# PR 42 review: lead the paper with its findings; add the larger budget and the graph result (#41)

| Check | Result |
|---|---|
| Branch `docs/41-...`, `Closes #41` | ok |
| Held for the owner: the abstract and the results change | held |
| Every number in the paper has a row in `sources.md`; the new ones (larger budget, graph reach, two references) read row by row | ok |
| The larger-budget figures are filled by a script from the run table, not typed: 2 of 23 against 2, a patch for 20 against 19, 5 of 139 tool calls to a graph tool, one run above 2,048 output tokens, one at the context limit | ok |
| The run was still going: the paper says "the 23 cheapest of the 48", in the abstract, Section 6 and the conclusion | ok |
| 20 of 473 tool calls = 6 of 145 + 5 of 139 + 9 of 189 | ok |
| Graph reach: 31 + 11 + 51 = 93; 20 + 2 + 29 = 51; 22 of 93 = 20 + 2. Two separately written implementations agree on all 93 tasks (`health-transformation-lab-nlp` pull request 660) | ok |
| "Names" is defined in the text ("by its identifier") and as a rule in `sources.md`; embedding search is said to be untested | ok |
| The two new references checked against their abstracts (ICLR 2025, ACL 2025) | ok |
| No number is presented as a competition score; the harness and the evaluator are named apart | ok |
| Word count: 2,805 before the references by the rules check; 2,971 for the pasted text with its references | ok |
| `check_rules.py --check` exits 0: 15 rows PASS, none FAIL; rows the files cannot show are OWNER | ok |
| PDF rebuilt by `build_pdf.js`: 6 pages, each read by eye; the new sentences are in its text | ok |
| No private Kaggle resource is named in the paper (a rules-check row) | ok |
| No secrets, no real data, no organisation names | ok |

## Notes
- Every cut is listed under "Not in the writeup" in `sources.md`. None removes a result; the largest are the former
  Section 7 and a related-work paragraph on health-data quality.
- The larger budget was run on the cheapest tasks first, so "2 against 2" says the tight limits did not decide the
  result on those; it says nothing about the dearer tasks. The paper's wording keeps to that.
- The graph counts read "names" by a fixed rule, so they are lower bounds on what a reader of a statement could
  work out. The paper says "names", not "could find".
- `sources.md` cites `health-transformation-lab-nlp` pull requests 660 and 661; both need to be merged for its
  paths to resolve on `main`.

## Blocking
None. Waits for the owner's "merge".
