# The remediation ladder (stop at the first rung that resolves the issue)

1. Deterministic: retry, rerun an idempotent step, hold downstream. No AI.
2. Classify by rules, in order. Configuration-management classes first, because they page people and
   hide in logs: credential_expiry, vulnerability, deprecation, config_drift, config. Then platform,
   schema_drift, volume_anomaly, quality_fail, cost_anomaly, source_late, unknown. Only unknown needs
   reasoning over code.
3. Root cause: the run row, the last N runs, lineage one hop, the runbook entry. Never the whole log.
4. Recommend: the first allowed action in the runbook entry, the impact one hop down the lineage, the
   severity, the owner. Never an action off the list.
5. Automate: a reversible class runs unattended after N matches with the human; two misses send it back.

Agents recommend; code acts. A fix in a metadata-driven repository is usually a configuration change
(retry policy, expectation threshold, schema mode, a setting check) plus the test that proves it, not new
control flow.
