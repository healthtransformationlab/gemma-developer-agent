# What HARNESS_README.md tells us (read Oct 29, 2026)

The competition's rulebook for the exam room: the submission schema, the tools, the budgets, how patches
are extracted and graded. What changed in this repo because of it, and what to remember.

## Submission schema (adk-submission, declarative only)
- One root config (`agent.yaml`); `eval_config.yaml` optional at the root. No Python entrypoints; YAML
  compiled against closed registries. `!include` for `.md`/`.txt` (raw) and `.yaml` (recursive, depth 10).
- `LlmAgent` fields: `name`, `model`, `adapter`, `description`, `instruction` (supports
  `{problem_description}` and `{hints}` from session state), `tools` (tool names, `agent_tool:
  {config_path, skip_summarization}`, or inline agents), `skills` (relative paths), `sub_agents`
  (`{config_path}`), `output_key`, `include_contents`, `generate_content_config`. Also `SequentialAgent`,
  `ParallelAgent`, `LoopAgent` (max 500 iterations).
- `generate_content_config`: `max_output_tokens` 1-32,768 (default 16,384); `thinking_config.thinking_budget`
  0-32,768 (default 4,096); `include_thoughts`; omit `thinking_level` on the vLLM endpoint.
- Allowed file extensions only: `.yaml .yml .md .txt .py .json .safetensors`; no symlinks; < 3 GiB unpacked.
- Single base model across all agents; different LoRA adapters per agent are allowed (`adapters/<name>/`).

## Prizes and the two final submissions

From the competition's Overview page, as the owner pasted it on November 15, 2026 (not in `HARNESS_README.md`):

- **Main prizes:** 1st $37,000, 2nd $18,000, 3rd $10,000, to the top three overall, whatever the model. (The Paper
  Track's $35,000 is a separate competition; its deadline was November 12.)
- **Small-model bonus: $10,000** to the highest-ranking submission that uses Gemma **E2B or E4B** as its base model.
  It must be **one of the team's two selected final submissions**. LoRA adapters are allowed, as in the main track,
  and an eligible submission stays eligible for the main prizes. The same deadlines and tie-breaking apply.
- **Small-model standings:** a host notebook updates them daily,
  [`ryanholbrook/gemma-4-developer-agent-small-model-leaderboard`](https://www.kaggle.com/code/ryanholbrook/gemma-4-developer-agent-small-model-leaderboard).
  Read it with `kaggle kernels output ryanholbrook/gemma-4-developer-agent-small-model-leaderboard -p <dir>`, which
  writes `leaderboard.csv` (`Rank`, `TeamName`, `PublicScore`). Its November 14, 2026 output (23:55 UTC) put the top
  two at 0.12, ten more at 0.10, and this entry (team `jcblearning`) 699th of 1,035 at 0.05. These are public scores,
  on about half the hidden tasks (about 58, so one task is about 0.017), and the final standings use the other half.
- **One submission a day** (`maxDailySubmissions` 1). The entry and team-merger deadline is November 25, 2026, and
  the final submission deadline December 2, 2026, both at 23:59 UTC.
- **Time:** 12 hours for all tasks, sandbox setup included and patch validation not. Per-task limits in
  `eval_config.yaml` are optional (below).
- **GPU quota:** notebooks on L4x4 machines use Kaggle GPU quota at twice the rate of T4x2 and P100 machines, and
  L4s are only for notebooks attached to this competition, with internet off.

So the two final submissions are chosen for two prizes: one is the best E4B entry, for the small-model bonus, and
the other may use any allowed model (`gemma-4-31b-it-qat-w4a16-ct` included), for the main prizes. Every agent in
one submission uses the same base model.

## Hardware and serving
4 × L4 (96 GB), vLLM tensor-parallel 4, `max_model_len` 32,768, Gemma 4 tool and reasoning parsers; each
sandbox container has 4 GiB RAM and 2 vCPUs, no network.

## Budgets (per task; `eval_config.yaml` → `evaluation:`)
Defaults in scoring: 60 min, 100 tool calls, 500 turns, 300 s per command; the sample submission used 1 min
and 10 calls. The whole run has 12 hours for ~120 tasks including sandbox setup, so ~5 min per task is the
real ceiling. `submit_patch` and `get_status` are free. A `budget_warning` field appears in every tool
response when ≤ 10 calls remain. Three consecutive turns without a tool call end the session (nudges).

## Tools (9)
`run_command` (300 s, 5,000 chars), `submit_patch` (free), `get_status` (free), `read_file` (150 lines /
10,000 chars, line ranges), `edit_file` (3-tier matching: exact, whitespace-flexible, regex; unique match
required), `write_file`, `get_code_neighbors`, `search_similar_code` (resolves a symbol name against the
precomputed vectors; no live embedding model; lexical fallback), `get_code_subgraph`.

## Patch extraction and grading
`git add -N . && git diff --binary HEAD` from `/workspace`; untracked files are included. Diff hunks to test
files and runner config (`conftest.py`, `pytest.ini`, `pyproject.toml`, `tox.ini`, `setup.cfg`) are stripped.
If the agent never calls `submit_patch`, the working-tree diff is still extracted and graded. Phase 2: fresh
container, 4-pass patch apply, protected files reset, `test_patch` applied, hermetic pytest with JUnit XML;
resolved iff exit 0 and every required test passed (not skipped).

## Local evaluation
`swegemma eval --tasks tasks.jsonl --snapshots-dir snapshots --submission-dir <dir> --results-dir <dir>
--sandbox docker|subprocess --max-tool-calls N --max-time-minutes M --concurrency K`; `--skip-agent-patch`
runs Phase 2 with an empty patch, which is exactly the fail-to-pass gate our task set needs (spec 028 US3).
Results: `summary.json`, `task_results.jsonl`, `patches/`, `test_outputs/`, `traces/`, `logs/`.

## What this changed here
- `agent.yaml`: the analyzer is an `agent_tool` with `skip_summarization: true` (keeps its `read_file`
  output out of the coder's context), not a `sub_agents` include.
- `configs/sampling.yaml`: `max_output_tokens` 12,288, `thinking_budget` 4,096, `include_thoughts`. At 16,384
  the input got only half of the server's 32,768-token window, and a fifth of the runs ended at it (issue 99); at
  8,192 one edit was cut off before its tool call closed (issue 105). 12,288 leaves 20,480 for the input, above the
  largest prompt seen (17,426 tokens), and 8,192 for an answer after thinking.
- `eval_config.yaml`: 5 min, 40 calls, 60 turns, 120 s per command.
- `skills/edit-fallback` (#122): skills may ship `.py` scripts, and `run_skill_script` runs them in the task's
  sandbox, so one call with no arguments installs `find.py` and `edit.py` to `/tmp/h/` for plain `run_command` lines
  (`docs/fallback-scripts-study.md`).
- `prompts/system.md`: `{problem_description}` and `{hints?}` (optional: the evaluator sets `hints` only for a task that has
  some, and a required variable that is not set ends the agent before its first model call; issue 33); submit-before-budget first; the stripped
  files; scratch in `/tmp`; symbol names for the graph tools; no `pip install`.
- For the DataOps task set: a fix that lives only in `pyproject.toml` or a test file cannot be scored, so
  such tasks are excluded (spec 028 US3); fixes in `ops/*.yaml` are fine.
