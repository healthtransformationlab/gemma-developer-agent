# ADR 0001: The paper as submitted is a tag, a release and a branch at one commit

Date: 2026-11-12 · Status: accepted · Issue: #93

## Context

The Kaggle Writeup's text loads Figure 1 from one commit of `main`, and its links name this repository. `main`
moves after a submission: the agent in draft pull request 60, new runs, the README. Nothing marked the submitted
commit, so a judge following a link later would see something other than what was submitted, and nobody could say
which commit the Writeup was. The owner asked for a tag, a branch and a release before submitting (November 12, 2026).

## Decision

- Each version pasted into the Writeup is frozen by the `Release the paper` workflow, run by hand, at one commit
  of `main`: the tag `paper-v<n>` (n is the paper's version), a GitHub release of that tag with the PDF attached,
  and the branch `release/paper-track`, moved forward to that commit.
- The tag is at the commit the Writeup's Figure 1 link names, so the text on Kaggle and the release are one commit.
- A tag is never moved. A later version gets the next tag, the branch moves forward, and the newest release is the
  submitted one.
- The workflow checks its inputs first, then the paper at that commit against the competition's rules, and stops
  before writing anything if either fails.
- `release/paper-track` is not a working branch. No pull request is opened from it, so the branch-name rule, which
  CI checks on pull requests, does not apply to it.
- The paper's text is not changed to point at a tag: its links name the repository, whose README links the newest
  release.

## Consequences

- A reader can get the paper exactly as submitted, and compare it with `main`.
- One more step when the paper changes: run the workflow, then paste. If the step is skipped, the newest release is
  behind the Writeup; the Writeup's Figure 1 link still shows which commit it is.
- The source repository is frozen only by the commit named in the release's notes; a release of its own would need
  the same workflow there.

## Revisit when

- Judging ends and `main` no longer needs to differ from what was submitted.
- A second paper or track is submitted from this repository: the tag and branch names assume one.
