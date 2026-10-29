# The competition dataset format (from the Data tab, read Oct 29, 2026)

The target format for our DataOps task set. Match it field for field; where we cannot (the embedding
model), say so in the paper.

## tasks.jsonl (one JSON object per line)

| Field | Type | Meaning |
|---|---|---|
| `instance_id` | string | `<repo_short>_<issue_or_pr_number>`, e.g. `fastapi_11194`, `rich_3454` |
| `repo` | string | `owner/repo` |
| `base_commit` | string | 40-hex SHA of the snapshot immediately before the fix |
| `problem_statement` | string | the issue text given to the agent as the task prompt |
| `hints_text` | string | optional issue comments or maintainer hints; may be empty |
| `patch` | string | reference unified diff that resolves the issue on `base_commit` (published set only) |
| `test_patch` | string | unified diff adding the verification tests pytest runs in Phase 2 (published set only) |
| `created_at` | string | ISO-8601 timestamp of the issue or PR |

Scoring output: `submission.parquet` with `id` (= `instance_id`) and `prediction` (the agent's diff relative
to `base_commit`, or `NO_PATCH`).

## snapshots/<instance_id>.tgz
A full git repository frozen at `base_commit` with forward history removed, so `git status`, `git log`
and `git diff` inside `/workspace` leak nothing. `sandbox/setup.py` then resolves dependencies from
`/wheels/` (`pip install --no-index --find-links=/wheels -e .`) and makes a clean baseline commit so
`git diff HEAD` is exactly the agent's edits.

## graphs/<instance_id>.json (NetworkX node-link JSON; also `<repo_short>_<base_commit>.json`)
```
directed: true, multigraph: true, graph: {…metadata…}
nodes[*]: id (fully qualified symbol, e.g. fastapi.routing._prepare_response_content), name (= id), text (source of the def at base_commit)
edges[*]: source, target, type (e.g. "calls"), key (int, parallel-edge index)
```
Backs `get_code_neighbors` and `get_code_subgraph`.

## embeddings/<instance_id>.npz (also `<repo_short>_<base_commit>.npz`)
One array per node: `<node_id>.npy`, float32, length 256. Backs `search_similar_code` (cosine similarity).
The embedding model is not named on the Data tab; check `HARNESS_README.md`. If it is not reproducible, our
set ships graphs without embeddings, or with embeddings from a named open model, stated in the paper.

## Curation rules (ours must pass the same)
1. Commit mined jointly modifies functional code (`.py`) and tests (`test_*.py` / `*_test.py`).
2. Linked to an issue, PR thread or bug report that supplies `problem_statement`.
3. Not a mechanical refactor, docs-only change or large automated change; acceptance criteria reproducible.
4. **Fail-to-pass:** `test_patch` applied to `base_commit` without `patch` → tests fail (non-zero exit).
5. **Pass-to-pass:** `patch` + `test_patch` on `base_commit` → the whole suite passes (exit 0).
6. (Test set only) a frontier model passes or comes within one failing test.

## Other dataset parts
`wheels/` (124 offline wheels), `docker/` (Python 3.13 sandbox, `imp`/`telnetlib` shims), `sample_submission/`
(the authoritative ADK YAML baseline), `HARNESS_README.md` (swegemma, adk-submission, adk-eval-core, the
two-container sandbox lifecycle, tool signatures, context compaction, local CLI evaluation). Apache 2.0.

## What this means for `tasks/build_tasks.py`
For each row of the NLP repo's `data/ops/incident.csv` whose fix is a commit in that repo:
- `instance_id` = `htlnlp_<issue_number>` (the repo's issues are the natural numbers);
- `base_commit` = the fix commit's parent; `patch` = the fix commit's diff to non-test files;
  `test_patch` = its diff to `python/tests/`; `problem_statement` = the issue body; `hints_text` = the
  incident's `recorded_in_text` and runbook entry; `created_at` = the issue's timestamp;
- snapshot = `git archive` at `base_commit` into a fresh repo with history truncated, `.tgz`;
- graph = NetworkX node-link JSON built with an AST pass over the package (calls/imports edges), same keys;
- verify fail-to-pass and pass-to-pass in the sandbox image before writing the row.
The repo's convention that every change traces to an issue and a test is what makes this mechanical.
