# The DataOps task set (competition format)

93 tasks in the Gemma 4 Developer Agent Competition's layout, each verified with the competition's own evaluator, built from the merged-change history of
[health-transformation-lab-nlp](https://github.com/healthtransformationlab/health-transformation-lab-nlp): every
change that touched code and tests, which is the competition's own mining rule. This folder holds only this note.

| What | Where |
|---|---|
| The tasks (`tasks.jsonl`, `snapshots/`, `graphs/`, `embeddings/`), CC BY 4.0 | [Kaggle: health-transformation-lab-coding-agent-tasks](https://www.kaggle.com/datasets/jcblearning/health-transformation-lab-coding-agent-tasks) |
| The manifest, gates, exclusions, the evaluator's verdicts and run tables | that repository, `data/tasks/` |
| The builders | that repository, `python/scripts/46_mine_tasks.py`, `55_build_tasks.py`, `57_gate_tasks.py` |
| The harness and the Kaggle runner | that repository, `python/health_transformation_lab_nlp/agent_harness.py`, `python/scripts/59_run_agent.py`, `60_kaggle_agent.py` |
| The spec | that repository, `specs/028-dataops-task-set/`, `specs/035-local-agent-harness/` |

```
tasks.jsonl        # instance_id, repo, base_commit, problem_statement, hints_text, patch, test_patch, created_at
snapshots/         # one .tgz per task: the tree at base_commit as a single commit
graphs/            # directed code graphs, NetworkX node-link JSON, the competition's keys
embeddings/        # 256-d vectors per graph node (EmbeddingGemma; parity with the competition's model unverified)
```

Counts: 197 merged changes, 116 candidates, 114 pass both gates (the tests fail before the fix and pass after it),
93 published (the ones whose reference patch the competition's evaluator resolves, and whose empty patch it does not). Each task carries a fidelity tier for its problem statement: A from an issue (49 candidates), B from
a pull request description (45), C from a commit message (22). Format: [`docs/dataset-format.md`](../docs/dataset-format.md).

What has been measured on it, and how: [`paper/small-local-agent-redo-cloud-agent-work.md`](../paper/small-local-agent-redo-cloud-agent-work.md).
