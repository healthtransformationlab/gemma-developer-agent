# The leaderboard plan

One table for every entry of this repository's agent in the Gemma 4 Developer Agent competition: the commit, the one
change it measures, the evidence behind the change, and its score. Issue #126; the decisions behind it are in
[health-transformation-lab-nlp ADR 0007](https://github.com/healthtransformationlab/health-transformation-lab-nlp/blob/main/docs/adr/0007-gpu-hours-are-a-reserve-and-score-questions-go-to-the-leaderboard.md). Scores come from the ledger, [health-transformation-lab-nlp
`data/tasks/leaderboard_entries.csv`](https://github.com/healthtransformationlab/health-transformation-lab-nlp/blob/main/data/tasks/leaderboard_entries.csv), which a workflow there refreshes every two hours.

## The rules

- **One change per entry.** Each queued entry differs from the entry named in "Compared with" by one change, so the score
  difference is that change's effect. The public score is about 58 hidden tasks, and the same submission varies by about
  ±1.6 of them (paper track write-ups 91230 and 93326), so a difference of one or two tasks is noise; a change is judged
  on every entry and trace that bears on it, never on one score.
- **One pending entry at a time.** Kaggle refuses a new submission while one is pending ("Your team already has 1 pending
  submissions"), and scoring machines are short (forum topic 747519). Entries go in this order, each when none is
  pending; an agent session's scheduled queue reads the order from this page.
- **Gates.** If entry 5 (copyfix) scores 0.00 or errors, the entries that carry copyfix (5b, 6, 7, 8) wait and versions
  without the adapter are proposed; 31B-b and 5c carry no copyfix and still go. If 31B-b runs past the 12-hour limit, its per-task
  budget is shortened before December 2, and 31B-c (the same 8-minute budget) does not go until it is.
- **The 31B comes second** (the owner, November 15, 2026: the main prizes can only be won with the 31B; the small
  model can win only the $10k bonus), so its first score and timing come before the small model's other changes. That
  slot is 31B-b, the Budget-Fit budget, since the 5-minute 31B entry ran out of time on every task of its smoke test (#138).
- **Built from a fresh checkout**, with no `__pycache__` or `.pyc` (the evaluator refuses them), named `submission.zip`.

## Entries

Every agent commit is in [healthtransformationlab/gemma-developer-agent](https://github.com/healthtransformationlab/gemma-developer-agent); the `Code` column gives its branch. Scores and development-set runs are in [healthtransformationlab/health-transformation-lab-nlp](https://github.com/healthtransformationlab/health-transformation-lab-nlp).

| Entry | Ref | Commit | Code | Model | The one change | PR / issue | Compared with | Evidence before submitting | Expected | Score |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 58290615 | | | E4B | one agent, answer cap 6,144, 4.5 minutes | | | | | **0.05** |
| 3 | 58333590 | | | E4B | lean prompt, no `submit_patch` | | 1 | | | **0.03** |
| 4 | 58364801 | [76bc6d6](https://github.com/healthtransformationlab/gemma-developer-agent/commit/76bc6d6) | [gemma-developer-agent](https://github.com/healthtransformationlab/gemma-developer-agent) `main` | E4B | localize-first prompt (PR 98) and an 8,192-token answer cap (PR 100) | #97, #99 | 1 | 23 development tasks: 4 of 23 against 3 (p = 1.0); no context-window endings ([health-transformation-lab-nlp `data/tasks/official_agent_runs/`](https://github.com/healthtransformationlab/health-transformation-lab-nlp/tree/main/data/tasks/official_agent_runs)) | small | **0.05** |
| **5** | | [9c9cd3a](https://github.com/healthtransformationlab/gemma-developer-agent/commit/9c9cd3a) | [gemma-developer-agent](https://github.com/healthtransformationlab/gemma-developer-agent) `main` | E4B | **copyfix**, a training-free rank-128 LoRA for the QAT model's copying defect | PR 109, #108 | 4 | copy failures 15 → 1 of 18 on Kaggle's vLLM (write-up 90715); another team 0.05 → 0.10, repeat 0.05 (92175); our traces ([`analysis/edit_failures.csv`](https://github.com/healthtransformationlab/gemma-developer-agent/blob/main/analysis/edit_failures.csv)): 37% of edits fail; of the 90 "old_string not found" failures, 28 are near-copies (below) | fewer failed edits | queued |
| **31B-b** | | [c75c619](https://github.com/healthtransformationlab/gemma-developer-agent/commit/c75c619) | [gemma-developer-agent](https://github.com/healthtransformationlab/gemma-developer-agent) [`feat/136-31b-budget-fit`](https://github.com/healthtransformationlab/gemma-developer-agent/tree/feat/136-31b-budget-fit) | **31B** | **the Budget-Fit budget**: 8 minutes, 28 calls, 80 turns, 300-second commands (the 31B entry kept E4B's 5 minutes and 40 calls) | #136 | none: the first 31B entry scored | the public "Budget-Fit Single Agent" budget, scored normally by several teams on the 31B at about 0.20 to 0.24; one team measured about 225 s a task on the scorer's 4×L4 including setup, about 7.5 hours for 120 tasks; the smoke test of the 5-minute 31B entry (health-transformation-lab-nlp #818, Modal A100, November 15): the 31B served fine, but all 3 tasks hit the 5-minute limit (35, 18 and 7 tool calls) and 2 of 3 submitted no patch | more 31B tasks finished in time | queued |
| **5b** | | [80d23e8](https://github.com/healthtransformationlab/gemma-developer-agent/commit/80d23e8) | [gemma-developer-agent](https://github.com/healthtransformationlab/gemma-developer-agent) [`feat/122-skill-on-copyfix`](https://github.com/healthtransformationlab/gemma-developer-agent/tree/feat/122-skill-on-copyfix) | E4B | **edit-fallback skill**: `find.py` ranks the code to fix, `edit.py` rescues a failed edit | PR 123, #122 | 5 | CPU only: right file first in 39 of 129 development tasks against grep's 12; damaged edits right 3,739 against `edit_file`'s 2,820, wrong 62 against 79 ([`docs/fallback-scripts-study.md`](https://github.com/healthtransformationlab/gemma-developer-agent/blob/main/docs/fallback-scripts-study.md)); on 255 tasks from four repositories, 150 of them from [getcommunityone/open-navigator](https://github.com/getcommunityone/open-navigator) (commit messages standing in for issues): right file first 87 against grep's 25, damaged edits right 14,506 against 10,191 and wrong 391 against 810; caveat: most of that check is one repository (open-navigator: 150 of the 255 tasks, 11,373 of the 16,806 edits); a harness run with a scripted model installs, finds, edits and submits | the largest of these | queued |
| **31B-c** | | [2b1c444](https://github.com/healthtransformationlab/gemma-developer-agent/commit/2b1c444) | [gemma-developer-agent](https://github.com/healthtransformationlab/gemma-developer-agent) [`feat/140-31b-single-agent`](https://github.com/healthtransformationlab/gemma-developer-agent/tree/feat/140-31b-single-agent) | **31B** | **a single agent**: 31B-b without the `code_analyzer` sub-agent | #140 | 31B-b | our recorded spans (two 23-task development-set runs): model calls 71–81% of task time, the analyzer 13% of one run's (23 uses, median 23.5 s, a second model loop each) and 3% of the other's; all 3 tasks of the Modal smoke test hit the 5-minute limit (nlp #818); every scored bundle of the write-ups' teams at 0.20 or above is a single agent (15 of 15), and sub-agent versions tied or lost | more 31B tasks finished in time | queued |
| **5c** | | [0b7c63b](https://github.com/healthtransformationlab/gemma-developer-agent/commit/0b7c63b) | [gemma-developer-agent](https://github.com/healthtransformationlab/gemma-developer-agent) [`feat/125-distilled-adapter`](https://github.com/healthtransformationlab/gemma-developer-agent/tree/feat/125-distilled-adapter) | E4B | **distilled LoRA** from the 31B (omallo, Apache 2.0, rank 16) in place of copyfix | #125 | 5 | its card: 9.7 → 19.7 of 47 locally (93065), partly trained on the public tasks; against it, 92175, 89814 and 93591 found distilled adapters loop and score lower | a test, not an expected gain; read its loop count too | queued |
| **6** | | [d265a78](https://github.com/healthtransformationlab/gemma-developer-agent/commit/d265a78) | [gemma-developer-agent](https://github.com/healthtransformationlab/gemma-developer-agent) `main` | E4B | drop `get_code_neighbors` and `get_code_subgraph` | PR 115, #113 | 5 | 129 development tasks offline: graph expansion no better than regex (13 / 7 tasks, p = 0.26); leaving tests out helps (p = 0.016) ([`docs/localization-study.md`](https://github.com/healthtransformationlab/gemma-developer-agent/blob/main/docs/localization-study.md)) | about two tool calls a task saved | queued |
| **7** | | [7153a87](https://github.com/healthtransformationlab/gemma-developer-agent/commit/7153a87) | [gemma-developer-agent](https://github.com/healthtransformationlab/gemma-developer-agent) `main` | E4B | edit anchors of 1 to 3 plain lines, one retry | PR 117, #116 | 6 | 252 edits in four runs ([PR 117 review](https://github.com/healthtransformationlab/gemma-developer-agent/blob/main/pull_requests/pr-117-review.md)): anchors with a backslash fail 50% (p = 0.015), of 9+ lines 54% (p = 0.025); 25 of 119 failures are ambiguous matches, which shorter anchors can add to (below) | fewer "not found", possibly more ambiguous | queued |
| **8** | | [5d68ce8](https://github.com/healthtransformationlab/gemma-developer-agent/commit/5d68ce8) | [gemma-developer-agent](https://github.com/healthtransformationlab/gemma-developer-agent) `main` | E4B | delete scratch files before submitting, and 12,288 output tokens | PR 107 (with 106), #104, #105 | 7 | 23 development tasks: 4 of 23 as main; no scratch files in patches, no cut-off answers, no context-window endings | cleaner patches | queued |
| 31B | | [ed11c15](https://github.com/healthtransformationlab/gemma-developer-agent/commit/ed11c15) | [gemma-developer-agent](https://github.com/healthtransformationlab/gemma-developer-agent) [`feat/124-31b-entry`](https://github.com/healthtransformationlab/gemma-developer-agent/tree/feat/124-31b-entry) | **31B** | main `c7d68ea` (the skill, no graph tools, short anchors, scratch cleanup, 12,288) on the 31B, no adapter, 5 minutes and 40 calls a task | #124 | none: the first 31B entry | forum: about 5.5 minutes a task fits the 12 hours; 31B entries in the paper-track write-ups score about 0.13 to 0.24, and the board's top is 0.29 | the main-prize candidate | held: replaced by 31B-b in the second slot (#138), after the smoke test (health-transformation-lab-nlp #818) found every task hitting its 5-minute limit |

Entry 2 is not in the ledger: the account's history lists entries 1 and 3 only.

## Why edits fail (the evidence for entries 5, 5b and 7)

`analysis/edit_failures.py` reads each failed `edit_file` call's own error (#132), then compares each "old_string not
found" with everything the agent had seen in that trace. Over five development-set runs on the same 23 tasks (November
11, PR 100, PR 60, main at 8,192 and PR 107; traces from the kernels' output), `analysis/edit_failures.csv`:

| The tool's error, and the cause | Failed edits | What acts on it |
|---|---|---|
| **not found**, near_copy: a block it read is at least 95% alike | 28 | copyfix (5), `edit.py` (5b) |
| **not found**, paraphrase: 80% to 95% alike, rewritten from memory | 36 | short anchors and one re-read (7); `edit.py` refuses most, by design |
| **not found**, not_read: nothing it read is that close | 19 | short anchors and re-reading (7) |
| **not found**, seen_yet_failed: the exact text was in what it read | 7 | mostly a stale read: an earlier successful edit had changed the file |
| **not found**, whitespace_only or backslash_only | 0 | none needed: a whitespace- or escape-tolerant match would fix nothing |
| **ambiguous**: "Target string occurs N times", the anchor matched more than once | 25 | `edit.py --near` (5b: all 15 replayed applied); the rule to add a neighbouring line (7) |
| **other**: empty old_string, no change to apply, a tool error | 4 | |
| **All** | **119** | |

A shorter anchor fails "not found" less often (PR 117's statistics) but matches more than once more often: entry 7
trades one failure for the other, and its score is read with that in mind. The first version of this table (#126)
counted every failure as "not found" and put most ambiguous matches under seen_yet_failed; this one reads the tool's
own message.

## Choosing the two final submissions

One must be an E2B or E4B entry for the small-model bonus; it is the E4B entry with the most evidence behind it across
all entries and traces, not the single best public score. The other is the owner's choice, the 31B entry the likely
candidate. Both are chosen before December 2, 23:59 UTC.
