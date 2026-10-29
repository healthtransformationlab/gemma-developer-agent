# The DataOps task set (competition format)

Tasks in the Gemma 4 Developer Agent Competition's layout, built from the incident history of
[health-transformation-lab-nlp](https://github.com/healthtransformationlab/health-transformation-lab-nlp)
(`data/ops/incident.csv`, spec 027): each incident has an issue, a snapshot commit before the fix, the
reference patch, and the validation tests, which is exactly what the competition's curation requires.

```
tasks/
├── tasks.jsonl        # issue text, task id, repo, base commit, reference patch, test command
├── snapshots/         # git working trees frozen before each fix (built by build_tasks.py; not committed)
├── graphs/            # directed code graphs, same format as the competition's
└── embeddings/        # 256-d vectors, same format as the competition's
```

`build_tasks.py` (planned) reads the incident set, finds each fix commit from `recorded_in_text`, and
writes the rows. The comparison the paper reports: the same agent config on the competition's 129-task
development set (FastAPI, Requests, Rich, HTTPX) and on this set, with and without the pipeline-doctor
skill, pass rate on both.
