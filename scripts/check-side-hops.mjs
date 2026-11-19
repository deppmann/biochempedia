#!/usr/bin/env node
/**
 * Side Hops guard (source-level; needs no build).
 *
 * Each src/data/side-hops/<slug>.json must follow the schema and fit its lesson: every card names a
 * real ## heading, no two cards share a heading, a story or claim has an https source, a lesson has
 * at most one analogy, and the audio is on disk (public/side-hops/) or uploaded (media-manifest.json).
 *
 * Run: node scripts/check-side-hops.mjs   (also run by CI on every push)
 *      node scripts/check-side-hops.mjs --dir <folder>   checks another folder of data files
 */
import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { lessonHeadings, problemsIn } from './side-hops/shared.mjs';

const at = process.argv.indexOf('--dir');
const DIR = at > 0 ? process.argv[at + 1] : 'src/data/side-hops';
const manifest = existsSync('media-manifest.json') ? JSON.parse(readFileSync('media-manifest.json', 'utf8')) : {};
const audioFound = (file) => existsSync(join('public', file)) || Boolean(manifest[file]);

const files = existsSync(DIR) ? readdirSync(DIR).filter((f) => !f.startsWith('.')).sort() : [];
let failures = 0;
for (const f of files) {
  const report = (m) => { failures++; console.log(`FAIL  ${f}: ${m}`); };
  if (!f.endsWith('.json')) { report('not a .json file'); continue; }
  const fileSlug = f.slice(0, -5);
  let data;
  try { data = JSON.parse(readFileSync(join(DIR, f), 'utf8')); } catch (e) { report(`not JSON (${e.message})`); continue; }
  const lesson = join('src/content/lessons', String(data?.slug ?? fileSlug), 'lesson.mdx');
  const headings = existsSync(lesson) ? lessonHeadings(readFileSync(lesson, 'utf8')) : null;
  problemsIn(data, { fileSlug, headings, audioFound }).forEach(report);
}
console.log(`check-side-hops: ${files.length} lesson(s), ${failures} failure(s)`);
process.exit(failures ? 1 : 0);
