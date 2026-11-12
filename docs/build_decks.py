"""Build the slide deck from its slide sources: docs/<deck>/slides/NN-<id>.html, one <section> per slide with the
speaker notes in its <aside>. Writes each deck's deck.html (one self-contained page that shows a slide at a time:
arrow keys or swipe to page, N for the notes; it prints as one slide a page) and full_text_and_notes.md (every
slide as an image, with its notes and its text, for reading on GitHub or for search).

    python docs/build_decks.py           # build every deck
    python docs/build_decks.py --check   # fail if a built file is behind its slides, if a slide carries a number
                                         # that neither the paper nor the README has, if the slide images and the
                                         # PDF were made from another build, or if the README, which shows the
                                         # slides, misses one (CI runs this)

The images (docs/<deck>/img/) and deck.pdf are drawn from deck.html by `node docs/render_slides.js`, which needs a
browser; run it after this script whenever a slide changes. The layout follows the source repository's
docs/build_decks.py, without its slide library: this deck has to open from a downloaded file.
"""

import hashlib
import html
import json
import re
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent
ROOT = DOCS.parent
PERSONAL = "A personal learning project, not affiliated with or endorsed by any employer, institution or vendor."
REPO = "https://github.com/healthtransformationlab/gemma-developer-agent"
PAPER = f"{REPO}/blob/main/paper/small-local-agent-redo-cloud-agent-work.pdf"
PAPER_MD = ROOT / "paper" / "small-local-agent-redo-cloud-agent-work.md"
# deck folder under docs/ -> (title, the line above the slides)
DECKS = {
    "pitch": ("Can a small local agent redo a cloud agent's work? The pitch",
              f"{PERSONAL} Every patient record in the source repository is synthetic. Each number is the paper's or the "
              "README's; paper/sources.md says where the paper's come from."),
}
FONTS = ("https://fonts.googleapis.com/css2?family=Libre+Baskerville:wght@400;700&family=Public+Sans:wght@400;500;600;700"
         "&display=swap")
