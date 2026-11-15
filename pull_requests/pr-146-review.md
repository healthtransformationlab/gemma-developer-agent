# PR 146 review: 31B-d, a patch-first rule for the 31B

Closes #145. Reviewed against `.conventions/AGENTS-common.md` and `AGENTS.md`.

- One change per entry: 31B-d differs from 31B-c by `prompts/system.md` only (zip compared file by file).
- Evidence names its runs (nlp #818; the recorded traces); the expected effect is stated as a hypothesis with a kill criterion, as the three-task rule asks.
- Tests first on the entry branch; the plan tests updated for the new row; 82 passed, 1 skipped.
- No submission, GPU or rule change: an agent may merge it when green.

Nothing blocking.
