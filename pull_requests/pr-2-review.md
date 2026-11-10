---
pr: 2
branch: chore/1-add-apache-licence
title: "000 CHORE1: add the Apache 2.0 licence"
author: Claude Code (agent session for jcbowyer)
reviewed_at: 2026-11-10
reviewer: the authoring session (a check of the diff and the licence text's hash; no reviewer subagent run)
verdict: approve, for the owner to merge (the choice of licence is the owner's)
---

# PR Review: 000 CHORE1: add the Apache 2.0 licence

## Summary
Adds `LICENSE` (Apache License 2.0), `NOTICE` and one README line. The repository had no licence file. Nothing
blocking. It waits for the owner because choosing a licence is the owner's decision, not an agent's.

## Scope of Change
- Files changed: 3 (`LICENSE` new, `NOTICE` new, `README.md` +2 lines), plus this review
- Range reviewed: `origin/main..chore/1-add-apache-licence`

## Checks
| Check | Result |
|---|---|
| `LICENSE` is the unmodified Apache 2.0 text | yes: SHA-256 `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`, 11,358 bytes, the standard `LICENSE-2.0.txt` |
| Branch name and issue link (`pr_conventions.py`) | `chore/1-add-apache-licence`, `Closes #1` |
| Tests | none in this repository; no code changed |

## Secrets, Real Data and Claims Scan
- Secrets: none. Real data: none.
- Claims: the README line says Apache 2.0 is "the licence type the competition names for winning submissions",
  which is rule 1.6 of the paper track's rules as read on Nov 10, 2026. Rule 2.5 asks only for an OSI-approved
  licence that permits commercial use, which MIT also meets.

## For the owner to decide
- Apache 2.0 here while `health-transformation-lab-nlp` and `pipeline-doctor` stay MIT. Both satisfy rule 2.5.
  If one licence across the three repositories is wanted, that is a separate change in each.
- `skills/pipeline-doctor/` carries the method from `pipeline-doctor` (MIT, same copyright holder); MIT code may
  be included in an Apache 2.0 work.

## Not covered
Whether the licence grant is sufficient for prize acceptance is the sponsor's call, not something this review
can confirm.
