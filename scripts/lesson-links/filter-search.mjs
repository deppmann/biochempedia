#!/usr/bin/env node
/**
 * Tests every search phrase in src/data/lesson-links.json against the site's own search (the built
 * index in dist/ and src/lib/lesson-search.ts, as scripts/test-search.mjs does). A phrase whose
 * lesson is not in the top 3 for it, even with the phrase in the index, matches other lessons better:
 * it does not belong to this lesson, and --write removes it.
 *
 *   node scripts/lesson-links/filter-search.mjs [--write] [--only slug,slug]
 *
 * Needs a build first. Run it after generating records and building, then rebuild.
 */
import { readFileSync, writeFileSync } from 'node:fs';
import { nodeEngine, lib } from '../lesson-search-node.mjs';
import { DATA_FILE } from './lib.mjs';

const argv = process.argv.slice(2);
const only = argv.includes('--only') ? new Set(argv[argv.indexOf('--only') + 1].split(',')) : null;
const engine = nodeEngine();
const data = JSON.parse(readFileSync(DATA_FILE, 'utf8'));
let tested = 0;
let dropped = 0;
const lines = [];
for (const [slug, rec] of Object.entries(data.lessons)) {
  if (only && !only.has(slug)) continue;
  const keep = [];
  for (const p of rec.search) {
    tested++;
    const hits = await lib.searchLessons(p, { engine, limit: 5 });
    const at = hits.findIndex((h) => h.slug === slug);
    if (at >= 0 && at < 3) { keep.push(p); continue; }
    dropped++;
    lines.push(`${slug}: drop "${p}" (lesson ${at < 0 ? 'not in the top 5' : `at ${at + 1}`}; top: ${hits.slice(0, 3).map((h) => h.slug).join(', ') || 'none'})`);
  }
  rec.search = keep;
}
console.log(lines.join('\n'));
console.log(`\n${tested} phrase(s) tested, ${dropped} match other lessons better (${tested ? ((100 * dropped) / tested).toFixed(1) : 0}%).`);
if (argv.includes('--write')) { writeFileSync(DATA_FILE, JSON.stringify(data, null, 1) + '\n'); console.log('Written.'); }
