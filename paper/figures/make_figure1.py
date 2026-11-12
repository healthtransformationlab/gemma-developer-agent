"""Draw Figure 1 of the writeup: task counts at each step, on one scale.

Run from anywhere: python3 paper/figures/make_figure1.py
Writes figure1.svg beside this file. paper/build_pdf.js turns it into figure1.png.

Every count is already in paper/small-local-agent-redo-cloud-agent-work.md; paper/sources.md says where each comes from. A count that changes there
changes here: the lists below are the only place the figure's numbers live.
"""
from html import escape
from pathlib import Path

GROUPS = [
    ("Building the task set (Sections 4 and 5)", [
        ("Merged changes mined", 197),
        ("Touch code and tests (candidates)", 116),
        ("Built, pass both gates, licensed", 113),
        ("Verified by the competition's evaluator (published)", 93),
    ]),
    ("Baseline: Gemma 4 E4B on published tasks (Section 6)", [
        ("Attempted and scored", 48),
        ("Wrote a patch", 40),
        ("Resolved", 5),
    ]),
    ("Pre-registered experiment on one A100: resolved, of 93 (Section 6). No difference detected.", [
        ("As published", 4),
        ("With graph retrieval", 6),
        ("With the failing test's report, from the hidden test", 4),
    ]),
    ("AI-assisted screen of the published tasks, and what five Colab runs resolved (Section 6): a description, not a test.", [
        ("Tests need a name or text the statement never gives", 76),
        ("of those 76, resolved in some Colab run", 1),
        ("Pass both questions (the core split)", 17),
        ("of those 17, resolved in some Colab run", 8),
    ]),
]
TITLE = "Figure 1. Task counts at each step, on one scale."

WIDTH, LEFT, BAR_X, BAR_MAX = 720, 12, 356, 300      # px; BAR_MAX is the length of the longest bar
BAR_H, ROW, HEAD, GAP, TOP = 12, 19, 22, 8, 32        # bar thickness, row pitch, group heading, gap between groups
INK, INK_2, RULE, BAR = "#0b0b0b", "#52514e", "#c9c8c2", "#2a78d6"
FONT = "Inter, 'Helvetica Neue', Arial, 'Liberation Sans', sans-serif"


def bar(x, y, length, h, r=4):
    """A bar square at the baseline and rounded at its data end."""
    r = min(r, length / 2, h / 2)
    return (f"M{x},{y} h{length - r:.1f} a{r},{r} 0 0 1 {r},{r} v{h - 2 * r:.1f} "
            f"a{r},{r} 0 0 1 -{r},{r} h-{length - r:.1f} z")


def build():
    top = max(v for _, rows in GROUPS for _, v in rows)
    out, y = [], TOP
    out.append(f'<text x="{LEFT}" y="20" font-size="13" font-weight="600" fill="{INK}">{escape(TITLE)}</text>')
    for heading, rows in GROUPS:
        y += GAP
        out.append(f'<text x="{LEFT}" y="{y + 12}" font-size="11.5" font-weight="600" fill="{INK}">{escape(heading)}</text>')
        y += HEAD
        y0 = y
        for label, value in rows:
            length = BAR_MAX * value / top
            mid = y + BAR_H / 2 + 4
            out.append(f'<text x="{BAR_X - 10}" y="{mid}" font-size="11.5" text-anchor="end" fill="{INK_2}">{escape(label)}</text>')
            out.append(f'<path d="{bar(BAR_X, y, length, BAR_H)}" fill="{BAR}"><title>{escape(label)}: {value}</title></path>')
            out.append(f'<text x="{BAR_X + length + 7:.1f}" y="{mid}" font-size="11.5" font-weight="600" fill="{INK}">{value}</text>')
            y += ROW
        out.append(f'<line x1="{BAR_X}" y1="{y0 - 4}" x2="{BAR_X}" y2="{y - ROW + BAR_H + 4}" stroke="{RULE}" stroke-width="1"/>')
    height = y + 6
    described = "; ".join(f"{label}: {value}" for _, rows in GROUPS for label, value in rows)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {height}" width="{WIDTH}" height="{height}" '
            f'role="img" aria-label="{escape(TITLE)} {escape(described)}" font-family="{FONT}">\n'
            f'<rect width="{WIDTH}" height="{height}" fill="#ffffff"/>\n' + "\n".join(out) + "\n</svg>\n")


if __name__ == "__main__":
    target = Path(__file__).with_name("figure1.svg")
    target.write_text(build(), encoding="utf-8")
    print("wrote", target)
