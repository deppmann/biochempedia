// check-listen: every polished lesson keeps its Kokoro voice.
//
// A rewrite changes paragraph text, and a clip is tied to its exact text (rehype-listen.mjs hashes
// it), so a level-up can silently leave a lesson with no matching clips: the Listen player then hides
// (it never falls back to the device voice). This check runs after `npm run build` (which writes
// .listen/<slug>.json) and FAILS for any published lesson in a POLISHED course whose current text
// has no clip at all in src/data/listen-manifest.json. Lessons with partial coverage are listed as
// warnings. Fix: node scripts/listen-render.mjs --only <slug> (renders, uploads, updates the manifest).
//
//   node scripts/check-listen.mjs            # fail on lessons with no clips
//   node scripts/check-listen.mjs --strict   # also fail below 90% coverage
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { POLISHED } from './listen-courses.mjs';

const strict = process.argv.includes('--strict');
if (!existsSync('.listen')) { console.error('check-listen: no .listen/ folder. Run `npm run build` first.'); process.exit(1); }
const manifest = JSON.parse(readFileSync('src/data/listen-manifest.json', 'utf8'));
const none = [], partial = [];
let checked = 0;
for (const dir of readdirSync('src/content/lessons').sort()) {
  const f = join('src/content/lessons', dir, 'lesson.mdx');
  if (!existsSync(f)) continue;
  const fm = (/^---\n([\s\S]*?)\n---/.exec(readFileSync(f, 'utf8')) || [])[1] || '';
  const val = (k) => ((new RegExp(`^${k}:\\s*["']?([^"'\\n]+?)["']?\\s*$`, 'm').exec(fm)) || [])[1];
  if (val('draft') === 'true') continue;
  const course = val('course') || 'biochemistry';
  if (!POLISHED.has(course)) continue;
  const slug = val('slug') || dir;
  const lf = join('.listen', `${slug}.json`);
  if (!existsSync(lf)) continue;
  const blocks = JSON.parse(readFileSync(lf, 'utf8'));
  if (!blocks.length) continue;
  checked++;
  const have = new Set(manifest[slug] || []);
  const hit = blocks.filter((b) => have.has(b.hash)).length;
  const pct = Math.round((100 * hit) / blocks.length);
  if (hit === 0) none.push(`${slug} (${course}): 0 of ${blocks.length} blocks voiced`);
  else if (pct < 90) partial.push(`${slug} (${course}): ${hit} of ${blocks.length} blocks voiced (${pct}%)`);
}
if (partial.length) console.warn(`check-listen: ${partial.length} polished lesson(s) partly voiced (edited paragraphs are skipped until re-rendered):\n  ${partial.join('\n  ')}`);
if (none.length || (strict && partial.length)) {
  console.error(`check-listen: ${none.length} polished lesson(s) have NO Kokoro clips for their current text, so Listen is hidden:\n  ${none.join('\n  ')}\nRender them: node scripts/listen-render.mjs --only <slug>`);
  process.exit(1);
}
console.log(`check-listen: ${checked} polished lessons, all have Kokoro clips${partial.length ? ` (${partial.length} partial)` : ''}.`);
