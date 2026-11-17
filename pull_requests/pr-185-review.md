# PR 185 review: the README opens with a picture of the agent (#184)

Reviewed against `.conventions/AGENTS-common.md` and `AGENTS.md`.

| Check | Result |
|---|---|
| One issue, branch `docs/184-readme-agent-picture`, `Closes #184` | yes |
| Tests | `pytest -q tests`: 104 passed, 1 skipped |
| No number is a result until a run produced it | The added README text has no number. The picture's figures match "Results at a glance" and the run table: 5 of 48 (10.4%, 95% CI 4.5–22.2); 8 of 17 and 1 of 76 fixed at least once over five runs; 4, 6 and 4 of 93 in the pre-registered experiment on one A100; 3 of the 23 development tasks a notebook can verify (95% CI 4.5–32.1); about 2 GPU-hours, an estimated 3.50 to 3.76 US dollars |
| The open-navigator figure | 150 of 255 tasks, from `docs/leaderboard-plan.md` entry 5b; that check's caveat (most of it one repository) is in the plan, not on the picture |
| Personal learning project, synthetic only | stated on the picture |
| Nothing else in the README changed | yes: one block inserted above the Paper Track line |

## Findings

- **Not blocking:** the picture is a PNG, so its figures will not update when the README's do. If a run changes "Results at a glance", redraw from `docs/img/coding_agent_architecture.drawio`.
- **Not blocking:** "Snowflake + dbt: design phase" records the owner's intent; nothing in the repository runs there.
- **Not checked:** how the picture reads on GitHub at phone width.

Nothing blocking.