HEAD = """<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><link rel="stylesheet" href="{fonts}">
<style>html,body{{height:100%}}body{{margin:0;background:#2b2b2b;font-family:'Public Sans',Arial,sans-serif;overflow:hidden}}*{{box-sizing:border-box;margin:0}}
td,th{{padding:12px 16px;border-bottom:1px solid #D9D3C4;vertical-align:top}}table{{border-collapse:collapse}}ul{{padding-left:1.2em}}
.topnav{{position:fixed;top:0;left:0;right:0;z-index:50;height:56px;background:#0F2A33;border-bottom:1px solid rgba(213,227,225,.14)}}
.topnav .bar{{height:100%;padding:0 16px;display:flex;align-items:center;justify-content:space-between;gap:12px}}
.home{{display:flex;align-items:center;gap:10px;font-family:'Libre Baskerville',Georgia,serif;font-weight:700;font-size:15px;color:#F7F5EF;text-decoration:none;white-space:nowrap}}
.home .mark{{display:grid;place-items:center;width:28px;height:28px;border-radius:8px;background:#F2A070;color:#0F2A33;font-size:15px}}
.home:hover .name{{text-decoration:underline}}
.topnav .links{{display:flex;flex:1 1 auto;justify-content:flex-end;align-items:center;gap:4px;min-width:0}}
.topnav .links a,.topnav button{{color:#D5E3E1;text-decoration:none;font:600 14px 'Public Sans',Arial,sans-serif;padding:7px 11px;border-radius:8px;background:none;border:0;cursor:pointer;white-space:nowrap}}
.topnav .links a:hover,.topnav button:hover{{color:#F7F5EF;background:rgba(255,255,255,.07)}}.topnav button[aria-pressed=true]{{color:#F2A070}}
.topnav .links a.cta{{background:#F2A070;color:#0F2A33;margin-left:6px}}.topnav .links a.cta:hover{{background:#F7F5EF}}
.topnav select{{flex:1 1 auto;width:300px;max-width:300px;min-width:72px;font:600 14px 'Public Sans',Arial,sans-serif;color:#F7F5EF;background:#15303A;border:1px solid rgba(213,227,225,.3);border-radius:8px;padding:6px 8px}}
.topnav .pager{{display:flex;flex:0 1 auto;align-items:center;gap:4px;min-width:0}}
.topnav .pager button{{color:#0F2A33;background:#F2A070;padding:7px 12px}}.topnav .pager button:hover{{color:#0F2A33;background:#F7F5EF}}
.topnav .pager button:disabled{{opacity:.35;cursor:default;background:#F2A070}}
.topnav button:focus-visible,.topnav select:focus-visible,.topnav a:focus-visible{{outline:2px solid #F7F5EF;outline-offset:2px}}
.disclaimer{{position:fixed;top:56px;left:0;right:0;z-index:40;padding:6px 16px;background:#15303A;color:#D5E3E1;font:13px/1.45 'Public Sans',Arial,sans-serif}}
.stage{{position:fixed;top:84px;left:0;right:0;bottom:0;overflow:hidden}}
.slides{{position:absolute;left:50%;top:50%;width:1920px;height:1080px;transform-origin:center center;transform:translate(-50%,-50%)}}
.slides>section{{width:1920px;height:1080px;overflow:hidden;text-align:left}}.slides aside{{display:none}}
.slides a{{color:inherit}}
.count{{position:fixed;right:14px;bottom:10px;z-index:30;font:600 13px 'Public Sans',Arial,sans-serif;background:rgba(15,42,51,.8);color:#F7F5EF;border-radius:6px;padding:3px 8px}}
.notes-panel{{position:fixed;left:0;right:0;bottom:0;z-index:45;max-height:35vh;overflow:auto;background:#f4f1ea;color:#222;padding:16px 20px 28px;font-size:15px;line-height:1.5;box-shadow:0 -8px 24px rgba(0,0,0,.3)}}
.notes-panel[hidden]{{display:none}}
@media screen{{.slides>section{{position:absolute;left:0;top:0}}.slides>section:not(.on){{display:none!important}}}}
/* printed, the deck is one slide a page, with nothing around it */
@media print{{@page{{size:1920px 1080px;margin:0}}html,body{{height:auto;overflow:visible;background:#fff}}
.topnav,.disclaimer,.notes-panel,.count{{display:none!important}}.stage{{position:static;overflow:visible}}
.slides{{position:static;transform:none!important;height:auto}}.slides>section{{position:relative;break-after:page}}}}
/* the slide picker shrinks first; then the name goes, then the paper's link; on phones the pager's labels go too,
   so Previous, the picker, Next and Notes always fit */
@media (max-width:1100px){{.home .name{{display:none}}}}
@media (max-width:820px){{.topnav .links a.deck{{display:none}}}}
@media (max-width:560px){{.topnav .pager .lbl,.topnav .links a.cta{{display:none}}.topnav .pager button{{padding:7px 13px;font-size:16px}}}}</style></head><body>
<nav class="topnav" aria-label="Deck"><div class="bar">
<a class="home" href="{repo}#readme" title="Back to the repository's README"><span class="mark" aria-hidden="true">←</span><span class="name">gemma-developer-agent</span></a>
<div class="links"><a class="deck" href="{paper}">The paper</a><span class="pager"><button id="deck-prev" aria-label="Previous slide" title="Previous slide (←)">‹<span class="lbl"> Previous</span></button>
<select id="deck-jump" aria-label="Go to slide">{options}</select>
<button id="deck-next" aria-label="Next slide" title="Next slide (→)"><span class="lbl">Next </span>›</button></span>
<button id="deck-notes-btn" aria-pressed="false" title="Speaker notes (N)">Notes</button>
<a class="cta" href="{repo}" target="_blank" rel="noopener">GitHub ↗</a></div></div></nav>
<p class="disclaimer" id="deck-disclaimer">{note}</p>
<main class="stage" id="deck-stage"><div class="slides" id="deck-slides">
"""
TAIL = """</div></main>
<p class="count" id="deck-count" aria-hidden="true"></p>
<div class="notes-panel" id="deck-notes" hidden></div>
<script>
document.querySelectorAll('.slides a[href^="http"]').forEach(function(a){a.target='_blank';a.rel='noopener'})
var slides=[].slice.call(document.querySelectorAll('#deck-slides>section')),at=0,box=document.getElementById('deck-slides'),
  stage=document.getElementById('deck-stage'),jump=document.getElementById('deck-jump'),prev=document.getElementById('deck-prev'),
  next=document.getElementById('deck-next'),panel=document.getElementById('deck-notes'),btn=document.getElementById('deck-notes-btn'),
  bar=document.getElementById('deck-disclaimer'),count=document.getElementById('deck-count')
// the slide area sits between the disclaimer (it wraps on narrow screens) and the notes panel, when open
function fit(){stage.style.top=(56+bar.offsetHeight)+'px';stage.style.bottom=(panel.hidden?0:panel.offsetHeight)+'px'
  box.style.transform='translate(-50%,-50%) scale('+Math.min(stage.clientWidth/1920,stage.clientHeight/1080)+')'}
function show(n,quiet){at=Math.max(0,Math.min(slides.length-1,n));slides.forEach(function(s,k){s.classList.toggle('on',k===at)})
  jump.selectedIndex=at;prev.disabled=at===0;next.disabled=at===slides.length-1;count.textContent=(at+1)+' / '+slides.length
  var a=slides[at].querySelector('aside');panel.innerHTML='<b>Slide '+(at+1)+' notes:</b> '+(a?a.innerHTML:'')
  if(!quiet&&history.replaceState)history.replaceState(null,'','#'+slides[at].id);fit()}
function fromHash(){var id=location.hash.slice(1);for(var k=0;k<slides.length;k++)if(slides[k].id===id)return k;return 0}
function toggleNotes(){var on=panel.hidden;panel.hidden=!on;btn.setAttribute('aria-pressed',on);fit()}
jump.addEventListener('change',function(){show(jump.selectedIndex);jump.blur()})
btn.addEventListener('click',toggleNotes)
// after a mouse click, blur so the arrow keys page again; a keyboard press (detail 0) keeps focus on the button
prev.addEventListener('click',function(e){show(at-1);if(e.detail)prev.blur()})
next.addEventListener('click',function(e){show(at+1);if(e.detail)next.blur()})
addEventListener('keydown',function(e){if(e.target.closest&&e.target.closest('.topnav')||e.altKey||e.ctrlKey||e.metaKey)return
  var k=e.key;if(k==='ArrowRight'||k==='PageDown'||k===' ')show(at+1);else if(k==='ArrowLeft'||k==='PageUp')show(at-1)
  else if(k==='Home')show(0);else if(k==='End')show(slides.length-1);else if(k==='n'||k==='N')toggleNotes();else return
  e.preventDefault()})
var x0=null,y0=null
stage.addEventListener('touchstart',function(e){x0=e.changedTouches[0].clientX;y0=e.changedTouches[0].clientY},{passive:true})
stage.addEventListener('touchend',function(e){if(x0===null)return;var dx=e.changedTouches[0].clientX-x0,dy=e.changedTouches[0].clientY-y0
  if(Math.abs(dx)>50&&Math.abs(dx)>Math.abs(dy)*1.5)show(at+(dx<0?1:-1));x0=null},{passive:true})
addEventListener('hashchange',function(){show(fromHash(),true)})
addEventListener('resize',fit)
show(fromHash(),true)
</script></body></html>
"""
NUMBER = re.compile(r"(?<![\w.])\d+(?:,\d{3})*(?:\.\d+)?%?(?!\w|[.,]\d)")   # 93, 2,269, 10.4%, 0.375; not the 4 of E4B


