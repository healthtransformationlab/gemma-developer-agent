# PR 67 review: the paper gives the L4 runs' cost in dollars (#66)

| Check | Result |
|---|---|
| Branch `docs/66-l4-dollars`, `Closes #66` | ok |
| Merge: the owner asked for the dollar costs by adding the price source to the session's network on November 11, 2026, and had said "Merge" for the paper's pull requests that day. Merging starts no run and publishes nothing; the Writeup needs pasting again after it | ok |
| The clause, "about 1.59 and 1.50 US dollars at a median rental of 0.83 an L4-hour", against `NLP` at its pull request 683: `estimated_cost_usd` sums to 6.37 over the `graph` arm's 93 rows and 7.50 over the `report` arm's; 6.37 / 4 = 1.59 and 7.50 / 5 = 1.50. Recomputed from the rebuilt tables for this review | ok |
| The price: `l4_usd_per_gpu_hour` 0.83 in `NLP/ops/cost_settings.yaml`, the median on-demand price across providers for the week of October 26, 2026 in the source's weekly series (0.8319 over 14 providers), the same week and figure as the T4's 0.69 (0.691 over 10) | ok |
| Estimates, and said to be: "about", and "(Kaggle's were free)" closes the paragraph for both GPUs. `sources.md` says the estimate covers the tasks' own time, not the model's loading or the hours one kernel ran with a dead server | ok |
| No amount in the paper carries a dollar sign: six amounts in one paragraph would give a page that renders mathematics three pairs of dollar signs to read as formulas. The PDF's text holds none either | ok |
| The count does not go up: the pasted text is 2,682 words before the references and 2,902 with them (2,679 and 2,899 before this change; the three words are "US dollars" and "dollars"). Four short trims made the room: "a median rental of" before the T4's price, "of them" after 240, and three pointers to sections | ok |
| The abstract is unchanged (223 words); Figure 1 is unchanged and on page 1; the PDF is 6 pages | ok |
| `check_rules.py --check` exits 0; every quoted phrase in `paper/sources.md` is in the paper (100 of 100) | ok |
| The README's cost line gives the same two amounts and says they are estimates; its link to the experiment's tables is at the source repository's commit that holds the filled cost column | ok |
| No first person, secrets, real data or organisation names | ok |

Nothing blocking.

## Notes
- The T4 and L4 prices are for one week of one source, so the two estimates can be set side by side. The source's
  figure for the week of November 9 is lower for a T4 (0.59) and about the same for an L4 (0.84). Moving both is a
  change to the source repository's settings, and would move the T4 amounts the paper already gives.
- The text pasted into the Writeup before this change had three dollar signs in one sentence. If the Writeup's page
  renders mathematics, that sentence may have shown as a formula; the new text has none.
