# PR 119 review: the rule notes say what the prizes are, and where the small-model standings are (#118)

| Check | Result |
|---|---|
| Branch `docs/118-prizes-and-final-submissions`, `Closes #118`; issue 118 has its Problem, Done when, Contract and Read first | ok |
| The prize terms match the Overview page as the owner pasted it on November 15: main $37,000 / $18,000 / $10,000; the small-model bonus $10,000 to the highest-ranking E2B or E4B submission, one of the two selected final submissions, still eligible for the main prizes | ok |
| The standings snapshot is read from the host notebook's `leaderboard.csv` (November 14, 23:55 UTC): 0.12 for the top two, 0.10 for the next ten, `jcblearning` 699th of 1,035 at 0.05; labelled as public scores on about half the hidden tasks | ok |
| One submission a day matches the competition's API (`maxDailySubmissions` 1); the deadlines, the 12-hour limit and the L4x4 quota rate match the pasted page | ok |
| Docs only: no submission file changes; `python paper/check_rules.py --check` exits 0; `python -m pytest -q tests`: 19 passed | ok |
| No secrets, real data or organisation names | ok |

Nothing blocking.

## Notes
- "About 58 hidden tasks on the public half" is the other session's estimate, also in `health-transformation-lab-nlp`
  AGENTS.md; the Overview page gives no task count.
- The snapshot dates; the notebook is the source to read again before choosing the final submissions.
