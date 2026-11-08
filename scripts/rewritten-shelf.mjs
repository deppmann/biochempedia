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
import { readFileSync, writeFileSync, readdirSync, existsSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { execFileSync } from 'node:child_process';

const NOTES = process.env.LEVELUP_NOTES || '/Users/deppmann/biochempedia/docs/expansion/levelup';
if (!existsSync(NOTES)) { console.error(`rewritten-shelf: no level-up notes at ${NOTES}`); process.exit(1); }
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
    const fm = (/^---\n([\s\S]*?)\n---/.exec(readFileSync(f, 'utf8')) || [])[1] || '';
    if (/^draft:\s*true/m.test(fm)) continue;
    const marks = ['lesson.before.mdx', 'review.md'].filter((m) => existsSync(join(w, m))).map((m) => statSync(join(w, m)).mtime);
    const began = new Date(Math.min(...marks.map(Number)));
    const since = `${began.getFullYear()}-${String(began.getMonth() + 1).padStart(2, '0')}-${String(began.getDate()).padStart(2, '0')} 00:00`;
    let date = '';
    try { date = execFileSync('git', ['log', 'origin/main', `--since=${since}`, '--reverse', '--format=%cs', '--', f], { encoding: 'utf8' }).split('\n')[0].trim(); } catch { /* not in git */ }
    if (date) out.push({ slug, date });
  }
}
// Newest first; same-day lessons keep a stable order (by slug).
out.sort((a, b) => b.date.localeCompare(a.date) || a.slug.localeCompare(b.slug));
const seen = new Set();
const list = out.filter((r) => (seen.has(r.slug) ? false : seen.add(r.slug)));
writeFileSync('src/data/recently-rewritten.json', JSON.stringify(list, null, 1) + '\n');
console.log(`rewritten-shelf: ${list.length} rewritten lessons; newest ${list[0]?.date ?? 'none'}.`);
