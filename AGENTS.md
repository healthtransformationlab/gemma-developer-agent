# AGENTS.md

The shared rules are in `.conventions/AGENTS-common.md` (vendored from pipeline-doctor; version in
`.conventions/VERSION`). This file adds what is specific to this repository: a competition entry and its paper.

## Ground rules for this repo

- **No number is a result until a run produced it.** The evaluator writes `results/<run>/summary.json`;
  a figure in `paper/` or `README.md` names the run it came from, with its interval. A dry run or a sample
  of two tasks is labelled as such.
- **The competition's rules win.** `docs/rulebook-notes.md` and `docs/dataset-format.md` summarise them;
  the dataset's `HARNESS_README.md` is authoritative where they differ. One base model across all agents;
  declarative YAML only; allowed file extensions only; no symlinks; under 3 GiB.
- **The grader strips test files and runner config** from every patch, so the agent fixes library code.
- **Task text is never written after the fact.** The DataOps task set's problem statements are the source
  repo's own issues, PR descriptions and commit messages, with a fidelity tier.
- **Secrets**: the Kaggle token lives in the Kaggle account and a GitHub environment secret, never here.

## Layout

`agent.yaml`, `prompts/`, `sub_agents/`, `configs/`, `eval_config.yaml`, `skills/` are the submission;
`tasks/` is the DataOps task set; `paper/` the writeup; `docs/` what the rules and the starter notebook say.
