# PR 63 review: say what a failing test's report adds to what the graph can tell the agent (#61)

| Check | Result |
|---|---|
| Branch `docs/61-failing-test-report`, `Closes #61` | ok |
| Merge: the owner asked for issue 61 to be done and said "merge" for the paper update on November 11, 2026; the Writeup needs pasting again after it | ok |
| Section 4.3's new paragraph against `NLP/data/tasks/trace_reach.csv` (51 rows), joined to `graph_coverage.csv` and `statement_search.csv`: an edited function among those called in 23, median 7 public functions called, 1 of the 23 outside the 42 the statement reaches; 15 import errors, 13 naming a module the fix changes, 5 of those outside the 42; 42 + 1 + 5 = 48. Recomputed for this review; the script's own summary prints the same split since `NLP` pull request 673 | ok |
| The split is the corrected one: the review of `NLP` pull request 671 had credited all 6 tasks to the functions called, and issue 61's comment caught it. The paper says "report", and gives the two parts | ok |
| "which its OpenTelemetry spans would record": every public function in the package is `@traced`; `sources.md` says the functions were recorded by a profiler, not read from exported spans | ok |
| The paragraph says the report uses the hidden test and is not a benchmark condition; `sources.md` adds that no agent run had it | ok |
| Issue 61 asked for the paragraph in Section 4.3: it follows the graph counts there | ok |
| The dollars: 1.53 × 2 × 0.69 / 4 = 0.53, 1.82 × 2 × 0.69 / 3 = 0.84, 9.01 × 2 × 0.69 / 5 = 2.49, from `screen_routing.csv`, `cost_by_graph_reach.csv` and `NLP/ops/cost_settings.yaml` (a median T4 rental, read November 4, 2026). Labelled "about", and the text says Kaggle's GPUs were free | ok |
| The dollars price the agent's own time only, not model loading or notebook start-up; `sources.md` says so, the paper does not | note |
| Cuts to keep the count flat are listed in the change log at the end of `sources.md`; none removes a number that another sentence depends on. "`PYTHONSAFEPATH` unset" stays in the known differences | ok |
| Word count: 2,808 before the references by the rules check (2,812 before); the pasted text is 2,758 before the references and 2,972 with them | ok |
| The abstract is unchanged (232 words); Figure 1 stays on page 1; the PDF is 6 pages | ok |
| `check_rules.py --check` exits 0: no row fails | ok |
| No first person, secrets, real data or organisation names | ok |

Nothing blocking.

## Notes
- The paragraph counts where the report points. Whether a model does better when given the report is a run, not a
  count, and has not been made.
- A pull request for issue 62 (the competition's development set beside this set) follows and will rebuild the PDF
  again.
