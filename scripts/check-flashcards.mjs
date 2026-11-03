#!/usr/bin/env node
/**
 * Flashcard deck guard (source-level; needs no build).
 *
 * Every deck in src/data/flashcards/<slug>.json must match a lesson and pass
 * the card schema (type, level 1–4, goals, cloze markup, a source quote).
 * FAILS on schema errors. WARNS, without failing, when a card's quote is no
 * longer in its lesson or a section has changed since the deck was written:
 * lessons are edited all the time, the page already holds such cards back, and
 * the fix is to regenerate those sections (scripts/flashcards/README.md), not
 * to block someone else's lesson edit.
 *
 * Run: node scripts/check-flashcards.mjs   (also run by CI on every push)
 */
import { readdir, readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { join } from 'node:path';
import { splitMdx, checkDeck } from './flashcards/lib.mjs';

const DIR = join(process.cwd(), 'src', 'data', 'flashcards');
const failures = [];
const warnings = [];
const files = existsSync(DIR) ? (await readdir(DIR)).filter((f) => f.endsWith('.json')).sort() : [];
for (const f of files) {
  const deck = JSON.parse(await readFile(join(DIR, f), 'utf8'));
  const lesson = join(process.cwd(), 'src', 'content', 'lessons', deck.slug ?? '', 'lesson.mdx');
  if (`${deck.slug}.json` !== f) { failures.push(`${f}: slug "${deck.slug}" does not match the file name`); continue; }
  if (!existsSync(lesson)) { failures.push(`${f}: no lesson ${deck.slug}`); continue; }
  const { body } = splitMdx(await readFile(lesson, 'utf8'));
  const { errors, warnings: w, stale } = checkDeck(deck, body);
  for (const e of errors) (/quote not found/.test(e) ? warnings : failures).push(`${f}: ${e}`);
  for (const x of w) warnings.push(`${f}: ${x}`);
  if (stale.length) warnings.push(`${f}: ${stale.length} section(s) changed since generation: ${stale.join('; ')}`);
}
for (const w of warnings) console.log(`warn  ${w}`);
for (const e of failures) console.log(`FAIL  ${e}`);
console.log(`check-flashcards: ${files.length} deck(s), ${failures.length} failure(s), ${warnings.length} warning(s)`);
process.exit(failures.length ? 1 : 0);
