# Can a small local agent redo a cloud agent's work? The pitch: every slide, with its notes

A personal learning project, not affiliated with or endorsed by any employer, institution or vendor. Every patient record in the source repository is synthetic.

12 slides. Each number is from [the paper](../../paper/small-local-agent-redo-cloud-agent-work.md); [`paper/sources.md`](../../paper/sources.md) says where it comes from. To page through them: [`deck.pdf`](deck.pdf), or download [`deck.html`](deck.html) and open it in a browser.

Built from [`slides/`](slides/) by `python docs/build_decks.py`; edit a slide, then rebuild and run `node docs/render_slides.js`.

## Slide 1: Can a small local agent redo a cloud agent's work?

![Slide 1: Can a small local agent redo a cloud agent's work?](img/01-cover.png)

**Speaker notes:** In fifteen days, one person working with a cloud coding agent took a health-data repository from nothing to 960 commits and 2,269 tests, without typing code. This deck asks what a small model, one that runs on a single GPU, can take out of that loop. The answer comes with a task set anyone can use: 93 real changes from that repository, each verified by the competition's own evaluator. Every patient record in the repository is synthetic. This is a personal project, not any organization's plan.

<details><summary>The slide's text</summary>

Gemma 4 Developer Agent Competition · Paper Track · November 2026  
Can a small local agent  
redo a cloud agent's work?  
93 real tasks from a health-data repository that a cloud agent built, each verified by the competition's own evaluator, with an open harness and a Gemma 4 E4B baseline.  
Health Transformation Lab ·  
Evidence you can check  
Synthetic patient records  
John Bowyer · personal project, not affiliated with any organization

</details>

## Slide 2: Built for the people who build and score coding agents

![Slide 2: Built for the people who build and score coding agents](img/02-audience.png)

**Speaker notes:** Three kinds of reader. People who build benchmarks from a repository's history: we ask them to check each task's statement against its tests before quoting a score, because here the fixes were almost all in the tasks that passed that check. People who build agents on small local models: the 93 tasks are public and in the competition's layout, so its evaluator runs on them as published. And teams whose repositories are built with agents: an issue, a pull request and a review for every change is what made this history usable. So far this is one repository and one model. A person checked 42 of the screen's 93 verdicts, in summary, and no partner has been contacted.

<details><summary>The slide's text</summary>

Who it's for, what we ask, what changes  
Built for the people who build and score coding agents  
Who  
What we ask them to do  
What changes  
Benchmark builders  
who mine tasks from a repository's history  
Ask of every task: does its statement say what its tests check?  
A score is quoted on tasks that can tell one agent from another  
Agent builders  
working with small local models  
Run their agent on the 93 tasks, with the competition's evaluator  
A comparable score on health-data work, beside the popular libraries  
Teams whose repositories are built with agents  
Keep an issue, a pull request and a review for every change  
Their own history can become a task set  
The impact:  
a task set that says which of its tasks can measure an agent. So far it is one repository and one model, and the screen is an AI's, checked by a person in part.  
A personal project: no partner has been contacted

</details>

## Slide 3: Coding benchmarks draw on a few popular libraries. Data work fails differently.

![Slide 3: Coding benchmarks draw on a few popular libraries. Data work fails differently.](img/03-problem.png)

**Speaker notes:** The competition asks whether a model that fits on one accelerator can do the work of the large cloud models behind today's best coding agents. Its tasks, like SWE-bench's, come from a handful of popular libraries. Two kinds of repository are scarce in such sets. In a data repository the costly defect is silent: nothing crashes, and a number in a table is wrong. And a repository built by an agent, under rules that require an issue, a pull request and a review for every change, leaves a record that can be mined. This repository is both. Of its 960 commits, 775 are marked as agent-authored, and it held 2,269 tests on November 8.

<details><summary>The slide's text</summary>

The problem  
Coding benchmarks draw on a few popular libraries. Data work fails differently.  
SWE-bench draws on twelve popular Python libraries; the competition's development set, on four.  
In a  
data repository  
the costly defect is silent: a pipeline finishes and a number in its table is wrong.  
An  
agent-built repository  
can leave an unusually complete record: an issue, a pull request and a review for each change.  
960  
commits on  
main  
775  
of them marked as agent-authored  
2,269  
tests, run by CI on every pull request  
240  
pull requests, each with a committed review  
One person in the loop with a cloud coding agent built this repository in fifteen days, without typing code.  
What can a small local model take out of that loop?  
Source: the paper, Sections 1 and 3

</details>

## Slide 4: A task set made by the competition's own rule, and checked by its evaluator

![Slide 4: A task set made by the competition's own rule, and checked by its evaluator](img/04-solution.png)

**Speaker notes:** The tasks are made the way the competition makes its own: every merged change whose diff touches both code and tests is a candidate. Of 197 merged changes, 116 are candidates. One was withdrawn, one failed a gate and one was withheld for unlicensed third-party files, leaving 113, and the competition's own evaluator verifies 93 of those: the published set. On them it resolves every reference patch and no empty patch. A local harness, which anyone can run, gives the same verdict as the evaluator on all 48 of the model's patches that were compared. Each task comes with a snapshot of the repository, a code graph, embeddings, and a label saying whether its statement came from an issue, a pull request or a commit message.

<details><summary>The slide's text</summary>

What was built  
A task set made by the competition's own rule, and checked by its evaluator  
merged changes mined  
197  
touch code and tests (candidates)  
116  
built, pass both gates, licensed  
113  
verified by the competition's evaluator:  
the published set  
93  
Controls.  
The evaluator resolves 93 of 93 reference patches and 0 of 93 empty patches.  
An open harness.  
It gives the evaluator's verdict on every one of the model's patches compared: 25 of 25 and 23 of 23.  
Each task carries  
a snapshot, a code graph, embeddings, and where its statement came from: an issue, a pull request or a commit message.  
Source: the paper, Sections 4 and 5

</details>

## Slide 5: A few small fixes. More context did not reliably help.

![Slide 5: A few small fixes. More context did not reliably help.](img/05-results.png)

**Speaker notes:** Left on its own on two free T4 GPUs, taking the cheapest tasks first, Gemma 4 E4B resolved 5 of the 48 tasks it ran, all of them small. Under the competition's evaluator it resolved 3 of 23 of the competition's own development tasks. Then came an experiment whose plan was fixed before any result: all 93 tasks on one A100, three ways. As published, the model resolved 4. With graph retrieval done for it, 6. With a failing test's report, 4. Neither added context differs detectably from the baseline, and a difference is not ruled out either: at 4 of 93 only a large effect could show. Retrieval's two extra fixes do not establish a reliable improvement. The report uses the hidden test, so it is not a benchmark condition.

<details><summary>The slide's text</summary>

What the small model did  
A few small fixes. More context did not reliably help.  
On its own, free T4 GPUs  
5 of 48  
Gemma 4 E4B, cheapest tasks first (10.4%, 95% CI 4.5–22.2): a CI rule, a warning message, a label parser and two settings.  
3 of 23  
of the competition's own development tasks, under its evaluator.  
Pre-registered experiment · all 93 tasks · one A100  
As published  
4  
With graph retrieval  
6  
With the failing test's report  
4  
No difference detected:  
exact McNemar p = 0.5 and 1.0. An unplanned second session on an L4 resolved 5 and 8.  
The report comes from the hidden test: a test-first workflow's context, not a benchmark condition.  
Source: the paper, Section 6

</details>

## Slide 6: The fixes were where the statement says what the tests check

![Slide 6: The fixes were where the statement says what the tests check](img/06-finding.png)

**Speaker notes:** This is the result to take away. An AI screen asked of every task whether its statement says what its tests check. Seventeen of the 93 pass: the core split. The other 76 are real statements that leave out something their tests need, such as a name or a message. Over the five Colab runs, 8 of the 17 core-split tasks were resolved at least once, against 1 of the other 76. Counting every task in every run, that is 26 of 85 against 1 of 380. And finding is not fixing: in the 41 tasks where retrieval listed a function the fix edits, 5 of the core split's 7 were resolved in some run and none of the other 34. So valid tasks whose fix the graph found, but whose statements leave out what their tests need, measured little for this model. These are descriptions, not tests, and the second comparison was made after the runs. A person checked 42 of the screen's verdicts, in summary.

<details><summary>The slide's text</summary>

The main finding  
The fixes were where the statement says what the tests check  
8 of 17  
core-split tasks were resolved in some of the five Colab runs (26 of 85 task-runs)  
1 of 76  
of the other tasks (1 of 380 task-runs)  
The core split  
is the 17 tasks whose statements say what their tests check, by an AI screen of all 93.  
Finding is not fixing:  
where retrieval listed a function the fix edits (41 tasks), 5 of the core split's 7 were resolved in some run and none of the other 34.  
Described, not tested  
The second comparison was made after the runs. Source: the paper, Section 6

</details>

## Slide 7: Where a task's time went, and what a fix cost

![Slide 7: Where a task's time went, and what a fix cost](img/07-cost.png)

**Speaker notes:** The runs kept OpenTelemetry spans: names, counts and seconds, never prompts or replies. In the three Kaggle arms, 66 to 83 percent of a task's time was model calls and 14 to 15 percent was context compaction, which is the harness summarising older turns. The graph tools took under 0.1 percent. Forty-five of 207 runs ended when a prompt passed the model's context window. A fix took 1.9 GPU-hours with graph retrieval and 1.8 with the report, on four L4s: about 1.59 and 1.50 US dollars at a median rental price, though Kaggle's GPUs were free. On the T4 baseline, the 13 core-split tasks it ran took 17 percent of its 9.0 agent-hours and gave 4 of its 5 fixes: 0.38 hours a fix against 1.80 overall.

<details><summary>The slide's text</summary>

What it cost  
Where a task's time went, and what a fix cost  
Time  
66–83%  
of a task's time was model calls, and 14–15% was context compaction (the Kaggle arms, from OpenTelemetry spans). 45 of 207 runs ended at the model's context window.  
GPUs  
1.9 and 1.8  
GPU-hours a fix on four L4s, with graph retrieval and with the report: about 1.59 and 1.50 US dollars at a median rental of 0.83 an L4-hour. Kaggle's GPUs were free.  
Where to spend it  
0.38 vs 1.80  
agent-hours a fix on the T4 baseline: the 13 core-split tasks it ran took 17% of its 9.0 agent-hours and gave 4 of its 5 fixes.  
What it means:  
the model's own calls are where the time goes, not the graph tools, and the core-split tasks are where an hour of this model bought the most.  
Source: the paper, Section 6, "Time, GPUs and cost". The prices are rental estimates, not money spent

</details>

## Slide 8: Use the set. Quote results on the core split.

![Slide 8: Use the set. Quote results on the core split.](img/08-ask.png)

**Speaker notes:** Four things to do with this. Run your agent on the set: 93 tasks under CC BY 4.0, in the competition's layout, so its evaluator runs on them as published, and a quickstart notebook loads a task. Quote results on the core split of 17: over every run, 9 of the 10 distinct tasks this model has resolved are in it. Screen your own task set the same way before quoting a score on it. And check any number here: each one in the paper has a row in paper/sources.md that names the file it came from.

<details><summary>The slide's text</summary>

What to do with it  
Use the set.  
Quote results on the core split.  
Run your agent on it.  
93 tasks, CC BY 4.0, in the competition's layout: its evaluator runs on them as published.  
Quote results on the core split.  
Over every run, 9 of the 10 distinct tasks this model has resolved are among its 17.  
Screen your own tasks.  
Ask of each one whether its statement says what its tests check, before a score is quoted on it.  
Check any number.  
Each one in the paper has a row in  
paper/sources.md  
naming the file it came from.  
Tasks: kaggle.com/datasets/jcblearning/health-transformation-lab-coding-agent-tasks  
Paper, sources and agent configuration: github.com/healthtransformationlab/gemma-developer-agent

</details>

## Slide 9: Drill-down

![Slide 9: Drill-down](img/09-drill.png)

**Speaker notes:** Do not present these. Jump to one only when asked. Everything here is in the paper, and paper/sources.md says where each number comes from.

<details><summary>The slide's text</summary>

Can a small local agent redo a cloud agent's work?  
Drill-down  
Backup slides for questions. The full detail is in the paper.  
What this does not show  
This set beside the competition's own tasks  
How each number is kept honest

</details>

## Slide 10: What this does not show

![Slide 10: What this does not show](img/10-limits.png)

**Speaker notes:** Six limits, all in the paper. One repository, set beside the competition's development set. No cloud baseline: the cloud agent that made these changes with a person in the loop was not rerun on the statements alone, so the title's question is answered for the small model only. A small experiment: at 4 of 93 only a large effect could show. No leaderboard score: the runs used 5 minutes and 40 tool calls where the competition allows 60 and 100. The screens are an AI's: a person checked 42 verdicts in summary, after seeing the AI's, and 51 have AI ratings only. And every task comes with a failing test, so noticing a silent defect unprompted is not measured.

<details><summary>The slide's text</summary>

Drill-down · limits  
What this does not show  
One new repository,  
compared with the competition's development set.  
No cloud baseline.  
The cloud agent that made these changes, with a person in the loop, was not rerun on the statements alone.  
A small experiment.  
At a baseline of 4 of 93 only a large effect could show.  
No leaderboard score.  
Every run under the competition's evaluator used 5 minutes and 40 tool calls, not 60 and 100, once per arm and machine.  
AI screens.  
A person checked 42 verdicts, the core split's 17 among them, in summary and after seeing the AI's; 51 have AI ratings only.  
Prompted repair.  
Each task comes with a failing test: noticing a silent defect unprompted is not measured.  
Read the results as:  
what one small model did on one repository's tasks, with the screen's verdicts checked by one person in part.  
Source: the paper, Section 7

</details>

## Slide 11: The two sets differ in their tests more than their statements

![Slide 11: The two sets differ in their tests more than their statements](img/11-competition.png)

**Speaker notes:** The same counts were made on the competition's own development tasks. Its graph holds more of the fixes: 114 of 129, against 51 of 93 here. Its statements are vague a little more often: 11 of 40, against 19 of 93. The difference is in the tests: in this set the tests of 76 of 93 tasks need a name or a text the statement never gives, against 14 of 40 there. The screen and the agent took a seeded 40 of the 129, stratified by repository. In a Kaggle notebook the evaluator's sandbox cannot install test dependencies, so 23 of the 40 can be verified there, and the model resolved 3 of them.

<details><summary>The slide's text</summary>

Drill-down · the competition's own tasks  
The two sets differ in their tests more than their statements  
This set  
Development set  
The fix edits a function the graph holds  
51 of 93  
114 of 129  
Of those: a name or call edge reaches it; with embedding search too  
22; 42  
52; 66  
Statement vague or worse (AI screen)  
19 of 93  
11 of 40  
Tests need a name or text the statement never gives  
76 of 93  
14 of 40  
Resolved as published, on Kaggle  
0 of 21  
3 of 23  
On the competition's tasks the graph holds more of the fixes and the screen passes half. The screen and the agent took a seeded 40 of its 129 development tasks; a Kaggle notebook can verify 23 of them.  
Source: the paper, Section 6, "Beside the competition's own tasks"

</details>

## Slide 12: How each number is kept honest

![Slide 12: How each number is kept honest](img/12-evidence.png)

**Speaker notes:** Four habits keep the numbers honest. Every figure in the paper has a row in paper/sources.md naming the file it came from, and rows stay when text is cut. The experiment's plan was hashed before any result, and each addendum before its run. A script checks the paper against the competition's rules on every change, and another checks that every number in this deck is one the paper or the README has. And what went wrong is in the paper: on Colab the network was open to the agent's commands, 3 of 687 commands ran an installer, in tasks no run resolved, and none left its workspace. The unplanned second session on an L4 is described beside the registered experiment and never added to it.

<details><summary>The slide's text</summary>

Drill-down · evidence you can check  
How each number is kept honest  
A source for every number.  
paper/sources.md  
has a row for each figure in the paper, naming the file it came from, and keeps the rows of text that was cut.  
A plan before the results.  
The experiment's plan was hashed before any result, and each addendum before its run started (source repository, issues 674 and 687).  
Checked on every change.  
In CI,  
paper/check_rules.py  
checks the paper against the competition's rules, and  
docs/build_decks.py  
checks this deck's numbers against the paper.  
What went wrong is in the paper.  
Colab's network was open to the agent: 3 of the five runs' 687 commands ran an installer, in tasks no run resolved, and none left its workspace.  
Not a result:  
anything from a dry run or a sample is labelled as one, and the unplanned second session is described beside the registered one, never added to it.  
Sources: paper/sources.md, paper/rules_check.md and the paper, Section 6

</details>
