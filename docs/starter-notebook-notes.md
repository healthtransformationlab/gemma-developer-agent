# What the starter notebook tells us (read Oct 29, 2026)

Source: the competition's "Getting Started: Gemma 4 Developer Agent" notebook (not committed here).

## The evaluation stack
- Packages from the dataset's wheelhouse: `swegemma` (`models.load_tasks`, `graph`, `config.EvalConfig`,
  `evaluate.Evaluator`, `sandbox.subprocess`, `harness.agent_runner`) and `adk_submission` (`VllmConfig`,
  `VllmServer`, `discover_adapters`, `validate_directory`).
- Models served by vLLM on the L4x4 (tensor parallel 4), `max_model_len` 32768, tool and reasoning parser
  `gemma4`; LoRA adapters discovered from `adapters/<name>/`, max rank 128 by default.
- Exactly one declared model across `agent.yaml` and `sub_agents/*.yaml`; `adapter:` lines are stripped when
  switching away from 31B (the sample adapters are 31B-shaped).
- The dataset ships `sample_submission/` (agent.yaml, sub_agents, adapters): the authoritative template.
- `eval_config.yaml` → `evaluation:` with `timeout_seconds`, `verification_timeout_seconds`, `max_tool_calls`,
  `max_time_minutes`, `max_turns` (or `max_llm_calls`).
- Context cache (min 2048 tokens, 30 min TTL) and event compaction (every 15 events, keep 5) are on.
- Package check: no symlinks, allowed extensions only, 3 GiB max, `agent.yaml` at the archive root.

## The task object
Fields seen: `instance_id` (e.g. `fastapi_15661`), `repo` (`fastapi/fastapi`), `base_commit`. The rest
(issue text, reference patch, test command, test patch) is in `tasks.jsonl` and `HARNESS_README.md`: still
needed before `tasks/build_tasks.py` can match the format.

## The code graph
`sg.get_graph(repo_name, graph_dir, embeddings_dir, base_commit)` returns a networkx graph; node names are
`<repo>;<module>.<Class>.<method>`. `get_neighbor`, `get_similar_nodes` (cosine over the 256-d embeddings),
`get_induced_subgraph` back the three graph tools. FastAPI: 4,263 nodes, 2,430 edges. Graphs are pre-built
per (repo, base_commit); whether `swegemma.graph` exposes a builder for a new repo is unknown.

## What the sample run shows (the lesson)
Both sample tasks: the agent explored (ls, grep, read_file ×6), exhausted a 10-call tool budget or the
1-minute limit, never called `submit_patch`, and scored NO_PATCH. Budget discipline is the first
optimization, before any prompt cleverness: submit something, read line ranges, never re-read a file.
Our `eval_config.yaml` and the first paragraph of `prompts/system.md` encode this.
