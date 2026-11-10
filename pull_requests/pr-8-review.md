---
pr: 8
branch: fix/7-evaluator-is-distributed
title: "000 BUG2: the official evaluator was available and was not run"
author: Claude Code (agent session for jcbowyer)
reviewed_at: 2026-11-10
reviewer: the authoring session (the evidence was read through the Kaggle API; no reviewer subagent run)
verdict: approve
---

# PR Review: 000 BUG2: the official evaluator was available and was not run

## Summary
Removes a false statement from the paper. The writeup said the competition's evaluator is not distributed; the
starter notebook installs it from a public Kaggle dataset. Two files, documentation only. Nothing blocking.

## How the error got in
`health-transformation-lab-nlp` issue 449 looked for a `swegemma` wheel among the competition's own files, found
none, and concluded the evaluator was not distributed. The writeup, drafted on November 10, repeated that without
checking it. This repository's `docs/starter-notebook-notes.md` (October 29) had already said the packages come
"from the dataset's wheelhouse".

## Checks
| Check | Result |
|---|---|
| "not distributed" no longer appears in the writeup | yes |
| The starter notebook's sources include `metric/gemma-4-developer-agent-wheelhouse` | read November 10, 2026 |
| That dataset holds `swegemma-0.2.11-py3-none-any.whl` | read November 10, 2026 |
| Word limit (3,000, references excluded per the host) | 2,845 without references by `wc -w` |
| Branch name and issue link | `fix/7-evaluator-is-distributed`, `Closes #7` |

## Secrets, Real Data and Claims Scan
- Secrets: none. Real data: none.
- Claims: the writeup now states that the official evaluator was not run and that no score is comparable to the
  leaderboard. Contribution 2 (an open, calibrated re-implementation) still stands as described, but it is no longer
  presented as the only way to score these tasks.

## Should fix (non-blocking, elsewhere)
- `health-transformation-lab-nlp` still records the wrong conclusion in spec 028 (T007, T011b), spec 035 and issue
  449, and spec 035 says "Kaggle has no vLLM" while the starter notebook serves models with vLLM on Kaggle. Those
  are records to correct there, and T011b (score the set with `swegemma eval`) is no longer blocked.

## Not covered
Whether the official evaluator can score this task set as published (its sandbox installs each task's dependencies
from the competition's wheels, and this repository's package sits in a subfolder) has not been tried.
