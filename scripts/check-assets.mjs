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
await stat(DIST); // touch, keep import used
