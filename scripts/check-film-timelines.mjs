#!/usr/bin/env node
/**
 * check-film-timelines: every hand-checked film map (src/data/film-maps/<lesson>/<name>.json) must
 * be usable as written. The build fails when a map
 *   - is for a film the site does not have, or is not valid JSON;
 *   - names a scene the film's script does not have, a lesson heading that does not exist, or a
 *     figure that is not in the lesson or whose file is missing from public/;
 *   - would show a figure before the film has given the answer that figure shows, puts anything on
 *     the film's own question, or leaves a figure without a recorded judgement ("answers");
 *   - gives a word a definition the film does not say.
 * (The rules are in scripts/film-timelines/lib.mjs, applyMap.) A map with a problem is never used
 * by the page; this check is what stops it from sitting there unnoticed.
 *
 * When dist/ exists (after a build) it also confirms that the lesson anchors the theater links to
 * are real ids on the built lesson pages: every mapped section, and each film's own section.
 *
 * Run: node scripts/check-film-timelines.mjs   (CI runs it after the build)
 */
import { existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';
import { allMaps, filmTimeline } from './film-timelines/lib.mjs';
import { timelineFilms } from './film-timelines/catalog.mjs';

const ROOT = process.cwd();
const failures = [];
const films = timelineFilms(ROOT);
const byKey = new Map(films.map((f) => [f.key, f]));
const maps = allMaps(ROOT);
let figures = 0;

for (const m of maps) {
  const film = byKey.get(m.key);
  if (m.error) { failures.push(`${m.file}: not valid JSON (${m.error})`); continue; }
  if (!film || film.kind !== 'lesson') { failures.push(`${m.file}: there is no lesson film "${m.key}"`); continue; }
  const t = filmTimeline(ROOT, film);
  if (!t.times) { failures.push(`${m.file}: the film's scenes could not be timed (${t.why}), so a map cannot be placed`); continue; }
  for (const p of t.mapProblems) failures.push(`${m.file}: ${p}`);
  for (const part of t.parts) {
    if (!part.figure) continue;
    figures++;
    if (!existsSync(join(ROOT, 'public', part.figure.src))) failures.push(`${m.file}: figure file missing from public/ (${part.figure.src})`);
  }
}

let anchors = 0;
if (existsSync(join(ROOT, 'dist', 'lessons'))) {
  const ids = new Map();
  const idsOf = (lesson) => {
    if (!ids.has(lesson)) {
      const file = join(ROOT, 'dist', 'lessons', lesson, 'index.html');
      ids.set(lesson, existsSync(file) ? new Set([...readFileSync(file, 'utf8').matchAll(/\sid="([^"]+)"/g)].map((x) => x[1])) : null);
    }
    return ids.get(lesson);
  };
  for (const f of films) {
    if (f.kind !== 'lesson') continue;
    const have = idsOf(f.lesson);
    if (!have) continue;
    const t = filmTimeline(ROOT, f);
    const wanted = new Set([t.region.section?.id, ...t.parts.map((p) => p.section?.id)].filter(Boolean));
    for (const id of wanted) {
      anchors++;
      if (!have.has(id)) failures.push(`${f.key}: the theater links to /lessons/${f.lesson}/#${id}, which is not an id on the built lesson page`);
    }
  }
}

for (const f of failures) console.error(`✗ check-film-timelines: ${f}`);
if (failures.length) process.exit(1);
console.log(`✓ check-film-timelines: ${maps.length} hand-checked map(s), ${figures} figure cue(s), none before its answer${anchors ? `; ${anchors} lesson anchors found on the built pages` : ' (no dist/: lesson anchors not checked)'}.`);
