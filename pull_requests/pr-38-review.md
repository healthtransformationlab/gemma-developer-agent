# PR 38 review: check the paper against the competition's rules; cut it to 2,780 words (#37)

| Check | Result |
|---|---|
| Branch `docs/37-...`, `Closes #37` | ok |
| Every automated rule row PASS; failure cases (3,001 words, a tracked HARNESS_README) FAIL | ok |
| Same table under CI's pinned pypdf 6.1.3 and local 6.17 | ok |
| Paper cut changes no number or claim; every number still has its row in `sources.md` | ok |
| PDF rebuilt from the text by `build_pdf.js`, 7 pages, page 1 checked by eye | ok |
| OWNER rows named plainly, not marked as passing | ok |

## Notes
- The check is a reading of the rules, not legal advice; the forum post (3.6.b) and the paper track's AI policy are
  the owner's to confirm before submitting.

## Blocking
None.
