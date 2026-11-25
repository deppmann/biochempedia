#!/usr/bin/env node
/* Short versions that are not simpler: the rewrite list.

   Each lesson's hop sentence offers a short version of the lesson one level down (frontmatter
   explainLevels; which one is QUICK_DOWN in src/lib/hop-words.mjs). Once RELABEL_NOT_SIMPLER in
   that file is switched on (it is off, waiting on Chris), the site calls it "Simpler"
   only when it reads at least two grades easier than the lesson body (simplerCheck in
   src/lib/readability.ts, the same code the page uses at build). This script lists the lessons
   where it does not, so the short versions can be rewritten.

   Run:  node scripts/list-not-simpler.mjs            print the list
         node scripts/list-not-simpler.mjs --write    also write production/short-versions-not-simpler.json
   No network, no model: it reads src/content/lessons/ and takes a second or two. */
import { readdirSync, readFileSync, writeFileSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parse } from 'yaml';
import { simplerCheck, SIMPLER_MARGIN } from '../src/lib/readability.ts';
import { courseOf } from '../src/data/courses.ts';
import { stageOf } from '../src/data/stages.ts';
import { LEVEL_KEYS, QUICK_DOWN } from '../src/lib/hop-words.mjs';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const dir = join(root, 'src/content/lessons');
const OUT = 'production/short-versions-not-simpler.json';

const rows = [];
let measured = 0;
let unmeasured = 0;
for (const name of readdirSync(dir).sort()) {
  const file = join(dir, name, 'lesson.mdx');
  if (!existsSync(file)) continue;
  const m = /^---\r?\n([\s\S]*?)\r?\n---\r?\n?([\s\S]*)$/.exec(readFileSync(file, 'utf8'));
  if (!m) continue;
  const d = parse(m[1]);
  if (!d || d.draft) continue;
  let rank;
  try { rank = LEVEL_KEYS.indexOf(stageOf(courseOf(d.course))); } catch { continue; }
  const key = QUICK_DOWN[rank];
  const short = key ? (d.explainLevels ?? []).find((x) => x.level === key) : undefined;
  if (!short) continue;
  const c = simplerCheck(short.text, m[2]);
  if (!c) { unmeasured++; continue; }
  measured++;
  if (!c.simpler) rows.push({ slug: d.slug ?? name, course: d.course, version: key, shortGrade: c.short, lessonGrade: c.lesson, easierBy: Math.round((c.lesson - c.short) * 10) / 10 });
}
rows.sort((a, b) => a.easierBy - b.easierBy || a.slug.localeCompare(b.slug));

for (const r of rows) console.log(`${String(r.easierBy).padStart(5)}  ${r.slug}  (${r.course}; ${r.version} version grade ${r.shortGrade}, lesson grade ${r.lessonGrade})`);
console.log(`\n${rows.length} of ${measured} short versions are less than ${SIMPLER_MARGIN} grades easier than their lesson${unmeasured ? `; ${unmeasured} too short to measure` : ''}.`);

if (process.argv.includes('--write')) {
  const out = {
    note: `Lessons whose "one level simpler" short version (frontmatter explainLevels) reads less than ${SIMPLER_MARGIN} Flesch-Kincaid grades easier than the lesson body. The page would label these "Short version" instead of "Simpler" once RELABEL_NOT_SIMPLER (src/lib/hop-words.mjs) is switched on; it is off, waiting on Chris. Rewrite the short version, then run: node scripts/list-not-simpler.mjs --write`,
    margin: SIMPLER_MARGIN,
    measured,
    lessons: rows,
  };
  writeFileSync(join(root, OUT), JSON.stringify(out, null, 2) + '\n');
  console.log(`Wrote ${OUT}`);
}
