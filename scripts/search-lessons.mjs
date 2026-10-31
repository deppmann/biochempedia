#!/usr/bin/env node
/**
 * Search the lessons from the command line, offline, with the same index and ranking as the site.
 * For course planning ("which lessons cover X, and where in them?") and for feeding passages to a model.
 *
 *   node scripts/search-lessons.mjs "health department"
 *   node scripts/search-lessons.mjs "synaptic plasticity" --course neuroscience --limit 5
 *   node scripts/search-lessons.mjs "western blot" --json          full hits, one JSON array
 *   node scripts/search-lessons.mjs "western blot" --model         text block for a prompt
 *
 * Reads dist/ (run `npm run build` first) and needs Node 22.18 or newer, which runs the TypeScript
 * ranking module directly. See src/lib/lesson-search.ts.
 */
import { nodeEngine, lib } from './lesson-search-node.mjs';

const args = process.argv.slice(2);
const flag = (name) => { const i = args.indexOf(`--${name}`); if (i === -1) return undefined; const v = args[i + 1]; args.splice(i, v && !v.startsWith('--') ? 2 : 1); return v && !v.startsWith('--') ? v : true; };
const course = flag('course');
const limit = Number(flag('limit')) || 8;
const json = flag('json');
const model = flag('model');
const query = args.filter((a) => !a.startsWith('--')).join(' ').trim();
if (!query) { console.error('Usage: node scripts/search-lessons.mjs "query" [--course slug] [--limit n] [--json | --model]'); process.exit(2); }

let hits;
try {
  hits = await lib.searchLessons(query, { engine: nodeEngine(), scope: typeof course === 'string' ? course : 'all', limit, excerptLength: model ? 60 : undefined });
} catch (e) {
  console.error(e instanceof Error ? e.message : e);
  process.exit(1);
}
if (json) console.log(JSON.stringify(hits, null, 2));
else if (model) console.log(lib.formatForModel(hits, 'https://biochemistrypedia.com'));
else {
  if (!hits.length) console.log(`No lesson matches “${query}”.`);
  for (const h of hits) {
    console.log(`\n${h.score.toFixed(2)}  ${h.title}   [${h.courseTitle} · lesson ${h.n}]   ${h.url}`);
    for (const s of h.spots) console.log(`      ${s.label}\n        ${s.excerptText.replace(/\s+/g, ' ')}\n        ${s.url}`);
  }
}
