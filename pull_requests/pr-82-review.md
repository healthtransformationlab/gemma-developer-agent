# PR 82 review: cost in the README, what it means for decisions, and the performance work that comes next (#81)

| Check | Result |
|---|---|
| Branch `docs/81-cost-and-decisions`, `Closes #81` | ok |
| Merge: the owner asked on November 12, 2026 for clearer cost information, its implication for decisions and a mention of future work on performance optimisation, and said "Merge" for the paper's pull requests on November 11. The README is the page the paper links to. Merging starts no run and publishes nothing outside this repository | ok |
| The paper, its PDF and `paper/sources.md` are not in the diff. The run table and the bullets under it are unchanged | ok |
| Every figure in the new table, recomputed for this review from the source repository's `_gpu.csv` tables at `526ea08`, the commit the README already cites. GPU-hours for the run: 1.96, 1.87 and 2.01 on one A100; 3.62 and 3.30 on one L4; 7.67 and 9.04 on four L4s. Estimated rental: 3.66, 3.50 and 3.76; 3.01 and 2.74; 6.37 and 7.50. For each task fixed: 0.91, 0.58 and 0.94; 0.60 and 0.34; 1.59 and 1.50. The four-L4 row is the two arms that ran all 93 tasks; the baseline arm there ran 21 | ok |
| The prices are the declared ones: 0.83 US dollars an L4-hour and 1.87 an A100-hour, medians read from a public listing (`ops/cost_settings.yaml` in the source repository, which also gives the weekly allowance of about 30 hours) | ok |
| The section says the rental figures are estimates and not money spent, twice: above the table and under it. No dollar sign is used: GitHub can take text between two of them for a formula | ok |
| It says what limits the comparison of machines: each ran in its own session, with its own software versions, once for each arm, and a run fixed between 4 and 8 tasks. "Rent one GPU, not four" is said of these runs, and the list of work to come has the run that would confirm it: the same tasks on one GPU and on four under the same software | ok |
| The other numbers were already in the README: 1.2 to 1.5 minutes a task on four L4s and 1.2 to 1.3 on the A100, the tokens read and written (its run table); 66–83%, 14–15%, under 0.1% and 45 of 207 (the three Kaggle arms, and the section says so); the first baseline's 13 tasks, 17%, 4 of 5, and 0.38 against 1.80 hours | ok |
| "It reads roughly twenty times what it writes": the run table's evaluator rows give between 17 and 22 times | ok |
| The performance work is under "None of this has been done or measured yet", and each item is a thing to try or to measure, not a result | ok |
| The deck's cost slide gives the same three machines, shares and decisions; `python docs/build_decks.py --check` exits 0, so each number on it appears in the README or the paper; the slide was rendered and looked at | ok |
| All links resolve, the two new ones to the source repository included. The section was rendered at phone width, where the table first ran off the side and was made narrower | ok |
| No first person, secrets, real data or organisation names | ok |

Nothing blocking.

## Notes
- The paper gives the four-L4 runs' cost and says nothing of the Colab machines' ("the paper gives no cost for
  them", `paper/sources.md`). The README now sets the three machines side by side. That is more than the paper says,
  from the same tables, and it is labelled as what these runs took and not as a benchmark of the machines.
- "Rent one GPU, not four" is the plainest reading of one session on each machine. It could be wrong for another
  serving setup: the four L4s ran one model across all four cards, and nobody tried four copies of it side by side.
  The list of work to come says so in its own way.
- The cost of a fix divides by 4 to 8 fixed tasks. One fix more or fewer moves it by a fifth or more, which is why
  the section gives ranges and says they move.
