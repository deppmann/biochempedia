#!/usr/bin/env node
/* Which cards need a model again after a lesson edit? node scripts/flashcards/stale.mjs [slug ...]
   Lists, per deck, the sections whose text changed since generation and the cards
   written from them (plus any card whose quote has gone). Only those go back to the
   drafter and arbiter; every other card is kept as it is. */
import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import { splitMdx, checkDeck } from './lib.mjs';

const slugs = process.argv.slice(2).length ? process.argv.slice(2) : readdirSync('src/data/flashcards').filter((f) => f.endsWith('.json')).map((f) => f.slice(0, -5));
for (const slug of slugs) {
  const deck = JSON.parse(readFileSync(join('src/data/flashcards', `${slug}.json`), 'utf8'));
  const { body } = splitMdx(readFileSync(join('src/content/lessons', slug, 'lesson.mdx'), 'utf8'));
  const { errors, stale } = checkDeck(deck, body);
  const lost = errors.filter((e) => /quote not found/.test(e)).map((e) => /card (\S+):/.exec(e)[1]);
  const redo = deck.cards.filter((c) => stale.includes(c.section ?? '(opening)') || lost.includes(c.id));
  console.log(`${slug}: ${stale.length} changed section(s), ${redo.length} of ${deck.cards.length} cards to redo`);
  for (const s of stale) console.log(`  section: ${s}`);
  for (const c of redo) console.log(`  card: ${c.id}`);
}
