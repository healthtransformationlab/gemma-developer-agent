// Build paper/small-local-agent-redo-cloud-agent-work.docx, the Word copy of the paper for peer review, from
// paper/small-local-agent-redo-cloud-agent-work.md (#95).
//
//   node paper/build_docx.js "Review copy · version 14 · November 12, 2026 · repository commit d6decb4"
//
// The one argument is what the header of every page says: which version this copy is. Needs pandoc, the `docx`
// package (npm install -g docx) and Python 3. The body is the paper's text, word for word: change the words in the
// Markdown, never here. Added for reviewers: line numbers, page numbers and the header. The file's description
// holds the SHA-256 of the Markdown it was built from, which paper/check_docx.py compares with the paper's.
const { execFileSync } = require('child_process');
const crypto = require('crypto');
const fs = require('fs');
const os = require('os');
const path = require('path');
const d = require('docx');

const here = __dirname;
const mdPath = path.join(here, 'small-local-agent-redo-cloud-agent-work.md');
const figurePath = path.join(here, 'figures', 'figure1.png');
const outPath = path.join(here, 'small-local-agent-redo-cloud-agent-work.docx');
const stamp = (process.argv[2] || '').trim();
if (!stamp) {
  console.error('say what the header should say, e.g. node paper/build_docx.js "Review copy · version 14 · November 12, 2026 · repository commit d6decb4"');
  process.exit(1);
}
const mdSha256 = crypto.createHash('sha256').update(fs.readFileSync(mdPath)).digest('hex');
const ast = JSON.parse(execFileSync('pandoc', [mdPath, '-f', 'gfm', '-t', 'json'], { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 }));
const SERIF = 'Times New Roman', SANS = 'Arial', MONO = 'Courier New';
const WIDTH = 9360;                                   // 6.5 in of text on US Letter with 1 in margins, in DXA
const LINK = '0563C1';

// ---- inlines: a list of pandoc inlines -> runs, with neighbouring text of one format merged into one run
function runs(inl, fmt = {}) {
  const out = [];
  let buf = '';
  const flush = () => {
    if (!buf) return;
    out.push(new d.TextRun({ text: buf, bold: fmt.bold, italics: fmt.italics, size: fmt.size, font: fmt.font,
      color: fmt.color, underline: fmt.underline }));
    buf = '';
  };
  for (const x of inl) {
    if (x.t === 'Str') buf += x.c;
    else if (x.t === 'Space' || x.t === 'SoftBreak') buf += ' ';
    else if (x.t === 'Strong') { flush(); out.push(...runs(x.c, { ...fmt, bold: true })); }
    else if (x.t === 'Emph') { flush(); out.push(...runs(x.c, { ...fmt, italics: true })); }
    else if (x.t === 'Code') {
      flush();
      out.push(new d.TextRun({ text: x.c[1], font: MONO, size: fmt.size ? fmt.size - 2 : 20, bold: fmt.bold, italics: fmt.italics }));
    } else if (x.t === 'Link') {
      flush();
      out.push(new d.ExternalHyperlink({ link: x.c[2][0], children: runs(x.c[1], { ...fmt, color: LINK, underline: { type: d.UnderlineType.SINGLE } }) }));
    } else if (x.t === 'Image') {
      flush();
      const alt = x.c[1].map(i => (i.t === 'Str' ? i.c : ' ')).join('');
      out.push(new d.ImageRun({ type: 'png', data: fs.readFileSync(figurePath), transformation: { width: 624, height: Math.round(624 * 1272 / 2160) },
        altText: { title: 'Figure 1', name: 'Figure 1', description: alt + '. Bars of task counts at each step: building the task set, the baseline, the pre-registered experiment and the screen.' } }));
    } else throw new Error('inline not handled: ' + x.t);
  }
  flush();
  return out;
}
const text = inl => inl.map(x => (x.t === 'Str' ? x.c : x.t === 'Space' || x.t === 'SoftBreak' ? ' ' : x.t === 'Code' ? x.c[1] : Array.isArray(x.c) ? text(x.t === 'Link' || x.t === 'Image' ? x.c[1] : x.c) : '')).join('');

