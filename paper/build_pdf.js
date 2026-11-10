// Build paper/small-local-agent-redo-cloud-agent-work.pdf (and paper/figures/figure1.png) from paper/small-local-agent-redo-cloud-agent-work.md.
//
//   python3 paper/figures/make_figure1.py   # only when a count in the figure changes
//   node paper/build_pdf.js                 # needs pandoc and Playwright's Chromium
//
// The PDF is the writeup's text, unchanged: this script only lays it out (title block, page numbers,
// tables that do not split across pages). Change the words in small-local-agent-redo-cloud-agent-work.md, never here.
const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const here = __dirname;
const md = path.join(here, 'small-local-agent-redo-cloud-agent-work.md');
const css = fs.readFileSync(path.join(here, 'pdf.css'), 'utf8');
const svgPath = path.join(here, 'figures', 'figure1.svg');

function html() {
  let body = execFileSync('pandoc', [md, '-f', 'gfm', '-t', 'html5', '--wrap=none'], { encoding: 'utf8' });
  // Everything before the abstract is the title block.
  const cut = body.indexOf('<h2 id="abstract">');
  if (cut < 0) throw new Error('small-local-agent-redo-cloud-agent-work.md has no "## Abstract" heading');
  body = `<header class="title-block">${body.slice(0, cut)}</header>\n<main>${body.slice(cut)}</main>`;
  // The abstract and the "Data and code" paragraph sit in a box on page 1.
  body = body.replace(/<h2 id="abstract">Abstract<\/h2>\s*(<p>[\s\S]*?<\/p>)\s*(<p><strong>Data and code\.<\/strong>[\s\S]*?<\/p>)/,
    (_, abstract, links) => `<section class="abstract"><h2 id="abstract">Abstract</h2>${abstract}${links.replace(/<\/a>\. /g, '</a>.<br>')}</section>`);
  // The figure goes in as vector art, with the image's alt text kept for screen readers.
  body = body.replace(/<p><img src="figures\/figure1\.png" alt="([^"]*)"\s*\/?><\/p>/,
    (_, alt) => `<figure><img src="file://${svgPath}" alt="${alt}"></figure>`);
  if (!body.includes('class="abstract"')) throw new Error('small-local-agent-redo-cloud-agent-work.md has no "Data and code." paragraph under the abstract');
  if (!body.includes('<figure>')) throw new Error('small-local-agent-redo-cloud-agent-work.md does not include figures/figure1.png');
  const title = (body.match(/<h1[^>]*>([\s\S]*?)<\/h1>/) || [])[1] || 'Writeup';
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"><title>${title.replace(/<[^>]+>/g, '')}</title>` +
    `<meta name="author" content="John Bowyer"><style>${css}</style></head><body>${body}</body></html>`;
}

(async () => {
  const browser = await chromium.launch();
  // 1. The figure as a PNG, for places that do not take SVG (a Kaggle writeup).
  const fig = await browser.newPage({ deviceScaleFactor: 3 });
  await fig.goto('file://' + svgPath);
  const box = await fig.evaluate(() => { const r = document.documentElement.getBoundingClientRect(); return { w: r.width, h: r.height }; });
  await fig.setViewportSize({ width: Math.ceil(box.w), height: Math.ceil(box.h) });
  await fig.screenshot({ path: path.join(here, 'figures', 'figure1.png') });
  // 2. The paper.
  const out = process.argv[2] || path.join(here, 'small-local-agent-redo-cloud-agent-work.pdf');
  const tmp = path.join(here, '.writeup.build.html');
  fs.writeFileSync(tmp, html());
  const page = await browser.newPage();
  await page.goto('file://' + tmp, { waitUntil: 'load' });
  const foot = 'font-family: Inter, Arial, sans-serif; font-size: 7.5pt; color: #666; width: 100%; padding: 0 0.9in; display: flex; justify-content: space-between;';
  await page.pdf({
    path: out, format: 'Letter', printBackground: true, displayHeaderFooter: true,
    margin: { top: '0.85in', bottom: '0.9in', left: '0.9in', right: '0.9in' },
    headerTemplate: '<span></span>',
    footerTemplate: `<div style="${foot}"><span>Bowyer · Can a small local agent redo a cloud agent's work? · Gemma 4 Developer Agent Competition, Paper Track</span>` +
      '<span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>',
  });
  fs.unlinkSync(tmp);
  await browser.close();
  console.log('wrote', out);
})();