def slides(folder: Path):
    for path in sorted((folder / "slides").glob("[0-9][0-9]-*.html")):
        src = path.read_text(encoding="utf-8")
        notes = re.search(r"<aside>(.*?)</aside>", src, re.DOTALL)
        yield path.stem, re.sub(r"\s*<aside>.*?</aside>", "", src, flags=re.DOTALL), \
            notes.group(1).strip() if notes else ""


def visible_text(section: str) -> list[str]:
    section = re.sub(r"<svg.*?</svg>", "", section, flags=re.DOTALL)
    parts = (html.unescape(p).strip() for p in re.split(r"<[^>]+>", section))
    return [p for p in parts if p]


def heading(section: str, stem: str) -> str:
    """The slide's h1s or its h2, for the jump menu and the notes page."""
    found = re.findall(r"<h[12][^>]*>(.*?)</h[12]>", section, re.DOTALL)
    return " ".join(html.unescape(re.sub(r"<[^>]+>", "", f)).strip() for f in found) if found else stem


def render(deck: str) -> tuple[str, str]:
    """deck.html and full_text_and_notes.md for docs/<deck>/."""
    title, note = DECKS[deck]
    all_slides = list(slides(DOCS / deck))
    options = "".join(f'<option value="{stem.split("-", 1)[1]}">{n}. {html.escape(heading(section, stem))}</option>'
                      for n, (stem, section, _) in enumerate(all_slides, 1))
    out = [HEAD.format(title=html.escape(title), note=html.escape(note), repo=REPO, paper=PAPER, fonts=FONTS, options=options)]
    md = [f"# {title}: every slide, with its notes\n\n",
          f"{PERSONAL} Every patient record in the source repository is synthetic.\n\n",
          f"{len(all_slides)} slides. Each number is one that [the paper](../../paper/small-local-agent-redo-cloud-agent-work.md) or the "
          "[README](../../README.md) gives; [`paper/sources.md`](../../paper/sources.md) says where the paper's come from. To page through "
          "them: "
          "[`deck.pdf`](deck.pdf), or download [`deck.html`](deck.html) and open it in a browser.\n\n",
          "Built from [`slides/`](slides/) by `python docs/build_decks.py`; edit a slide, then rebuild and run "
          "`node docs/render_slides.js`.\n"]
    for n, (stem, section, notes) in enumerate(all_slides, 1):
        out.append(section.replace("</section>", f"<aside>{notes}</aside>\n</section>", 1) + "\n")
        head = heading(section, stem)
        md.append(f"\n## Slide {n}: {head}\n\n![Slide {n}: {head}](img/{stem}.png)\n")
        if notes:
            md.append(f"\n**Speaker notes:** {html.unescape(re.sub(r'<[^>]+>', '', notes))}\n")
        md.append("\n<details><summary>The slide's text</summary>\n\n" + "  \n".join(visible_text(section)) + "\n\n</details>\n")
    out.append(TAIL)
    return "".join(out), "".join(md)


