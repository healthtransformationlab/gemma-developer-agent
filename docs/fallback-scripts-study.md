# Fallback scripts for finding the code and rescuing failed edits, tested on CPU (November 15, 2026)

Issue #122. The Kaggle GPU hours were nearly spent, so the question was what scripts could fix the E4B agent's two
mechanical failures, shown on CPU, across all four repositories of the competition's development set (67 fastapi,
48 rich, 13 requests, 1 httpx). The scripts ship as the skill `skills/edit-fallback`. One `run_skill_script` call with
no arguments copies them to `/tmp/h/`, and the agent then runs them through `run_command` with a plain string.
Array arguments can hang the tool-call parser (forum topics 746336 and 753973), so no call passes any.

- **`find.py NAME ...`**: the repository's Python files ranked by the issue's names. Tests, docs and examples are
  left out. Each file comes with its matching line numbers.
- **`edit.py FILE [--near LINE]`**: a SEARCH/REPLACE block on stdin, for when `edit_file` fails.

Everything here ran on CPU from public clones of the four repositories, checked out at each task's base commit. Nothing
from the competition's files is committed: the CSVs hold ids, counts and outcomes only. `analysis/fallback_summary.py`
prints every table below from them.

## Why edits fail (the recorded runs)

In the two development-set runs with traces (`devset-max-output-8192`, `devset-prompt98-out8192`; 23 tasks each),
43 of 118 `edit_file` calls failed: 28 with "old_string not found" and 15 with "occurs N times". The agent made a
successful retry after only 7 of the 43. The replay rebuilds each file and applies the calls in order with the
harness's own matcher (`swegemma.edit.apply_replacement`). It gives the recorded outcome for 116 of the 118 calls.
Read by hand, the 28 "not found" are of four kinds:

| Kind | Example | What a fallback should do |
|---|---|---|
| Escaped text | a literal `\n` or `\"` inside `old_string` | undo one level of escaping, then match |
| Copy error | `fastapi.ti.ti.tiangolo.com`; a final "s" dropped (the E4B QAT defect, forum topic 753277) | match the closest place, and keep the file's own copy of the lines not being changed |
| Already applied | the agent resends an edit that worked | say so, so the agent moves on |
| Not in the file | invented code, often 10 or more lines | refuse, and show the closest lines with their numbers |

## edit.py

The order: exact text; then the text with escapes undone; then lines compared ignoring spaces; then the closest
block. The closest block must have similarity 0.8 or more and be at least 0.05 ahead of any other place, and it is
tried only when SEARCH has 8 lines or fewer.

A close match is applied as a three-way merge, with SEARCH as the base. The agent's changes are taken from REPLACE.
Every other line keeps the file's own form, including lines SEARCH left out, so a copy error in SEARCH is never
written into the file. When the file has lines SEARCH left out exactly where REPLACE adds lines, where the change
belongs is a guess, so it refuses. It also reports when REPLACE is already in the file, and lists the line numbers
when SEARCH occurs more than once.

### Test across the four repositories (`analysis/fallback_synth.py`, `fallback_synth.csv`)

Each of the 613 reference-patch hunks in non-test files becomes the edit a model would write. SEARCH is the hunk's
old lines with up to two lines of context; REPLACE is its new lines. Each edit is then damaged the ways real failures
were. Both matchers are scored against the file with that hunk applied: correct, wrong (changed but not as
expected), or refused (unchanged). For "not in the file" and "already done", correct means unchanged.

| Damage | Edits | `edit_file`: correct / wrong / refused | `edit.py` |
|---|---|---|---|
| none | 613 | 613 / 0 / 0 | 613 / 0 / 0 |
| escaped (one JSON-escaped line) | 613 | 613 / 0 / 0 | 613 / 0 / 0 |
| a final "s" dropped | 433 | 5 / 0 / 428 | **300** / 4 / 129 |
| 4 spaces less indentation | 368 | 349 / 16 / 3 | 364 / 1 / 3 |
| one context line left out | 581 | 58 / 19 / 504 | **202** / 59 / 320 |
| tool-call debris (`",`) after the last line | 613 | 0 / 0 / 613 | **463** / 4 / 146 |
| SEARCH from another file | 613 | 613 / 0 / 0 | 609 / 4 / 0 |
| change already made | 613 | 569 / 44 / 0 | 609 / 4 / 0 |
| **all** | 4,447 | 2,820 / 79 / 1,548 | **3,773 / 76 / 598** |

