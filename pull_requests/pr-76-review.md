# PR 76 review: a README with a role table and a slide deck, in the lab's style (#75)

| Check | Result |
|---|---|
| Branch `docs/75-readme-roles-slides`, `Closes #75` | ok |
| Merge: the owner asked for this README on November 12, 2026 ("Create a nicely formatted readme with role drilldowns with slides like nlp"), and had said "Merge" for the paper's pull requests on November 11. The README is the page the paper links to. Merging starts no run and publishes nothing outside this repository | ok |
| No number changes. The paper, its PDF, `paper/sources.md` and `paper/rules_check.md` are not in the diff, so the Kaggle Writeup needs no new paste | ok |
| The README keeps what `paper/sources.md` says it keeps: the run table (the larger-budget run among its rows) and the time bullet (a task's GPU-seconds and watt-hours on the four L4s, the graph tools' share of time). The diff of the README adds a top and a "Run it" section and removes nothing below them but the old top, whose question and table of ingredients now stand under "The question behind the agent" | ok |
| The three headline results in the README each name their run and carry their interval or their label: 5 of 48 (10.4%, 95% CI 4.5–22.2); 4, 6 and 4 of 93 with "No difference detected (exact McNemar p = 0.5 and 1.0)" and "from the hidden test: not a benchmark condition"; 8 of 17 against 1 of 76 with "Described, not tested". The limits are one click away | ok |
| Every number on a slide, in its text or its notes, is one the paper or the README has: `python docs/build_decks.py --check` exits 0, and was seen to fail before the deck was built and drawn | ok |
| The check compares number by number, not sentence by sentence, so each slide's statements were also read against the paper by a second reader working alone (below). The titles and labels were reworded after that reading; the reworded text was read against the paper again for this review | ok |
| The slides say what the paper says about what is and is not shown: "No difference detected", "Described, not tested", "The second comparison was made after the runs", "from the hidden test … not a benchmark condition", "one repository and one model", "no partner has been contacted", and a slide of the paper's six limits | ok |
| The cost slide gives prices as the paper does, in words and as "rental estimates, not money spent"; no dollar sign is in the deck, the README or the new page | ok |
| `deck.html` pages in a browser from a file, with no script from elsewhere: keys, buttons, the picker, the notes panel, a link to one slide and a swipe were driven at desktop and phone size, with no script error. Its fonts come from Google Fonts when the network allows and fall back to the system's otherwise | ok |
| The twelve slide images were looked at one by one; none is cut off (the renderer reports a slide whose content runs past its edge). `deck.pdf` has 12 pages | ok |
| `docs/agent_walkthrough.md` against the files it describes: the nine tools, the analyzer as a tool with `skip_summarization`, the prompt's four parts, the sampling values and the file's own reasons, the four budgets beside the harness's defaults (from `docs/rulebook-notes.md`), the skill, and the three observations, each already in the README or the paper | ok |
| Every relative link in the README, the walkthrough and the notes page resolves, anchors included (81 links) | ok |
| The new workflow runs the deck check on changes to `docs/`, the README or the paper's text, so a number that leaves the paper while a slide still carries it fails the pull request that removes it | ok |
| No first person outside the disclaimer the source repository's README also carries, no secrets, no real data, no organisation named as a partner; the deck names no private Kaggle resource | ok |
| The owner then read the slides and could not follow titles such as "The fixes were where the statement says what the tests check", and asked that titles be readable and say what their numbers mean. Every title is now a plain sentence with its numbers in it ("The model fixed 8 of the 17 clearly described tasks, and only 1 of the other 76"), every large number has a label above it saying what is counted, and plain words come first with the paper's term once in brackets: fixed (resolved), description (statement), scoring program (evaluator), clearly described tasks (the core split), a list of code to look at (graph retrieval), planned in advance (pre-registered). The README's three headline results are worded the same way | ok |

Nothing blocking.

## A second reader's findings

A second reader, given the paper as the source of truth, checked every statement on the slides, in their notes, in
the engineers' page and in the README's new top. It found eleven things. All were acted on before this review was
written; the first is also a slip in the paper, which gets its own change.

| Finding | What changed |
|---|---|
| "240 pull requests, each with a committed review": 240 counts the review files. At the commit of November 8 the source repository has 305 merged pull requests on `main`, and 75 of them have no review file (recounted for this review: 305, 240 and 75) | the slide says "240 written reviews of pull requests, kept in the project". The paper's Section 3 says "Each pull request has a committed review (240)", which is the same slip: issue 77 |
| The notes said the experiment on one A100 had a plan "fixed before any result". That is the plan for Kaggle (source repository, issue 674); the A100 runs were under addenda hashed before each started, with Kaggle's outcome known | the notes say so: registered in advance, then run again on one A100 under additions fixed before each run started |
| "The unplanned second session is ... never added to" the planned experiment, while the main finding's 26 of 85 counts both sessions | "kept out of its tests. A count that covers both says five runs" |
| "cannot install test dependencies, so 23 of the 40 can be verified": the paper gives no "so" | the paper's own account: the reference patch fails 16 of the 40 and one passes with an empty patch, leaving 23 |
| "an issue, a pull request and a review for every change is what made this history usable": a cause, and 45 candidates had no issue and 22 no pull request | "this repository's issues, pull requests and commit messages are where its task descriptions come from" |
| "3 of 23" stood under a label about free T4 GPUs; that run used four L4s, and the 23 are the verifiable ones | "3 of the 23 verifiable tasks of the competition's own ... on four L4 GPUs" |
| "197 merged changes mined" left out that they are the changes as of October 29, 2026: the first five of the fifteen days | the bar and the notes give the date |
| The title "More context did not reliably help" is stronger than the paper's "no difference is claimed or ruled out", and set the experiment beside another run's 5 of 48 | "Alone, the model fixed 5 of 48 tasks. In a planned experiment, extra help showed no reliable improvement." |
| "Each number on a slide is the paper's": the check only shows that each number appears somewhere in the paper or the README | every place says that: the README, the engineers' page, the slide, and the deck's own notes |
| The engineers' page said the entry has "no code of its own" and that the skill classifies "from those tables". The skill ships `scripts/classify.py`, which matches words in the issue's text and reads the runbook | the page says what the script does, and that it is the entry's one piece of code |
| `node paper/build_pdf.js` needs pandoc as well as Playwright | the README says so |

## Notes
- The deck is new prose about the paper's results, written the day the paper was due. It is guarded two ways: a
  check that every number appears in the paper or the README, and a second reader for the sentences. Neither replaces reading a slide
  before presenting it.
- The repository grows by about 2.7 MB: twelve slide images, a cover and a PDF. They are built files, kept so that
  the README and the notes page show the slides on GitHub without a download.
- `deck.html` does not use the slide library the source repository's decks use. That library is loaded from a
  content network, and this deck has to open from a downloaded file; it also could not be reached from where the
  deck was built, so it could not have been tested.
- One tracked file does not belong: `paper/__pycache__/check_rules.cpython-313.pyc`, committed in pull request 38.
  It is left for its own small change.
