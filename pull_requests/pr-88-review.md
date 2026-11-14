# PR 88 review: the paper says its main result plainly where a reader looks first (#87)

| Check | Result |
|---|---|
| Branch `docs/87-main-result-plain`, `Closes #87` | ok |
| Merge: the owner said "Merge" for the paper's pull requests on November 11, 2026, and on November 12 asked whether the paper's most important content was as clear as the pitch deck's. Merging starts no run and publishes nothing; the Writeup needs pasting again after it, and the PDF swapping | ok |
| The diff of the paper's text, read word by word. Abstract: the question is the title's; the lead-ins are "Alone,", "The code graph", "With more context," and "The main result (described, not tested):"; the last sentence gives the size of the fixes. Section 1: a fourth contribution names the result. Section 6: the result has its own paragraph, led by "The main result.", with the three registered runs alone, one plain sentence and the size of the fixes. Section 8: one long sentence is two, and the last names the runtime work that comes next | ok |
| A second reader, given the diff and the run tables and not the author's view of them, recounted from the five Colab tables, `core_split.csv` and `context_pairs_colab_graph.csv` in the source repository: 8 of 17 and 1 of 76 distinct tasks; 26 of 85 and 1 of 380 task-runs; 41 tasks where the retrieval listed an edited node, 7 in the core split and 34 outside it, 5 of the 7 and none of the 34 resolved; 3 installers in 687 commands; 66.3, 76.5 and 82.8% of time in model calls on the three Kaggle arms. Every number in a changed sentence agreed | ok |
| The reader's findings on the first commit, each made in the second. (1) The core split is also a split by size, and the paper did not say so: Section 6 and the abstract now do. (2) "The main result" stood in the abstract without "described, not tested", and pooled the registered session with the unplanned one: the label is in the abstract, and Section 6 gives the three registered runs alone. (3) Cutting who made the other commits left "without typing code" unsupported: Section 3 keeps the 175 merge commits. (4) Section 4.3 used "a failing test's report" before saying what it is: the bracket moved there from Section 6. (5) "On free T4 GPUs" read as covering the run under the competition's evaluator, which used four L4s: it now follows the 48 tasks that ran on T4s | ok |
| The new counts, recounted for this review from the source repository's tables. Registered runs alone (`colab-statement`, `colab-graph`, `colab-report`): 6 of the 17 and none of the 76. Files changed by the reference patch (`graph_coverage.csv`, `changed_file_count`): core split median 2 (1 to 11), others median 10.5 (1 to 65). 53 tasks have a fix of more than 5 files and none was resolved in any of the five runs. At 5 files or fewer: 8 of 12 in the core split, 1 of 28 outside it; the same direction at every cut-off from 1 to 11 files | ok |
| The size counts are labelled "post hoc" in both places, and `paper/sources.md` says the cut-off of 5 was chosen after seeing the results and that the count does not say why a task went unresolved | ok |
| Nothing a cut removed is relied on elsewhere: no "those three" is left; "48 of the 51" stays in Section 4.3; "(114 of 129 ...)" stays in the Section 6 table; the T4 baseline's cost by core split is in the README, which the pitch deck's cost slide cites | ok |
| `paper/sources.md`: a row for each new sentence and count; rows for text that left are kept and marked "No longer in the writeup since November 12, 2026"; five clauses the reader found false after the first commit are corrected (the abstract's last sentence, "contribution 4", "that loop", "unattended", "never added to the A100's counts") | ok |
| The pasted text is 2,761 words before the references and 2,981 with them (2,757 and 2,977 before); the limit is 3,000 before the references | ok |
| The abstract is 232 words (1,303 characters) and ends on page 1; Figure 1 is on page 1, looked at in the render; the PDF is 6 pages and its text holds no dollar sign | ok |
| `check_rules.py --check` exits 0 (15 rows pass); every quoted phrase in `paper/sources.md` is in the paper (112 of 112); `docs/build_decks.py --check` exits 0 | ok |
| No first person, secrets, real data or organisation names; the paper names no private Kaggle resource | ok |

Nothing blocking.

## Notes
- Not taken from the second reading: "in one or more of those five runs" in the abstract. It keeps "over those five
  runs": the task-runs left the abstract, so one unit remains there, and the label and the size sentence took the room.
- The pitch deck's slide on this result and the README's "Results at a glance" give the 8 of 17 against 1 of 76 as the
  paper's Section 6 does, without the size of the fixes. They are not wrong, and they are not changed here: a
  follow-up adds the size sentence to both.
- The size of the fixes was not looked at before this review. A check that every number has a source does not ask
  what else differs between two groups; a reader who was given the tables and no conclusion did.
- The text pasted into the Writeup loads Figure 1 from this repository at one commit. The figure did not change;
  the paste file is made again with this merge's commit all the same, and so is the Word copy made for peer review.
