#!/usr/bin/env node
/**
 * Production record guard (source-level; needs no build).
 *
 * production/record/<course>.jsonl must hold exactly one valid row per lesson, in the right course file,
 * sorted by slug, with every field from the fixed vocabulary, and with the fields the tree determines
 * (course, tier, films and their lengths, deck size and date, Listen clips, the single-film flag)
 * agreeing with the tree. The record is public: the check also FAILS on anything that looks like a cost,
 * a model version string or a local path.
 *
 * Fix drift with: node scripts/production-record.mjs derive
 * Run: node scripts/check-production-record.mjs   (also run by CI on every push)
 */
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import {
  ROOT, RECORD_DIR, readTree, readRecord, deriveRows, canonical, validateRow, forbiddenIn,
} from './production-record.mjs';

const failures = [];
const dir = join(ROOT, RECORD_DIR);
if (!existsSync(dir)) {
  console.log(`FAIL  no ${RECORD_DIR}/`);
  process.exit(1);
}
// Raw text first: forbidden content, one JSON object per line, sorted by slug.
for (const f of readdirSync(dir).filter((x) => x.endsWith('.jsonl')).sort()) {
  const text = readFileSync(join(dir, f), 'utf8');
  for (const what of forbiddenIn(text)) failures.push(`${f}: contains ${what}; the record is public`);
  const slugs = text.split('\n').filter((l) => l.trim()).map((l) => { try { return JSON.parse(l).slug; } catch { return null; } });
  if (slugs.includes(null)) failures.push(`${f}: a line is not JSON`);
  const sorted = [...slugs].sort((a, b) => String(a).localeCompare(String(b)));
  if (slugs.join() !== sorted.join()) failures.push(`${f}: rows are not sorted by slug`);
}
for (const f of readdirSync(dir).filter((x) => !x.endsWith('.jsonl') && !x.startsWith('.'))) failures.push(`${f}: not a .jsonl file`);

let rows = [];
try { rows = readRecord(); } catch (e) { failures.push(e.message); }
const tree = await readTree();
const seen = new Map();
for (const r of rows) {
  for (const e of validateRow(r)) failures.push(e);
  if (seen.has(r.slug)) failures.push(`${r.slug}: more than one row (${seen.get(r.slug)} and ${r._file})`);
  seen.set(r.slug, r._file);
  if (!tree.lessons.has(r.slug)) failures.push(`${r.slug}: row with no lesson (src/content/lessons/${r.slug}/lesson.mdx)`);
  else if (r._file !== `${r.course}.jsonl`) failures.push(`${r.slug}: in ${r._file}, but its course is ${r.course}`);
  if (JSON.stringify(canonical(r)) !== JSON.stringify(r)) failures.push(`${r.slug}: not in canonical form (key order, sorted lists)`);
}
for (const slug of tree.lessons.keys()) if (!seen.has(slug)) failures.push(`${slug}: lesson has no row`);

// Derivable fields agree with the tree.
const { rows: derived } = deriveRows(rows.filter((r) => tree.lessons.has(r.slug)), tree);
const now = new Map(rows.map((r) => [r.slug, JSON.stringify(canonical(r))]));
let drift = 0;
for (const d of derived) {
  const cur = now.get(d.slug);
  if (cur && cur !== JSON.stringify(d)) {
    drift++;
    if (drift <= 20) {
      const a = JSON.parse(cur);
      const diff = Object.keys(d).filter((k) => JSON.stringify(a[k]) !== JSON.stringify(d[k]));
      failures.push(`${d.slug}: ${diff.join(', ')} out of date with the tree`);
    }
  }
}
if (drift > 20) failures.push(`... and ${drift - 20} more rows out of date`);
if (drift) failures.push('run: node scripts/production-record.mjs derive');

for (const e of failures) console.log(`FAIL  ${e}`);
console.log(`check-production-record: ${rows.length} row(s), ${tree.lessons.size} lesson(s), ${failures.length} failure(s)`);
process.exit(failures.length ? 1 : 0);
