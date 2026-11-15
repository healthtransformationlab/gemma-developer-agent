# PR 155 review: the agent installs the helpers and runs find.py as its first two calls (#154)

Reviewed by the author session against `AGENTS.md`, `.conventions/AGENTS-common.md` and the submission rules
(`docs/rulebook-notes.md`).

| Check | Result |
|---|---|
| Branch `feat/154-first-calls-install-find`, `Closes #154`, issue with its four parts before the first commit | ok |
| Test first: `test_the_first_two_calls_install_and_find` and the changed edit.py-missing assertion failed on main (2 failures) | ok |
| The evidence is checked at the source: the 10 traces in `jcblearning/htlnlp-colab-official-colab-skill`, read in this session, give 0 of 10 `run_skill_script` calls and 0 `find.py` calls | ok |
| The existing wiring tests still hold: install before find.py, find.py before the first read, grep as the fallback, no `args` | ok |
| Declarative only, allowed file types, placeholders kept, no new `{...}` in the prompt (ADK would read it as a state variable) | ok |
| No number presented as a result: the mechanism check is named as still to run | ok |
| Secrets, data, claims | none |

## Findings

None blocking.

- **Risk, accepted.** Two forced calls cost each task about two model turns. Four of the 10 colab-skill tasks hit the
  5-minute limit. The calls themselves run on CPU in well under a second. What `find.py` buys is the right file first
  in 39 of 129 development tasks, against grep's 12, and wrong-file failures are 27% of our failure stages. The
  5-task check also reads the time a task takes; if it rises enough to push tasks past the limit, the plan says so.
- **Risk, open.** The model may still skip the calls. Only a model run shows whether a prompt is followed, which is why
  the plan holds E4B-all on the check rather than on this PR.
- **Nit, left as is.** The two calls are described twice, at the top and in step 2 of "Order of work". Step 2 is now one
  short pointer that keeps the grep fallback, and the duplication is about 200 characters.

## Verdict

Approve. It starts no run and publishes nothing. It changes the prompt that E4B-all will carry once the plan points at
it, and that is a separate plan PR, held on the check. Merge when the checks are green.
