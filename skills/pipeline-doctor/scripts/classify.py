"""Classify an issue against the repository's pipeline metadata. Thin wrapper over pipeline-doctor,
vendored at evaluation time (no internet in the sandbox): see resources/ladder.md for the rules."""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

CLASS_WORDS = {
    # configuration-management classes first: invisible in logs until the damage is done, visible in tables before
    "credential_expiry": ("expired", "401", "403", "unauthorized", "invalid token", "token expired", "access denied"),
    "vulnerability": ("cve-", "vulnerability", "security advisory", "dependabot", "ghsa-"),
    "deprecation": ("deprecated", "no longer supported", "end of life", "retired", "model not found", "endpoint not found",
                    "removed in version"),
    "config_drift": ("differs between", "mismatch", "only in dev", "only in prod", "config drift", "environments differ"),
    "config": ("setting", "secret", "connection string", "not set", "parameter", "credential", "token"),
    "platform": ("gpu", "illegal seek", "signal", "killed", "memory", "py4j", "communication channel", "no space"),
    "schema_drift": ("new column", "schema", "mergeschema", "column added", "columns"),
    "volume_anomaly": ("fewer rows", "row count", "truncated", "partial", "10 rows", "empty file"),
    "quality_fail": ("check fail", "threshold", "data quality", "conformance", "plausibility", "out of range"),
    "cost_anomaly": ("budget", "cost", "usd", "dbu", "runaway"),
    "source_late": ("late", "did not arrive", "stale", "freshness", "sla"),
}


def classify(text: str) -> dict:
    t = text.lower()
    for cls, words in CLASS_WORDS.items():
        hit = [w for w in words if w in t]
        if hit:
            return {"failure_class_code": cls, "evidence": hit}
    return {"failure_class_code": "unknown", "evidence": []}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--issue", required=True, help="file holding the issue text")
    a = p.parse_args()
    text = pathlib.Path(a.issue).read_text()
    out = classify(text)
    runbook = pathlib.Path("/workspace/ops/runbook.yaml")
    if runbook.exists():
        m = re.search(rf"failure_class_code: {out['failure_class_code']}\n(?:.*\n)*?\s*allowed_action_codes: \[(.*?)\]",
                      runbook.read_text())
        out["allowed_action_codes"] = [x.strip() for x in m.group(1).split(",")] if m else []
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
