# PR 94 review: freeze the paper as submitted with a tag, a release and a branch (#93)

| Check | Result |
|---|---|
| Branch `ci/93-release-the-paper`, `Closes #93` | ok |
| Merge: the owner asked for a tag, a branch and a release on November 12, 2026, before submitting. Merging runs nothing; the workflow is then run once by hand for `paper-v14`, which is the public tag, release and branch the owner asked for, in this repository only | ok |
| Settings are checked before any work: a tag name that is not `paper-v<n>` and a SHA that is not 40 hex characters each fail at once and name the setting. Run here with one good and three bad sets of inputs: exit 0, then 1, 1, 1 | ok |
| Nothing is written until the commit is known to be on `main`, the tag is known not to sit on another commit, the PDF is there, and `paper/check_rules.py --check` passes at that commit | ok |
| Every write can be repeated: a second run edits the same release and uploads the same file over itself (`--clobber`); the branch is pushed without force, so it only moves forward. Run here against a stand-in for `gh`: `release create --target <sha>` the first time, `release edit` and `release upload --clobber` the second | ok |
| Permissions are `contents: write` and nothing else; the token is the run's own; the three inputs reach the shell as environment variables, never as text inside the script | ok |
| No retry is set, and none is wanted: a wrong setting or a failing rules check must fail at once; the job has a 10-minute limit and one run at a time (`concurrency`) | ok |
| The release's notes, read as the script writes them: what the paper is, the commit, the branch, the tasks' licence, the source repository at a named commit, and the disclaimer. No first person, no organisation named beyond the competition, no private Kaggle resource | ok |
| ADR 0001 gives the context, the decision, its consequences and when to revisit, in the template's four parts; it says why `release/paper-track` is outside the branch-name rule (no pull request is opened from it) | ok |
| The README's new link goes to the newest release, so it needs no change when a later version is released | ok |
| The paper, its PDF and `paper/sources.md` are not touched; `docs/build_decks.py --check` exits 0 | ok |
| No secrets, real data or organisation names | ok |

Nothing blocking.

## Notes
- A workflow cannot be run before it is on `main`, so its first real run is the one that makes `paper-v14`. Its steps
  were run here one by one beforehand; the run's own log is the last check, and it is read before anything is said
  to exist.
- The README's link answers only once that first release exists, a few minutes after the merge.
