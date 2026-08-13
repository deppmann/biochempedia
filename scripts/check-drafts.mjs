#!/usr/bin/env node
/**
 * Draft-route assertion (post-build; run after `astro build`).
 *
 * A lesson marked `draft: true` must not produce a page. The homepage, the
 * sitemap, and getStaticPaths in [...slug].astro each filter drafts
 * independently — three copies of the same filter — so this asserts the
 * outcome: no draft slug exists under dist/lessons/. If someone adds a
 * fourth surface and forgets the filter, or the route filter is edited away,
 * this fails the build instead of quietly publishing unfinished lessons.
 *
 * Run: node scripts/check-drafts.mjs   (also run by CI on every push)
 */
import { readdir, readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { join } from 'node:path';

const LESSONS = join(process.cwd(), 'src', 'content', 'lessons');
const DIST = join(process.cwd(), 'dist');

if (!existsSync(DIST)) {
  console.error('check-drafts: no dist/ found — run after `astro build`.');
  process.exit(1);
}

let drafts = 0;
const leaked = [];
for (const dir of (await readdir(LESSONS, { withFileTypes: true })).filter((d) => d.isDirectory())) {
  const file = join(LESSONS, dir.name, 'lesson.mdx');
  if (!existsSync(file)) continue;
  const fm = (await readFile(file, 'utf8')).split(/^---\s*$/m)[1] ?? '';
  if (!/^draft:\s*true\s*$/m.test(fm)) continue;
  drafts++;
  const slug = fm.match(/^slug:\s*["']?([^"'\n]+)["']?\s*$/m)?.[1] ?? dir.name;
  if (existsSync(join(DIST, 'lessons', slug, 'index.html'))) leaked.push(slug);
  // The sitemap must not advertise it either.
  const sitemap = join(DIST, 'sitemap.xml');
  if (existsSync(sitemap) && (await readFile(sitemap, 'utf8')).includes(`/lessons/${slug}/`)) {
    leaked.push(`${slug} (in sitemap.xml)`);
  }
}

if (leaked.length) {
  console.error(`\n✗ check-drafts: draft lesson(s) built into the public site:\n`);
  for (const s of leaked) console.error(`  /lessons/${s}/`);
  console.error('');
  process.exit(1);
}
console.log(`✓ check-drafts: ${drafts} draft lesson(s), none reachable in dist/.`);
