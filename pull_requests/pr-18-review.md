---
pr: 18
branch: fix/17-commit-groups-sum
title: "000 BUG4: make the writeup's commit groups sum to 960"
author: Claude Code (agent session for jcbowyer)
reviewed_at: 2026-11-10
reviewer: the authoring session (the groups were recounted from the other repository's history; no reviewer subagent run)
verdict: approve
---

# PR Review: 000 BUG4: make the writeup's commit groups sum to 960

## Summary
One sentence in Section 3 and one row in `paper/sources.md`. The groups now sum to the total and the 175 are named
for what they are. Nothing blocking.

## Checks
| Check | Result |
|---|---|
| The groups sum | 775 + 175 + 5 + 4 + 1 = 960; in `sources.md`, 710 + 65 + 175 + 5 + 4 + 1 = 960 |
| Recounted at the cited commit | `git log b12e2e0` in `health-transformation-lab-nlp`: 710 with the co-author trailer, 65 authored as the agent, 175 with subject "Merge pull request #n" and committer GitHub, 5 by the bot, 4 by the owner alone, 1 "Initial commit" |
| "for pull requests", not "for agent pull requests" | right: some of the 175 merge results branches a workflow opened |
| 775 "marked as agent-authored" unchanged | 710 + 65 |
| Word count | 2,970 without references |
| Branch name and issue link | `fix/17-commit-groups-sum`, `Closes #17` |

## Secrets, Real Data and Claims Scan
Secrets: none. Real data: none. Claims: none added; one count corrected.
