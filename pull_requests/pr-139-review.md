# PR 139 review: 31B-b takes the second slot; the 5-minute 31B is held

Closes #138. Reviewed against `.conventions/AGENTS-common.md` and `AGENTS.md`.

- Numbers come from a run in the repo: the smoke test result is recorded on health-transformation-lab-nlp #818 (Modal A100, labelled a smoke test, not a timing for the 12 hours).
- One change per entry still holds: 31B-b differs from the held 31B by `eval_config.yaml` only.
- The owner's agreement is recorded; no submission, GPU or rule change in this PR: an agent may merge it when green.
- Tests: the superseded order test replaced; 79 passed, 1 skipped.

Nothing blocking.
