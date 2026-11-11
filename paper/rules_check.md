# The paper against the competition's rules

Written by `python paper/check_rules.py` from the paper's text, its PDF and this repository's files; do not
edit by hand. OWNER rows are confirmed by the owner before submitting. A reading of the rules, not legal
advice.

| Rule | Requirement | How checked | Result |
|---|---|---|---|
| Paper track: length | at most 3,000 words, references excluded | words before "## References" in the paper's text | PASS (2,808 words) |
| Paper track: the file submitted | the PDF carries the same text as the paper | PDF exists; its word count within 10% of the text's (layout adds page numbers, captions); title in it | PASS |
| 2.4.a Data access and use | Competition Data used only as the Website and Rules permit | the paper reports the evaluator's verdicts on this project's own tasks; no competition task is published | PASS |
| 2.4.b Data security | Competition Data not redistributed | no competition file (wheels, sample_submission, HARNESS_README, swegemma, adk_submission) is tracked | PASS |
| 2.5, 3.6.c Licences | code under an OSI licence that allows commercial use | the paper names Apache 2.0 for the code and CC BY 4.0 for the tasks; LICENSE is Apache 2.0 | PASS |
| 2.6 External data | external data public and free to all Participants | the task set's public Kaggle link is in the paper and the PDF | PASS |
| 3.6.b Public code sharing | code shared publicly, and on the competition's forum or notebooks | the public repositories are linked in the paper and the PDF; the forum post is the owner's | PASS (links); OWNER (forum post) |
| 3.4.b No hand labelling of test data | no human labels of the competition's validation or test records | the only screen in the paper is of this project's own tasks | PASS |
| 3.14.a Original work | the Submission is your own work; no third-party rights infringed | the paper discloses the cloud agent's part and cites its sources | PASS |
| 3.1.c Eligibility, employer | not entered for an employer without its consent | the paper states it is not affiliated with any employer; the employer's own policy is the owner's | PASS (statement); OWNER (employer policy) |
| Honest reporting | no number presented as a competition score | the paper says no score here is a competition or leaderboard score | PASS |
| 3.5 Individual account, teams | one Kaggle account; no private sharing outside a Team | not checkable from files | OWNER |
| Paper track: required parts | title and subtitle, abstract, introduction, methods and experiments, related work and citations | the paper's first line is its title and its third the subtitle; headings for the abstract, introduction, related work, the task set, the baseline and the references | PASS |
| Paper track: code as a public notebook | code is submitted as a public notebook in Project Links | the public quickstart notebook is linked in the paper and the PDF; adding it to Project Links is the owner's | PASS (link); OWNER (Project Links) |
| Paper track: private resources | a private Kaggle resource attached to a Writeup is made public after the deadline | the paper names no private dataset or notebook of the runs (htlnlp-agent-, htlnlp-run-, htlnlp-colab-, htlnlp-offrun-); what is attached in the form is the owner's | PASS (paper); OWNER (attachments) |
| Paper track: original, unpublished research | not published elsewhere; the track is non-archival | not checkable from files: the paper is in a public repository and at no venue | OWNER |
| Paper track: submitted, not a draft | only submitted Writeups are judged; a tie goes to the earlier entry | not checkable from files | OWNER |
| Paper track: AI-assisted writing | no rule on it in the Official Rules or on the Paper Track page (as the owner pasted it on November 10, 2026) | the paper says a cloud agent built the repository and wrote most of its issue text | PASS |
