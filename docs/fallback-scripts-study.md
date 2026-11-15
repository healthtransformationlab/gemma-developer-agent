# Fallback scripts for finding the code and rescuing failed edits, tested on CPU (November 15, 2026)

Issue #122. The Kaggle GPU hours were nearly spent, so the question was what scripts could fix the E4B agent's two
mechanical failures, shown on CPU.

- **What decides:** the competition's own development set, 129 tasks from four repositories (67 fastapi, 48 rich,
  13 requests, 1 httpx).
- **The generality check:** this organisation's own repositories, 255 tasks from health-transformation-lab-nlp,
  pipeline-doctor, gemma-developer-agent and getcommunityone/open-navigator.

The scripts ship as the skill `skills/edit-fallback`. One `run_skill_script` call with no arguments copies them to
`/tmp/h/`, and the agent then runs them through `run_command` with a plain string. Array arguments can hang the
tool-call parser (forum topics 746336 and 753973), so no call passes any.

- **`find.py NAME ...`**: the repository's Python files ranked by the issue's names. Tests, docs and examples are
  left out, and top-level `scripts/` and `benchmarks/` rank a little lower. Each file comes with its matching line
  numbers.
- **`edit.py FILE [--near LINE]`**: a SEARCH/REPLACE block on stdin, for when `edit_file` fails.

Everything ran on CPU from git clones, checked out at each task's base commit. Nothing from the competition's files is
committed: the CSVs hold ids, file names, counts and outcomes only. `analysis/fallback_summary.py` prints every table
below from them.

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

The other session classified all 119 such failures from five development-set runs against what the agent had read:

| Kind of failure | Failures | Share |
|---|---|---|
| Near-copies (similarity 0.95 or more) | 30 | 25% |
| Paraphrases (0.80–0.95) | 29 | 24% |
| Text in nothing the agent read | 32 | 27% |
| Exact text it had seen | 24 | 20% |
| Escaping only | 4 | 3% |

`edit.py` is built to rescue the near-copies and escaping, and to refuse the paraphrases and invented text rather than
guess.

## edit.py

It tries SEARCH in three forms, in this order:
1. as written, blank lines at either end included;
2. trimmed of blank lines, and without a last line of tool-call debris (`",`);
3. with one level of escapes undone.

For each form it tries an exact match, then a match ignoring spaces. Then, for a SEARCH of 8 lines or fewer, it tries
the closest block: similarity 0.8 or more, and at least 0.05 ahead of any other place. `--near` only breaks a
near-tie.

A close match is applied as a three-way merge, with SEARCH as the base. The agent's changes come from REPLACE, and
every other line keeps the file's own form, so a copy error in SEARCH is never written into the file. Wherever the
merge would be a guess, it changes nothing and prints the file's lines instead:
- the file has lines SEARCH left out where REPLACE adds lines;
- REPLACE changes part of a block the file has in a different form;
- REPLACE changes a SEARCH line the file doesn't have, or adds lines next to one;
- the indentation shift disagrees between lines (only SEARCH's first line may differ, as when it was copied from
  mid-line);
- tabs are mixed with spaces.