- **Correct:** only `edit_file` got 11 edits right, and only `edit.py` got 964 right (exact McNemar test,
  p ≈ 10⁻²⁶⁸).
- **Wrong:** only `edit_file` got 55 edits wrong, and only `edit.py` 52 (p = 0.85). So `edit.py` is wrong no more
  often than the harness's matcher and right far more often.

It holds in each repository:

| Repository | Edits | `edit_file` | `edit.py` |
|---|---|---|---|
| fastapi | 2,924 | 1,836 / 42 / 1,046 | 2,472 / 43 / 409 |
| rich | 1,246 | 795 / 34 / 417 | 1,052 / 29 / 165 |
| requests | 147 | 96 / 2 / 49 | 135 / 3 / 9 |
| httpx | 130 | 93 / 1 / 36 | 114 / 1 / 15 |

### The length check

The same test was run with no limit on SEARCH length (not committed; `MAX_FUZZY_LINES=1000`):

| Length limit | Correct | Wrong | Wrong against `edit_file` (only it / only `edit.py`) | Slowest call |
|---|---|---|---|---|
| none | 4,048 | 119 | 55 / 95, **p = 0.0014** | 12.2 s |
| 8 lines | 3,773 | 76 | 55 / 52, p = 0.85 | **0.29 s** |

Without the check, `edit.py` is wrong significantly more often than `edit_file`, and one call takes 12 seconds. The
tasks run one after another inside the 12-hour limit (forum topics 743063 and 745805), so that time is not free.

