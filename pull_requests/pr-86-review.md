# PR 86 review: the README's slides link plays the deck (#85)

| Check | Result |
|---|---|
| Branch `docs/85-play-the-deck`, `Closes #85` | ok |
| Merge: the owner turned GitHub Pages on, said "Done test" on November 12, 2026, and had asked how to make the HTML slides show from the README. Merging starts no run. The page is public because the owner's setting made it so; this pull request only links to it | ok |
| The address was seen to answer before any link was changed: `https://healthtransformationlab.org/gemma-developer-agent/pitch/deck.html` returns 200 as `text/html`, and its bytes are those of `docs/pitch/deck.html` on `main` | ok |
| The live deck was driven in a phone-sized browser: it opens on the cover, the Next button and a swipe both page, its two fonts load, and no script error is raised. The site's front page lands on the deck | ok |
| The deck's PDF, its slide images and the cover picture answer at the same site | ok |
| In the README, the cover picture and the first link in the executives' row open the live deck, and a line under the cover gives the three ways to see the slides: play them, read them with notes, or open the PDF. The words "(download and open in a browser)" are gone | ok |
| The page with every slide and its notes links the live deck too; it is written by `docs/build_decks.py`, which now holds the site's address in one place. `deck.html` itself is unchanged, so the slide images and the PDF are still the ones drawn from it; `python docs/build_decks.py --check` exits 0 | ok |
| The paper and its files are not in the diff | ok |
| No first person, secrets, real data or organisation names | ok |

Nothing blocking.

## Notes
- The link is to the lab's own domain, which is where GitHub serves this repository's pages. If that domain ever
  changes, the address in `docs/build_decks.py` and three links in the README change with it.
- GitHub Pages now serves everything under `docs/`, not only the deck: the notes on the rules, the dataset format
  and the starter notebook are reachable as files at the same site. All of it was already public in the repository.
