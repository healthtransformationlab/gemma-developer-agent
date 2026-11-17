# PR 187 review: the README picture shows how a failed run's cause is found from its trace (#186)

Reviewed against `.conventions/AGENTS-common.md` and `AGENTS.md`.

| Check | Result |
|---|---|
| One issue, branch `docs/186-readme-picture-trace-cause`, `Closes #186` | yes |
| Tests | `pytest -q tests`: 104 passed, 1 skipped |
| Stage names | match `analysis/failure_stages.py`: localize, edit, complete, patch_wrong_file, patch_right_file, resolved, in plain words |
| No number is a result until a run produced it | no number added; the picture's figures are unchanged from #185 |
| The submission | untouched: only `README.md`, `docs/img/` and this review |

## Findings

- **Not blocking:** the picture is a PNG; redraw it from `docs/img/coding_agent_architecture.drawio` when the README's figures change.
- **Not checked:** how the picture reads on GitHub at phone width.

Nothing blocking.
