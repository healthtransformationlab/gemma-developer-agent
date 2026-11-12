# PR 92 review: Section 3 accounts for all 960 commits again (#91)

| Check | Result |
|---|---|
| Branch `docs/91-all-960-commits`, `Closes #91` | ok |
| Merge: the owner asked for this correction on November 12, 2026, and said "Merge" for the paper's pull requests on November 11. Merging starts no run and publishes nothing; the Writeup needs pasting again after it, and the PDF swapping | ok |
| The diff of the paper's text is two sentences, read word by word. Section 3 again reads "775 are marked as agent-authored; the rest are merge commits (175), a bot's (5), the author's (4) and the initial one", the sentence of version 12. Section 8 reads "Retrieval's two extra fixes do not establish a reliable improvement", without its bracket on the second session | ok |
| The counts add up: 775 + 175 + 5 + 4 + 1 = 960. Their source row is the one version 12 had (the 250 commits without a trailer, grouped by author, committer and subject, at the source repository's `b12e2e0`) | ok |
| Nothing is lost with the bracket: the abstract has "an unplanned second session on an L4 resolved 5 and 8", and Section 6 has the session's counts, its p of 0.375 and that it is described, not tested. `paper/sources.md` keeps how the three is counted | ok |
| The pasted text is 2,763 words before the references and 2,983 with them (2,761 and 2,981 before); the limit is 3,000 before the references. The owner asked on November 11 for more margin than 2,994, which is why the restored words are paid for | ok |
| The abstract is unchanged (232 words, 1,303 characters) and ends on page 1; Figure 1 is on page 1; the PDF is 6 pages and its text holds no dollar sign | ok |
| `check_rules.py --check` exits 0 (15 rows pass); every quoted phrase in `paper/sources.md` is in the paper (112 of 112); `docs/build_decks.py --check` exits 0 | ok |
| No first person, secrets, real data or organisation names; the paper names no private Kaggle resource | ok |

Nothing blocking.

## Notes
- Version 13 kept the merge commits so that "without typing code" had its support, and stopped ten commits short.
  The second reader of pull request 88 had recounted all 185 and suggested the short form; the owner's reading is
  the better one: a count that starts "Of 960" should end at 960.
- The paste file and the Word copy are made again from this merge's commit.
