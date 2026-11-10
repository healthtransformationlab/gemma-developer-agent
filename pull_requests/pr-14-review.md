---
pr: 14
branch: docs/13-shorter-abstract
title: "000 DOCS3: shorten the writeup's abstract"
author: Claude Code (agent session for jcbowyer)
reviewed_at: 2026-11-10
reviewer: the authoring session (each figure in the new abstract was checked against the body and `paper/sources.md`; no reviewer subagent run)
verdict: approve
---

# PR Review: 000 DOCS3: shorten the writeup's abstract

## Summary
The abstract loses the account of how the competition's evaluator was run and the mining funnel, both of which the
body already gives. It keeps what is released, how it was checked and the baseline result. Nothing blocking.

## Checks
| Check | Result |
|---|---|
| Every figure in the abstract is in the body | 960 and 775 (Section 3); 113 and 93 (Sections 4.1 and 5); 5 of 51 (Section 6); 25 agent patches (Section 5) |
| Every figure has a row in `paper/sources.md` | yes; no new figure |
| "agrees with the official evaluator on all 25 agent patches compared" is not wider than the evidence | it names agent patches only; the 18 reference patches where the two verifiers differ stay in Section 5 |
| The abstract still says the agent ran on a re-implementation, not the official evaluator | yes |
| Word count | abstract 147 (was 190); body 2,940 without references, under the 3,000 limit |
| Branch name and issue link | `docs/13-shorter-abstract`, `Closes #13` |

## Secrets, Real Data and Claims Scan
Secrets: none. Real data: none. Claims: none added; two narrowed to the body.
