# The leaderboard plan

One table for every entry of this repository's agent in the Gemma 4 Developer Agent competition: the commit, the one
change it measures, the evidence behind the change, and its score. Issue #126; the decisions behind it are in
health-transformation-lab-nlp ADR 0007. Scores come from the ledger, health-transformation-lab-nlp
`data/tasks/leaderboard_entries.csv`, which a workflow there refreshes every two hours.

## The rules

- **One change per entry.** Each queued entry differs from the entry named in "Compared with" by one change, so the score
  difference is that change's effect. The public score is about 58 hidden tasks, and the same submission varies by about
  ±1.6 of them (paper track write-ups 91230 and 93326), so a difference of one or two tasks is noise; a change is judged
  on every entry and trace that bears on it, never on one score.
- **One pending entry at a time.** Kaggle refuses a new submission while one is pending ("Your team already has 1 pending
  submissions"), and scoring machines are short (forum topic 747519). Entries go in this order, each when none is
  pending; an agent session's scheduled queue reads the order from this page.
- **Gates.** If entry 5 (copyfix) scores 0.00 or errors, the entries that carry copyfix (5b, 6, 7, 8) wait and versions
  without the adapter are proposed; the 31B and 5c carry no copyfix and still go. If the 31B entry runs past the 12-hour
  limit, its per-task budget is shortened before December 2.
- **Built from a fresh checkout**, with no `__pycache__` or `.pyc` (the evaluator refuses them), named `submission.zip`.

## Entries

| Entry | Ref | Commit | Model | The one change | PR / issue | Compared with | Evidence before submitting | Expected | Score |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 58290615 | | E4B | one agent, answer cap 6,144, 4.5 minutes | | | | | **0.05** |
| 3 | 58333590 | | E4B | lean prompt, no `submit_patch` | | 1 | | | **0.03** |
| 4 | 58364801 | 76bc6d6 | E4B | localize-first prompt (PR 98) and an 8,192-token answer cap (PR 100) | #97, #99 | 1 | 23 development tasks: 4 of 23 against 3 (p = 1.0); no context-window endings (health-transformation-lab-nlp `data/tasks/official_agent_runs/`) | small | pending (submitted Nov 15, 02:18 UTC) |
| **5** | | 9c9cd3a | E4B | **copyfix**, a training-free rank-128 LoRA for the QAT model's copying defect | PR 109, #108 | 4 | copy failures 15 → 1 of 18 on Kaggle's vLLM (write-up 90715); another team 0.05 → 0.10, repeat 0.05 (92175); our traces: 37% of edits fail "old_string not found", 33 of 119 failures are near-copies (below) | fewer failed edits | queued |
| **5b** | | 80d23e8 | E4B | **edit-fallback skill**: `find.py` ranks the code to fix, `edit.py` rescues a failed edit | PR 123, #122 | 5 | CPU only: right file first in 39 of 129 development tasks against grep's 12; damaged edits right 3,739 against `edit_file`'s 2,820, wrong 62 against 79 (`docs/fallback-scripts-study.md`); a harness run with a scripted model installs, finds, edits and submits | the largest of these | queued |
| **31B** | | ed11c15 | **31B** | main `c7d68ea` (the skill, no graph tools, short anchors, scratch cleanup, 12,288) on the 31B, no adapter, 5 minutes and 40 calls a task | #124 | none: the first 31B entry | forum: about 5.5 minutes a task fits the 12 hours; 31B entries in the paper-track write-ups score about 0.13 to 0.24, and the board's top is 0.29 | the main-prize candidate | queued |
| **5c** | | 0b7c63b | E4B | **distilled LoRA** from the 31B (omallo, Apache 2.0, rank 16) in place of copyfix | #125 | 5 | its card: 9.7 → 19.7 of 47 locally (93065), partly trained on the public tasks; against it, 92175, 89814 and 93591 found distilled adapters loop and score lower | a test, not an expected gain; read its loop count too | queued |
| **6** | | d265a78 | E4B | drop `get_code_neighbors` and `get_code_subgraph` | PR 115, #113 | 5 | 129 development tasks offline: graph expansion no better than regex (13 / 7 tasks, p = 0.26); leaving tests out helps (p = 0.016) (`docs/localization-study.md`) | about two tool calls a task saved | queued |
| **7** | | 7153a87 | E4B | edit anchors of 1 to 3 plain lines, one retry | PR 117, #116 | 6 | 252 edits in four runs: anchors with a backslash fail 50% (p = 0.015), of 9+ lines 54% (p = 0.025) | fewer failed edits | queued |
| **8** | | 5d68ce8 | E4B | delete scratch files before submitting, and 12,288 output tokens | PR 107 (with 106), #104, #105 | 7 | 23 development tasks: 4 of 23 as main; no scratch files in patches, no cut-off answers, no context-window endings | cleaner patches | queued |

Entry 2 is not in the ledger: the account's history lists entries 1 and 3 only.

## Why edits fail (the evidence for entries 5, 5b and 7)

`analysis/edit_failures.py` compares each failed `edit_file` call ("old_string not found") with everything the agent
had seen in that trace. Over five development-set runs on the same 23 tasks (November 11, PR 100, PR 60, main at 8,192
and PR 107; traces from the kernels' output), `analysis/edit_failures.csv`:

| Cause | Failed edits | What acts on it |
|---|---|---|
| near_copy: a block it read is at least 95% alike | 33 | copyfix (5), `edit.py` (5b) |
| paraphrase: 80% to 95% alike, rewritten from memory | 36 | short anchors and one re-read (7); `edit.py` refuses most, by design |
| not_read: nothing it read is that close | 22 | short anchors and re-reading (7) |
| seen_yet_failed: the exact text was in what it read | 24 | unexplained: the file may have changed through `run_command`; worth a look |
| backslash_only | 4 | short anchors (7) |
| whitespace_only | 0 | none needed: a whitespace-tolerant match would fix nothing |
| **All** | **119** | |

## Choosing the two final submissions

One must be an E2B or E4B entry for the small-model bonus; it is the E4B entry with the most evidence behind it across
all entries and traces, not the single best public score. The other is the owner's choice, the 31B entry the likely
candidate. Both are chosen before December 2, 23:59 UTC.
