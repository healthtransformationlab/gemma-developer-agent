---
pr: 32
branch: docs/31-writeup-title-block-and-format
title: "000 DOCS11: name the author and the competition in the writeup; links and a figure on page 1 (held for the owner)"
author: Claude Code (agent session for jcbowyer)
reviewed_at: 2026-11-10
reviewer: the authoring session (each new line was checked at its source and the PDF was read page by page; no reviewer subagent run)
verdict: approve, held for the owner
---

# PR Review: 000 DOCS11: name the author and the competition in the writeup; links and a figure on page 1 (held for the owner)

## Summary
The writeup did not say who wrote it or which competition it is for, and its links were unlinked names in the last
paragraph. This pull request adds a title block (author, competition and track, topic, date), a "Data and code"
paragraph with three links under the abstract, one figure, the competition's own citation as reference 17, and a
script that lays the text out as a PDF. It adds no number and changes no result. Two sentences are removed because
the new paragraph says the same thing on page 1. Nothing blocking. It waits for the owner because it puts the
owner's name on the paper, and for pull request 30, which it is stacked on.

## Checks
| Check | Result |
|---|---|
| The author's name | "John Bowyer", the author name on this repository's commits. The owner asked for the name; how it should read is theirs to confirm |
| "Gemma 4 Developer Agent Competition, Paper Track" and reference 17 | the "Citation" block of the competition's Overview page as the owner pasted it on November 10, 2026: the ten authors, "Google - The Gemma 4 Developer Agent Competition", the URL, 2026, Kaggle. The paper track is the second competition that page links to |
| "Topic: Tasks & Benchmarks" | the same page's list of paper topics, third item, quoted in `paper/sources.md` |
| The three links | each answered with 200 on November 10, 2026; a made-up dataset address on the same site answered 404, so 200 means the page exists. Licences as the closing paragraph gave them: CC BY 4.0, Apache 2.0, Apache 2.0 |
| Figure 1 adds no number | its ten counts are the Section 4.1 table (197, 116, 113, 93), Section 6 "Results" (48, 40, 5) and Section 6 "Task fairness" (30, 25, 5). All bars share one scale, so the 5 resolved reads as small as it is |
| Figure 1's colour | one hue for one measure; the palette check passes against a light surface (lightness, chroma, contrast at least 3:1). Every bar carries its value, so nothing depends on colour |
| The two removed sentences | "Data, harness and run tables are public." and the closing "Released: ..." paragraph. The new paragraph names the same three releases and licences. "Every run table cited here" is now "run tables" beside the harness repository's link, where they are |
| Three wording changes after an outside review of version 6 | (1) Section 1's "A growing share of code is written by agents under a person's direction" had no measurement or citation behind it; the sentence now describes this repository only, and "leaves an unusually complete record" is "can leave". (2) Section 9's "let others measure that gap" is "let others test other models and settings": the paper does not score the cloud agent on the same statements. (3) The title block says "(resource paper)", the author's own description of the contribution. None changes a number |
| Nothing else changed | the diff of `paper/writeup.md` was read line by line: 9 places, all listed in the pull request |
| Word count | 2,996 without references by `wc` (2,992 before); 2,876 real words; limit 3,000. The title block and the image line are counted |
| Citations and references agree | [1] to [17]: each cited, each listed |
| The PDF | 7 pages, built by `node paper/build_pdf.js` from `writeup.md` as committed. Read page by page at 80 dpi: no table or figure splits across pages, the three links and reference 17 are live, the footer carries the author, title, track and page number. `pdftotext` gives back the abstract word for word |
| The build script changes no word | it wraps the lines before "## Abstract" as the title block, boxes the abstract with the links, swaps the PNG for the SVG, and prints. It fails if the abstract heading, the "Data and code." paragraph or the figure is missing |
| `paper/sources.md` | a new block for the title block, Figure 1 and the PDF; the two removed sentences under "Not in the writeup" |
| Branch name and issue link | `docs/31-writeup-title-block-and-format`, `Closes #31`; `pr_conventions.py` passes |

## Should fix
- Do not merge before pull request 30.
- The owner should confirm the name and whether "Health Transformation Lab" belongs beside it. The disclaimer under
  it still says the project is personal and not affiliated with any employer, institution or vendor.
- The count stands four words under the limit. A result from the run under the competition's evaluator will need
  a cut of its own size.
- The body font in the PDF is Liberation Serif and the headings Inter, the faces installed where it was built. A
  rebuild elsewhere may pick other faces and paginate differently.
- The PDF is committed, so it goes stale when `writeup.md` changes: rebuild it in the same pull request.
- Left for another change: Section 6 says the baseline ran `gemma-4-e4b-it` in fp16, and the competition's list of
  supported variants names the quantised `gemma-4-e4b-it-qat-w4a16-ct`. Section 5's "Known differences" could say
  so in a clause.

## Secrets, Real Data and Claims Scan
Secrets: none. Real data: none; the author's name is public on the repository's commits and no contact detail is
added. Claims: none added about results. The paper now says which competition it is submitted to; submitting is
the owner's act.
