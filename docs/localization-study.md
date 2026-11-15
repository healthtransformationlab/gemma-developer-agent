# Where does the agent find the code to fix? An offline localization study (November 15, 2026)

Issue #112. health-transformation-lab-nlp raised match rates by combining regex with BERT. The question here is the
same: does a regex-plus-embeddings combination, or the competition's code graph, find the code the reference patch
changes more often than regex on the issue's identifiers alone? Leaderboard entries and GPU runs are too few and too
noisy to answer that, so it is measured offline, on CPU, on all 129 development tasks of the competition, with the
same graphs and embeddings the shipped tools read (`graphs/` and `embeddings/` in the competition's files). Nothing
from them is committed; `analysis/localization_ranks.csv` holds one row per task with ids and ranks only.

## Method

`analysis/localize.py`, for each task:

- **The answer**: the files the reference patch changes, test files left out, and the functions or classes its hunks
  sit in. 124 of the 129 tasks change a file that exists in the graph; the other five add a new file, which no
  search can rank.
- **Regex**: the issue's identifier-like strings (backticked spans, dotted names, words with an underscore, an inner
  capital or a call), as the prompt's grep step uses them. Each graph node (function, class or method, with its
  source) scores 3 × idf when its name is the identifier and 1 × idf when its source contains it. A file ranks by its
  best node. Run with test code kept and with it left out.
- **Embedding expansion**: cosine similarity to the top three regex nodes, over the competition's 256-dimensional node
  embeddings. That is what `search_similar_code` does offline: it resolves a symbol name and returns its nearest
  nodes. It does not embed free text, since the sandbox has no embedding model.
- **Graph expansion**: the top three regex nodes and their one-hop callers and callees, as `get_code_neighbors` gives.
- **Hybrids**: reciprocal-rank fusion (k = 60) of regex with each expansion.
- **Score**: whether a changed file is in the top 1, 5 or 10 files, and a changed function in the top 5 or 10
  nodes. Pairs of methods are compared on the same tasks with the exact McNemar test.

## Results (124 tasks)

| Method | File top 1 | Top 5 | Top 10 | Against regex, top 10 (only regex / only this) |
|---|---|---|---|---|
| **Regex, tests left out** | 38 | **57** | **69** | |
| Regex, tests kept | 36 | 52 | 62 | 7 / 0, **p = 0.016** |
| Embedding expansion | 36 | 56 | 70 | 11 / 12, p = 1.0 |
| Graph expansion | 38 | 60 | 63 | 13 / 7, p = 0.26 |
| Regex + embeddings (fused) | 35 | 57 | 69 | 8 / 8, p = 1.0 |
| Regex + graph (fused) | 38 | 58 | 71 | 3 / 5, p = 0.73 |

Changed function in the top 5 nodes: 33 with tests left out, 28 with them kept (5 / 0, p = 0.062).

- **Leaving test code out of the ranking helps.** 7 more tasks have the right file in the top 10, and none fewer.
  It is the only difference here that a paired test supports.
- **Neither the embeddings nor the graph add to regex**, alone or fused. The expansions find some files regex
  misses and miss others it finds, in about equal numbers. Here the regex-plus-BERT idea doesn't carry over: the
  embeddings can only start from symbols regex already found, so they add no new signal.
- **Regex finds a changed file in the top 10 for 69 of 124 tasks (56%).** In PR 60's run on 23 of these tasks, the
  agent read a file the reference patch changes in 15 (65%). For most of the rest, the issue names no identifier
  from the code.

## From the traces (PR 60's run, 23 tasks; health-transformation-lab-nlp PR 767)

- `search_similar_code` was called 82 times. **163 of its 735 results (22%) were test code**, sharing its
  5,000-character output cap with the code to fix.
- `read_file` opened a test file 5 times in 143 reads: the prompt's grep, which leaves tests out, already keeps reads
  on source.
- `get_code_neighbors` was called 43 times and `get_code_subgraph` once, about two of the 40 tool calls per task.

## What follows

- Drop `get_code_neighbors` and `get_code_subgraph` (#113): no measured value, about two tool calls a task.
- Keep `search_similar_code` as the fallback when grep finds nothing, and tell the agent that results under `tests.`
  are tests, not the code to fix.
- Keep test code out of every search the prompt asks for, as step 2's grep already does.

## Limits

One development set of 129 tasks from four repositories (67 fastapi, 48 rich, 13 requests, 1 httpx). The identifier
extraction is one reasonable rule, not the agent's own choice of strings. Ranking quality is not resolve rate: finding
the file is necessary, not enough. Write-ups 92541 and 92027 found that even oracle localization adds little for E4B
unless the edit is right.
