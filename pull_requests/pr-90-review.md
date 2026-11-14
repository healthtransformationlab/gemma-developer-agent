# PR 90 review: the README and slide 6 say the clearly described tasks are also the smaller ones (#89)

| Check | Result |
|---|---|
| Branch `docs/89-size-of-fixes-readme-deck`, `Closes #89` | ok |
| Merge: the README and the deck are the owner's requests of November 12, 2026, and this keeps them level with the paper merged the same day (pull request 88). Merging starts no run. The project's page is served from `docs/` on `main`, so the live deck updates; nothing else is published | ok |
| Every count added is in the paper's Section 6 and has a row in `paper/sources.md`: 6 of 17 and 0 of 76 in the three registered runs; a median of 2 files against 10.5; 8 of 12 against 1 of 28 among tasks whose fix changes 5 files or fewer; no task with a larger fix resolved | ok |
| The README gives one row per number, in two tables with short cells; at 390 pixels wide no table runs off the side | ok |
| The README says the size count was made after the runs and tests nothing; the slide's strip says the same ("the size check was made after the runs") | ok |
| Slide 6, looked at in its render: the new paragraph fits in the old one's place, and nothing runs off the slide. The comparison within the 41 tasks left the slide for the speaker notes, which now say that most of the other 34 are large changes | ok |
| `python docs/build_decks.py --check` exits 0: `deck.html`, `full_text_and_notes.md`, the images and `deck.pdf` are from this build, and every number on a slide is in the paper or the README | ok |
| Only slide 6's image changed among the twelve; the cover is unchanged | ok |
| The paper, its PDF and `paper/sources.md` are not touched | ok |
| No secrets, real data or organisation names | ok |

Nothing blocking.

## Notes
- "Fixed" is the README's and the deck's word for the paper's "resolved", as the README says at the top of its results.
- The slide's title is unchanged: 8 of the 17 against 1 of the other 76 is still the count, now with what else
  differs between the two groups said beside it.
