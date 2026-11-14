// rewritten-shelf: write src/data/recently-rewritten.json for the homepage "Recently rewritten" strip.
//
//   node scripts/rewritten-shelf.mjs      # run after a level-up PR merges (the level-up skill's last step)
//
// Source: the level-up notes. A lesson counts as rewritten when the level-up work folder
// docs/expansion/levelup/<course>/<slug>/ holds its saved original (lesson.before.mdx) or its
// expert review (review.md). docs/expansion is private (push_public.sh strips it), so this runs
// locally and the JSON it writes is committed; the homepage reads it at deploy time.
// Date: the first commit on origin/main that touches the lesson on or after the day its level-up
// work began (the saved original or the review), i.e. the day the rewrite reached the site.
//
// `new` (2026-11-11): what changed, for the "Rewritten on <date>: new text, figures and flashcards"
// line under each lesson title (src/lib/rewritten.ts). "text" always; "figures" when the lesson now
// places a figure its saved original did not (or, with no saved original, a figure file under
// public/figures/<slug>/ arrived on origin/main on or after the date); "flashcards" when the deck
// src/data/flashcards/<slug>.json changed on or after the date; "film" when the lesson's film
// (explainer or films in the frontmatter) changed on or after the date. A `new` list set by hand in
// the JSON wins over the worked-out one, so a wrong sentence can be fixed without editing this script.
import { readFileSync, writeFileSync, readdirSync, existsSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';

const NOTES = process.env.LEVELUP_NOTES || fileURLToPath(new URL('../docs/expansion/levelup', import.meta.url));
if (!existsSync(NOTES)) { console.error(`rewritten-shelf: no level-up notes at ${NOTES}`); process.exit(1); }
const OUT = 'src/data/recently-rewritten.json';
// Earlier entries are kept (2026-11-11): a machine whose notes folder lacks a course, or whose copied
// notes carry fresh file times, used to drop those lessons from the list (the Nov 10 run on the
// Studio cut 170 entries to 8). An entry leaves only when its lesson is gone or back to draft.
let prior = [];
try { prior = JSON.parse(readFileSync(OUT, 'utf8')); } catch { /* first run */ }
const handNew = new Map(prior.filter((r) => r.hand && r.new).map((r) => [r.slug, r.new]));
const figSrcs = (t) => new Set([...t.matchAll(/<(?:LessonFigure|ScaffoldFigure)\s[^>]*?src="([^"]+)"/g)].map((m) => m[1]));
const changedSince = (since, ...paths) => {
  try { return execFileSync('git', ['log', 'origin/main', `--since=${since}`, '--format=%h', '--', ...paths], { encoding: 'utf8' }).trim() !== ''; } catch { return false; }
};
/** Did the film frontmatter (explainer: or films:) change on origin/main since the date? */
const filmChangedSince = (since, f) => {
  try {
    const log = execFileSync('git', ['log', 'origin/main', `--since=${since}`, '-p', '--format=', '--', f], { encoding: 'utf8' });
    // A new or re-cut film changes its length (durationSec) or adds the explainer/films block.
    return /^[+-]\s*(explainer:|films:|durationSec:)/m.test(log);
  } catch { return false; }
};
/** One list entry, with what changed worked out (or the hand-set list). */
function entry(slug, date, before) {
  const hand = handNew.get(slug);
  if (hand) return { slug, date, new: hand, hand: true };
  const f = join('src/content/lessons', slug, 'lesson.mdx');
  const day = `${date} 00:00`;
  const parts = ['text'];
  const nowFigs = figSrcs(readFileSync(f, 'utf8'));
  const hadFigs = before && existsSync(before) ? figSrcs(readFileSync(before, 'utf8')) : null;
  if (hadFigs ? [...nowFigs].some((s) => !hadFigs.has(s)) : (nowFigs.size > 0 && changedSince(day, join('public/figures', slug)))) parts.push('figures');
  if (changedSince(day, join('src/data/flashcards', `${slug}.json`))) parts.push('flashcards');
  if (changedSince(day, join('public/explainers', slug)) || filmChangedSince(day, f)) parts.push('film');
  return { slug, date, new: parts };
}
/**
 * Has this lesson's level-up actually shipped? Notes folders also exist for work that only touched
 * a film or a quiz (2026-11-14: gpcrs-and-g-proteins got one for film work, then a commit added only
 * MCAT questions, and the date logic proposed it as "rewritten"). A lesson counts only if
 *  (a) its frontmatter carries the chapter-pair film (films: id "chapter-2") plus take-homes, the
 *      shape every level-up since 2026-11-11 ships, or
 *  (b) its lesson body (everything after the frontmatter) differs from the saved original
 *      lesson.before.mdx, so a frontmatter-only change (MCAT, quiz, film links) never counts.
 */
const levelUpShipped = (src, before) => {
  const fm = (/^---\n([\s\S]*?)\n---/.exec(src) || [])[1] || '';
  if (/^\s*-\s*id:\s*["']?chapter-2["']?\s*$/m.test(fm) && /^\s*takeaways:/m.test(fm)) return true;
  if (!before || !existsSync(before)) return false;
  const body = (t) => t.replace(/^---\n[\s\S]*?\n---\n?/, '').replace(/\s+/g, ' ').trim();
  return body(src) !== body(readFileSync(before, 'utf8'));
};
const out = [];
for (const course of readdirSync(NOTES)) {
  const cdir = join(NOTES, course);
  let kids = [];
  try { kids = readdirSync(cdir, { withFileTypes: true }).filter((d) => d.isDirectory()).map((d) => d.name); } catch { continue; }
  for (const slug of kids) {
    const w = join(cdir, slug);
    if (!existsSync(join(w, 'lesson.before.mdx')) && !existsSync(join(w, 'review.md'))) continue;
    const f = join('src/content/lessons', slug, 'lesson.mdx');
    if (!existsSync(f)) continue;
    const src = readFileSync(f, 'utf8');
    const fm = (/^---\n([\s\S]*?)\n---/.exec(src) || [])[1] || '';
    if (/^draft:\s*true/m.test(fm)) continue;
    if (!levelUpShipped(src, join(w, 'lesson.before.mdx'))) continue;
    const marks = ['lesson.before.mdx', 'review.md'].filter((m) => existsSync(join(w, m))).map((m) => statSync(join(w, m)).mtime);
    const began = new Date(Math.min(...marks.map(Number)));
    const since = `${began.getFullYear()}-${String(began.getMonth() + 1).padStart(2, '0')}-${String(began.getDate()).padStart(2, '0')} 00:00`;
    let date = '';
    try { date = execFileSync('git', ['log', 'origin/main', `--since=${since}`, '--reverse', '--format=%cs', '--', f], { encoding: 'utf8' }).split('\n')[0].trim(); } catch { /* not in git */ }
    if (date) out.push(entry(slug, date, join(w, 'lesson.before.mdx')));
  }
}
// Keep earlier entries this run did not find, if the lesson is still published.
const found = new Set(out.map((r) => r.slug));
for (const r of prior) {
  if (found.has(r.slug)) continue;
  const f = join('src/content/lessons', r.slug, 'lesson.mdx');
  if (!existsSync(f) || /^draft:\s*true/m.test((/^---\n([\s\S]*?)\n---/.exec(readFileSync(f, 'utf8')) || [])[1] || '')) continue;
  out.push(r.new ? r : entry(r.slug, r.date, null));
}
// Newest first; same-day lessons keep a stable order (by slug).
out.sort((a, b) => b.date.localeCompare(a.date) || a.slug.localeCompare(b.slug));
const seen = new Set();
const list = out.filter((r) => (seen.has(r.slug) ? false : seen.add(r.slug)));
writeFileSync(OUT, JSON.stringify(list, null, 1) + '\n');
console.log(`rewritten-shelf: ${list.length} rewritten lessons; newest ${list[0]?.date ?? 'none'}.`);
