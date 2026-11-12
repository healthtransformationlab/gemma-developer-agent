# PR 84 review: the slides shown in the README; docs/ ready to be served as a page (#83)

| Check | Result |
|---|---|
| Branch `docs/83-slides-from-readme`, `Closes #83` | ok |
| Merge: the owner asked on November 12, 2026 how to make the HTML slides show from the README, and said "Merge" for the paper's pull requests on November 11. The README is the page the paper links to. Merging starts no run and publishes nothing outside this repository: the two site files do nothing until the owner turns GitHub Pages on | ok |
| The README shows all twelve slides in a fold below the cover, each image with the slide's title as its text for screen readers, and a link to the page that has the speaker notes. Nothing else in the README changes | ok |
| `python docs/build_decks.py --check` exits 0, and was seen to exit 1 with "README.md shows the slides and misses docs/pitch/img/03-problem.png" when that line was taken out of the README | ok |
| `docs/.nojekyll` is empty, and `docs/index.html` is a page that sends the reader on to `pitch/deck.html`. With Pages serving `/docs` from `main`, the deck, its images and its PDF are at the same paths as in the repository, less the `docs/` | ok |
| The deck itself needs nothing from elsewhere to page (its own script and styles are inside it); its two fonts come from Google Fonts when the reader's network allows, and fall back otherwise | ok |
| All 64 links in the README resolve. The fold was rendered at phone width, opened, and looked at | ok |
| The paper and its files are not in the diff | ok |
| No first person, secrets, real data or organisation names | ok |

Nothing blocking.

## Notes
- What the owner asked for has a second half that is not in this pull request and cannot be: GitHub Pages is a
  repository setting. Until it is on, the README's "slides" link still opens the HTML file's source on GitHub, and
  says to download it. The fold is what makes the slides show today.
- The lab's own site is served from another repository. A project site for this repository would sit under it, at
  `/gemma-developer-agent/`, if GitHub serves project sites under the organisation's domain as it does by default.
  That was not tried here, since the setting is off: the address is checked once the owner turns it on, before the
  README's link is changed to it.
- The cover is in the README twice once the fold is open: as the picture that leads to the notes, and as slide 1.
