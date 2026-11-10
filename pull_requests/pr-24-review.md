---
pr: 24
branch: docs/23-outside-review-edits
title: "000 DOCS7: answer two outside reviews of the writeup (held for the owner)"
author: Claude Code (agent session for jcbowyer)
reviewed_at: 2026-11-10
reviewer: the authoring session (each outside-review point and each new figure was checked at its source; no reviewer subagent run)
verdict: approve, held for the owner
---

# PR Review: 000 DOCS7: answer two outside reviews of the writeup (held for the owner)

## Summary
Two other models reviewed the writeup and the owner pasted both reviews back. This pull request makes the changes
their valid points call for, and one correction neither caught. It adds no result: every new figure is a count from a
committed table or a quotation from a source read today. It narrows four claims, adds two limits and two
citations, and cuts three sentences to stay inside the word limit. Nothing blocking in the text. It waits for the
owner because it changes what the paper claims and removes three of the author's sentences, and for pull request
22, which it is stacked on.

## Checks
| Check | Result |
|---|---|
| MLOps-Bench: 212 tasks with fail-to-pass tests from 31 public ML repositories | arXiv:2610.23506 abstract, read today: "212 validated tasks from 31 public ML repositories, with 636 fail-to-pass tests and 856 pass-to-pass tests" |
| data-eng-bench scores a produced artefact | its README, read today: 103 dbt tasks, "a `pytest` verifier that checks the materialized tables row by row against a reference solution"; cited as its `CITATION.cff` asks (Snowflake Inc., version 1.0.0, 2026) |
| "MLOps-Bench is closest" | the only cited set besides the SWE-bench family that scores a change to an existing repository by fail-to-pass tests; its repositories are public ML projects, not one agent-built health-data repository |
| Published tiers 39, 34, 20 | the 93 task ids of `published_verification.csv` joined to `tier_code` in `task_manifest.csv` on `NLP` main; all 93 found; 39 + 34 + 20 = 93 |
| 67 of 116 issue records written afterwards | Section 4.2's own figure (45 + 22) and `paper/sources.md` |
| "48 of 93 tasks, cheapest first" | Section 6's setup sentence; 48 is the scorable count, 93 the published set |
| Wilson | recomputed: 5 of 48 gives 4.5 to 22.2, 2 of 23 gives 2.4 to 26.8; Clopper-Pearson would give 3.5 to 22.7 and 1.1 to 28.0 |
| NOHARM: 1,100 tasks, not cases; version 4, 2026 | the preprint's text: "1,100 items (100 clinical cases with 1,000 physician-perturbed variants)"; version 4 is dated July 13, 2026 and carries the title the reference gives; versions 1 and 2 gave 76.6%, not "more than 80%" |
| "No human screening" | no annotation pass over the tasks is recorded in either repository; the sentence that follows is true whether or not one was done |
| Nothing else changed a number | the diff was read line by line: 13 changed lines in the writeup, no table value altered except the tier column's added counts |
| Citations and references agree | [1] to [18]: each cited, each listed |
| Word count | 2,997 without references by `wc` (2,988 before); 2,878 real words; limit 3,000 |
| `paper/sources.md` | a row for each new figure, a new "Section 2" block, and the cut sentence recorded under "Not in the writeup" |
| Branch name and issue link | `docs/23-outside-review-edits`, `Closes #23`; `pr_conventions.py` passes |

## Should fix
- Do not merge before pull request 22, and that not before `health-transformation-lab-nlp` pull request 648.
- The owner should confirm "No human screening": if any tasks were read and checked by a person, the limit should
  say how many.
- Three sentences were cut to make room (Section 4.5's explanation of the untied commits, "The code was cheap.",
  and the first half of the conclusion's last sentence). They are the author's; restoring any of them needs a cut
  of the same size elsewhere, since the count stands three words under the limit.
- Six references were not checked (2, 3, 4, 12, 13, 14), nor the venues of 6, 8, 9 and 11. The outside review that
  marked all 16 correct showed no source and missed both errors in reference 16.
- Left for another change: the first review's main ask, running the agent under the competition's evaluator (a GPU
  run, the owner's call), and the second's split of tasks into fixes, features and maintenance.

## Secrets, Real Data and Claims Scan
Secrets: none. Real data: none. Claims: none added about results. Two outside benchmarks are described in their
authors' own words with citations; four of the paper's own claims are narrowed.
