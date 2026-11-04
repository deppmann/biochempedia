#!/usr/bin/env node
/* Pool several decks into one blinded, shuffled card list for an accuracy gate.
   node scripts/flashcards/gate_cards.mjs <outDir> arm=deck.json ...  → cards.md + cards.key.json */
import { readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { createHash } from 'node:crypto';
const [outDir, ...pairs] = process.argv.slice(2);
const all = [];
for (const p of pairs) {
  const [arm, file] = p.split('=');
  for (const c of JSON.parse(readFileSync(file, 'utf8')).cards) all.push({ arm, c });
}
const h = (s) => createHash('sha256').update(s).digest('hex');
all.sort((a, b) => (h(a.arm + a.c.id) < h(b.arm + b.c.id) ? -1 : 1));
const key = {};
const lines = [];
all.forEach(({ arm, c }, i) => {
  const id = `G${String(i + 1).padStart(3, '0')}`;
  key[id] = { arm, id: c.id };
  lines.push(`## ${id} (${c.type})`, `Front: ${c.front}`, ...(c.back ? [`Back: ${c.back}`] : []), ...(c.why ? [`Why: ${c.why}`] : []), '');
});
writeFileSync(join(outDir, 'cards.md'), lines.join('\n'));
writeFileSync(join(outDir, 'cards.key.json'), JSON.stringify(key));
console.log(`${all.length} cards pooled`);
