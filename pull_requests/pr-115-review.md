# PR 115 review: drop the code-graph tools; keep search_similar_code as the fallback (#113)

| Check | Result |
|---|---|
| Branch `feat/113-drop-graph-tools`, `Closes #113`, issue with its four parts first | ok |
| Test first: `test_graph_tools_are_not_given_or_named` fails on main (stashing the change: 1 failed, 12 passed) and passes here (13) | ok |
| `get_code_neighbors`, `get_code_subgraph` gone from both agents and both prompts; `search_similar_code` kept | ok |
| Step 4 still finds covering tests: one grep of `tests/` for the symbol names, or the analyzer | ok |
| The analyzer's prompt no longer asks for one-hop neighbours it can't get | ok |
| Copyfix (`adapter: copyfix`) and everything else as main `53b714c` | ok |
| Evidence: `docs/localization-study.md` (PR 114), graph vs regex top 10 13 / 7, p = 0.26; the traces' 44 graph calls in 23 tasks | ok |
| Secrets, data, claims | none; no score change claimed |

## Findings

- Minor: the analyzer keeps `read_file` and `search_similar_code` only, so its use may fall further. Whether to drop
  it too is a separate question for a later entry.
- Not measured: the change ships as a leaderboard entry after copyfix's, one change per entry, with no GPU hours.

## Verdict

Nothing blocking. Merge when CI is green and after entry 5 is submitted, so entry 5 stays copyfix alone.
