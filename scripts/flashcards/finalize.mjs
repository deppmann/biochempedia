#!/usr/bin/env node
/* Install a checked deck on the site:
     node scripts/flashcards/finalize.mjs <slug> <deck.json> '<generation record as JSON>'
   Adds each card's section, makes ids stable (<slug>-<drafter id>), records the
   section hashes the cards were written against, validates, and writes
   src/data/flashcards/<slug>.json. */
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { splitMdx, sections, sectionOf, checkDeck, hash } from './lib.mjs';

const [slug, file, gen = '{}'] = process.argv.slice(2);
const src = readFileSync(join('src/content/lessons', slug, 'lesson.mdx'), 'utf8');
const { fm, body } = splitMdx(src);
const title = /^title:\s*"?(.*?)"?\s*$/m.exec(fm)[1];
const secs = sections(body);
const draft = JSON.parse(readFileSync(file, 'utf8'));
const out = join('src/data/flashcards', `${slug}.json`);
const prev = existsSync(out) ? JSON.parse(readFileSync(out, 'utf8')) : null;

const cards = draft.cards.map(({ id, type, level, goals, front, back, why, quote }) => {
  const sec = sectionOf(secs, quote);
  const cid = id.startsWith(`${slug}-`) ? id : `${slug}-${id}`;
  return { id: cid, type, level, goals, front, back: back ?? '', ...(why ? { why } : {}), quote, section: sec?.heading === '(opening)' ? undefined : sec?.heading };
});
const used = new Set(cards.map((c) => c.section ?? '(opening)'));
const deck = {
  slug, title,
  generated: { date: new Date().toISOString().slice(0, 10), ...JSON.parse(gen) },
  lessonHash: hash(secs.map((s) => s.text).join('\n')),
  sectionHashes: Object.fromEntries(secs.filter((s) => used.has(s.heading)).map((s) => [s.heading, s.hash])),
  cards,
};
const { errors, warnings } = checkDeck(deck, body);
warnings.forEach((w) => console.log(`warn  ${w}`));
if (errors.length) { errors.forEach((e) => console.log(`ERROR ${e}`)); process.exit(1); }
writeFileSync(out, JSON.stringify(deck, null, 1) + '\n');
console.log(`${out}: ${cards.length} cards${prev ? ` (was ${prev.cards.length})` : ''}`);
