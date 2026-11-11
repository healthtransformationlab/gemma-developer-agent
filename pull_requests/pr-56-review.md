# PR 56 review: the README shows each run's result, time and tokens (#55)

| Check | Result |
|---|---|
| Branch `docs/55-readme-results-cost`, `Closes #55` | ok |
| Held for the owner: the repository's front page, which the owner is editing on `main` | held |
| A visible section, "What has been run, and what it cost", replaces the two-by-two plan in which three of four cells read "not run" | ok |
| One row per run: hardware and budget, resolved with its interval, agent time a task, tokens a task | ok |
| Local harness: 5 of 48, 95% CI 4.5–22.2; 9.01 agent-hours over 48 tasks is 11.3 min a task; 112k prompt and 4.4k output tokens a task, over the 46 of 48 runs that logged tokens | ok |
| Larger budget: 2 of the 23 cheapest, against 2 before; 2.08 hours over 23 is 5.4 min a task; tokens not in its table | ok |
| Competition's evaluator: 0 of the 20 in its sample, 95% CI 0–16.1; 99 s of agent time and 355 s of model loading a task; 123,900 prompt and 6,713 output tokens a task. The pilot task outside the sample (`htlnlp_143`) is left out, as in the paper | ok |
| The competition's development set is a row still to run, not a blank cell in the middle of the results | ok |
| Controls, cost of a fix (1.80 hours overall; 0.38 for the 13 that pass the screen, 4 of the 5 fixes for 17% of the time) and graph reach (42 of 51; 20 of 473 graph-tool calls; 2 and 2 in the paired rerun) match the paper | ok |
| Every linked table is at `health-transformation-lab-nlp` commit 254c44c, the one the paper used; all six links open | ok |
| Says why the agent runs have no Application Insights telemetry: Kaggle kernels run with internet off, so the harness logs timing and tokens to the run tables | ok |
| The "View submission" line moves above the sentence whose colon it interrupted; the title gets its apostrophe ("cloud agent's work") | ok |
| The plan section says the task set ran under both harnesses, the local one and the competition's own evaluator end to end (the owner found the old "not the competition's evaluator" outdated), and that the skill comparison is what has not run: the skill was available in the evaluator's run and never called. It keeps the switch-off caveat; the outdated "22 of the 93" graph sentence is replaced by the paper's 42 of 51 | ok |
| No dollar figures: the runs cost GPU time, and a price would need a cited source | ok |
| No new run; no secrets; no organisation names; not affiliated | ok |

Nothing blocking. Held for the owner's "merge".
