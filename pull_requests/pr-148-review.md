# PR 148 review: a failure-stage breakdown for every development run

Closes #147. Reviewed against `.conventions/AGENTS-common.md` and `AGENTS.md`.

- Data: the CSV holds run names, task ids, stage codes and counts; no task text, code or patches. Columns follow the data-name rules (`_code`, `_count`, `_num`).
- Numbers from a run in the repo: the five runs' traces are the kernels' outputs recorded in health-transformation-lab-nlp `data/tasks/official_agent_runs/`; the stage rule is stated in the docstring.
- Limits worth knowing: "read" counts a file named in a command as read; a patch that touches only test files counts as wrong file. Both are stated, not hidden.
- Tests first; 84 passed, 1 skipped. No compute or rule change: an agent may merge it when green.

Nothing blocking.
