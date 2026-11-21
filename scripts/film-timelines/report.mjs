#!/usr/bin/env node
/* Coverage of the film timelines: how many films get what, and why the others do not.
     node scripts/film-timelines/report.mjs            the counts
     node scripts/film-timelines/report.mjs --list     plus every film that is not fully timed, with the reason
     node scripts/film-timelines/report.mjs --json     the same as JSON (stable: sorted by film key) */
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { filmTimeline } from './lib.mjs';
import { timelineFilms } from './catalog.mjs';

const ROOT = join(fileURLToPath(new URL('.', import.meta.url)), '..', '..');

export function coverage(root = ROOT) {
  const films = timelineFilms(root).sort((a, b) => a.key.localeCompare(b.key));
  const rows = films.map((f) => {
    const t = filmTimeline(root, f);
    return {
      key: f.key, kind: f.kind, status: t.status, why: t.why,
      spoken: t.times?.spoken ?? 0, matched: t.times?.matched ?? 0, questions: t.times?.questions.length ?? 0,
      section: t.region.section?.id ?? null, figures: t.region.figures.length, mapProblems: t.mapProblems,
    };
  });
  const count = (fn) => rows.filter(fn).length;
  const byStatus = {};
  for (const r of rows) byStatus[r.status] = (byStatus[r.status] ?? 0) + 1;
  return {
    films: rows.length,
    byStatus,
    byKind: Object.fromEntries(['lesson', 'profile', 'method'].map((k) => [k, Object.fromEntries(Object.entries(byStatus).map(([s]) => [s, count((r) => r.kind === k && r.status === s)]).filter(([, n]) => n))])),
    withQuestion: count((r) => r.questions > 0),
    withSection: count((r) => r.section),
    withRegionFigures: count((r) => r.figures > 0),
    scenes: { spoken: rows.reduce((a, r) => a + r.spoken, 0), matched: rows.reduce((a, r) => a + r.matched, 0) },
    rows,
  };
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  const c = coverage();
  if (process.argv.includes('--json')) { console.log(JSON.stringify(c, null, 1)); process.exit(0); }
  const { rows, ...top } = c;
  console.log(JSON.stringify(top, null, 1));
  if (process.argv.includes('--list')) for (const r of rows) if (r.status !== 'timed' && r.status !== 'mapped') console.log(`${r.status.padEnd(9)} ${r.key}  ${r.why}`);
  for (const r of rows) for (const p of r.mapProblems) console.log(`map problem  ${r.key}: ${p}`);
}
