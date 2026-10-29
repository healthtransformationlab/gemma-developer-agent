---
name: pipeline-doctor
description: Troubleshoot a data-pipeline repository from its metadata tables (config, run log, lineage, runbook) before reading code or logs; classify the failure by rules, then recommend an action from the runbook's allow-list.
---

# pipeline-doctor skill

Use when the repository has pipeline metadata: `ops/pipeline_config.yaml`, `ops/runbook.yaml`,
`data/ops/incident.csv`, `data/ops/lineage_edge.csv`, or tables named `dim_pipeline`,
`fact_pipeline_run`, `dim_lineage_edge`, `dim_runbook_entry`.

Order of work:
1. `run_skill_script classify.py --issue <issue text file>`: maps the issue to a failure class
   (`credential_expiry`, `vulnerability`, `deprecation`, `config_drift`, `config`, `platform`, `schema_drift`,
   `volume_anomaly`, `quality_fail`, `cost_anomaly`, `source_late`, `unknown`) from the metadata, by rules. Only `unknown` needs you to reason from code.
2. `load_skill_resource ladder.md`: the remediation ladder and the allowed actions per class.
3. Read the runbook entry for the class; the allowed actions tell you what kind of fix the repository
   expects (a retry policy change, a schema merge, a setting check, a quality threshold).
4. Find the pipeline's outputs in the config and its consumers in lineage: the tests to run are the
   ones that cover those outputs.

Never read note text, PHI or row-level data. Reason over names, counts, durations, error types and
check results only.
