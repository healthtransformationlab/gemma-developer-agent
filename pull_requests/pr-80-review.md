# PR 80 review: each headline result in the README on its own row, with what it means (#79)

| Check | Result |
|---|---|
| Branch `docs/79-readme-results-plain`, `Closes #79` | ok |
| Merge: the owner quoted the README's second result on November 12, 2026 and said it was hard to understand. The README is the page the paper links to, and the owner said "Merge" for the paper's pull requests on November 11. Merging starts no run and publishes nothing outside this repository | ok |
| The diff is the top of `README.md` only. The run table, its bullets and the folded sections are unchanged, so the README still keeps what `paper/sources.md` says it keeps | ok |
| No number changes, and none is added or dropped. Each one in the new section, read against the paper: 5 of 48 (10.4%, 95% CI 4.5–22.2), "cheapest first under a GPU-hour cap, so no rate here estimates the 93"; 4, 6 and 4 of 93 on one A100 with exact McNemar p = 0.5 and 1.0; 17 of 93 in the core split; 8 of 17 and 1 of 76 resolved in some of the five Colab runs | ok |
| The labels that keep the results honest are all still there, in plain words: "no difference detected"; the failing test's report "comes from the hidden test, so a benchmark would not give it"; "counts of what happened, not a planned test"; and the line on one model, one repository and an AI screen checked in part, with its link to the limits | ok |
| "Extra help showed no reliable improvement" is the wording the second reader of pull request 76 asked for in place of a stronger one | ok |
| "Counting the three runs above and two more from an unplanned second session" says which five runs the 8 of 17 and 1 of 76 cover, and that two of them were not planned | ok |
| The 5 of 48 keeps its interval beside it; the experiment's three counts have theirs in the run table below, which the section links | ok |
| `python docs/build_decks.py --check` exits 0; all 47 links in the README resolve; the section was rendered at phone width and looked at | ok |
| No first person outside the disclaimer, no secrets, no real data | ok |

Nothing blocking.

## Notes
- The sentence the owner quoted was written an hour earlier in the day to answer the same owner's request that
  titles say what their numbers mean. It put the meaning after the numbers and kept all three in one sentence. A
  list of numbers followed by a list of meanings is the pattern to avoid: one row for each.
- The paper's abstract gives the same three counts in one sentence ("it resolved 4 of 93 as published, 6 with graph
  retrieval and 4 with a failing test's report"), where each count sits beside its condition. It is left as it is.
