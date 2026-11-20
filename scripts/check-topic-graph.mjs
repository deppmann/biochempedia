#!/usr/bin/env node
/**
 * Hop graph guard.
 *
 * src/data/topic-graph.json (which ideas the site teaches and where; written offline by
 * scripts/topic-graph) must be well formed and every part of it must pass the rules in
 * scripts/topic-graph/lib.mjs: each lesson and film it names exists and is live, every concept has at
 * least one lesson that teaches it, ids are kebab-case and unique, an alias is not another concept's
 * name, and blurbs, notes and reasons keep to their length and wording rules (no product, company or
 * test names, nothing phrased as medical advice, no analogy formulas). Any of that FAILS: a broken
 * record is caught here, not on the page.
 *
 * Three things are only WARNINGS, each listed by slug, because blocking someone's lesson edit on a
 * model call would be worse than a graph that is a few days behind:
 *   - a live lesson with no record (it still works everywhere, by course and level);
 *   - a record written before its lesson's teaching text last changed (the hash covers the hook,
 *     summary, objectives, headings and body prose only, so a new quiz question or a credit line
 *     does not count);
 *   - an anchor that no longer matches a section heading (the link falls back to the lesson top).
 * Refresh a lesson with: node scripts/topic-graph/assign.mjs --emit <slug>   (then --apply)
 *
 * Anchors are checked against the BUILT pages when dist/ is there (CI runs this after the build),
 * otherwise against ids worked out from the lesson source. It also checks that the two agree, so the
 * source-side id rule cannot drift from what the site really serves.
 *
 * Run: node scripts/check-topic-graph.mjs [--strict-anchors]   (also run by CI on every push)
 */
import { readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { ROOT, GRAPH_FILE, loadGraphSite, validateGraph, normalizeGraph, serializeGraph, describeGraph } from './topic-graph/lib.mjs';

if (!existsSync(GRAPH_FILE)) {
  console.log('check-topic-graph: no src/data/topic-graph.json, nothing to check');
  process.exit(0);
}
const raw = readFileSync(GRAPH_FILE, 'utf8');
let graph;
try { graph = JSON.parse(raw); } catch (e) { console.log(`FAIL  src/data/topic-graph.json is not valid JSON: ${e.message}`); process.exit(1); }
const site = await loadGraphSite();

const dist = join(ROOT, 'dist', 'lessons');
const haveDist = existsSync(dist) && !process.argv.includes('--no-dist');
const builtCache = new Map();
// Reading 414 built pages takes about a second on a healthy disk. On a stalled or networked volume one
// page can take seconds, so the built-page reads share a time budget: once it is spent, the remaining
// anchors are checked against ids worked out from source (the same rule, minus the cross-check), and
// the summary says so. The check must never hang a build.
const BUDGET_MS = Number(process.env.TOPIC_GRAPH_DIST_BUDGET_MS ?? 20000);
let spent = 0, skipped = 0;
const builtHeadings = (slug) => {
  if (!haveDist) return undefined;
  if (!builtCache.has(slug)) {
    if (spent > BUDGET_MS) { skipped++; return undefined; }
    const t = Date.now();
    const f = join(dist, slug, 'index.html');
    builtCache.set(slug, existsSync(f) ? new Set([...readFileSync(f, 'utf8').matchAll(/<h2[^>]*\bid="([^"]+)"/g)].map((m) => m[1])) : undefined);
    spent += Date.now() - t;
  }
  return builtCache.get(slug);
};

const { errors, warnings, notes, stats } = validateGraph(graph, site, { builtHeadings });

// The committed file must be in the one fixed order the tools write, so diffs stay readable and a
// hand edit that leaves the reverse index behind is caught.
if (!errors.length && serializeGraph(normalizeGraph(graph, site)) !== raw) errors.push('the file is not in the order the tools write (or its lesson index is out of step with its rungs): run node scripts/topic-graph/ingest.mjs --graph src/data/topic-graph.json, or re-apply the change through assign.mjs');

// The id rule itself: every section id worked out from source must be on the built page.
if (haveDist) {
  const drift = [];
  for (const l of site.lessons.values()) {
    const built = builtHeadings(l.slug);
    if (!built) continue;
    for (const id of l.h2) if (!built.has(id)) drift.push(`${l.slug}#${id}`);
  }
  if (drift.length) warnings.push(`${drift.length} section id(s) worked out from the lesson source are not on the built page, so the id rule in src/lib/topic-graph-core.mjs has drifted from the site: ${drift.slice(0, 6).join(', ')}${drift.length > 6 ? ', …' : ''}`);
}

for (const w of warnings) console.log(`warn  ${w}`);
for (const e of errors) console.log(`FAIL  ${e}`);
if (!errors.length) {
  const d = describeGraph(graph, site);
  console.log(`check-topic-graph: ${stats.concepts} concept(s), ${stats.core} core and ${stats.uses} uses rung(s), ${stats.films} film link(s), ${stats.near} sideways hop(s); ${d.lessonsCovered} of ${d.lessonsLive} live lessons have a record${notes.filter((n) => /no idea filed/.test(n)).length ? ` (${notes.filter((n) => /no idea filed/.test(n)).length} read with no idea filed)` : ''}; anchors checked against ${!haveDist ? 'the lesson source (no dist/)' : skipped ? `the built pages for ${builtCache.size} lesson(s) and the lesson source for the rest (reading dist/ was too slow: ${Math.round(spent / 1000)} s)` : 'the built pages'}.`);
}
console.log(`check-topic-graph: ${errors.length} failure(s), ${warnings.length} warning(s)`);
process.exit(errors.length ? 1 : 0);
