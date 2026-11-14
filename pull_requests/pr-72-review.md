# PR 72 review: six clarity edits to the paper after an outside review of the Colab version (#71)

| Check | Result |
|---|---|
| Branch `docs/71-clarity-edits`, `Closes #71` | ok |
| Merge: the owner said "Merge" for the paper's pull requests on November 11, 2026, and passed this review on, on November 12, without a word of their own, as they did the earlier ones they asked to have acted on. Merging starts no run and publishes nothing; the Writeup needs pasting again after it, and the PDF swapping | ok |
| No number changes: the diff of the paper's text was read word by word. Every figure in a changed sentence is the one it had (4, 6 and 4 of 93; p = 0.5, 1.0 and 0.375; 5 and 8; 297–419 GPU-seconds, 4.8–6.7 Wh, 1.9 and 1.8 GPU-hours, 1.59 and 1.50 at 0.83 an L4-hour) | ok |
| The abstract's experiment is a sentence, and "0.5 and 1.0, respectively" follows the order the sentence names the two contexts in: graph retrieval, then the report. It keeps "(from the hidden test: not a benchmark condition)", which the review's own rewrite dropped | ok |
| "Unregistered, so described and not tested" is why the L4 pair's p is not a test: no plan named that pair before it ran, and the rule recorded on the source repository's issue 687 before any patch was verified says it is described. The review's wording ("avoiding p-hacking") was not used: the paper says what was done, not what it avoids | ok |
| "(weekly GPU quota reached)" is Kaggle's own message ("Maximum weekly GPU quota of 30.00 hours reached"), which `sources.md` quotes | ok |
| "Context compaction (summarising older turns)", checked against the evaluator's installed code: `EventsCompactionConfig` (a token threshold, a number of events kept) and `LlmEventSummarizer`, which has the agent's own model write the summary. The runs' settings give 14,336 tokens and 5 events. `sources.md` has a new row for it | ok |
| The cost sentence is two sentences; nothing was added or dropped. The review also asked for the time percentages to be apart from the costs: they already were in a sentence of their own | ok |
| "Finding is not fixing: where retrieval listed an edited function (41 tasks, of Section 4.3's 51), the graph arm resolved 3 and the baseline 2" is unchanged, as the review asked | ok |
| What left: "A first seeded sample of 20 resolved none". The run is still in the README's table, Section 6's table still has the Kaggle baseline's 0 of 21, and `sources.md` keeps its two rows, marked no longer in the writeup. "Then all 93 were to run three times" stays as written, since a row quotes it | ok |
| The pasted text is 2,752 words before the references and 2,972 with them (2,747 and 2,967 before); the limit is 3,000 before the references | ok |
| The abstract is 227 words (1,283 characters) and ends on page 1; Figure 1 is on page 1; the PDF is 6 pages and its text holds no dollar sign. A first wording of the abstract, at 1,309 characters, pushed Figure 1 to page 2 and was shortened | ok |
| `check_rules.py --check` exits 0 (15 rows pass); every quoted phrase in `paper/sources.md` is in the paper (108 of 108) | ok |
| The last change-log entry's two counts were written without their thousands separators ("2967", "2747"); corrected | ok |
| No first person, secrets, real data or organisation names; the paper names no private Kaggle resource | ok |

Nothing blocking.

## Notes
- The review scores the paper 47.5 of 50 and calls it a frontrunner. That is one reader's opinion, and an AI
  reviewer's at that; nothing in the paper or the README repeats it.
- Two of the review's suggestions were taken in substance and not in its words: "due to platform quota exhaustion"
  became Kaggle's own "weekly GPU quota reached", and its rewrite of the abstract's sentence was shortened so that
  the abstract and Figure 1 still fit on page 1.
- The text pasted into the Writeup loads Figure 1 from this repository at one commit. The figure did not change,
  so either commit serves it; the paste file is made again with this merge's commit all the same.
