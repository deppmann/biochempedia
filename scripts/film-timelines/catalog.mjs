/* The films the timelines cover, read straight from the lesson files (no Astro), for the report, the
   check and the tests. The site's own catalog (src/lib/film-catalog.ts) is the authority on what the
   library lists; this is the same walk, kept to what the timeline code needs. */
import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';
import yaml from 'js-yaml';

const keyOf = (src) => String(src).replace(/^\/explainers\//, '').replace(/\.mp4$/, '');

/** [{ key, kind: 'lesson' | 'profile' | 'method', lesson, index, duration, title }] for published lessons,
 *  then the method films that are not also a lesson's film. */
export function timelineFilms(root) {
  const dir = join(root, 'src/content/lessons');
  const out = [];
  const seen = new Set();
  const add = (f) => { if (!seen.has(f.key)) { seen.add(f.key); out.push(f); } };
  for (const d of readdirSync(dir, { withFileTypes: true }).filter((x) => x.isDirectory()).sort((a, b) => a.name.localeCompare(b.name))) {
    const file = join(dir, d.name, 'lesson.mdx');
    if (!existsSync(file)) continue;
    const fm = /^---\n([\s\S]*?)\n---\n/.exec(readFileSync(file, 'utf8').replace(/\r/g, ''));
    if (!fm) continue;
    const data = yaml.load(fm[1]);
    if (!data || data.draft) continue;
    const lesson = data.slug ?? d.name;
    if (data.explainer?.src) add({ key: keyOf(data.explainer.src), kind: 'lesson', lesson, index: null, duration: data.explainer.durationSec, title: data.explainer.title });
    (data.films ?? []).forEach((f, i) => add({ key: keyOf(f.src), kind: 'lesson', lesson, index: i, duration: f.durationSec, title: f.title }));
    for (const s of data.scientists ?? []) if (s.film?.src) add({ key: keyOf(s.film.src), kind: 'profile', lesson, index: null, duration: s.film.durationSec, title: s.name });
  }
  const methods = readFileSync(join(root, 'src/data/methods.ts'), 'utf8');
  // Method films: libFilm('<slug>', ...) is the methods library's own film; sectionFilm and openingFilm
  // reuse a lesson's film, which is already listed above.
  for (const m of methods.matchAll(/libFilm\('([a-z0-9-]+)',\s*(['"])(.*?)\2,\s*([\d.]+)\)/g)) add({ key: `method-${m[1]}/explainer`, kind: 'method', lesson: null, index: null, duration: Number(m[4]), title: m[3] });
  return out;
}
