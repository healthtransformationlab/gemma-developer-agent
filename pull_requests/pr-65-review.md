# PR 65 review: the development set beside this set, a pre-registered experiment, a core split (#62, #64)

| Check | Result |
|---|---|
| Branch `docs/62-devset-comparison`; `Closes #62` and `Closes #64` | ok |
| Merge: the owner said "Merge" for the final paper pull request on November 11, 2026. Merging starts no run and publishes nothing; the Writeup needs pasting again after it | ok |
| Issue 62: one table in Section 6 with both sets, one paragraph on how the 40 development tasks were drawn and why 23 can be verified | ok |
| Issue 62: the abstract, contributions, limitations and conclusion say what the comparison shows and no more (AI ratings only for the 40, one run, 5 minutes and 40 tool calls) | ok |
| Issue 62: Section 4.5 is gone; no competition text or file is committed or quoted; `check_rules.py` says so in its data rows and cites the host's two forum answers | ok |
| Issue 64: Section 6 gives each arm's tasks run and resolved with its interval, says the baseline arm ran 21 of 93 and why, and that no difference is claimed and none is ruled out | ok |
| Issue 64: the failing test's report is called context from the hidden test in the abstract, Section 6, Section 7, Section 8 and Figure 1; the 48 of 51 in Section 4.3 is labelled oracle-assisted | ok |
| Issue 64: the core split is named in the abstract, Section 6 and Section 8; "7 of the 8" and "8 of the 9" are given as described, not tested | ok |
| Issue 64: no dollar figure for the L4 runs (no price for them is cited); GPU-hours and watt-hours only | ok |
| The numbers, recomputed from the run tables by an independent, read-only reviewer that was given the files and not the answers: each arm's tasks run, resolved, interval and core-split count; both paired tests and the other reading's p-values; "7 of the 8", "6 of the 8" and "8 of the 9" with the task ids and the earlier table for each; every cell of the development-set table and its controls; the time shares, GPU-seconds, watt-hours, GPU-hours a fix and the T4 dollars; the settings; Sections 4.1 and 4.3. No number in the paper, the PDF or Figure 1 differed | ok |
| What that review found in the wording, each checked against the tables before it was changed (below) | fixed |
| What that review found in `paper/sources.md` (below) | fixed |
| No sentence says or implies that either context improved on the baseline. The abstract: "neither context could be tested". Section 6: "no difference is claimed and none is ruled out". Section 8: "whether either context helps is still open". Figure 1: "No arm resolved any of the 21 the baseline ran" | ok |
| Every quoted phrase in `paper/sources.md` is in the paper (98 of 98); the cuts and changes are listed in its change log | ok |
| Word count: 2,729 before the references by the rules check; the pasted text is 2,679 before the references and 2,899 with them. The owner asked for more room than the 6 words the first version of this pull request left | ok |
| The abstract is 223 words; Figure 1 is on page 1; the PDF is 6 pages | ok |
| `check_rules.py --check` exits 0: no row fails | ok |
| The README's run table: the development-set row and the three arms, each from the arm's table; links at the commit of the source repository that holds them | ok |
| No first person, secrets, real data or organisation names | ok |

Nothing blocking.

## What the independent review found, and what was done

In the paper's wording:

| Finding | Done |
|---|---|
| Figure 1 drew the three arms as 0, 4 and 5 on one scale, with only the bracketed denominators to say the baseline ran 21, and no hidden-test label on the report's bar | the group's heading says that no arm resolved any of the baseline's 21 tasks; the bars read "21 of 93 run" and "93 run"; the report's bar says "from the hidden test" |
| The abstract's "What more context did" asserts an effect, and "(none resolved)" beside 4 and 5 invites the comparison | "With more context"; "which no arm resolved" |
| The abstract gave the core split as fact; it is an AI screen's verdict | "an AI screen finds 17 whose statements say what their tests check" |
| Section 5 said each task ran in a notebook "beside that task only"; the evaluator's notebooks held all 93, sealed and opened one at a time | "with the others absent or sealed", and a row in `sources.md` for each kind of run |
| The development-set notebook has the competition's reference patches mounted, and the paper did not say how that run was kept honest | one sentence: the patches are mounted, and no tool call named a path outside the workspace (0 in all 40 rows) |
| "no pip ... so the reference patch fails 16 of the 40" gives one cause for all 16; it was read for 7 and inferred for 9 | "so" is gone; `sources.md` keeps the 7 and the 9 |
| The 23 verifiable tasks are rich 15 and fastapi 8, with no requests task, and are not a sample of the 129 | "(rich 15, fastapi 8)" is back in Section 6; `sources.md` says they are not a sample |
| "counting the 72 as baseline failures" was not labelled as the reading kindest to the contexts | "even counting"; `sources.md` says why, and that the addendum's 0.025 threshold has no claim to apply to |
| "83 of 439" tool calls are over the 40 tasks run, beside a row over the 23 | the row says "(all runs)" |
| The time paragraph did not say whose spans, and mixed GPU-hours on four L4s with agent hours on two T4s | "The three arms'"; "agent-hours"; "for its two T4s". The development-set kernel's shares, which lie outside the ranges, are in `sources.md` |
| Section 2 called the cited entry's counts "close to the counts here": true of two of its three | the clause is gone; `sources.md` gives all three pairs |
| Reference 15's title was neither the post's nor the notebook's | the title its author gave the post |

In `paper/sources.md`: the row behind reference 15 called 52 "a name or one call edge" (it is a name or a call path of any length; one edge gives 33, two give 36); the T4 baseline's time was 32,443 seconds and 9.01 hours, not 32,472 and 9.02 (the paper's "9.0" stands); six rows were dated November 12 for changes made on November 11; four rows pointed at paragraphs since renamed; and the change log said the report is labelled "wherever a result of it is given", which the time paragraph's "1.8 with the report" is not. All corrected.

Left as it is, with the reason:

- "The other 72 count as not run under the plan." For 60 of them this is a reading of the plan's "agent phase did not start", written into the runner after the report arm had been collected. The paper gives the other reading's p-values, `sources.md` gives the timing, and nothing is claimed under either.
- The kernels' patches, traces and telemetry files are not committed, so the review recomputed from the committed tables. The verdicts were made twice from one kernel's output with no row changing (`health-transformation-lab-nlp` pull request 682).

## Notes
- The experiment does not say whether graph retrieval or a failing test's report helps: its baseline arm ran 21 of
  the 93 tasks before its model server stopped answering, and Kaggle refused the rerun. The baseline for the other
  72 is owed (`health-transformation-lab-nlp` issue 681) and needs the owner's word and GPU allowance.
- The tables the paper cites reach the source repository's `main` when its pull request 682 merges. Until then
  they are on that pull request's branch.
- The text pasted into the Writeup loads Figure 1 from this repository at one commit, not from `main`, so the
  submitted figure cannot change after the deadline when the figure here is next redrawn.
