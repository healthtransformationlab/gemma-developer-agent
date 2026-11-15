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

## Kaggle GPU hours

Development-set runs of this repository's PRs use the same Kaggle account, and so the same weekly GPU hours, as
health-transformation-lab-nlp, whose AGENTS.md ("Failures, retries and reruns") holds the full rules (#110). On
November 15 the week's hours were spent a day in.

- **Read the quota before and after every run**: `python kaggle/gpu_quota.py` in health-transformation-lab-nlp
  (used, allowed, left, refresh; it refreshes Saturday 00:00 UTC). Put the run's cost in its record.
- **One GPU run at a time**, across every session on the account. Say so to the other sessions before starting one.
- **A PR's effect on the score is measured by a leaderboard entry**, which runs on the host's machines; a
  development-set run of 23 tasks is for a mechanism (failed edits, context-window endings), not a resolve rate.
- **Keep a reserve** of about 10 hours until the last two days before the refresh.
- **The owner's explicit yes starts a Kaggle GPU run**, given for that run in the session that starts it; "do what you
  recommend" doesn't. **Recorded traces and CPU come first** (a kernel's traces download for free; the competition's
  graphs and embeddings run on CPU), and a development-set run is never started to compare resolve counts: six of them
  on the same 23 tasks resolved 3 or 4 each (p = 1.0). **One change per leaderboard entry**, booked in a shared plan.
  The decision and its reasons: health-transformation-lab-nlp ADR 0007 (#120).

## Layout

`agent.yaml`, `prompts/`, `sub_agents/`, `configs/`, `eval_config.yaml`, `skills/` are the submission;
`tasks/` is the DataOps task set; `paper/` the writeup; `docs/` what the rules and the starter notebook say.