With the check, 275 long synthetic edits that could have been rescued are refused instead. That is the right trade
for the real failures: every long SEARCH that failed in the recorded runs was code that is not in the file. The prompt
also asks for anchors of 1 to 3 lines, since anchors of 9 or more lines failed 54% of the time (#116).

| SEARCH lines | Damaged edits, limit 8: correct / wrong / refused |
|---|---|
| 1-3 | 69 / 0 / 1 |
| 4-6 | 2,175 / 55 / 195 |
| 7-8 | 285 / 16 / 17 |
| 9-12 | 271 / 5 / 147 |
| 13-20 | 196 / 0 / 133 |
| 21 and more | 164 / 0 / 105 |

### The recorded failures (`analysis/fallback_replay.py`, `fallback_replay.csv`)

Each failed call is given to `edit.py` as is, and again with `--near` the middle of the agent's last `read_file`
range of that file:

| Failure | Failed edits | `edit.py`, no hint | with `--near` |
|---|---|---|---|
| not found | 28 | applied 8, already done 5, refused as long 9, refused with closest lines 5, conflict 1 | applied 10, already done 5, long 9, closest 3, conflict 1 |
| occurs N times | 15 | lists the lines 15 | applied 15 |

Only 7 of the 43 have a label, the agent's own later fix. Two of the applied edits land where that fix did. Rescuing
an edit is also not the same as fixing the task: several of these edits were wrong fixes in the right place.

## find.py (`analysis/find_eval.py`, `find_ranks.csv`)

Each task's query is the issue's first five identifiers (`analysis/localize.py`, as in #112). Files are ranked by:
- how many of the names they contain;
- whether they define them (`def`, `class` or a module-level assignment);
- whether a dotted name is their module path.

Tests, docs and examples come last, shown only when nothing else matches. The baseline is the prompt's step 2 before
this change: `grep -rnE … | head -40`, with files taken in order of appearance.

| Repository | Tasks | Right file first: grep / find.py | In the top 3 | In the top 8 |
|---|---|---|---|---|
| fastapi | 67 | 5 / 15 | 12 / 26 | 16 / 36 |
| rich | 48 | 5 / 16 | 14 / 18 | 18 / 27 |
| requests | 13 | 1 / 11 | 4 / 11 | 7 / 11 |
| httpx | 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| **all** | 129 | **12 / 43** | **31 / 56** | **42 / 75** |

- **First place:** only grep ranks the right file first in 3 tasks, only `find.py` in 34 (p = 1.2 × 10⁻⁷).
- **Top 8:** 7 against 40 (p = 1.1 × 10⁻⁶).
- **Speed:** the slowest search took 0.70 seconds.
- **Output size:** `find.py` prints at most 8 files and 3 lines each, which stays well inside the 5,000-character
  output cap.

## End to end in the harness

The harness's own `swegemma eval` ran one task (`htlnlp_68`, from this project's task set) with the subprocess sandbox,
which our Kaggle runs used, and a scripted stand-in for the model (`analysis/harness_check_model.py`). This is
SIMULATED: no model ran, so it shows the plumbing, not the agent.

- **First run: a real defect.** `run_skill_script` ran `install.py`, which reported success, but the next command,
  `python3 /tmp/h/find.py`, failed with "No such file". The subprocess sandbox rewrites `/tmp` inside a command to its
  own folder, which it also sets as `TMPDIR`, while Python code writing to the literal `/tmp/h` reaches the real
  `/tmp`. This is likely the earlier note that skill scripts were unreliable in the harness.
- **The fix:**
  - `install.py` writes the helpers to `/tmp/h` and to `$TMPDIR/h`, and reports the failure when it can write to
    neither.
  - `find.py` searches the current git checkout first.
  - The prompt says what to do without the helpers.
- **After the fix, in order:**
  1. The install succeeded.
  2. `find.py parse_answer` put `python/dental_omop_nlp/llm_reader.py` first, with the `def` line (133).
  3. `edit.py` matched line 133, first with `--dry-run`, then for real; `git diff --stat` showed one file changed.
  4. `submit_patch` gave a patch of 602 bytes with one file changed. Neither the helpers nor the harness's own
     temporary script entered the patch.

The scorer's Docker sandbox runs commands as typed, so `/tmp/h` is the same folder for the install and for the
command. The first leaderboard entry is still the first test on the competition's own machines.

## What changed in the submission

- `skills/edit-fallback/`:
  - `SKILL.md`;
  - `scripts/install.py`, `scripts/find.py` and `scripts/edit.py`, standard library only, parsing as Python 3.8.
- `agent.yaml` gives the skill.
- `prompts/system.md`:
  - **Step 2** installs the helpers (one `run_skill_script`, no other argument), then localizes with `find.py`.
    Grep stays as the fallback, tests left out.
  - **Editing:** after a failed `edit_file`, never send the same `old_string` again; send the change to `edit.py`.
- **Tests:** `tests/test_edit_fallback.py` covers each failure kind above. It also runs `install.py` through ADK's own
  skill wrapper, which needs `google-adk` and is skipped in CI. `tests/test_find.py` covers `find.py`, and
  `tests/test_submission.py` checks the prompt.
- **Compiler:** the competition's compiler (`adk_submission.compile_submission`) loads the submission with both
  skills.

## Limits

- **Synthetic damage is our model of the errors.** It was built from the kinds read in 28 real failures, one damage
  per edit. Real failures can stack several.
- **Thin labels:** the replay has labels for only 7 failed edits.
- **One development set:** four repositories, 129 tasks. The hidden tasks come from other, private repositories
  (forum topic 748428). Nothing here is tuned to one repository, but that is not shown.
- **No resolve rate.** Finding the file and applying the edit are necessary, not enough. Whether the agent calls the
  scripts, and whether more tasks resolve, is for a run.
  - Under AGENTS.md, a run asking why the agent fails goes to the owner's Colab.
  - A change to the score is measured by one leaderboard entry, booked in the shared plan.
- **Cost:** the install is one more tool call per task, out of 40.
