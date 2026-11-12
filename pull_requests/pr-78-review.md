# PR 78 review: what the record holds about reviews; a plain lead-in in the abstract (#77)

| Check | Result |
|---|---|
| Branch `docs/77-reviews-count-and-label`, `Closes #77` | ok |
| Merge: the owner said "Merge" for the paper's pull requests on November 11, 2026, and on November 12 asked that titles such as "fixes were" be made readable. The first change corrects a sentence that said more than its source, which is this repository's first rule for the paper. Merging starts no run and publishes nothing; the Writeup needs pasting again after it, and the PDF swapping | ok |
| The diff of the paper's text is two sentences, read word by word: Section 3's "Each pull request has a committed review (240)" is now "Reviews of 240 pull requests are committed as files", and the abstract's lead-in "Where those fixes were" is now "Which tasks it fixed". No count changes | ok |
| The 240, recounted for this review at the source repository's `b12e2e0` (November 8, where `main` has 960 commits): 240 files match `pull_requests/pr-*-review.md`, each for a different pull request, numbered up to 634 | ok |
| Why the old sentence was wrong, recounted the same way: the first-parent history of `main` at that commit has 362 commits, 305 of which merge a pull request (175 "Merge pull request #n" and 130 squash merges ending "(#n)"). 230 of those pull requests have a review file and 75 do not: 56 merged on October 25 to 27, 11 on October 28 and 8 after it. Ten review files are for pull requests that history does not name | ok |
| The new sentence claims only what the files show. The 305 and the 75 are in `paper/sources.md` and not in the paper: they are counted from commit subjects, not from GitHub's own list of pull requests | ok |
| Nothing else in the paper says every pull request has a review: Section 1's "can leave an unusually complete record: an issue, a pull request and a review for each change" says what such a repository can leave, and the row for the abstract's "CI-enforced record" already says it describes "what the record holds, not that every change has all three" | ok |
| "Which tasks it fixed" is followed by the same sentence as before, which gives the tasks first and the task-runs in brackets. The four lead-ins of the abstract are listed in `sources.md` in their new wording | ok |
| The pasted text is 2,757 words before the references and 2,977 with them (2,756 and 2,976 before); the limit is 3,000 before the references | ok |
| The abstract is 233 words (1,302 characters) and ends on page 1; Figure 1 is on page 1; the PDF is 6 pages and its text holds no dollar sign | ok |
| `check_rules.py --check` exits 0 (15 rows pass); every quoted phrase in `paper/sources.md` is in the paper (109 of 109); `docs/build_decks.py --check` exits 0, so every number on a slide is still in the paper or the README | ok |
| The pitch deck's slide already says "240 written reviews of pull requests" (pull request 76) | ok |
| No first person, secrets, real data or organisation names; the paper names no private Kaggle resource | ok |

Nothing blocking.

## Notes
- The sentence's source row read "240 review files". The row was right and the sentence was not: a check that every
  number has a row does not check the words around the number. A second reader, given the paper as the source of
  truth for the deck, went to the repository and counted.
- The text pasted into the Writeup loads Figure 1 from this repository at one commit. The figure did not change;
  the paste file is made again with this merge's commit all the same.
- The Word copy made for peer review on November 12 has the old two sentences. It is made again from this version.
