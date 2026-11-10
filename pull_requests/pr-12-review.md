---
pr: 12
branch: fix/11-benchmark-repo-licence
title: "000 BUG3: the writeup names the benchmark repository's old licence"
author: Claude Code (agent session for jcbowyer)
reviewed_at: 2026-11-10
reviewer: the authoring session (the licence file on the other repository's main branch was read; no reviewer subagent run)
verdict: approve
---

# PR Review: 000 BUG3: the writeup names the benchmark repository's old licence

## Summary
One word in Section 9: the benchmark repository is Apache 2.0 since its pull request 639, not MIT. Nothing blocking.

## Checks
| Check | Result |
|---|---|
| `health-transformation-lab-nlp` `main` `LICENSE` is the Apache 2.0 text | yes: SHA-256 begins `cfc7749b96f6`, the same file as this repository's |
| No other mention of MIT in `paper/` or `README.md` | none |
| Word count unchanged in effect | 2,985 without references |
| Branch name and issue link | `fix/11-benchmark-repo-licence`, `Closes #11` |

## Secrets, Real Data and Claims Scan
Secrets: none. Real data: none. Claims: none added.
