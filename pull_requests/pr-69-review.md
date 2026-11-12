# PR 69 review: what retrieval found beside what the agent fixed; the README's 25 and 23 (#68)

| Check | Result |
|---|---|
| Branch `docs/68-found-not-fixed`, `Refs #68` (the issue's third part, the Colab paired run, is not in this pull request) | ok |
| Merge: the owner said "Merge" for the paper's pull requests on November 11, 2026, and asked that day how to use the time left before the deadline after an outside review. Merging starts no run and publishes nothing; the Writeup needs pasting again after it | ok |
| The sentence, "Finding is not fixing: the graph arm resolved 2 of the 41 tasks where its retrieval listed an edited function (of Section 4.3's 51)", against the source repository's `context_pairs_graph.csv`, recomputed for this review: 51 rows with `is_edit_task`; `is_edited_node_listed` true in 41 and false in 10; `is_graph_resolved` true in 2 of the 41 (`htlnlp_111`, `htlnlp_226`) and 0 of the 10 | ok |
| It is a description and reads as one: it follows "Described, not tested", names no baseline and makes no claim that retrieval helps or does not. `sources.md` says that with no baseline for 72 tasks nothing says what the arm would have resolved without the retrieval | ok |
| The 41 is not Section 4.3's 42, and `sources.md` says why: 41 is what the arm was given, with its lists capped; 42 counts where any name, call path or first-ten embedding match leads | ok |
| The README's 48: 25 saved patches on the first release and 23 from a rerun on the corrected release, the two rows of the paper's Section 5 table and of `sources.md` ("25 + 23 = 48") | ok |
| The two cuts lose nothing: contribution 4 says the set is compared with the competition's tasks; Section 5's first sentence says the same in three fewer words | ok |
| The pasted text is 2,698 words before the references and 2,918 with them (2,682 and 2,902 before): 82 under the limit counted with references, which the rule does not count | ok |
| The abstract is unchanged (223 words); Figure 1 is unchanged and on page 1; the PDF is 6 pages and its text holds no dollar sign | ok |
| `check_rules.py --check` exits 0; every quoted phrase in `paper/sources.md` is in the paper (101 of 101) | ok |
| No first person, secrets, real data or organisation names | ok |

Nothing blocking.

## Notes
- The outside review's largest point is not answered here: the baseline is missing for 72 of the 93 tasks. The source
  repository's issue 687 runs both arms again on one Colab GPU under a plan frozen before either ran
  (SHA-256 `312041e8…2fc9` on that issue). If it completes by 12:00 UTC on November 12 its result gets its own row in
  Section 6 and its own pull request here; if not, the paper says nothing new about it.
- The review also asked for a person's check of the 12 core-split verdicts no person has seen. That is the owner's
  to do; the paper's Limitations already say those 12 have AI ratings only.
- The text pasted into the Writeup loads Figure 1 from this repository at one commit. The figure did not change, so
  the commit pinned for the last paste still serves it.
