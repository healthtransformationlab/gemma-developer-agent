"""Put <w:suppressLineNumbers/> where Word's schema wants it in each paragraph's properties (#95).

The docx library writes it after the spacing and alignment, which the schema does not allow, so a strict reader
rejects the file. paper/build_docx.js calls this on the file the library wrote. Standard library only.

    python paper/fix_docx_order.py in.docx out.docx
"""
import re
import sys
import zipfile
from pathlib import Path

LEAD = re.compile(r"^((?:<w:(?:pStyle|keepNext|keepLines|pageBreakBefore|framePr|widowControl)\b[^>]*/>|<w:numPr>.*?</w:numPr>)*)", re.S)
TAG = "<w:suppressLineNumbers/>"


def fix(match: re.Match) -> str:
    body = match.group(1)
    if TAG not in body:
        return match.group(0)
    assert body.count(TAG) == 1
    body = body.replace(TAG, "")
    lead = LEAD.match(body).group(1)
    return "<w:pPr>" + lead + TAG + body[len(lead):] + "</w:pPr>"


def main(src: Path, dst: Path) -> int:
    moved = 0
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename.startswith("word/") and item.filename.endswith(".xml"):
                xml = data.decode("utf-8")
                if TAG in xml:
                    new = re.sub(r"<w:pPr>(.*?)</w:pPr>", fix, xml, flags=re.S)
                    assert new.count(TAG) == xml.count(TAG)
                    moved += xml.count(TAG)
                    data = new.encode("utf-8")
            zout.writestr(item, data)
    return moved


if __name__ == "__main__":
    source, target = Path(sys.argv[1]), Path(sys.argv[2])
    print("moved", main(source, target), "elements; wrote", target.name)
