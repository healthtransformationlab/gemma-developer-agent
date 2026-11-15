"""No compiled Python is tracked: the evaluator refuses __pycache__ and .pyc files (#134)."""
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_no_tracked_pycache_or_pyc():
    tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.split("\n")
    bad = [p for p in tracked if "__pycache__" in p or p.endswith((".pyc", ".pyo"))]
    assert bad == [], bad
