# PR 194 review: the architecture page's Side by side tab drills into each part of the picture

Closes #192. Files: `docs/architecture/index.html`, `tests/test_architecture_page.py`.

## Findings (verified)

- ✅ Each line's box was read off the picture (3236 × 1673) and checked in a browser: agent, cause and showed zoom onto their own parts.
- ✅ The deep link, the line click and the picture click were all exercised in headless Chromium, with no console errors and no phone-width horizontal scroll.
- 🟡 Should fix later: the boxes are hand-set fractions. If the drawio picture is redrawn, they must be re-read (the test checks only that they're inside the picture).
- 🔵 Nit: on a narrow phone the zoomed "showed" column is tall and thin, so it zooms less than the others.

## Compliance

| Rule | Result |
|---|---|
| Test first | ✅ the new test failed on 3 of 5 before the change |
| Self-contained page | ✅ no external script or font |
| Publishes outside the repo | waits for the owner's "merge" |

## Verdict

Approve with nits.
