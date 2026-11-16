# PR 175 review: 31B-d2-5m scored 0.12; the public 31B bundle goes next and E4B-all is held (#174)

Reviewed by the author session against `AGENTS.md`, `.conventions/AGENTS-common.md` and the submission rules
(`docs/rulebook-notes.md`).

| Check | Result |
|---|---|
| Branch `docs/174-31b-public-next-e4b-held`, `Closes #174`, issue with its four parts before the first commit | ok |
| Test first: the four changed or new tests failed on main's plan (4 failed, 14 passed), then 101 passed, 1 skipped | ok |
| The score is checked at the source: ref 58406723 reads 0.12 on the owner's screenshot of the board and in the other session's read of the submission list | ok |
| The board's counts are recounted from Kaggle's download of November 16, 16:58 UTC: 5,896 teams, 1,118 at 0.18, 1,075 at 0.17, 518 at 0.20, 102 at 0.22, 635 at 0.20 or above | ok |
| The four hashes are recomputed from the notebook as pulled on November 16 | ok |
| The owner's words are quoted, with the date; the decision is in ADR 0002, not only in the issue | ok |
| No file of the bundle is committed (the notebook states no licence); no competition task text | ok |
| No number presented as a result that isn't one: the entry's own score is named as what this queues | ok |
| Secrets, data, claims | none |

## Findings

None blocking.

- **Risk, accepted: this entry is not one change.** Against 31B-d2-5m it differs in the prompt, the skill, the first two
  calls and the time cap, so its score can't be split among them. That is the point: it is a baseline. The row says so,
  and ADR 0002's amendment records it as an exception beside the two stacks. `AGENTS.md` still says "one change per
  leaderboard entry … except the two final candidates" and points at ADR 0002, which now carries the third case.
- **Risk, accepted: running time.** 120 tasks at 8 minutes is 16 hours if every task uses all of it. The notebook says a
  scored run with these caps finished inside 12 hours, and our own 31B at 8 minutes on a Modal A100 averaged 209 s a
  task. The scorer's four L4s are not an A100, so the kill criterion names "over 12 hours: cut its 8 minutes".
- **Risk, open: one score is ±2–3 tasks.** A 0.17 and a 0.20 from this entry are the same result. The kill criterion
  asks for a repeat only under 0.15; the development-set run of the same bundle on Colab (health-transformation-lab-nlp
  #849) is the second reading.
- **Nit, left as is.** The Modal figures in the evidence cell (209 s, 7 of 23; 13 of 33 at the cap, 8 with no patch)
  are read from the two runs' traces in their Kaggle datasets, which the cell names. Their per-task tables
  (`analysis/devset_traces.py`) are not committed here yet; they belong with the full four-chunk run when it finishes.
- **Not ours.** The bundle is another participant's public notebook, used the way its own text says to use it. The rule
  added here says a final candidate is still ours to build.

## Verdict

Approve. It starts no GPU run and changes no setting. Merging it makes the submission queue's next entry the public
bundle, when the daily slot opens at 00:00 UTC on November 17, which is what the owner chose. Merge when the checks are
green.
