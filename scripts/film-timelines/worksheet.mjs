#!/usr/bin/env node
/* One film on one screen, for whoever writes or checks its map (see README.md):
     node scripts/film-timelines/worksheet.mjs diffusion-and-osmosis/chapter-2 */
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { filmTimeline, scriptPath, lessonOutline } from './lib.mjs';
import { timelineFilms } from './catalog.mjs';

const ROOT = join(fileURLToPath(new URL('.', import.meta.url)), '..', '..');
const key = process.argv[2];
const film = timelineFilms(ROOT).find((f) => f.key === key);
if (!film || film.kind !== 'lesson') { console.error(`No lesson film "${key}". Give <lesson>/<name>, for example action-potential/explainer.`); process.exit(2); }
const t = filmTimeline(ROOT, film);
const [folder, name] = [key.slice(0, key.lastIndexOf('/')), key.slice(key.lastIndexOf('/') + 1)];
console.log(`# ${key}  "${film.title}"  ${film.duration}s  status: ${t.status}${t.why ? ` (${t.why})` : ''}\n`);
if (t.times) {
  const script = JSON.parse(readFileSync(join(ROOT, scriptPath(folder, name)), 'utf8'));
  const byId = new Map(script.scenes.map((s) => [s.id, s]));
  console.log('## Scenes');
  for (const s of t.times.scenes) {
    const src = byId.get(s.id) ?? {};
    console.log(`\n${s.start === null ? '  ?  ' : String(s.start).padStart(5)}  ${s.id}  [${s.kind}]`);
    if (s.text) console.log(`       says: ${s.text}`);
    if (src.visual) console.log(`       shows: ${src.visual}`);
  }
  console.log('\n## Questions the film asks');
  for (const q of t.times.questions) console.log(`- ${q.scene} at ${q.start}s; the answer starts with ${q.reveal} at ${q.revealStart}s\n  "${q.text}"`);
  if (!t.times.questions.length) console.log('(none)');
}
const outline = lessonOutline(readFileSync(join(ROOT, 'src/content/lessons', film.lesson, 'lesson.mdx'), 'utf8'));
console.log(`\n## The lesson's figures (this film goes with: ${t.region.section ? `#${t.region.section.id}` : 'the opening of the lesson'})`);
for (const f of outline.figures) {
  console.log(`\n- ${f.src}${t.region.figures.some((x) => x.src === f.src) ? '   (in this film\'s part of the lesson)' : ''}${f.scaffold ? '   (scaffold figure: key words are held back)' : ''}\n  under #${f.heading}\n  caption: ${f.caption}\n  alt: ${f.alt}`);
}
console.log('\n## Lesson headings');
for (const h of outline.headings) console.log(`${'  '.repeat(h.depth - 2)}#${h.id}`);
if (t.mapProblems.length) { console.log('\n## Problems in the map on disk'); for (const p of t.mapProblems) console.log(`- ${p}`); }
