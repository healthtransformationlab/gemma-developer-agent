// Draw each slide of a deck as an image, and the whole deck as a PDF, from the built docs/<deck>/deck.html:
//   python docs/build_decks.py && node docs/render_slides.js [deck ...]
// Writes docs/<deck>/img/NN-<id>.png (one per slide, 1920 x 1080), docs/<deck>/deck.pdf (one slide a page),
// docs/img/<deck>_deck_cover.png (the first slide, for the README) and docs/<deck>/img/rendered.json, which records
// the build of deck.html these were drawn from: `python docs/build_decks.py --check` fails when it is another one.
// Needs Playwright with Chromium (`npm i playwright && npx playwright install chromium`), and the two fonts the
// slides name (Libre Baskerville, Public Sans), from Google Fonts over the network or installed on the machine.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { chromium } = require('playwright');

const docs = __dirname;
const decks = process.argv.slice(2).length ? process.argv.slice(2) : ['pitch'];

(async () => {
  const browser = await chromium.launch();
  for (const deck of decks) {
    const folder = path.join(docs, deck);
    const htmlPath = path.join(folder, 'deck.html');
    const stems = fs.readdirSync(path.join(folder, 'slides')).filter(f => /^\d\d-.*\.html$/.test(f)).sort().map(f => f.replace(/\.html$/, ''));
    const imgDir = path.join(folder, 'img');
    fs.mkdirSync(imgDir, { recursive: true });
    for (const old of fs.readdirSync(imgDir)) if (old.endsWith('.png')) fs.unlinkSync(path.join(imgDir, old));

    const page = await browser.newPage({ viewport: { width: 1920, height: 1200 }, deviceScaleFactor: 1 });
    await page.goto('file://' + htmlPath, { waitUntil: 'domcontentloaded' });
    await page.evaluate(() => Promise.race([document.fonts.ready, new Promise(r => setTimeout(r, 8000))]));
    const fonts = await page.evaluate(() => ['700 40px "Libre Baskerville"', '400 40px "Public Sans"'].map(f => f + ': ' + document.fonts.check(f)));
    // the slide area is the window less the nav and the disclaimer: size the window so a slide is drawn 1:1
    const top = await page.evaluate(() => 56 + document.getElementById('deck-disclaimer').offsetHeight);
    await page.setViewportSize({ width: 1920, height: 1080 + top });
    await page.addStyleTag({ content: '.count{display:none!important}' });
    const count = await page.evaluate(() => document.querySelectorAll('#deck-slides>section').length);
    if (count !== stems.length) throw new Error(`${deck}: ${count} slides in deck.html, ${stems.length} in slides/: rebuild first`);
    const overflow = [];
    for (let k = 0; k < count; k++) {
      await page.evaluate(n => { document.getElementById('deck-jump').selectedIndex = n; document.getElementById('deck-jump').dispatchEvent(new Event('change')); }, k);
      await page.waitForTimeout(120);
      // a slide whose content runs past its 1080 px is cut off: say so, since the picture would hide it
      const over = await page.evaluate(() => { const s = document.querySelector('#deck-slides>section.on'); return Math.max(s.scrollHeight - s.clientHeight, s.scrollWidth - s.clientWidth); });
      if (over > 0) overflow.push(`${stems[k]} (+${over}px)`);
      await page.locator('#deck-slides').screenshot({ path: path.join(imgDir, stems[k] + '.png') });
    }
    // the cover for the README, at two thirds of the size
    const small = await browser.newPage({ viewport: { width: 1920, height: 1080 + top }, deviceScaleFactor: 2 / 3 });
    await small.goto('file://' + htmlPath, { waitUntil: 'domcontentloaded' });
    await small.evaluate(() => Promise.race([document.fonts.ready, new Promise(r => setTimeout(r, 8000))]));
    await small.addStyleTag({ content: '.count{display:none!important}' });
    fs.mkdirSync(path.join(docs, 'img'), { recursive: true });
    await small.locator('#deck-slides').screenshot({ path: path.join(docs, 'img', `${deck}_deck_cover.png`) });
    await small.close();
    // the PDF: the deck's own print layout, one slide a page
    await page.emulateMedia({ media: 'print' });
    await page.pdf({ path: path.join(folder, 'deck.pdf'), preferCSSPageSize: true, printBackground: true });
    await page.close();

    const sha = crypto.createHash('sha256').update(fs.readFileSync(htmlPath)).digest('hex');
    fs.writeFileSync(path.join(imgDir, 'rendered.json'), JSON.stringify({ deck_html_sha256: sha, slide_count: count }, null, 2) + '\n');
    console.log(`drew docs/${deck}: ${count} slides, deck.pdf, the cover; fonts ${fonts.join(', ')}`);
    if (overflow.length) { console.error('cut off: ' + overflow.join(', ')); process.exitCode = 1; }
  }
  await browser.close();
})();
