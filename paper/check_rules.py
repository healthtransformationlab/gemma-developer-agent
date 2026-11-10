"""Check the paper against the competition's rules, and write the result as a table (#37).

    python paper/check_rules.py            # checks, writes paper/rules_check.md, exits 1 if an automated check fails
    python paper/check_rules.py --check    # also fails if paper/rules_check.md is out of date (CI)

Each row is one rule from the Official Competition Rules (kaggle.com/competitions/gemma-4-developer-agent/rules) or
the paper track's stated limit. A row checked here reads the paper's text (`small-local-agent-redo-cloud-agent-
work.md`), its PDF (the file submitted) and this repository's tracked files. A row marked "owner" cannot be checked
from files: the owner confirms it before submitting. This is a reading of the rules, not legal advice.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MD = HERE / "small-local-agent-redo-cloud-agent-work.md"
PDF = HERE / "small-local-agent-redo-cloud-agent-work.pdf"
OUT = HERE / "rules_check.md"
WORD_LIMIT = 3000
DATASET = "kaggle.com/datasets/jcblearning/health-transformation-lab-coding-agent-tasks"
REPOS = ("github.com/healthtransformationlab/health-transformation-lab-nlp",
         "github.com/healthtransformationlab/gemma-developer-agent")
# the competition's own files: never committed here (rule 2.4.b, data security)
COMPETITION_FILES = re.compile(r"(\.whl$|sample_submission/|HARNESS_README|(^|/)swegemma/|adk_submission/)", re.I)


def body_words(md: str) -> int:
    """Words before "## References": the host's ruling in the competition's "Word Count" discussion (Oct 27, 2026)."""
    return len(md.split("## References")[0].split())


def pdf_text(pdf: Path) -> str:
    from pypdf import PdfReader
    return " ".join(page.extract_text() or "" for page in PdfReader(str(pdf)).pages)


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("­", "").replace("-\n", "")).lower()


def tracked() -> list[str]:
    return subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.split()


def rows() -> list[tuple[str, str, str, str]]:
    """(rule, requirement, how checked, result) for each rule; result is PASS, FAIL or OWNER."""
    md = MD.read_text()
    text = norm(pdf_text(PDF)) if PDF.exists() else ""
    both = lambda s: s.lower() in norm(md) and s.lower() in text   # noqa: E731
    n = body_words(md)
    pdf_n = len(text.split())
    committed = [f for f in tracked() if COMPETITION_FILES.search(f)]
    r = lambda ok: "PASS" if ok else "FAIL"   # noqa: E731
    return [
        ("Paper track: length", f"at most {WORD_LIMIT:,} words, references excluded",
         "words before \"## References\" in the paper's text", f"{r(n <= WORD_LIMIT)} ({n:,} words)"),
        ("Paper track: the file submitted", "the PDF carries the same text as the paper",
         "PDF exists; its word count within 10% of the text's (layout adds page numbers, captions); title in it",
         r(PDF.exists() and abs(pdf_n - len(md.split())) <= 0.10 * len(md.split())
           and "can a small local agent redo a cloud agent" in text)),
        ("2.4.a Data access and use", "Competition Data used only as the Website and Rules permit",
         "the paper reports the evaluator's verdicts on this project's own tasks; no competition task is published",
         r(both("own verification") or both("competition's own")) ),
        ("2.4.b Data security", "Competition Data not redistributed",
         "no competition file (wheels, sample_submission, HARNESS_README, swegemma, adk_submission) is tracked",
         r(not committed) + (f": {', '.join(committed[:5])}" if committed else "")),
        ("2.5, 3.6.c Licences", "code under an OSI licence that allows commercial use",
         "the paper names Apache 2.0 for the code and CC BY 4.0 for the tasks; LICENSE is Apache 2.0",
         r(both("apache 2.0") and both("cc by 4.0") and "apache license" in (ROOT / "LICENSE").read_text().lower())),
        ("2.6 External data", "external data public and free to all Participants",
         "the task set's public Kaggle link is in the paper and the PDF", r(both(DATASET))),
        ("3.6.b Public code sharing", "code shared publicly, and on the competition's forum or notebooks",
         "the public repositories are linked in the paper and the PDF; the forum post is the owner's",
         ("PASS (links)" if all(both(x) for x in REPOS) else "FAIL (links)") + "; OWNER (forum post)"),
        ("3.4.b No hand labelling of test data", "no human labels of the competition's validation or test records",
         "the only screen in the paper is of this project's own tasks", r(both("screened 30 of the 93"))),
        ("3.14.a Original work", "the Submission is your own work; no third-party rights infringed",
         "the paper discloses the cloud agent's part and cites its sources", r(both("cloud agent") and "## references" in md.lower())),
        ("3.1.c Eligibility, employer", "not entered for an employer without its consent",
         "the paper states it is not affiliated with any employer; the employer's own policy is the owner's",
         ("PASS (statement)" if both("not affiliated") else "FAIL (statement)") + "; OWNER (employer policy)"),
        ("Honest reporting", "no number presented as a competition score",
         "the paper says no score here is a competition or leaderboard score",
         r(both("no number here is a competition score") or both("comparable to the leaderboard"))),
        ("3.5 Individual account, teams", "one Kaggle account; no private sharing outside a Team",
         "not checkable from files", "OWNER"),
        ("Paper track: AI-assisted writing", "whatever the paper-track page says about AI-written text",
         "not in the Official Rules; read the competition's Writeup instructions", "OWNER"),
    ]


def table(rs) -> str:
    head = ["# The paper against the competition's rules", "",
            "Written by `python paper/check_rules.py` from the paper's text, its PDF and this repository's files; do not",
            "edit by hand. OWNER rows are confirmed by the owner before submitting. A reading of the rules, not legal",
            "advice.", "", "| Rule | Requirement | How checked | Result |", "|---|---|---|---|"]
    return "\n".join(head + [f"| {a} | {b} | {c} | {d} |" for a, b, c, d in rs]) + "\n"


def main() -> int:
    rs = rows()
    out = table(rs)
    if "--check" in sys.argv and (not OUT.exists() or OUT.read_text() != out):
        print("paper/rules_check.md is out of date: run python paper/check_rules.py")
        return 1
    OUT.write_text(out)
    print(out)
    failed = [x[0] for x in rs if x[3].startswith("FAIL")]
    if failed:
        print("FAILED: " + "; ".join(failed))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
