---
pr: 16
branch: docs/15-silent-defects-framing
title: "000 DOCS4: lead the writeup with silent defects, which is what the source benchmarks are for"
author: Claude Code (agent session for jcbowyer)
reviewed_at: 2026-11-10
reviewer: the authoring session (both cited abstracts were read on arXiv; no reviewer subagent run)
verdict: approve
---

# PR Review: 000 DOCS4: lead the writeup with silent defects, which is what the source benchmarks are for

## Summary
The title and introduction now say what the source repository is for, with two cited figures, and one limitation
keeps the title from promising more than the paper measures. Nothing blocking.

## Checks
| Check | Result |
|---|---|
| 81% and 22% across twelve models | GlobalDentBench, arXiv:2605.24636v2, abstract: 81.34% multiple-choice, 22.34% case-based, "12 frontier LLMs". The multiple-choice questions are from qualification examinations and the case questions from published case reports, as the paper's wording says |
| Omissions more than 80% of severe errors, 1,100 cases | NOHARM, arXiv:2512.01241v4, abstract. The text calls it a preprint and says "medical consultation cases", not dental. An earlier version of that preprint gave a different share, so the current one is quoted |
| "A model can pass the exam and still leave out the warning a patient needed" | a summary of the two figures, hedged with "can"; no rate is claimed for it |
| The title does not claim the tasks are silent defects | the new limitation says each task comes with a failing test and what the set does and does not measure |
| "open benchmarks I built", "not affiliated" | the disclaimer under the title is unchanged; no employer or organisation is named |
| Wording rule (finding gum disease in records) | kept |
| Trims change no number | read line by line: the review counts still sum (119 + 64 + 9 = 192, all approve forms); the four reserved cases are the same four |
| Word count | 2,967 without references |
| Branch name and issue link | `docs/15-silent-defects-framing`, `Closes #15` |

## Should fix
- Section 3's commit groups sum to 959, not 960 (the initial commit is in no group), and the 175 are merge commits,
  not squash merges. Older than this change; its own issue.

## Secrets, Real Data and Claims Scan
Secrets: none. Real data: none. Claims: two added, both cited and quoted in `paper/sources.md`.
