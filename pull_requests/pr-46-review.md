# PR 46 review: answer two reviews of the paper; add the embedding search, the cost split and the full screen (#45)

| Check | Result |
|---|---|
| Branch `docs/45-...`, `Closes #45` | ok |
| Held for the owner: the abstract and the results change | held |
| The abstract's headings no longer claim: "What it did unattended", "What stayed in the loop", "What the person in the loop can now see" only sort the results. Both reviews had named the earlier headings as the paper's costliest sentences | ok |
| The abstract says the 48 were run cheapest first and that the five resolved were all small | ok |
| Embedding search (Section 4.3): an edited node in the first ten for 20 of the 29 tasks names and call edges miss, and for 30 of the 51; from `health-transformation-lab-nlp` pull request 663, run twice from separate code with the same ranks; called a count from the published files, not an agent run | ok |
| 22 + 20 = 42 tasks where a name, a call edge or embedding search leads to the fix; the abstract gives the two numbers, not a sum | ok |
| Cost by graph reach (Section 6): 20%, 43%, 20% and 17% add to 100; 12 + 19 + 9 + 8 = 48 runs; 3 + 2 + 0 + 0 = 5 resolved; cost is the agent's own time, which every run records | ok |
| The second screen (Section 6): all 93, 17 pass; the same verdict as the first on all 30 the owner checked; 26 tasks rated twice agree; from pull request 665. The paper calls both screens AI screens and says a person checked 30 | ok |
| "4 of the 13 that pass and 1 of the 35 that fail": 13 + 35 = 48, 4 + 1 = 5 | ok |
| What the tasks are and how they are made (application work in health data; every step a script; the competition's format): each has a row in `sources.md`, and the row on the scripts says rebuilding on later history has not been done | ok |
| No claim of being first; the recipe is said to have been run in full on one repository only | ok |
| No number changes from earlier runs; no first person; no claim about who maintains other benchmarks | ok |
| Word count: 2,810 before the references (2,803 on `main`); the pasted text with its references is 2,974 | ok |
| `check_rules.py --check` exits 0: 15 rows PASS, none FAIL. The row for rule 3.4.b now looks for the reworded screening sentence | ok |
| PDF rebuilt: 6 pages, all read by eye, Figure 1 on page 1 | ok |
| No secrets, no real data, no organisation names | ok |

## Notes
- Figure 1 still shows the first screen's 30 tasks, as its caption says. The second screen's 93 are in Section 6.
- What the reviews marked down and this cannot change: one repository, small samples, and screens made by AI
  reviewers. Section 7 states each.
- `sources.md` cites `health-transformation-lab-nlp` pull requests 663 and 665; both need to be merged for its paths
  to resolve on `main`.
- Cut to make room, each listed in `sources.md`: the paired rerun's table, the prompt-defect sentence, the dollar
  estimate, several clauses in Sections 1, 4.5, 5 and 6, and the abstract's examples of the five resolved tasks.

## Blocking
None. Waits for the owner's "merge".
