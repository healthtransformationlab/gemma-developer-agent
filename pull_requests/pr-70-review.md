# PR 70 review: the experiment on one Colab GPU, with a baseline; the owner's check of the core split (#68)

| Check | Result |
|---|---|
| Branch `docs/68-colab-pair`, `Closes #68`: the issue's third part, the paired run on Colab, is what this pull request reports (its first two were pull request 69) | ok |
| Merge: the owner said "Merge" for the paper's pull requests on November 11, 2026, and on November 12 asked whether the runs could be finished on Colab and said to do the right thing to win. Merging starts no run and publishes nothing; the Writeup needs pasting again after it, and the PDF swapping | ok |
| Every new count against the source repository at `526ea08` (its pull request 690), recomputed for this review from the committed tables: `colab-statement` 4, `colab-graph` 6, `colab-report` 4, `colab-statement-l4` 5 and `colab-graph-l4` 8 of 93; Wilson intervals 1.7–10.5, 3–13.4, 1.7–10.5; core split 4, 6, 4, 5 and 7, so 26 of 85 task-runs, and 1 of 380 on the other 76 (`htlnlp_116` in the L4's graph arm) | ok |
| The two registered tests: graph retrieval against the baseline, both 4, the baseline alone 0, graph alone 2, exact McNemar p = 0.5; the report against the baseline, both 3, 1 and 1, p = 1.0. The paper claims no difference and says none is ruled out. The L4 pair (both 4, 1 and 4, p = 0.375) is called unplanned and described, in the abstract, Section 6 and the conclusion, and is never added to the A100's counts | ok |
| "The two baselines differed on 3 tasks": both resolved 3, the A100's alone `htlnlp_226`, the L4's alone `htlnlp_144` and `htlnlp_174` | ok |
| "9 of the 10 tasks this model has resolved are in the core split": the nine before Colab and `htlnlp_170`, resolved for the first time in the L4's graph arm; all but `htlnlp_116` are in the split | ok |
| Found and fixed, now with a baseline beside it: where the retrieval listed an edited function (41 of Section 4.3's 51 tasks), `colab-graph` resolved 3 and `colab-statement` 2 | ok |
| The open network is said, in Section 6: "Colab's network was open to the agent: 3 of the five runs' 687 commands ran an installer, in tasks no run resolved, and none left its workspace". The runs' own records had said the proxies held; an independent review of the source repository's pull request found they did not reach the agent's commands. Recounted here from the five runs' traces: 4,383 tool calls, 687 commands, three editable installs of the repository itself in two tasks no run resolved, no such word in any of the 27 task-runs that resolved, and no command naming a path outside its workspace | ok |
| The abstract gives the completed experiment, the L4 session's two counts and "26 of 27 in the core split" (4 + 6 + 4 + 5 + 8 = 27 fixes, 26 on core-split tasks). It no longer gives the Kaggle arms, which Section 6's table keeps beside the A100's | ok |
| Figure 1's third group: 4, 6, 4, headed "No difference detected", so three bars are not read as a ranking | ok |
| The owner's check of the core split's other 12 verdicts (source repository, pull request 689): "42 verdicts, the core split's 17 among them", "51 of ours ... have AI ratings only"; the paper says the check was in summary and after seeing the AI's verdict | ok |
| What left the paper is in `sources.md` as rows marked "no longer in the writeup": the Kaggle arms' paired tests and the other reading of "not run", "7 of the 8" and "6 of the 8", the Kaggle graph arm's 2 of 41, the T4 baseline's cost of a fix in dollars, and Section 7's sentence on the report arm's context, which the abstract and Sections 4.3, 6 and 8 still say | ok |
| The pasted text is 2,747 words before the references and 2,967 with them (2,698 and 2,918 before); the limit is 3,000 before the references | ok |
| The abstract is 222 words and ends on page 1; Figure 1 is on page 1; the PDF is 6 pages and its text holds no dollar sign | ok |
| `check_rules.py --check` exits 0 (15 rows pass); every quoted phrase in `paper/sources.md` is in the paper (108 of 108) | ok |
| The README's table has the five Colab runs, its bullets say the same as the paper, and its link to the experiment's tables is at the source repository's commit that holds them | ok |
| No first person, secrets, real data or organisation names; the paper names no private Kaggle resource | ok |

Nothing blocking.

## Notes
- The result is a null result with a baseline, where the last version had two arms and no baseline. In both
  sessions graph retrieval resolved more tasks than the baseline (6 against 4, 8 against 5), and neither difference
  is near the registered threshold. The paper gives both pairs and claims nothing from either. A reader who wants
  to know whether retrieval helps this model needs repeats: two runs of the same baseline differ on three tasks.
- The report arm on Colab was registered after the Colab baseline's outcome was known (addendum 3 says so, and so
  does `sources.md`). Its test is against that baseline. Nothing is claimed from it.
- The Colab runs are not the Kaggle arms' environment: one GPU, Python 3.13, nine packages at other versions and an
  open network. The paper says each. The Kaggle baseline's rerun is still owed (source repository, issue 681).
- The text pasted into the Writeup loads Figure 1 from this repository at one commit. The figure changed, so the
  paste file is made again after this merges, with that commit.
