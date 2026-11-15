# PR 131 review: cite the 255-task check, most of it open-navigator, for entry 5b (#130)

| Check | Result |
|---|---|
| Branch `docs/130-5b-open-navigator`, `Closes #130`, issue with its four parts first | ok |
| Test first: `test_entry_5b_cites_the_wider_check_with_open_navigator` failed, then passed; 75 pass | ok |
| Numbers match `docs/fallback-scripts-study.md`'s 255-task tables: find.py 87 vs grep 25; edit.py right 14,506 vs 10,191, wrong 391 vs 810; open-navigator 150 tasks and 11,373 of 16,806 edits | ok |
| The study's caveat (most of the check is one repository) is stated beside the numbers | ok |
| Docs only | ok |

Nothing blocking. Merge when CI is green.
