# PR 160 review: entry 5 is skipped; 31B-d goes second when its timing run clears (#159)

Reviewed by the author session against `AGENTS.md`, ADR 0002 and the plan's rules.

| Check | Result |
|---|---|
| Branch `docs/159-skip-entry-5`, `Closes #159`, issue with its four parts before the first commit | ok |
| Test first: `test_entry_5_is_skipped_and_31b_d_goes_second` and the two queued-order tests failed on main (3 failures) | ok |
| The owner's decision is quoted: "Skip 5, 31B-d next (Recommended)", with the option's fallback text | ok |
| The copyfix gate still exists: it moves to E4B-all, the first entry that carries copyfix | ok |
| ADR 0002 gets a dated amendment line | ok |
| Secrets, data, claims | none |

## Findings

None blocking.

- **Risk, accepted.** With no row queued, the slot waits for the 31B timing run or the 02:00 UTC fallback, which is up to
  two hours. Entry 5 would have filled it at once, but for about 12 hours.
- **Risk, accepted.** If copyfix fails on the scorer, we learn it from E4B-all rather than entry 5, at the same cost of
  one slot. The fallback version without the adapter is then proposed, as before.

## Verdict

Approve. It starts no run and changes no submission file. It changes the queue as the owner chose. Merge when the
checks are green.
