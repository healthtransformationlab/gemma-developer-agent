---
pr: 10
branch: docs/9-official-verifier-results
title: "000 DOCS2: the competition's own verifier on the task set, and where the time went"
author: Claude Code (agent session for jcbowyer)
reviewed_at: 2026-11-10
reviewer: the authoring session (every number recomputed; no reviewer subagent run)
verdict: approve-with-nits
---

# PR Review: 000 DOCS2: the competition's own verifier on the task set, and where the time went

## Summary
Replaces "the official evaluator was not run" with what it gives on the published task set, corrects the baseline's
denominator and its account of the empty patches, and adds the author's own estimate of where their time went.
Two files, documentation only. Nothing blocking.

## Checks
| Check | Result |
|---|---|
| 93 of 113, 0 of 113, 25 of 25 | recomputed from the verification table (`health-transformation-lab-nlp`, branch `data/636-028-official-evaluator-check`) |
| The 20 unresolved reference patches: 12 + 6 + 2 | each rerun with full output and grouped by its error |
| Baseline over 51: 5 resolved, 39 non-empty patches, 34 fail the tests, 12 empty | recomputed from the run table on `main`, with the 7 set-aside tasks named in `sources.md` |
| Four of six empty patches hit the token limit | read from each run's `result.json` (`turns[].output_tokens`) |
| Word limit (3,000, references excluded per the host) | 2,984 |
| Branch name and issue link | `docs/9-official-verifier-results`, `Closes #9` |

## Secrets, Real Data and Claims Scan
- Secrets: none. Real data: none.
- Competition materials: nothing from the evaluator's wheel or guide is quoted; the writeup names the package and
  its version.
- Claims: "more than half of my time" is labelled as the author's estimate, with the pull request title count
  (38 of 305) beside it, which is far smaller and is said to be so.

## Should fix (non-blocking)
- **The verification table is on a branch**, not on `main`, in the other repository. `sources.md` says so. It needs
  its own pull request there.
- **The dataset is still version 3.** The paper says it needs a fix and that a corrected release is the next step.
  If a corrected version is published before the deadline, Sections 4, 5 and 8 and the abstract change again.
- **The release line says the benchmark repository is MIT.** It becomes Apache 2.0 when pull request 639 there
  merges.

## Nits
- A paired rerun of 33 tasks is in progress; Section 6's table changes when it lands.
- The "as published" check ran on three tasks, not all 113. The cause (the package is not on the import path) is the
  same for every task, but only three were run.

## Not covered
The competition's evaluator was used for verification only. It has not run the agent on these tasks.