// ---- tables
function table(c) {
  const head = c[3][1], bodies = c[4];
  const rows = [...head.map(r => ({ cells: r[1], header: true })), ...bodies.flatMap(b => b[3].map(r => ({ cells: r[1], header: false })))];
  const n = rows[0].cells.length;
  const cellText = cell => cell[4].map(b => text(b.c)).join(' ');
  // widths in proportion to the longest text in each column, within bounds, summing to the text width
  const weight = Array.from({ length: n }, (_, k) => Math.min(46, Math.max(9, ...rows.map(r => cellText(r.cells[k]).length))));
  const total = weight.reduce((a, b) => a + b, 0);
  const widths = weight.map(w => Math.round(WIDTH * w / total));
  widths[n - 1] += WIDTH - widths.reduce((a, b) => a + b, 0);
  const line = { style: d.BorderStyle.SINGLE, size: 4, color: 'BFBFB8' };
  return new d.Table({
    width: { size: WIDTH, type: d.WidthType.DXA }, columnWidths: widths,
    rows: rows.map(r => new d.TableRow({
      tableHeader: r.header, cantSplit: true,
      children: r.cells.map((cell, k) => new d.TableCell({
        width: { size: widths[k], type: d.WidthType.DXA },
        shading: r.header ? { type: d.ShadingType.CLEAR, color: 'auto', fill: 'EAE8E1' } : undefined,
        margins: { top: 60, bottom: 60, left: 100, right: 100 },
        borders: { top: line, bottom: line, left: line, right: line },
        children: cell[4].length ? cell[4].map(b => new d.Paragraph({ spacing: { before: 0, after: 0, line: 252, lineRule: d.LineRuleType.AUTO }, suppressLineNumbers: true,
          children: runs(b.c, { font: SANS, size: 18, bold: r.header || undefined }) })) : [new d.Paragraph({ spacing: { before: 0, after: 0, line: 252, lineRule: d.LineRuleType.AUTO }, suppressLineNumbers: true, children: [] })],
      })),
    })),
  });
}

// ---- blocks
const children = [];
const numbering = [{ reference: 'bullets', levels: [{ level: 0, format: d.LevelFormat.BULLET, text: '•', alignment: d.AlignmentType.LEFT,
  style: { paragraph: { indent: { left: 540, hanging: 270 } } } }] }];
let ordered = 0, seenAbstract = false, titleSeen = false, front = 0;

function listItems(items, ref, size) {
  for (const item of items) item.forEach((b, k) => {
    if (b.t !== 'Plain' && b.t !== 'Para') throw new Error('list block not handled: ' + b.t);
    children.push(new d.Paragraph({ numbering: k === 0 ? { reference: ref, level: 0 } : undefined, indent: k ? { left: 540 } : undefined,
      spacing: { after: 80 }, children: runs(b.c, size ? { size } : {}) }));
  });
}

for (const b of ast.blocks) {
  if (b.t === 'Header') {
    const [level, , inl] = b.c;
    if (level === 1) { titleSeen = true; children.push(new d.Paragraph({ heading: d.HeadingLevel.TITLE, alignment: d.AlignmentType.CENTER, children: runs(inl) })); continue; }
    if (level === 2 && !seenAbstract) seenAbstract = true;
    children.push(new d.Paragraph({ heading: level === 2 ? d.HeadingLevel.HEADING_1 : d.HeadingLevel.HEADING_2, children: runs(inl) }));
  } else if (b.t === 'Para') {
    if (b.c.length === 1 && b.c[0].t === 'Image') {
      children.push(new d.Paragraph({ alignment: d.AlignmentType.CENTER, spacing: { before: 160, after: 200, line: 240, lineRule: d.LineRuleType.AUTO }, suppressLineNumbers: true, children: runs(b.c) }));
    } else if (titleSeen && !seenAbstract) {
      // the title block: subtitle, author, track, disclaimer
      front += 1;
      const fmt = front === 1 ? { font: SANS, size: 24 } : front === 4 ? { size: 20, color: '444444' } : { font: SANS, size: 21 };
      children.push(new d.Paragraph({ alignment: d.AlignmentType.CENTER, spacing: { after: front === 1 ? 200 : front === 4 ? 280 : 60 }, children: runs(b.c, fmt) }));
    } else children.push(new d.Paragraph({ children: runs(b.c) }));
  } else if (b.t === 'BulletList') listItems(b.c, 'bullets');
  else if (b.t === 'OrderedList') {
    ordered += 1;
    const ref = 'ordered' + ordered;
    const isRefs = b.c[1].length > 10;                // the reference list is the long one
    numbering.push({ reference: ref, levels: [{ level: 0, format: d.LevelFormat.DECIMAL, text: '%1.', alignment: d.AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 540, hanging: 400 } } } }] });
    listItems(b.c[1], ref, isRefs ? 20 : undefined);
  } else if (b.t === 'Table') { children.push(table(b.c)); children.push(new d.Paragraph({ spacing: { after: 60 }, suppressLineNumbers: true, children: [] })); }
  else throw new Error('block not handled: ' + b.t);
}

