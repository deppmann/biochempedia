/**
 * agent-markdown — after the build, write a plain Markdown copy of every lesson for AI agents.
 *
 *   node scripts/agent-markdown.mjs <dist>        (run by the build: astro.config.mjs, astro:build:done)
 *
 * For each lesson in <dist>/catalog.json it reads the built page <dist>/lessons/<slug>/index.html and
 * writes <dist>/lessons/<slug>.md: title, summary, what you'll learn, then the lesson prose with its
 * section headings, lists, tables, worked examples, "check your prediction" answers, figure captions
 * and image descriptions, Equation Cards (as text) and film transcripts. Abbreviations come out spelled
 * out, as on the page. Left out: page furniture, simulations (named, not drawn), the practice and MCAT
 * questions and their answers, notes and highlights. It also writes <dist>/llms-full.txt, every lesson
 * in catalog order.
 *
 * It reads the BUILT page so the copy says exactly what a reader sees. If a page's layout changes so
 * the lesson body can't be found, the build fails rather than shipping empty copies.
 */
import { fromHtml } from 'hast-util-from-html';
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const dist = process.argv[2] || 'dist';
const SITE = 'https://biochemistrypedia.com';
const catalog = JSON.parse(readFileSync(join(dist, 'catalog.json'), 'utf8'));

const cls = (n) => (n.properties?.className || []).join(' ');
const has = (n, c) => (n.properties?.className || []).includes(c);
const find = (n, pred) => {
  if (pred(n)) return n;
  for (const c of n.children || []) { const r = find(c, pred); if (r) return r; }
  return null;
};
const SKIP = new Set(['script', 'style', 'svg', 'button', 'input', 'select', 'textarea', 'nav', 'form', 'video', 'audio', 'canvas', 'noscript', 'template', 'dialog']);
const squash = (s) => s.replace(/\s+/g, ' ').trim();

/** Plain text of a node, skipping controls and scripts. */
function text(n) {
  if (n.type === 'text') return n.value;
  if (n.type !== 'element' && n.type !== 'root') return '';
  if (SKIP.has(n.tagName) || n.properties?.ariaHidden === 'true') return '';
  if (n.tagName === 'br') return ' ';
  return (n.children || []).map(text).join('');
}

