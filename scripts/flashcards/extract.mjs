#!/usr/bin/env node
/* Deterministic first stage of the flashcard pipeline (no model, no tokens).

   node scripts/flashcards/extract.mjs <slug> [outDir]

   Writes two files to outDir (default: the current directory):
     digest.md   the compact text a model drafts from: the lesson body as plain
                 sections, the objectives and the quiz keys. It leaves out the
                 frontmatter a card never needs (films, scientists' stories,
                 explain-at-my-level texts), which is about 40% of the file.
     extract.json  an extraction-only deck: definitions as cloze cards, the
                 lesson's rule boxes and equations, every Predict box and
                 worked problem, and the quiz as recall cards. This is arm X of
                 the pilot A/B test, and the scaffold the model arms start from. */

import { readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import yaml from 'js-yaml';
import { splitMdx, plain, sections, norm, hash } from './lib.mjs';

const [slug, outDir = '.'] = process.argv.slice(2);
if (!slug) { console.error('usage: extract.mjs <slug> [outDir]'); process.exit(2); }
const src = readFileSync(join('src/content/lessons', slug, 'lesson.mdx'), 'utf8');
const { fm, body } = splitMdx(src);
const meta = yaml.load(fm);
const secs = sections(body);

const sentences = (t) => t.split(/(?<=[.?!])\s+(?=[A-Z(“"])|\s*¶\s*/).map((s) => s.trim()).filter(Boolean);
const firstSentences = (t, max = 380) => {
  let out = '';
  for (const s of sentences(t)) { if ((out + ' ' + s).length > max && out) break; out = (out ? out + ' ' : '') + s; }
  return out;
};
const sectionFor = (quote) => secs.find((s) => s.text.includes(norm(quote)))?.heading ?? null;

// Best-matching body sentence for a quiz item, by rare shared words (as src/lib/quiz-anchors.ts does for sections).
const STOP = new Set('about above after again also because been before being between both does from have into more most only other over same should some such than that their them then there these they this those through under were what when where which while will with would your answer correct choice following true false best explains likely'.split(' '));
const words = (t) => t.toLowerCase().replace(/[^a-z0-9+\- ]/g, ' ').split(/\s+/).filter((w) => w.length >= 4 && !STOP.has(w));
const allSent = secs.flatMap((s) => sentences(s.text));
const df = new Map();
for (const s of allSent) for (const w of new Set(words(s))) df.set(w, (df.get(w) ?? 0) + 1);
function bestSentence(text) {
  const qw = new Set(words(text));
  let best = null; let score = 0;
  for (const s of allSent) {
    if (s.length > 260) continue;
    let sc = 0;
    for (const w of new Set(words(s))) if (qw.has(w)) sc += Math.log(1 + allSent.length / df.get(w));
    if (sc > score) { score = sc; best = s; }
  }
  return best;
}

const cards = [];
const add = (c) => {
  if (!c.quote || !sectionFor(c.quote)) return;
  cards.push({ id: `${slug}-x${String(cards.length + 1).padStart(3, '0')}`, ...c, section: sectionFor(c.quote) });
};

// 1. Definitions: a sentence that bolds a short term and defines it.
for (const m of body.matchAll(/^(?!\s*[>#])(.*\*\*([^*]{2,40})\*\*.*)$/gm)) {
  const line = m[1];
  const term = m[2];
  if (/^\*\*(Predict|Tetrodotoxin|TEA|Demyelination)\b/.test(line.trim())) continue;
  for (const s of sentences(plain(line))) {
    if (!s.includes(term) || s.length > 240) continue;
    if (!/\b(is|are|means|is called|called|says|refers to)\b/.test(s)) continue;
    if (term.split(' ').length > 4 || /^\d/.test(term)) continue;
    add({ type: 'cloze', level: 1, goals: ['lesson', 'course'], front: s.replace(term, `{{c1::${term}}}`), back: '', quote: s });
    break;
  }
}

// 2. Rule boxes and equations: > **Label.** text, and > **A = B**.
for (const m of body.matchAll(/^> \*\*(.+?)\*\*(.*)$/gm)) {
  const [label, rest] = [m[1].trim(), m[2].trim()];
  if (!rest && label.includes('=')) {
    const [lhs, ...rhs] = label.split('=');
    const eq = plain(label);
    add({ type: 'cloze', level: 1, goals: ['lesson', 'course', 'mcat'], front: `${lhs.trim()} = {{c1::${rhs.join('=').trim()}}}`, back: '', quote: eq });
  } else if (rest) {
    const text = plain(rest);
    add({ type: 'qa', level: 2, goals: ['lesson', 'course'], front: `${label.replace(/\.$/, '')}: state it.`, back: firstSentences(text, 420), quote: firstSentences(text, 200) });
  }
}

// 3. Predict boxes and worked problems: the paragraph before <details>, and the answer inside.
for (const m of body.matchAll(/((?:^.+\n)+)\n<details>\n<summary>(.*?)<\/summary>\n([\s\S]*?)<\/details>/gm)) {
  const prompt = plain(m[1].trim().split('\n').slice(-3).join(' ')).replace(/^Predict\.\s*/, '');
  const answer = plain(m[3]);
  const isProblem = /one way to do it/i.test(m[2]);
  add({
    type: isProblem ? 'experiment' : 'predict', level: isProblem ? 4 : 3,
    goals: isProblem ? ['course', 'mcat'] : ['lesson', 'course', 'mcat'],
    front: isProblem ? firstSentences(prompt, 600) : prompt, back: firstSentences(answer, isProblem ? 520 : 420),
    quote: firstSentences(prompt, 160),
  });
}

// 4. The quiz, as question → answer + why. MCAT-style items go to the MCAT goal.
const quiz = [...(meta.practiceQuestions ?? []).map((q) => ({ q, mcat: false })), ...(meta.mcatQuestions ?? []).map((q) => ({ q, mcat: true }))];
for (const { q, mcat } of quiz) {
  const why = firstSentences(q.rationale.replace(/\s+/g, ' '), 300);
  const quote = bestSentence(`${q.stem} ${q.choices[q.answer]} ${q.rationale}`);
  const calc = /\d/.test(q.choices[q.answer]) && /[=×/]/.test(q.rationale);
  add({ type: calc ? 'calc' : 'qa', level: mcat ? 3 : 2, goals: mcat ? ['course', 'mcat'] : ['lesson', 'course'], front: q.stem, back: `${q.choices[q.answer]}. ${why}`, quote });
}

const deck = {
  slug, title: meta.title, arm: 'extract',
  sectionHashes: Object.fromEntries(secs.map((s) => [s.heading, s.hash])),
  lessonHash: hash(secs.map((s) => s.text).join('\n')),
  cards,
};
writeFileSync(join(outDir, 'extract.json'), JSON.stringify(deck, null, 1));

// Digest: everything a drafting model needs, nothing it does not.
const digest = [
  `# ${meta.title} (slug: ${slug})`,
  `Course: ${meta.course}. Summary: ${meta.summary.replace(/\s+/g, ' ')}`,
  '## Objectives', ...(meta.objectives ?? []).map((o, i) => `${i + 1}. ${o}`),
  '## Quiz (stem → correct answer)', ...quiz.map(({ q, mcat }, i) => `${i + 1}${mcat ? ' [MCAT]' : ''}. ${q.stem} → ${q.choices[q.answer]}`),
  '## Lesson body, by section (plain text; quotes must be copied from here verbatim)',
  ...secs.map((s) => `### [${s.heading}]\n${s.text}`),
].join('\n\n');
writeFileSync(join(outDir, 'digest.md'), digest);
console.log(`${slug}: ${cards.length} extracted cards; digest ${digest.split(/\s+/).length} words (lesson file ${src.split(/\s+/).length})`);
