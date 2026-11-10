---
pr: 6
branch: fix/5-second-repo-pr-count
title: "000 BUG1: state the second repository's counts that the history supports"
author: Claude Code (agent session for jcbowyer)
reviewed_at: 2026-11-10
reviewer: the authoring session (counts recomputed from the second repository's history and GitHub's search API; no reviewer subagent run)
verdict: approve
---

# PR Review: 000 BUG1: state the second repository's counts that the history supports

## Summary
Corrects an overclaim in the writeup that the author of the claim (this session) found when the repository's owner
asked why the pull request counts differed. Two files, documentation only. Nothing blocking.

## Checks
| Check | Result |
|---|---|
| The withdrawn claim ("the other 111 are direct commits") no longer appears | yes |
| 133 candidates, 22 tied to a pull request by subject, 0 linking an issue | recomputed on `getcommunityone/open-navigator` main at `6fa4943` |
| 169 merged of 204 pull requests | GitHub's search API, November 10, 2026 |
| Word limit (3,000) | 2,994 by `wc -w` |
| Branch name and issue link | `fix/5-second-repo-pr-count`, `Closes #5` |

## Secrets, Real Data and Claims Scan
- Secrets: none. Real data: none.
- Claims: the section now says 22 is what can be tied by commit subject and that fast-forwarded pull requests cannot be
  told from direct commits by history alone. It no longer states a count of direct commits.

## Nits
- "None links an issue" tests the commit message for `closes`, `fixes`, `resolves` or `refs` followed by `#n`. An issue
  mentioned only in a pull request's description would not be seen; `sources.md` gives the rule.
- The margin under the word limit is now 6 words by `wc -w`. Any further addition needs a cut.

## Not covered
The 14 fast-forwarded pull requests were not broken down into their own commits, so the true number of candidates that
came through a pull request is not known, only bounded below by 22.
