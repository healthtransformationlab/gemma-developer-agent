# Paper track writeup — outline and abstract (draft, Oct 29, 2026)

**Target:** Gemma 4 Developer Agent Paper Track, 3,000 words, due November 12, 2026. Non-archival.
**Awards it fits:** Best New Resource (the DataOps task set), Best New Application (code graphs and the
competition tools on a data-pipeline repository), Overall (if the experiment lands).
**Rule for every number in this paper:** it comes from a run in one of the three repos, with its interval,
or it is not in the paper. No premise is stated as a percentage.

## Title

**Reading the tables before the logs: repository metadata as context for a small local coding agent on
data-pipeline bugs**

Subtitle: a DataOps task set in the competition's format, an ADK skill that classifies the failure from the
repository's own configuration, run, lineage and runbook tables, and a switch-off test of what each table
contributes.

## Abstract (draft, ~200 words)

Coding-agent benchmarks are built from web libraries, where a bug is a code change. In data platforms, what
pages people is more often a configuration-management failure: a setting that differs between environments,
a credential that expired, a model or dependency that was deprecated, a vulnerability advisory. These are
invisible in logs until the damage is done and visible in tables before it. We identify five ingredients
that make a repository operable by an agent (a metadata-driven framework, consistent conventions including
every change traced to an issue, configuration management with a credential register and a dependency
inventory, OpenTelemetry on every call with timing and cost, and the forecasting the first four enable), and
we ask whether a small local agent (Gemma 4 E4B, the competition's tools) fixes such issues better when a
repository has them, and when the agent is told to read the tables first.

We contribute (1) a DataOps task set in the competition's format, built from a public synthetic-data
project's own history (196 merged changes, 115 of which change code and tests; every one traced to an issue,
67 of them by backfilled records that quote the original text verbatim), each with a problem statement, a
pre-fix snapshot, a reference patch and validation tests, and a fidelity tier that says where the statement
came from; (2) `pipeline-doctor`, an ADK skill and library that classifies a failure by rules over four
metadata tables (pipeline config, run log with OpenTelemetry timing and cost, lineage, runbook), recommends
only actions on the runbook's allow-list, and forecasts credential expiry, deprecation and cost, duration,
volume and schema trends with dates; and (3) a switch-off test that hides each ingredient in turn and
measures what the rules can still do. We report pass rate for the same agent on the competition's
development set and on the DataOps set, with and without the skill. [Results to be filled from runs.]

## Sections (word budget in brackets)

1. **Introduction** [400]. Web-library benchmarks vs. what breaks in data platforms. The claim as a
   question, not a premise. What a reader gets: a task set, a skill, a measurement.
2. **Related work** [300]. SWE-bench (Jimenez et al., 2024); the competition's code graphs and embeddings;
   DataOps and observability (freshness, volume, schema, distribution, lineage); OpenTelemetry for pipelines;
   LLM-as-judge and evaluation against human labels; DORA's four metrics applied to data pipelines.
3. **The DataOps task set** [500]. Mining the repo's history the way the competition mined its repos
   (changes that touch code and tests). Three fidelity tiers for the problem statement: A, an issue (48
   candidates); B, a PR without an issue (45); C, a direct commit (22). Backfilled issue records: verbatim
   text, labelled, closed on creation, no text written after the fact. The incident set marks which tasks
   are DataOps failures. The two gates (tests fail before the fix, suite passes after), run with the
   competition's own evaluator. A finding in its own right: the share of a repo's history that is
   agent-ready (traceable to an issue) went from under half to all of it once the branch-to-issue rule was
   enforced in CI.
4. **pipeline-doctor** [600]. The four tables, named and typed. The ladder: deterministic → classify by
   rules (configuration-management classes first) → root cause by LLM for `unknown` only → recommend from
   the allow-list with impact, severity and owner → graduate to automatic after N matches, back after two
   misses. Agents recommend; code acts. Context engineering as choosing which rows, against the anti-pattern
   of dumping the log into the prompt. The OpenTelemetry call stack (depth, timing, cost) as the source of
   the run table.
5. **The agent** [300]. agent.yaml on Gemma 4 E4B; a read-only analyzer subagent using
   `get_code_neighbors`, `search_similar_code`, `get_code_subgraph`; the skill's `classify.py` and
   `ladder.md`; the system prompt's order of work (conventions before code, failing test before fix).
6. **Experiments** [600].
   - E1, offline: the doctor on the incident set; accuracy, action agreement, share without the LLM, impact
     known, fields handed to the LLM; the switch-off test per table.
   - E2, online: pass rate of the same agent on the competition dev set and on the DataOps set, with and
     without the skill (2×2). The interesting cell: skill helps on DataOps, not on web libraries.
   - E3, cost: tokens and wall-clock per task with and without the skill (the skill should cut context).
7. **Limitations** [200]. Nine incidents; one project's conventions; synthetic data; the author wrote both
   the conventions and the rules (so E2 on an outside project is the real test); E4B only.
8. **Conclusion** [100]. What to publish next: the task-set builder and a second project.

## What exists today vs. what the paper needs

| Needed | Exists | Where |
|---|---|---|
| pipeline-doctor library, 31 tests, configuration-management classes | yes | healthtransformationlab/pipeline-doctor |
| Incident set, nine rows, with classes and actions | yes | health-transformation-lab-nlp `data/ops/incident.csv` (PR #357) |
| Task manifest: 196 changes, 115 candidates, tiers, every candidate with an issue | yes | health-transformation-lab-nlp `data/tasks/task_manifest.csv` (PR #358) |
| E1 numbers with intervals | yes (nine incidents) | spec 027, "The switch-off test" |
| Configuration-management incident rows (credential, deprecation, drift) | no | add from the project's secrets register, model inventory and environment configs |
| Task set in competition format (`tasks.jsonl`, snapshots, graphs) | no | NLP repo spec 028 US3-US4 (`47_build_tasks.py`, planned); format in `docs/dataset-format.md` |
| Agent run on the dev set (E2 baseline) | no | one Kaggle L4x4 run |
| Agent run on the DataOps set, both conditions | no | two runs |
| Paper text | this outline | `paper/writeup.md` |

## Schedule to November 12

- Oct 30–Nov 2: task-set builder (spec 028 US3-US4); candidates validated with `swegemma eval --skip-agent-patch`
  (fail before) and with `patch` (pass after); drop what fails a gate. Add the configuration-management
  incidents from the project's own records (secrets register, model inventory, environment configs).
- Nov 3–5: one dev-set run without the skill (baseline); one DataOps run without the skill.
- Nov 6–8: both runs with the skill. E3 from the harness budget reports.
- Nov 9–11: writeup, 3,000 words, numbers from runs only. Decision point Nov 5: if the baseline runs
  haven't happened, skip the paper and target the December 2 agent deadline.

## Lines that carry over from the interview preparation (reuse verbatim where they fit)

- "Context engineering is deciding what the model sees — lineage, schema, recent runs, runbooks — so the
  root-cause guess is grounded in the platform, not in general knowledge."
- "Agents recommend; deterministic code acts — and anything that changes data goes through an approval
  step with a fallback to the old manual path."
- "A labeled evaluation set, an LLM judge scored against human labels, and one production metric that
  would move if it's working."
- "Past incidents with the on-call's final call are free labels."
- "If the agent is wrong twice in a row on a class, that class goes back to recommend-only."
- The anti-pattern: "dumping the whole log into the prompt."
