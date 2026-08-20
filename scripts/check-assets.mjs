#!/usr/bin/env node
/**
 * Post-build asset + internal-link checker (the regression gate the site eval asked for).
 * Scans every built dist/**.html for local src/href/srcset/poster references and fails the
 * build if any points at a file that does not exist in dist/. Catches missing slide WebP,
 * narration MP3, scientist portraits, OG image, and broken internal links before they ship.
 *
 * External (http/https/protocol-relative), data:, mailto:, tel:, and #fragment refs are skipped.
 * Run automatically after `astro build` (see package.json) or standalone: `npm run check:assets`.
 */
import { readdir, readFile, stat } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { join, posix } from 'node:path';

const DIST = join(process.cwd(), 'dist');

async function htmlFiles(dir) {
  const out = [];
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const p = join(dir, entry.name);
    if (entry.isDirectory()) out.push(...(await htmlFiles(p)));
    else if (entry.name.endsWith('.html')) out.push(p);
  }
  return out;
}

/** Map a local URL path to the dist file(s) that would satisfy it. Returns true if any exists. */
function resolves(urlPath) {
  const clean = urlPath.split('#')[0].split('?')[0];
  if (!clean || clean === '/') return existsSync(join(DIST, 'index.html'));
  const rel = clean.replace(/^\//, '');
  const candidates = [join(DIST, rel)];
  if (clean.endsWith('/')) candidates.push(join(DIST, rel, 'index.html'));
  else if (!posix.basename(clean).includes('.')) {
    candidates.push(join(DIST, rel + '.html'), join(DIST, rel, 'index.html'));
  }
  return candidates.some((c) => existsSync(c));
}

function extractRefs(html) {
  const refs = new Set();
  // src="...", href="...", poster="..."
  for (const m of html.matchAll(/(?:src|href|poster)\s*=\s*"([^"]+)"/g)) refs.add(m[1]);
  // srcset="url1 1x, url2 2x"
  for (const m of html.matchAll(/srcset\s*=\s*"([^"]+)"/g)) {
    for (const part of m[1].split(',')) {
      const u = part.trim().split(/\s+/)[0];
      if (u) refs.add(u);
    }
  }
  return refs;
}

function isLocal(u) {
  return u.startsWith('/') && !u.startsWith('//');
}

const files = existsSync(DIST) ? await htmlFiles(DIST) : [];
if (!files.length) {
  console.error('check-assets: no dist/ HTML found — run after `astro build`.');
  process.exit(1);
}

const missing = new Map(); // urlPath -> Set(pages)
let checked = 0;
for (const file of files) {
  const html = await readFile(file, 'utf8');
  const page = '/' + posix.relative(DIST.split(/[\\/]/).join('/'), file.split(/[\\/]/).join('/'));
  for (const ref of extractRefs(html)) {
    if (!isLocal(ref)) continue;
    checked++;
    if (!resolves(ref)) {
      if (!missing.has(ref)) missing.set(ref, new Set());
      missing.get(ref).add(page);
    }
  }
}

if (missing.size) {
  console.error(`\n✗ check-assets: ${missing.size} broken local reference(s) across ${files.length} pages:\n`);
  for (const [ref, pages] of [...missing].sort()) {
    const list = [...pages].slice(0, 3).join(', ') + (pages.size > 3 ? ` …(+${pages.size - 3})` : '');
    console.error(`  ${ref}\n      ↳ referenced by ${list}`);
  }
  console.error('');
  process.exit(1);
}

console.log(`✓ check-assets: ${checked} local references across ${files.length} pages all resolve.`);

/* ---------------------------------------------------------------------------
   Webfont gate.

   The brand tokens carry the Google Fonts @import that loads Playfair Display
   and Inter. This site has only the two `preconnect` hints in <head> and no
   stylesheet <link> of its own, so if that @import ever disappears the whole
   site silently falls back to system fonts — every heading, every lesson — and
   the build still passes. That happened once for real: bumping the `brand/`
   submodule pin to a commit that had moved the @import out to the consumer
   shipped a fontless site to production, and nothing caught it.

   So assert the fonts are actually reachable, by either route.
   --------------------------------------------------------------------------- */