const small = { font: SANS, size: 16, color: '666666' };
const doc = new d.Document({
  creator: 'John Bowyer', title: "Can a small local agent redo a cloud agent's work?",
  description: `Review copy of the paper. ${stamp}. Built from the paper's Markdown, sha256 ${mdSha256}`,
  styles: {
    default: {
      document: { run: { font: SERIF, size: 22 }, paragraph: { spacing: { after: 140, line: 300, lineRule: d.LineRuleType.AUTO } } },
      title: { run: { font: SANS, size: 40, bold: true }, paragraph: { spacing: { before: 0, after: 160, line: 264, lineRule: d.LineRuleType.AUTO }, keepNext: true } },
      heading1: { run: { font: SANS, size: 28, bold: true, color: '111111' }, paragraph: { spacing: { before: 320, after: 120 }, keepNext: true } },
      heading2: { run: { font: SANS, size: 24, bold: true, color: '111111' }, paragraph: { spacing: { before: 240, after: 100 }, keepNext: true } },
    },
    paragraphStyles: [{ id: 'SmallPrint', name: 'Small print', basedOn: 'Normal', quickFormat: true, run: { font: SANS, size: 16, color: '666666' },
      paragraph: { spacing: { before: 0, after: 0, line: 240, lineRule: d.LineRuleType.AUTO } } }],
  },
  numbering: { config: numbering },
  sections: [{
    properties: {
      page: { size: { width: 12240, height: 15840 }, margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } },
      lineNumbers: { countBy: 1, restart: d.LineNumberRestartFormat.CONTINUOUS, distance: 360 },
    },
    headers: { default: new d.Header({ children: [new d.Paragraph({ style: 'SmallPrint', alignment: d.AlignmentType.RIGHT, suppressLineNumbers: true, children: [new d.TextRun({ text: stamp, ...small })] })] }) },
    footers: { default: new d.Footer({ children: [new d.Paragraph({ style: 'SmallPrint', alignment: d.AlignmentType.CENTER, suppressLineNumbers: true,
      children: [new d.TextRun({ text: "Bowyer · Can a small local agent redo a cloud agent's work? · page ", ...small }), new d.TextRun({ children: [d.PageNumber.CURRENT], ...small }),
        new d.TextRun({ text: ' of ', ...small }), new d.TextRun({ children: [d.PageNumber.TOTAL_PAGES], ...small })] })] }) },
    children,
  }],
});

d.Packer.toBuffer(doc).then(buf => {
  const raw = path.join(os.tmpdir(), `paper-docx-${process.pid}.docx`);
  fs.writeFileSync(raw, buf);
  // the library writes one paragraph property where Word's schema does not allow it: put it in its place
  execFileSync('python3', [path.join(here, 'fix_docx_order.py'), raw, outPath], { stdio: 'inherit' });
  fs.unlinkSync(raw);
  console.log('wrote', path.relative(process.cwd(), outPath), fs.statSync(outPath).size, 'bytes;', children.length, 'blocks; built from sha256', mdSha256.slice(0, 12));
});