def numbers(text: str) -> set[str]:
    return {m.group(0).rstrip("%") for m in NUMBER.finditer(text)}


def check(deck: str) -> list[str]:
    """What is wrong with docs/<deck>/ as committed; empty when nothing is."""
    folder, problems = DOCS / deck, []
    out, md = render(deck)
    for name, want in (("deck.html", out), ("full_text_and_notes.md", md)):
        path = folder / name
        if not path.exists() or path.read_text(encoding="utf-8") != want:
            problems.append(f"docs/{deck}/{name} is behind its slides: run python docs/build_decks.py")
    known = numbers(PAPER_MD.read_text(encoding="utf-8")) | numbers((ROOT / "README.md").read_text(encoding="utf-8"))
    for stem, section, notes in slides(folder):
        if not notes:
            problems.append(f"docs/{deck}/slides/{stem}.html has no speaker notes")
        text = " ".join(visible_text(section)) + " " + html.unescape(re.sub(r"<[^>]+>", " ", notes))
        for number in sorted(numbers(text) - known):
            problems.append(f"docs/{deck}/slides/{stem}.html has {number}, which is in neither the paper nor the README")
        if not (folder / "img" / f"{stem}.png").exists():
            problems.append(f"docs/{deck}/img/{stem}.png is missing: run node docs/render_slides.js")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if f"docs/{deck}/img/" in readme:               # the README folds the slides in: it must show every one
        for stem, _, _ in slides(folder):
            if f"(docs/{deck}/img/{stem}.png)" not in readme:
                problems.append(f"README.md shows the slides and misses docs/{deck}/img/{stem}.png")
    stamp = folder / "img" / "rendered.json"
    made_from = json.loads(stamp.read_text(encoding="utf-8")).get("deck_html_sha256") if stamp.exists() else None
    if made_from != hashlib.sha256(out.encode("utf-8")).hexdigest():
        problems.append(f"docs/{deck}/img/ and deck.pdf were drawn from another build of deck.html: run node docs/render_slides.js")
    if not (folder / "deck.pdf").exists():
        problems.append(f"docs/{deck}/deck.pdf is missing: run node docs/render_slides.js")
    return problems


def main(argv):
    checking = "--check" in argv
    decks = [a for a in argv if a != "--check"] or sorted(DECKS)
    unknown = set(decks) - set(DECKS)
    if unknown:
        sys.exit(f"unknown deck {', '.join(sorted(unknown))}: choose from {', '.join(sorted(DECKS))}")
    if checking:
        problems = [p for deck in decks for p in check(deck)]
        print("\n".join(problems) if problems else f"decks up to date: {', '.join(decks)}")
        sys.exit(1 if problems else 0)
    for deck in decks:
        out, md = render(deck)
        (DOCS / deck / "deck.html").write_text(out, encoding="utf-8")
        (DOCS / deck / "full_text_and_notes.md").write_text(md, encoding="utf-8")
        print(f"built docs/{deck}: deck.html, full_text_and_notes.md")


if __name__ == "__main__":
    main(sys.argv[1:])