const FONT_HOST = 'fonts.googleapis.com';
let fontSource = null;

const cssDir = join(DIST, '_astro');
if (existsSync(cssDir)) {
  for (const entry of await readdir(cssDir)) {
    if (!entry.endsWith('.css')) continue;
    if ((await readFile(join(cssDir, entry), 'utf8')).includes(FONT_HOST)) {
      fontSource = `@import in _astro/${entry}`;
      break;
    }
  }
}
if (!fontSource) {
  // A <link rel="stylesheet"> in <head> is the other legitimate way to load them.
  for (const file of files) {
    const html = await readFile(file, 'utf8');
    if (/<link[^>]+rel=["']?stylesheet["']?[^>]*fonts\.googleapis\.com/i.test(html) ||
        /<link[^>]+fonts\.googleapis\.com[^>]*rel=["']?stylesheet/i.test(html)) {
      fontSource = `<link rel="stylesheet"> in ${posix.basename(file)}`;
      break;
    }
  }
}

if (!fontSource) {
  console.error(`\n✗ check-assets: no webfont source found in the build.`);
  console.error(`  Playfair Display and Inter would fall back to system fonts sitewide.`);
  console.error(`  Most likely cause: the brand/ submodule pin moved to a commit that`);
  console.error(`  dropped the Google Fonts @import from tokens.css and expects the`);
  console.error(`  consumer to carry its own <link rel="stylesheet"> in <head>.`);
  console.error(`  Fix: restore the pin (git ls-tree main brand), or add the <link> to`);
  console.error(`  BaseLayout.astro alongside the existing preconnect hints.\n`);
  process.exit(1);
}
console.log(`✓ check-assets: webfonts load via ${fontSource}.`);

await stat(DIST); // touch, keep import used

/* ---------------------------------------------------------------------------
   Analytics gate.

   Same failure shape as the webfont gate above: a <head> tag that can vanish
   without breaking anything visible. If the Plausible snippet stops emitting,
   every page still renders perfectly and the build still passes — the only
   symptom is a traffic graph that quietly flatlines, which nobody notices for
   weeks.

   Two ways it can silently disappear: BaseLayout's `import.meta.env.PROD`
   guard failing to be true in the deploy environment, or someone dropping
   `is:inline` and letting Astro bundle the tags into a module (the queue shim
   must run before the remote script, and hoisting breaks that order).

   So assert both halves are present, inline, in the built HTML.
   --------------------------------------------------------------------------- */
const PLAUSIBLE_HOST = 'plausible.io/js/';
let analyticsPage = null;
let missingInit = null;

for (const file of files) {
  const html = await readFile(file, 'utf8');
  if (!html.includes(PLAUSIBLE_HOST)) continue;
  // The remote tag alone is not enough — without the init call nothing fires.
  if (html.includes('plausible.init()')) {
    analyticsPage = posix.basename(file);
    break;
  }
  missingInit = posix.basename(file);
}

if (!analyticsPage) {
  console.error(`\n✗ check-assets: the Plausible snippet is not in the built HTML.`);
  if (missingInit) {
    console.error(`  Found the remote script in ${missingInit} but no plausible.init() call,`);
    console.error(`  so the tracker loads and never fires. Most likely cause: Astro bundled`);
    console.error(`  the inline shim — check that BOTH <script> tags still carry is:inline.`);
  } else {
    console.error(`  No page carries it, so biochemistrypedia.com records zero traffic.`);
    console.error(`  Most likely cause: the import.meta.env.PROD guard in BaseLayout.astro`);
    console.error(`  is false in this build, or the block was removed.`);
    console.error(`  Note: a dev build legitimately omits it — this gate runs after`);
    console.error(`  \`astro build\`, where PROD is true.`);
  }
  console.error(``);
  process.exit(1);
}
console.log(`✓ check-assets: Plausible snippet present and initialised (${analyticsPage}).`);
