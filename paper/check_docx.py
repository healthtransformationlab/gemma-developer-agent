"""The Word copy of the paper is built from the paper's current text (#95).

paper/build_docx.js writes the SHA-256 of small-local-agent-redo-cloud-agent-work.md into the Word file's description.
This fails when the two differ: the paper changed and the Word copy was not built again. Standard library only.

    python paper/check_docx.py
"""
import hashlib
import html
import re
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).parent
MD = HERE / "small-local-agent-redo-cloud-agent-work.md"
DOCX = HERE / "small-local-agent-redo-cloud-agent-work.docx"
BUILD = 'node paper/build_docx.js "<what the header should say>"'


def body_text(document_xml: str) -> str:
    """The text of a Word document's paragraphs, in order, tags removed."""
    paragraphs = re.findall(r"<w:p[ >].*?</w:p>", document_xml, flags=re.S)
    return " ".join(html.unescape("".join(re.findall(r"<w:t(?: [^>]*)?>(.*?)</w:t>", p, flags=re.S))) for p in paragraphs)


def problems() -> list[str]:
    if not DOCX.exists():
        return [f"{DOCX.name} is missing: run {BUILD}"]
    want = hashlib.sha256(MD.read_bytes()).hexdigest()
    with zipfile.ZipFile(DOCX) as z:
        core = z.read("docProps/core.xml").decode("utf-8")
        text = re.sub(r"\s+", " ", body_text(z.read("word/document.xml").decode("utf-8")))
    found = re.search(r"sha256 ([0-9a-f]{64})", core)
    out = []
    if not found:
        out.append(f"{DOCX.name} does not say which text it was built from: run {BUILD}")
    elif found.group(1) != want:
        out.append(f"{DOCX.name} was built from another version of {MD.name} ({found.group(1)[:12]}, now {want[:12]}): run {BUILD}")
    # the first sentence of the abstract, as the reader of the Word copy sees it
    abstract = MD.read_text(encoding="utf-8").split("## Abstract")[1].strip().replace("**", "")
    first = re.sub(r"\s+", " ", abstract.split(". ")[0])
    if first not in text:
        out.append(f"{DOCX.name} does not hold the abstract's first sentence")
    return out


if __name__ == "__main__":
    found = problems()
    for line in found:
        print("FAIL", line)
    if not found:
        print(f"ok: {DOCX.name} is built from the current {MD.name}")
    sys.exit(1 if found else 0)
