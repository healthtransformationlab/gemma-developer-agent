# PR 151 review: hold the 31B entries until the 10-task timing run

Closes #150. Reviewed against `.conventions/AGENTS-common.md` and `AGENTS.md`.

- The risk is stated with its arithmetic (120 x 8 min = 16 h against 12 h) and its evidence (#818: every smoke-test task used its full time).
- The decision rule is fixed before the result, so the result cannot be read to suit.
- Tests: the queued order and the three-task test updated; a new test for the hold; 87 passed, 1 skipped.
- No submission, GPU or rule change in the agent: an agent may merge it when green.

Nothing blocking.