/** Inline Markdown for a run of phrasing content. */
function inline(n) {
  if (n.type === 'text') return n.value.replace(/([*_`\\])/g, '\\$1');
  if (n.type !== 'element') return '';
  if (SKIP.has(n.tagName) || n.properties?.ariaHidden === 'true') return '';
  const inner = () => (n.children || []).map(inline).join('');
  switch (n.tagName) {
    case 'strong': case 'b': { const t = inner().trim(); return t ? `**${t}**` : ''; }
    case 'em': case 'i': { const t = inner().trim(); return t ? `*${t}*` : ''; }
    case 'code': return '`' + text(n) + '`';
    case 'br': return ' ';
    case 'a': {
      const t = inner().trim();
      let href = String(n.properties?.href || '');
      if (!href || href.startsWith('#') || href.startsWith('javascript:')) return t;
      if (href.startsWith('/')) href = SITE + href;
      return t ? `[${t}](${href})` : '';
    }
    default: return inner();
  }
}

const para = (n) => squash(inline(n));

function table(t) {
  const rows = [];
  const walk = (n) => { if (n.tagName === 'tr') rows.push(n); else (n.children || []).forEach((c) => c.type === 'element' && walk(c)); };
  walk(t);
  if (!rows.length) return '';
  const cells = rows.map((r) => (r.children || []).filter((c) => c.tagName === 'td' || c.tagName === 'th').map((c) => para(c).replace(/\|/g, '\\|')));
  const w = Math.max(...cells.map((r) => r.length));
  const line = (r) => '| ' + Array.from({ length: w }, (_, i) => r[i] ?? '').join(' | ') + ' |';
  return [line(cells[0]), '| ' + Array(w).fill('---').join(' | ') + ' |', ...cells.slice(1).map(line)].join('\n') + '\n\n';
}

function list(n, depth = 0) {
  const ordered = n.tagName === 'ol';
  let out = '';
  let i = 1;
  for (const li of n.children || []) {
    if (li.tagName !== 'li') continue;
    const own = { type: 'element', tagName: 'span', children: (li.children || []).filter((c) => c.tagName !== 'ul' && c.tagName !== 'ol') };
    out += `${'  '.repeat(depth)}${ordered ? `${i++}.` : '-'} ${para(own)}\n`;
    for (const sub of li.children || []) if (sub.tagName === 'ul' || sub.tagName === 'ol') out += list(sub, depth + 1);
  }
  return depth === 0 ? out + '\n' : out;
}

const quote = (s) => s.trim().split('\n').map((l) => (l ? `> ${l}` : '>')).join('\n') + '\n\n';

/** Text of a formula: button labels count, <sub>/<sup> become _x and ^x ("I_ion = g_ion × (Vm − E_ion)"). */
function formula(n) {
  if (n.type === 'text') return n.value;
  if (n.type !== 'element' || n.tagName === 'script' || n.tagName === 'style') return '';
  const inner = (n.children || []).map(formula).join('');
  if (n.tagName === 'sub') return `_${inner}`;
  if (n.tagName === 'sup') return `^${inner}`;
  // Block-level pieces (the steps of a worked example) are separated, not run together.
  if (['li', 'p', 'div', 'dt', 'dd', 'br', 'summary'].includes(n.tagName)) return ` ${inner} `;
  return inner;
}

/** An Equation Card as Markdown: what it is for, the formula, the words, the symbols, then its worked parts. */
function equationCard(f) {
  const lines = [];
  const kids = (f.children || []).filter((c) => c.type === 'element');
  const strip = (n) => ({ ...n, children: (n.children || []).filter((c) => !has(c, 'eqc-kicker')) });
  for (const c of kids) {
    if (has(c, 'eqc-purpose')) lines.push(`**Equation card: ${squash(text(strip(c)))}**`);
    else if (has(c, 'eqc-eq')) lines.push('', '    ' + squash(formula(c)), '');
    else if (has(c, 'eqc-say')) { const t = find(c, (x) => has(x, 'eqc-say-text')); if (t) lines.push(`In words: ${squash(text(t))}`); }
    else if (has(c, 'eqc-key')) {
      lines.push('');
      for (const row of (c.children || []).filter((r) => has(r, 'eqc-row'))) {
        const sym = find(row, (x) => has(x, 'eqc-symtxt'));
        const dd = find(row, (x) => x.tagName === 'dd');
        const unit = dd && find(dd, (x) => has(x, 'eqc-unit'));
        const def = dd ? squash(formula({ ...dd, children: (dd.children || []).filter((x) => x !== unit) })) : '';
        lines.push(`- ${squash(formula(sym || row))}: ${def}${unit ? ` (${squash(text(unit))})` : ''}`);
      }
      lines.push('');
    } else {
      const k = find(c, (x) => has(x, 'eqc-kicker'));
      const label = k ? squash(text(k)) : '';
      if (/refresher/i.test(label) || /^Need a refresher/i.test(squash(text(c)))) continue;
      const body = squash(formula(strip(c)).replace(/▶ Read aloud/g, ''));
      if (body) lines.push(`${label ? `${label.replace(/[.:]?$/, ':')} ` : ''}${body}`);
    }
  }
  return quote(lines.join('\n')) ;
}

function figure(f) {
  const c = cls(f);
  if (has(f, 'lf')) return ''; // a film player; its transcript follows it on the page
  if (has(f, 'lesson-figure')) {
    const img = find(f, (n) => n.tagName === 'img');
    const cap = find(f, (n) => n.tagName === 'figcaption');
    const alt = squash(String(img?.properties?.alt || '')).replace(/^AI-generated illustration:\s*/i, '');
    const capText = cap ? para(cap).replace(/\s*AI-generated illustration\.?\s*$/i, '') : '';
    return `*Figure (AI-generated illustration).* ${capText}${alt ? ` Image: ${alt}` : ''}`.trim() + '\n\n';
  }
  if (has(f, 'eqc')) return equationCard(f);
  // Any other figure is an interactive simulation or diagram on the page.
  const title = squash(text(f)).split('⚙')[0].split(/drag the sliders/i)[0].trim().slice(0, 120);
  return title ? `*Interactive on the lesson page:* ${title}\n\n` : '';
}

function details(d) {
  const sum = find(d, (n) => n.tagName === 'summary');
  const label = sum ? squash(text(sum)) : '';
  const rest = { type: 'element', tagName: 'div', children: (d.children || []).filter((c) => c !== sum) };
  const body = blocks(rest).trim();
  if (!body) return '';
  if (has(d, 'film-transcript')) {
    const title = label.replace(/^Read the transcript of\s*/i, '').replace(/^[“"]|[”"]$/g, '');
    return `**Film transcript: ${title}**\n\n${body.replace(/^Film transcript:[^\n]*\n+/i, '')}\n\n`;
  }
  return quote(`**${label.replace(/[.:]?$/, '.')}** ${body}`);
}

function blocks(n) {
  let out = '';
  for (const c of n.children || []) {
    if (c.type === 'text') { const t = squash(c.value); if (t) out += t + '\n\n'; continue; }
    if (c.type !== 'element' || SKIP.has(c.tagName)) continue;
    if (c.properties?.ariaHidden === 'true') continue;
    switch (c.tagName) {
      case 'p': { const t = para(c); if (t) out += t + '\n\n'; break; }
      case 'h2': out += `## ${squash(text(c))}\n\n`; break;
      case 'h3': out += `### ${squash(text(c))}\n\n`; break;
      case 'h4': case 'h5': case 'h6': out += `#### ${squash(text(c))}\n\n`; break;
      case 'ul': case 'ol': out += list(c); break;
      case 'blockquote': { const t = blocks(c); if (t.trim()) out += quote(t); break; }
      case 'table': out += table(c); break;
      case 'figure': out += figure(c); break;
      case 'details': out += details(c); break;
      case 'hr': out += '---\n\n'; break;
      case 'aside': break;
      case 'div': case 'section': case 'span': {
        if (has(c, 'design-answer') || has(c, 'hl-notes')) break; // answer boxes and personal notes
        if (has(c, 'table-cards')) { const t = find(c, (x) => x.tagName === 'table'); if (t) out += table(t); break; }
        out += blocks(c);
        break;
      }
      default: { const t = para(c); if (t) out += t + '\n\n'; }
    }
  }
  return out;
}

const full = [
  '# Biochemistrypedia: every lesson',
  '',
  `> Every lesson on ${SITE}, as plain Markdown, in course order. One lesson: ${SITE}/lessons/{slug}.md. Index: ${SITE}/llms.txt.`,
  '',
];
let written = 0;
for (const course of catalog.courses) {
  full.push(`# Course: ${course.title}`, '', `${course.tagline} Level: ${course.level}. ${course.url}`, '');
  for (const unit of course.units) {
    for (const l of unit.lessons) {
      const page = join(dist, 'lessons', l.slug, 'index.html');
      if (!existsSync(page)) throw new Error(`agent-markdown: no built page for ${l.slug}`);
      const tree = fromHtml(readFileSync(page, 'utf8'));
      const main = find(tree, (x) => x.tagName === 'div' && has(x, 'lesson-main'));
      const body = main && (main.children || []).find((x) => x.tagName === 'div' && has(x, 'prose-col'));
      if (!body) throw new Error(`agent-markdown: lesson body not found in ${page}; did the lesson page layout change?`);
      const review = find(tree, (x) => has(x, 'under-review-tag'));
      const head = [
        `# ${l.title}`,
        '',
        `> ${squash(l.summary)}`,
        '',
        `Course: ${course.title}${unit.name && course.units.length > 1 ? ` (${unit.name})` : ''}. Level: ${course.level}.${l.minutes ? ` About ${l.minutes} minutes.` : ''}`,
        `Lesson page (link this one when citing): ${l.url}`,
        ...(review ? ['Note: parts of this lesson are still being checked ("Under review").'] : []),
        '',
      ];
      if (l.objectives?.length) head.push("## What you'll learn", '', ...l.objectives.map((o) => `- ${squash(o)}`), '');
      const md = (head.join('\n') + '\n' + blocks(body))
        .replace(/\n{3,}/g, '\n\n')
        .trim() + `\n\n---\n\nFrom Biochemistrypedia (${SITE}), free lessons by Christopher Deppmann. Lesson text © the authors. Practice questions: ${l.url}\n`;
      writeFileSync(join(dist, 'lessons', `${l.slug}.md`), md);
      full.push(md.replace(/^(#+) /gm, '#$1 '), '');
      written++;
    }
  }
}
writeFileSync(join(dist, 'llms-full.txt'), full.join('\n'));
console.log(`agent-markdown: ${written} lesson Markdown copies and llms-full.txt written`);
