# PR 123 review: fallback scripts find the code and rescue failed edits, tested on CPU (#122)

Reviewed by a read-only reviewer subagent, given the code and asked for an unanchored read, over the range
`origin/main..5f82bae`, with repro scripts for each finding. The coordinator then verified each finding, fixed it
test-first, and re-ran every measurement.

| Check | Result |
|---|---|
| Branch `feat/122-edit-fallback-skill`, `Closes #122`, issue with its four parts before the first commit; dated "Changed" lines for what moved | ok |
| Test first: the install, prompt and sandbox tests failed before their code; each review finding has a regression test that failed first | ok |
| Every number in `docs/fallback-scripts-study.md` is printed by `analysis/fallback_summary.py` from the committed CSVs | ok |
| No secrets; no competition files (CSVs hold ids, file names, counts and outcomes) | ok |
| Simulated work labelled: `analysis/harness_check_model.py` and its section say SIMULATED | ok |
| CI: `conventions / check`, `check` (submission), `check` (paper rules) | green on every push so far; read again before merging |

## Findings

### Blocking: each wrote a wrong change and reported success (all fixed)

1. **A backslash in SEARCH sent the close match to the unescaped text** (`sep = "\n"` in code).
   - Fixed: every stage tries SEARCH as written first.
   - Test: `test_a_backslash_in_the_code_keeps_the_raw_text_first`.
2. **The merge duplicated lines** when one SEARCH block lined up with a different number of file lines, or when
   REPLACE changed a SEARCH line the file lacks.
   - Fixed: these are conflicts and are refused (`merge` raises `Conflict`), as is an insertion next to a missing line.
   - Tests: `test_a_changed_line_inside_an_unequal_block_is_a_conflict`,
     `test_changing_a_search_line_the_file_does_not_have_is_a_conflict`.
3. **Indentation came from the first line only.** In one case this moved `c()` inside an `if`.
   - Fixed: the shift must agree across the matching lines; only SEARCH's first line may differ. Tabs against spaces
     are refused.
   - Tests: `test_first_line_that_lost_its_indentation_does_not_shift_the_rest`,
     `test_tabs_in_the_file_against_spaces_in_search_are_refused`.
4. **The debris filter deleted a real `"",` line** before the exact match.
   - Fixed: debris is stripped only in a later attempt.
   - Test: `test_a_real_quote_line_is_not_taken_for_tool_call_debris`.

### Should fix (all fixed)

5. **A false "already done"** when REPLACE appeared anywhere, or next to SEARCH.
   - Fixed: reported only where REPLACE overlaps the place the change would go.
   - Test: `test_already_done_only_where_the_change_would_go`.
6. **`--near` beat similarity.**
   - Fixed: it only breaks near-ties, within `MIN_GAP`.
   - Test: `test_near_breaks_ties_only`.
7. **`splitlines()` damaged form feeds, lone carriage returns and line endings.**
   - Fixed: lines split on newlines only, each keeping its own `\r`; new lines get the file's ending.
   - Test: `test_only_newlines_split_lines_and_each_keeps_its_ending`.
8. **`find.py`** credited one name per line, and hid `scripts/`.
   - Fixed: every name counts. Top-level `scripts/` and `benchmarks/` are code with a small score penalty; on the
     development set the right file is first in 39 of 129, against 37 counted as plain code and 43 hidden. Files left
     out are counted, and the output is capped at 4,000 characters.
   - Tests: `test_every_name_on_a_line_is_credited`,
     `test_code_under_scripts_counts_and_left_out_files_are_counted`, `test_output_is_capped_even_with_long_paths`.

### Nits

- **Subprocess sandbox: `/tmp` rewritten inside a heredoc.** Documented in the study; it doesn't affect the scorer's
  Docker sandbox.
- **Subprocess sandbox: stdin left open.** Fixed: `edit.py` waits at most 5 seconds for a block.
- **Several blocks: "matched" printed before "nothing written".** Fixed: output now starts with
  `NOTHING WRITTEN: block k of n`. "Copy SEARCH from the lines above" appears only when lines are shown.
- **Exit code 1 doubled the output in the harness.** Fixed: a refusal exits 0 with `NOTHING WRITTEN` first; 2 is
  kept for usage errors. Recorded on the issue as a contract change.
- **`find.py` output size claim.** Fixed: the output is capped at 4,000 characters, and the doc says so.
- **CSV `file_path` column.** Renamed `file_name`. `_num` for line numbers is kept, as in the nlp repository's list.
- **`harness_check_model.log`.** `*.log` is now in `.gitignore`.
- **"Wrong no more often" held only overall.** The doc now names "one context line left out" as the one damage
  where `edit.py` errs more.

### Found after the review, by the generality check (fixed)

- **A SEARCH unique only with its blank last line** was trimmed and matched twice. Fixed: SEARCH is matched as
  written first. Test: `test_a_blank_line_at_the_end_of_search_is_part_of_it`.
- **A whole-file rewrite of a file ending in a blank line** kept the blank. Same fix. Test:
  `test_replacing_a_whole_file_that_ends_with_a_blank_line`.
- **Very common lines anchoring the search,** with a long SEARCH's listing, made calls slow (up to 6 seconds).
  Fixed: a line seen more than 50 times anchors nothing, and a SEARCH over 40 lines gets no listing. The slowest call
  is now 0.17 seconds on the development set and 0.15 seconds on our repositories.

### Checked by the reviewer, nothing found

- `install.py` under ADK's wrapper (relative `__file__`, exit codes).
- The `/tmp` and `$TMPDIR` fix.
- ASCII-only scripts that parse as Python 3.8.
- Heredocs under `sh` and `bash`.
- Writing all blocks or none.
- CRLF-only files and files without a final newline.
- Deletion, and a one-line SEARCH.
- Binary files and regex characters for `find.py`.
- That the prompt and `SKILL.md` agree.

## Results after the fixes

**The competition's development set:**
- `find.py`: right file first in 39 of 129 tasks, against 12 for grep (p = 1.4 × 10⁻⁶).
- `edit.py`, on 4,447 damaged edits:
  - right 3,739 against `edit_file`'s 2,820 (p ≈ 10⁻²⁴¹);
  - wrong 62 against 79 (37 to 54 discordant, p = 0.093);
  - slowest call 0.17 seconds.

**Generality check, 255 tasks from this organisation's repositories and open-navigator:**
- `find.py`: 87 against 25.
- `edit.py`:
  - right 14,506 against 10,191;
  - wrong 391 against 810 (p ≈ 10⁻⁷¹).

**End to end:** the harness's own `swegemma eval`, with the subprocess sandbox and a scripted stand-in model
(simulated), installs, finds, edits and submits a one-file patch.

## Verdict

Approve once the latest commit's checks are green. The PR starts no run and publishes nothing. Its effect on the score
is for one leaderboard entry (5b in the shared queue), built from `feat/122-skill-on-copyfix`: 9c9cd3a plus the skill
and its prompt lines only.
