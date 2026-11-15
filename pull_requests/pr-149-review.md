# PR 149 review: edit.py refuses an edit that would leave a Python file unable to compile (#144)

Reviewed by the author session against `AGENTS.md`, `.conventions/AGENTS-common.md` and the fallback study's own
standards.

| Check | Result |
|---|---|
| Branch `feat/144-edit-compile-check`, `Closes #144`, issue with its four parts before the first commit | ok |
| Test first: `test_an_edit_that_breaks_compilation_is_refused` failed before the change; `test_a_file_that_did_not_compile_is_still_edited` guards the version case | ok |
| No refusal from an older sandbox Python: the check runs only when the original compiled, and only on `.py` files | ok |
| Python 3.8 and standard library only: `compile(..., dont_inherit=True)`, caught `SyntaxError` and `ValueError` | ok; the 3.8 parse test passes |
| Every number in the study comes from the committed CSVs through `analysis/fallback_summary.py` | ok |
| Queued entries unchanged: 5b `80d23e8`, 31B-b `c75c619`, 31B-c `2b1c444` predate this, and the plan's numbers for 5b stay its own | ok; the study says so |
| Secrets, data, claims | none |

## Findings

None blocking.

- **Checked, not a defect.** The recorded-failure replay now refuses 14 edits that `edit.py` used to apply. For the 8
  that can be checked ("occurs N times"), applying the agent's own text by plain string replacement also breaks the
  file, so the check refuses the agent's broken edits, not `edit.py`'s merges. The 6 fuzzy cases can't be checked
  this way. They are the same tasks, and one, rich_3454, is also one of the two recorded patches that didn't compile.
- **Nit, left as is.** The 4 correct edits lost on our repositories are probably hunks that don't compile without the
  reference fix's other hunks, which is an artifact of the synthetic test applying one hunk at a time.
- **Nit, left as is.** The compiler names a different line for an unclosed bracket across Python versions: 3.10+ give
  the line it opens, older versions the next line. The test accepts either.

## Verdict

Approve. It starts no run and publishes nothing, and no queued zip changes. Merge when the checks are green.
