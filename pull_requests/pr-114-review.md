# PR 114 review: measure regex, embedding, graph and hybrid localization offline (#112)

| Check | Result |
|---|---|
| Branch `feat/112-localization-study`, `Closes #112`, issue with its four parts first | ok |
| Test first: `tests/test_localize.py` failed (no module), then passed; 16 pass | ok |
| Reproducible: the study run twice gives identical ranks (graph neighbours sorted; an earlier draft iterated a set and moved one figure) | ok |
| Numbers in `docs/localization-study.md` match `analysis/localization_ranks.csv` (recomputed: top-5/10 counts and every McNemar pair) | ok |
| No competition files committed (graphs, embeddings, task text); the table has ids, counts and ranks | ok |
| Not part of the submission: `analysis/` is outside the bundle's entries | ok |
| `ruff` clean (B023 waived in the file with its reason) | ok |
| Secrets, real data, claims | none; the doc says ranking is not resolve rate |

## Findings

- Minor: `search_similar_code`'s own lexical fallback for multi-word queries isn't modelled; the study's embedding
  arm starts from symbols, as the prompt tells the agent to query.
- Minor: the identifier rule is one reasonable choice, not the agent's. The doc says so.

## Verdict

Nothing blocking. Merge when CI is green.
