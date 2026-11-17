# PR 177 review: book the November 18 slot: repeat 31B-public (#176)

Reviewed by the author session against `AGENTS.md`, `.conventions/AGENTS-common.md` and the submission rules
(`docs/rulebook-notes.md`).

| Check | Result |
|---|---|
| Branch `docs/176-book-31b-public-repeat`, `Closes #176`, issue with its four parts before the first commit | ok |
| Test first: the new test and the changed one failed on main's plan (2 failed, 17 passed); then 102 passed, 1 skipped | ok |
| 31B-public is pending at the source: `kaggle competitions submissions` at 10:34 UTC lists ref 58448837, `SubmissionStatus.PENDING`, submitted 00:05:34 UTC | ok |
| 8 against 5 minutes recounted from the `result.json` files of `jcblearning/htlnlp-colab-official-devset-c31be8-c1` to `-c3` and the Modal runs `devset-m31be-c1` to `-c3`, matched on task id: 97 shared, 25 against 27 | ok |
| Big-fix rule recounted the same way: `devset-cpubbig-48` against `devset-cpub-c1` to `-c4`, 48 shared, 14 against 14 | ok |
| 12 against 12 on our own NLP repository is the other analysis session's grading with the verifier on CPU, not recounted here; the row says how it was graded | noted |
| One change per entry: a repeat changes nothing, and the row says it is not expected as a gain | ok |
| The 8-against-5 comparison is across machines (Colab against Modal); the row says so | noted |
| The four file hashes are 31B-public's, unchanged | ok |
| No secrets, no task text | ok |

## Verdict

Ready to merge once CI is green. It books a slot and submits nothing; the submission at 00:00 UTC follows the row.
