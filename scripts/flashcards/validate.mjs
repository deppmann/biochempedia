#!/usr/bin/env node
/* Validate one deck file against its lesson: node scripts/flashcards/validate.mjs <deck.json> <slug>
   Prints errors (fix these) and warnings; exits 1 on any error. */
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { splitMdx, checkDeck } from './lib.mjs';

const [file, slug] = process.argv.slice(2);
const deck = JSON.parse(readFileSync(file, 'utf8'));
const { body } = splitMdx(readFileSync(join('src/content/lessons', slug ?? deck.slug, 'lesson.mdx'), 'utf8'));
const { errors, warnings } = checkDeck(deck, body);
for (const w of warnings) console.log(`warn  ${w}`);
for (const e of errors) console.log(`ERROR ${e}`);
console.log(`${deck.cards?.length ?? 0} cards, ${errors.length} errors, ${warnings.length} warnings`);
process.exit(errors.length ? 1 : 0);
