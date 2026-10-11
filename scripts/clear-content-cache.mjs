// Remove Astro's parsed-content store before a production build.
//
// The store caches every lesson as it was parsed under the schema of the day. A build
// host that restores a cached node_modules/.astro (Cloudflare Workers Builds does) can
// hand a new schema lessons parsed under the old one: on 2026-10-11 that gave lessons
// with no `course` field, the homepage found no biochemistry lessons, and the deploy
// failed (the guard in src/pages/index.astro stopped an empty homepage from shipping).
// Parsing 70-odd lessons afresh costs about a second.
import { rmSync } from 'node:fs';

for (const p of ['node_modules/.astro/data-store.json', '.astro/data-store.json']) {
  rmSync(p, { force: true });
}
console.log('[clear-content-cache] content store cleared');