Lines are split on newlines only, and each keeps its own carriage return. "Already done" is reported only where
REPLACE sits at the place the change would go. An edit that would leave a `.py` file unable to compile is refused
(#144), but only when the file compiled before the edit, so a sandbox Python older than the repository's syntax never
causes a refusal. 2 of the 37 non-empty patches in our two recorded runs didn't compile. Output starts with
`NOTHING WRITTEN` when the file is unchanged, and the exit code is 0 either way, because the harness repeats a
failing command's output.

### Test across the four repositories (`analysis/fallback_synth.py`, `fallback_synth.csv`)

Each of the 613 reference-patch hunks in non-test files becomes the edit a model would write. SEARCH is the hunk's
old lines with up to two lines of context; REPLACE is its new lines. Each edit is then damaged the ways real failures
were. Both matchers are scored against the file with that hunk applied: correct, wrong (changed but not as
expected), or refused (unchanged). For "not in the file" and "already done", correct means unchanged.

| Damage | Edits | `edit_file`: correct / wrong / refused | `edit.py` |
|---|---|---|---|
| none | 613 | 613 / 0 / 0 | 613 / 0 / 0 |
| escaped (one JSON-escaped line) | 613 | 613 / 0 / 0 | 613 / 0 / 0 |
| a final "s" dropped | 433 | 5 / 0 / 428 | **303** / 1 / 129 |
| 4 spaces less indentation | 368 | 349 / 16 / 3 | 364 / 1 / 3 |
| one context line left out | 581 | 58 / 19 / 504 | 173 / 19 / 389 |
| tool-call debris (`",`) after the last line | 613 | 0 / 0 / 613 | **471** / 0 / 142 |
| SEARCH from another file | 613 | 613 / 0 / 0 | 612 / 1 / 0 |
| change already made | 613 | 569 / 44 / 0 | 593 / 20 / 0 |
| **all** | 4,447 | 2,820 / 79 / 1,548 | **3,742 / 42 / 663** |

- **Correct:** only `edit_file` got 23 edits right, and only `edit.py` 945 (exact McNemar test, p ≈ 10⁻²⁴⁵).
- **Wrong:** only `edit_file` got 62 edits wrong, and only `edit.py` 25 (p = 9.1 × 10⁻⁵).
- **"One context line left out":** this was the one damage where `edit.py` erred more (35 wrong against 19) until the
  compile check (#144). It is now 19 against 19. When the agent leaves a line out, where its change goes can look
  clear when it isn't, and the result often doesn't compile.
- **Entry 5b's numbers:** the queued commit `80d23e8` was built before the compile check. Its numbers on this test are
  the ones the leaderboard plan cites: right 3,739, wrong 62, refused 646.

| Repository | Edits | `edit_file` | `edit.py` |
|---|---|---|---|
| fastapi | 2,924 | 1,836 / 42 / 1,046 | 2,447 / 22 / 455 |
| rich | 1,246 | 795 / 34 / 417 | 1,049 / 18 / 179 |
| requests | 147 | 96 / 2 / 49 | 134 / 2 / 11 |
| httpx | 130 | 93 / 1 / 36 | 112 / 0 / 18 |

### The length check

The same test was run with no limit on SEARCH length (not committed; `MAX_FUZZY_LINES=1000`):

| Length limit | Correct | Wrong | Wrong against `edit_file` (only it / only `edit.py`) | Slowest call |
|---|---|---|---|---|
| none | 4,016 | 56 | 62 / 39, p = 0.028 | 0.51 s |
| 8 lines | 3,742 | 42 | 62 / 25, p = 9.1 × 10⁻⁵ | 0.23 s |

Both rows include the compile check (#144). The limit refuses 274 long synthetic edits that could have been rescued.
In exchange it gets 14 fewer wrong. That is
the right trade for the real failures: every long SEARCH that failed in the recorded runs was code that is not in the
file. The prompt also asks for anchors of 1 to 3 lines, since anchors of 9 or more lines failed 54% of the time
(#116).

Before the review's fixes, the version without the limit was also slow: 12 seconds on one call. The fixes stopped
lines that occur everywhere from anchoring the search, and dropped the listing for a SEARCH over 40 lines.

| SEARCH lines | Damaged edits, limit 8: correct / wrong / refused |
|---|---|
| 1-3 | 70 / 0 / 0 |
| 4-6 | 2,140 / 34 / 251 |
| 7-8 | 287 / 6 / 25 |
| 9-12 | 272 / 2 / 149 |
| 13-20 | 196 / 0 / 133 |
| 21 and more | 164 / 0 / 105 |

### The recorded failures (`analysis/fallback_replay.py`, `fallback_replay.csv`)

Each failed call is given to `edit.py` as is, and again with `--near` the middle of the agent's last `read_file`
range of that file:

| Failure | Failed edits | `edit.py`, no hint | with `--near` |
|---|---|---|---|
| not found | 28 | applied 3, already done 3, refused as long 10, refused with closest lines 6, refused as a syntax error 6 | applied 3, already done 3, long 10, closest 4, conflict 2, syntax error 6 |
| occurs N times | 15 | lists the lines 15 | applied 7, refused as a syntax error 8 |

With the compile check (#144), 14 of the edits `edit.py` would have applied are refused, because the file wouldn't
compile afterwards. In all 8 that can be checked, the "occurs N times" ones, the agent's own replacement text breaks the
file even when applied by plain string replacement. These were wrong edits whichever tool applied them, and a file
that doesn't compile fails every test. Only 7 of the 43 have a label, the agent's own later fix. Rescuing an edit is
also not the same as fixing the task: several of these edits were wrong fixes in the right place.

## find.py (`analysis/find_eval.py`, `find_ranks.csv`)

Each task's query is the issue's first five identifiers (`analysis/localize.py`, as in #112). Files are ranked by:
- how many of the names they contain, every name on a line counting;
- whether they define them (`def`, `class` or a module-level assignment);
- whether a dotted name is their module path.

Tests, docs and examples come last, shown only as a count when other files match. The output is cut at 4,000
characters, inside `run_command`'s 5,000. The baseline is the prompt's step 2 before this change:
`grep -rnE … | head -40`, with files taken in order of appearance.

| Repository | Tasks | Right file first: grep / find.py | In the top 3 | In the top 8 |
|---|---|---|---|---|
| fastapi | 67 | 5 / 15 | 12 / 28 | 16 / 40 |
| rich | 48 | 5 / 12 | 14 / 21 | 18 / 27 |
| requests | 13 | 1 / 11 | 4 / 11 | 7 / 11 |
| httpx | 1 | 1 / 1 | 1 / 1 | 1 / 1 |
| **all** | 129 | **12 / 39** | **31 / 61** | **42 / 79** |

- **First place:** only grep ranks the right file first in 3 tasks, only `find.py` in 30 (p = 1.4 × 10⁻⁶).
- **Top 8:** 3 against 40 (p = 3 × 10⁻⁹).
- **Speed:** the slowest search took 0.69 seconds.

Counting `scripts/` as ordinary code gave 37 first-place hits, and leaving it out entirely gave 43, but leaving it out
would hide a pipeline repository's code. A small score penalty keeps those files visible: 39, 61 and 79.

## The generality check: this organisation's repositories

The same two tests ran on 255 tasks from:
- **health-transformation-lab-nlp:** its published task set, 92 tasks whose problem statements are the issues' own
  text;
- **pipeline-doctor and gemma-developer-agent:** 4 and 9 commits that change non-test Python, with the commit message
  standing in for the issue (`analysis/commit_tasks.py`);
- **getcommunityone/open-navigator:** the 150 most recent such commits, the same way.

| Repository | Tasks | Right file first: grep / find.py | In the top 8 |
|---|---|---|---|
| health-transformation-lab-nlp | 92 | 14 / 30 | 33 / 59 |
| pipeline-doctor | 4 | 0 / 0 | 0 / 0 |
| gemma-developer-agent | 9 | 3 / 4 | 5 / 6 |
| open-navigator | 150 | 8 / 53 | 27 / 82 |
| **all** | 255 | **25 / 87** | **65 / 147** |

| Repository | Damaged edits | `edit_file`: correct / wrong / refused | `edit.py` |
|---|---|---|---|
| health-transformation-lab-nlp | 5,202 | 2,940 / 497 / 1,765 | 4,469 / 34 / 699 |
| pipeline-doctor | 106 | 65 / 2 / 39 | 88 / 0 / 18 |
| gemma-developer-agent | 125 | 79 / 0 / 46 | 109 / 2 / 14 |
| open-navigator | 11,373 | 7,107 / 311 / 3,955 | 9,836 / 76 / 1,461 |
| **all** | 16,806 | **10,191 / 810 / 5,805** | **14,502 / 112 / 2,192** |

- **`find.py`:** first place, only grep 13 against only `find.py` 75 (p ≈ 10⁻¹¹).
- **`edit.py`, correct:** 61 against 4,372.
- **`edit.py`, wrong:** 772 against 74 (p ≈ 10⁻¹⁴⁷). Before the compile check (#144) `edit.py` was wrong 391 times;
  the check refuses 279 of those and 4 correct edits. The 4 are probably hunks that don't compile without the
  reference fix's other hunks.
- **Speed:** the slowest `edit.py` call took 0.24 seconds, and the slowest `find.py` search 2.1 seconds, on
  open-navigator's 818 Python files.
- **"One context line left out":** this is still where `edit.py` errs most, but now less than `edit_file`: 78 wrong
  against 314 (354 before the compile check).

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
  - The prompt says to go on with grep and `edit_file` without the helpers.
- **After the fix, in order:**
  1. The install succeeded.
  2. `find.py parse_answer` put `python/dental_omop_nlp/llm_reader.py` first, with the `def` line (133).
  3. `edit.py` matched line 133, first with `--dry-run`, then for real; `git diff --stat` showed one file changed.
  4. `submit_patch` gave a patch of 602 bytes with one file changed. Neither the helpers nor the harness's own
     temporary script entered the patch.

**Two quirks of that sandbox, both from development runs:**
- It rewrites `/tmp` and `/workspace` inside a heredoc too, so a REPLACE containing the text `"/tmp/x"` would be
  written with the sandbox's path.
- It starts commands with stdin open, so `edit.py` waits at most 5 seconds for a block, then says none came.

The scorer's Docker sandbox runs commands as typed, so `/tmp/h` is the same folder for the install and for the
command. The first leaderboard entry is still the first test on the competition's own machines.

## The review (PR 123)

An independent review of the first version found four ways it could write a wrong change and report success:
- a backslash in the code sent the close match to the unescaped text;
- a block lined up with a different number of file lines duplicated lines;
- indentation was taken from the first line only;
- the debris filter deleted a real `"",` line.

It also found these should-fixes:
- a false "already done";
- `--near` overriding similarity;
- whole-file line-ending damage;
- two ranking issues in `find.py`.

Each is now a regression test in `tests/test_edit_fallback.py` or `tests/test_find.py`, and every number above is from
the fixed scripts. Running the generality check then found two more cases, both from trimming blank lines at the ends
of SEARCH: a SEARCH that was unique only with its blank last line, and a whole-file rewrite of a file ending in a
blank line. Both are fixed and tested.

## What changed in the submission

- `skills/edit-fallback/`:
  - `SKILL.md`;
  - `scripts/install.py`, `scripts/find.py` and `scripts/edit.py`, standard library only, parsing as Python 3.8.
- `agent.yaml` gives the skill.
- `prompts/system.md`:
  - **Step 2** installs the helpers (one `run_skill_script`, no other argument), then localizes with `find.py`.
    Grep stays as the fallback, tests left out.
  - **Editing:** after a failed `edit_file`, never send the same `old_string` again; send the change to `edit.py`.
    Without the helpers, re-read and retry once with a shorter anchor.
- **Tests:** `tests/test_edit_fallback.py` covers each failure kind and each review finding. It also runs `install.py`
  through ADK's own skill wrapper, which needs `google-adk` and is skipped in CI. `tests/test_find.py` covers
  `find.py`, and `tests/test_submission.py` checks the prompt and that the submission holds no `.pyc`.
- **Compiler:** the competition's compiler (`adk_submission.compile_submission`) loads the submission with both
  skills.

## Limits

- **Synthetic damage is our model of the errors.** It was built from the kinds read in the real failures, one damage
  per edit. Real failures can stack several, and the review found defects that no synthetic kind had exercised.
- **Thin labels:** the replay has labels for only 7 failed edits.
- **The development set:** four repositories. The hidden tasks come from other, private repositories (forum topic
  748428).
- **The generality check:** wider, but most of it is one repository (open-navigator), and for three of the four
  repositories the commit message stands in for the issue.
- **No resolve rate.** Finding the file and applying the edit are necessary, not enough. Whether the agent calls the
  scripts, and whether more tasks resolve, is for a run.
  - Under AGENTS.md, a run asking why the agent fails goes to the owner's Colab.
  - A change to the score is measured by one leaderboard entry, booked in the shared queue.
- **Cost:** the install is one more tool call per task, out of 40.
