"""Tasks from a repository's own commits, for the generality check of the edit-fallback skill (#122): every non-merge
commit on the current branch that changes a non-test Python file that already existed becomes one task. The base
commit is its parent, the reference patch is its diff, and the problem statement is its commit message with agent
trailers removed (a stand-in for issue text, lower fidelity than an issue). The competition's development set is what
decides; this only checks the scripts don't depend on its four repositories.

usage: commit_tasks.py <repo dir> <owner/name> <out tasks.jsonl> [max tasks, newest first]
"""
import json
import re
import subprocess
import sys

TEST = re.compile(r"(^|/)(tests?|testing)/|(^|/)test_[^/]*\.py$|_test\.py$|(^|/)conftest\.py$")
TRAILER = re.compile(r"^(Co-Authored-By|Co-authored-by|Claude-Session|Signed-off-by):.*$", re.M)


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True, check=True).stdout


def main(repo, name, out_path, limit=None):
    shas = git(repo, "rev-list", "--no-merges", "HEAD").split()
    rows = []
    for sha in shas:
        parents = git(repo, "rev-list", "--parents", "-n", "1", sha).split()[1:]
        if len(parents) != 1:
            continue
        changed = git(repo, "diff", "--name-status", parents[0], sha).splitlines()
        modified = [line.split("\t")[-1] for line in changed if line.startswith("M\t")]
        if not any(p.endswith(".py") and not TEST.search(p) for p in modified):
            continue
        message = TRAILER.sub("", git(repo, "log", "-1", "--format=%B", sha)).strip()
        rows.append(dict(instance_id=f"{name.split('/')[1]}_{sha[:8]}", repo=name, base_commit=parents[0],
                         patch=git(repo, "diff", parents[0], sha), problem_statement=message))
        if limit and len(rows) >= int(limit):
            break
    with open(out_path, "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    print(len(rows), "tasks from", len(shas), "commits")


if __name__ == "__main__":
    main(*sys.argv[1:5])
