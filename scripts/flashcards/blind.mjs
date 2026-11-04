#!/usr/bin/env node
/* Blind decks for judging: node scripts/flashcards/blind.mjs <outDir> <judgeName> arm=deck.json ...
   Writes <outDir>/<judge>/deck_<L>.md (L = A, B, C, ...) in a per-judge random order,
   with card ids renumbered so no id prefix leaks the arm, and <outDir>/<judge>.key.json. */
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';
import { createHash } from 'node:crypto';

const [outDir, judge, ...pairs] = process.argv.slice(2);
const arms = pairs.map((p) => { const [arm, file] = p.split('='); return { arm, deck: JSON.parse(readFileSync(file, 'utf8')) }; });
// Deterministic per-judge shuffle, so a rerun gives the same letters.
const seed = (s) => parseInt(createHash('sha256').update(judge + s).digest('hex').slice(0, 8), 16);
arms.sort((a, b) => seed(a.arm) - seed(b.arm));
const NAMES = { 1: 'Recall', 2: 'Explain', 3: 'Apply', 4: 'Integrate' };
mkdirSync(join(outDir, judge), { recursive: true });
const key = {};
arms.forEach(({ arm, deck }, i) => {
  const L = String.fromCharCode(65 + i);
  key[L] = arm;
  const lines = [`# Deck ${L} (${deck.cards.length} cards)`, ''];
  deck.cards.forEach((c, j) => {
    lines.push(`## ${L}${String(j + 1).padStart(2, '0')} · L${c.level} ${NAMES[c.level]} · ${c.type} · goals: ${c.goals.join(', ')}`);
    lines.push(`Front: ${c.front}`);
    if (c.back) lines.push(`Back: ${c.back}`);
    if (c.why) lines.push(`Why: ${c.why}`);
    lines.push('');
  });
  writeFileSync(join(outDir, judge, `deck_${L}.md`), lines.join('\n'));
});
writeFileSync(join(outDir, `${judge}.key.json`), JSON.stringify(key));
console.log(judge, Object.keys(key).join(''));
