---
name: edit-fallback
description: Two helper scripts for any Python repository - find.py ranks the files that mention the issue's names (tests left out), and edit.py applies a SEARCH/REPLACE block when edit_file fails, matching through escapes, spacing and small copy errors. Install once with run_skill_script and no arguments, then use run_command.
---

# edit-fallback skill

**Install first, once:** `run_skill_script` with `skill_name` `edit-fallback` and `file_path` `scripts/install.py`,
and no other argument. It copies the helpers to `/tmp/h/` and prints their usage. Never pass `args`,
`short_options` or `positional_args`.

**Find the code** (one `run_command`): `python3 /tmp/h/find.py NAME [NAME ...]`, with two to five names from the
issue (a function, class, module or variable name, or a short quoted error message). It prints the repository's
Python files, best first, with the matching lines and their numbers. Tests, docs and examples are left out.

**See the code in the same call:** add `--show` (`python3 /tmp/h/find.py --show NAME [NAME ...]`) and it also prints
the source of the top functions, line-numbered, so you need no `read_file` for them. For more code later, read
several ranges in one call: `python3 /tmp/h/find.py --read path/a.py:120-160 path/b.py:40-70`.

**After an edit, the tests to run:** `python3 /tmp/h/find.py --tests path/you/changed.py NAME [NAME ...]` prints one
line, `Tests to run: python3 -m pytest ... -x -q`: that file's own `test_<name>.py` first, then the test files that
mention the names. Run that, never the whole suite and never pytest on a source file.

**When `edit_file` fails**, never send the same `old_string` again. Run instead:

```
python3 /tmp/h/edit.py path/to/file.py <<'EOF'
<<<<<<< SEARCH
one to three lines as read_file showed them
=======
the same lines as they should be
>>>>>>> REPLACE
EOF
```

- It tries SEARCH as written, then trimmed and without tool-call debris, then with escapes undone (a literal `\n` or
  `\"`): exactly, then ignoring spaces, then the closest place (similarity 0.8 or more, clearly the best). The
  closest-place match is tried only when SEARCH has 8 lines or fewer, and refused wherever it would be a guess.
- A close match changes only the lines SEARCH and REPLACE differ in, and keeps the file's own copy of the rest.
- It refuses an edit that would leave a `.py` file that compiled unable to compile, and says where.
- "REPLACE is already in the file": the change is done; move on.
- "SEARCH occurs at lines ...": run again with `--near LINE`, the line you mean.
- Otherwise it prints `NOTHING WRITTEN` and the closest lines with their numbers to copy from.

Measured on CPU over the development set's four repositories (fastapi, rich, requests, httpx):
`docs/fallback-scripts-study.md`.
