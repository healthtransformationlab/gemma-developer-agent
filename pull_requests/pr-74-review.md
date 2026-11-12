# PR 74 review: the core split as the paper's central result; tasks and task-runs told apart (#73)

| Check | Result |
|---|---|
| Branch `docs/73-core-split-central`, `Closes #73` | ok |
| Merge: the owner said "Merge" for the paper's pull requests on November 11, 2026, and passed this second review on, on November 12, without a word of their own, as they did the first. Merging starts no run and publishes nothing; the Writeup needs pasting again after it, and the PDF swapping | ok |
| No count changed. The diff of the paper's text was read word by word: every figure in a changed sentence that was there before is the one it had (4, 6 and 4 of 93; p = 0.5 and 1.0; 5 and 8; 26 of 85 and 1 of 380; 41 tasks, 3 and 2; 9 of the 10; 66–83% and 14–15%; 45 of 207; 1.9 and 1.8 GPU-hours) | ok |
| The three counts that are new, recomputed twice from the source repository's tables at its `main` (`526ea08`), once for this review and once by a second reader working alone: 8 of the core split's 17 tasks and 1 of the other 76 were resolved in at least one of the five Colab runs; of the 41 tasks where the retrieval listed an edited function, 7 are in the core split and 34 are not, and 5 of the 7 and none of the 34 were resolved in some run (12 of 35 and 0 of 170 task-runs; 7 of 14 and 0 of 68 in the two graph-retrieval runs) | ok |
| The abstract ends on where the fixes were, in distinct tasks with the task-runs beside them. "Those five runs" are the five whose counts the two sentences before it give: 4, 6 and 4 on the A100, 5 and 8 on the L4. The share of time in model calls left the abstract and is still in Section 6 | ok |
| Tasks and task-runs: the abstract and Section 6 give "tasks" first and "task-runs" in brackets, and Section 6 says "the five Colab runs" beside them (17 × 5 = 85, 76 × 5 = 380); the conclusion says "9 of the 10 distinct tasks". "26 of 27", which counted fixes, is gone | ok |
| The graph outcome: "Retrieval's two extra fixes (three in an unplanned second session on an L4) do not establish a reliable improvement". On the A100, 6 against 4 with the baseline's four among the six; on the L4, 8 against 5. The abstract and Section 6 still give the test (p = 0.5) and "no difference is claimed or ruled out"; Figure 1's third group still says "No difference detected" | ok |
| The comparison of the 41 by core split was made on November 12, after every run. The text says "(a post hoc comparison)", in the paragraph that opens "Described, not tested". `sources.md` says it is exploratory, that the five runs repeat the same tasks, and that the core split's tasks may differ from the others in size or kind | ok |
| The conclusion's last clause is a description in the past tense: "valid tasks whose fix the graph found, but whose statements leave out what their tests need, measured little for this model". The 34 are verified by the competition's evaluator, the retrieval listed a function their fix edits, the screen finds their statements leave out what their tests need, and none was resolved in 170 task-runs. It does not say why, and `sources.md` says it does not | ok |
| "Finding is not fixing: where retrieval listed an edited function (41 tasks, of Section 4.3's 51), the graph arm resolved 3 and the baseline 2" is unchanged, as the first review asked | ok |
| Figure 1's last group: 76, 1, 17, 8, each in the text. Its heading says "a description, not a test". The bar "Screened: 93" left; the first group ends on the same 93. The row pitch went from 20 to 19 so that fourteen rows are about as tall as thirteen were. Page 1 was rendered and looked at: the abstract, the links and the whole figure are on it | ok |
| What left: the paragraph "A larger budget", "A task took 297–419 GPU-seconds on the four L4s and 4.8–6.7 Wh" and "under 0.1% in the graph tools". The README's table keeps the larger-budget run and its time bullet now holds the other two; `sources.md` keeps every row, marked "no longer in the writeup", and the two rows that said Section 6 has the larger budget now say it had. No sentence left in the paper points to any of the three | ok |
| The pasted text is 2,756 words before the references and 2,976 with them (2,752 and 2,972 before); the limit is 3,000 before the references | ok |
| The abstract is 233 words (1,304 characters) and ends on page 1; Figure 1 is on page 1; the PDF is 6 pages and its text holds no dollar sign | ok |
| `check_rules.py --check` exits 0 (15 rows pass); every quoted phrase in `paper/sources.md` is in the paper (108 of 108) | ok |
| The README says the same as the paper: the core split in tasks and task-runs, and the comparison with its task-runs and "made after the runs, described and not tested" | ok |
| No first person, secrets, real data or organisation names; the paper names no private Kaggle resource | ok |

Nothing blocking.

## A second reader's findings

A second reader, given only the diff and the tables, confirmed all four sets of numbers and found seven things to
change. None was a wrong number. All seven were acted on before this review was written.

| Finding | What changed |
|---|---|
| The conclusion's "a valid task whose fix the graph finds can still measure little when its statement leaves out what its tests need": "when" reads as a cause, and the evidence is a comparison made after the runs, on one model, not controlled for task size | reworded as what these tasks did: "valid tasks whose fix the graph found, but whose statements leave out what their tests need, measured little for this model" |
| Section 6's "5 of the core split's 7 were resolved in some run" reads as the two runs just named, where it would be 3 of 7 | "in some Colab run", and the sentence before it now says "in some of the five Colab runs" |
| In the abstract, once the sentence on the graph stood before the experiment, "it resolved" read as the graph | "Gemma resolved" |
| "Those five runs" and "task-runs" are not defined | Section 6 says "the five Colab runs" beside the task-runs. The abstract keeps "those five runs": the two sentences before it give five counts, and it was left as short as it is, since an abstract a few characters longer pushed Figure 1 to page 2 in the last version |
| The README's "a split made after the runs" reads as the core split being made afterwards | "a comparison made after the runs" |
| `sources.md` still described five headings in the abstract, in the old order | four, in the new order, with the date |
| "A fix took 1.9 GPU-hours" had lost "on the four L4s" with the sentence before it | "A fix there took", after the sentence on the Kaggle arms |

## Notes
- The review that prompted this scores the paper 4.1 of 5 and calls statement quality its most persuasive claim. That is
  one reader's opinion, and an AI reviewer's; nothing in the paper or the README repeats it. It read the version before
  the last one, so one of its three points (which p-value is whose) was already made.
- The new sentences are descriptions. The registered result is unchanged: no difference detected between the three
  arms. The core split's contrast is named as a description in both addenda; its comparison within the 41 is in
  neither, and is labelled post hoc.
- The core split comes from an AI screen that one person checked in summary. A reader who doubts the screen should
  doubt the contrast to the same degree; Section 7 says who checked what.
- The text pasted into the Writeup loads Figure 1 from this repository at one commit. The figure changed, so the
  paste file is made again after this merges, with that commit.
