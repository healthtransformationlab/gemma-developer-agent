# PR 201 review: take the docs work merged here by mistake out of the public repo

Closes #200. Reviewed by the author's session; no second reviewer.

## Findings

Nothing blocking.

- **Scope:** a revert of public #177, #179, #183, #185, #187, #189, #191, #195 and #197, newest first, with no conflicts.
  #181 (the Times note in `CLAUDE.md`) is kept.
- **Content is not lost:** the same files are in the private repository (private PR #79).
- **History:** not rewritten; the old commits stay reachable by SHA.
- **Checks:** `pytest -q tests`: 101 passed, 1 skipped.
- **Environments:** the public Pages site loses `docs/architecture/` when this merges.
