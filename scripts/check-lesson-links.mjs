#!/usr/bin/env node
/**
 * Lesson links guard (source-level; needs no build).
 *
 * src/data/lesson-links.json ("Before this / After this / Elsewhere" and search phrases, written
 * offline by scripts/lesson-links/generate.mjs) must be well formed, and every record must already
 * pass the rules in scripts/lesson-links/lib.mjs: each lesson and resource it names exists and is
 * live, no self-links or duplicates, review-first items come earlier in the course or from a level
 * no higher, next items come later or at most one level up, reasons are one plain sentence, and no
 * search phrase asks for medical advice or names a product. Any of that FAILS: a broken record is
 * caught here, not on the page (which would quietly drop the bad link).
 *
 * A record whose lesson file changed since it was written is only a WARNING, as for flashcards:
 * lessons are edited all the time, and blocking someone else's lesson edit on a model call would
 * be worse than a link that is a few days old. Refresh with
 *   node scripts/lesson-links/generate.mjs --only <slug>
 *
 * Run: node scripts/check-lesson-links.mjs   (also run by CI on every push)
 */
import { readFileSync, existsSync } from 'node:fs';
import { loadSite, cleanRecord, DATA_FILE } from './lesson-links/lib.mjs';

const failures = [];
const warnings = [];
if (!existsSync(DATA_FILE)) {
  console.log('check-lesson-links: no src/data/lesson-links.json, nothing to check');
  process.exit(0);
}
const data = JSON.parse(readFileSync(DATA_FILE, 'utf8'));
if (data.version !== 1) failures.push(`version is ${data.version}, expected 1`);
if (typeof data.model !== 'string' || !data.model) failures.push('header has no model');
if (!/^\d{4}-\d{2}-\d{2}$/.test(data.updated ?? '')) failures.push('header has no updated date');
if (data.model === 'mock') warnings.push('records were written by the mock generator, not a model');

const site = await loadSite();
const recs = Object.entries(data.lessons ?? {});
let stale = 0;
for (const [slug, rec] of recs) {
  const l = site.lessons.get(slug);
  if (!l) { failures.push(`${slug}: not a live lesson (drafted, renamed or removed): delete its record`); continue; }
  for (const k of ['before', 'after', 'elsewhere', 'search']) if (!Array.isArray(rec[k])) failures.push(`${slug}: "${k}" is not a list`);
  if (!/^[0-9a-f]{16}$/.test(rec.hash ?? '')) failures.push(`${slug}: no hash`);
  const { dropped } = cleanRecord(slug, rec, site);
  for (const d of dropped) failures.push(`${slug}: ${d}`);
  if (rec.hash !== l.hash) stale++;
}
if (stale) warnings.push(`${stale} record(s) were written before their lesson last changed; refresh with --only <slug>`);
const missing = [...site.lessons.keys()].filter((s) => !data.lessons?.[s]);
if (missing.length) warnings.push(`${missing.length} live lesson(s) have no record yet: ${missing.slice(0, 8).join(', ')}${missing.length > 8 ? ', …' : ''}`);

for (const w of warnings) console.log(`warn  ${w}`);
for (const e of failures) console.log(`FAIL  ${e}`);
console.log(`check-lesson-links: ${recs.length} record(s), ${failures.length} failure(s), ${warnings.length} warning(s)`);
process.exit(failures.length ? 1 : 0);
