# PR 189 review: the README has a title of its own, says the entry runs the 31B, and opens the architecture picture from a large button (#188)

Reviewed against `.conventions/AGENTS-common.md` and `AGENTS.md`.

| Check | Result |
|---|---|
| One issue, branch `docs/188-readme-title-architecture-button`, `Closes #188` | yes |
| Tests | `pytest -q tests`: 104 passed, 1 skipped; `python docs/build_decks.py --check`: decks up to date |
| The page | headless Chromium at 1400×900 and 390×844: both tabs show, `#side-by-side` opens that tab, no console errors, no sideways scroll |
| Which model, from the repository | `agent.yaml` on `main`: `gemma-4-e4b-it-qat-w4a16-ct` with `sub_agents/code_analyzer.yaml`; on `feat/173-31b-e8`: `gemma-4-31b-it-qat-w4a16-ct`, single agent (#140); the first 31B entry is 58406723, November 16 (`docs/leaderboard-plan.md`) |
| No number is a result until a run produced it | no run figure added; "A100 in our Colab runs" is from the leaderboard plan's 31B-e8 row |
| The paper | untouched: its title, text, PDF and the release workflow (ADR 0001); the README still names it by its submitted title |
| The submission | untouched: only `README.md`, `docs/architecture/`, `docs/img/view_architecture_button.svg` and this review |

## Findings

- **Not blocking:** the picture itself still says "one small open model" and "Gemma 4 E4B". That is true of `main`, and the page's "Which model" note says so. A redraw for the 31B belongs to its own change, from `docs/img/coding_agent_architecture.drawio`.
- **Not blocking:** until this merges and Pages publishes, the button's link returns 404.
- **Not checked:** how the SVG button renders in GitHub's dark theme. It is a solid teal with white text, so it should read on both themes.

Nothing blocking.
