# PR 117 review: anchor edits on 1-3 plain lines and recover once (#116)

| Check | Result |
|---|---|
| Branch `feat/116-short-edit-anchors`, `Closes #116`, issue with its four parts first | ok |
| Test first: `test_edits_anchor_on_short_plain_lines_and_recover_once` fails on main (stashing the prompt: 1 failed) and passes here (18) | ok |
| Evidence: 252 edits pooled from four runs' traces (downloaded from the kernels, no GPU); backslash 31/62 failed vs 61/190, p = 0.015; 9+ lines 20/37 vs 72/215, p = 0.025 | ok |
| Correctness of the rule: a line that must change and has a backslash is matched by its part before the backslash, so the old text is replaced, not duplicated (fixed before commit) | ok |
| Only `prompts/system.md` "Editing" and the test change; copyfix and the tool list are main's `d265a78` | ok |
| Secrets, data, claims | none; no score change claimed |

## Findings

- Minor: a 1-3 line anchor can match more than once; the existing bullet (add a neighbouring line when it could match
  elsewhere) still applies, and the error tells the agent.
- Not measured: the rule's effect is read from the next run's traces (edit fail rate) and the leaderboard entry of
  November 18, one change after entry 6.

## Verdict

Nothing blocking. Merge when CI is green.
