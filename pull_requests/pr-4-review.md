---
pr: 4
branch: docs/3-paper-writeup-and-readme
title: "000 DOCS1: draft the paper-track writeup; say what has been run"
author: Claude Code (agent session for jcbowyer)
reviewed_at: 2026-11-10
reviewer: the authoring session (numbers recomputed from the source tables; no reviewer subagent run)
verdict: approve-with-nits, for the owner to merge after reading "For the owner"
---

# PR Review: 000 DOCS1: draft the paper-track writeup; say what has been run

## Summary
Adds the paper draft and the list of where its numbers come from, and brings the README, the task-set note and the
outline in line with what has been run. Documentation only. Nothing blocking; it waits for the owner because the
paper is the owner's to edit and submit.

## Scope of Change
- Files changed: 5 (`paper/writeup.md` and `paper/sources.md` new; `README.md`, `tasks/README.md`,
  `paper/outline.md` edited), plus this review
- Range reviewed: `origin/main..docs/3-paper-writeup-and-readme`

## Checks
| Check | Result |
|---|---|
| Every number in the writeup has a row in `paper/sources.md` | yes |
| Numbers recomputed from `health-transformation-lab-nlp` main at `b12e2e0` | yes, November 10, 2026 |
| Word limit (3,000) | 2,970 by `wc -w`, references included |
| Required sections (title, subtitle, abstract, introduction, methods and experiments, related work, citations) | present |
| Simulated or unrun work presented as a result | none: the skill, the sub-agent, the development set and the switch-off test are named as not run or not used |
| Branch name and issue link | `docs/3-paper-writeup-and-readme`, `Closes #3` |

## Secrets, Real Data and Claims Scan
- Secrets: none. Real data: none; the writeup says the patient records are synthetic.
- Organisation claims: the writeup opens with the not-affiliated notice. It names one outside repository
  (`getcommunityone/open-navigator`) as the owner's second public repository.
- Competition materials: nothing is quoted from the competition's harness guide. The writeup says the prompt wording
  in the harness follows the guide and that the guide is not redistributed.

## Should fix (non-blocking)
- **References 5, 6, 7, 10 and 11** were first written from memory, then checked on November 10, 2026 against
  their arXiv records (2412.21139, 2504.21798, 2505.20411, 2411.07763, 2504.04808) and given their venues. The
  other ten were not re-checked.
- **The baseline's two groups are split by timestamp.** The run table has no batch column; `sources.md` says the
  split is ours. A `batch` or `is_graph_available` column in the run table would make it checkable.
- **The de-identification count (16 candidates, 8 attempted) is a keyword match on titles.** `sources.md` says so;
  the writeup says "a keyword match on titles".

## Nits
- Section 6 will change if the first 33 tasks are rerun on the fixed harness.
- Kaggle's word counter may differ from `wc -w`; the margin is 30 words.

## For the owner
- `getcommunityone/open-navigator`: confirmed by the owner on November 10, 2026 as the repository of a nonprofit
  the owner leads, and citable. Section 4.5 now says so. The wording of that role is the owner's to adjust.
- The statement "its author typed no code" is the owner's own; the commit counts beside it are in `sources.md`.

## Not covered
The empty-patch transcripts were not re-read (the artifact store is not reachable from the reviewing session); the
writeup cites the review of pull request 630 in `health-transformation-lab-nlp` for that finding.
