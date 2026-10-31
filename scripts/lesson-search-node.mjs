/**
 * Runs src/lib/lesson-search.ts in Node against the BUILT site (dist/), with no server: the same
 * Pagefind index and the same ranking code the browser uses. Used by scripts/search-lessons.mjs (a
 * command-line search for offline course planning) and scripts/test-search.mjs.
 *
 * Needs `npm run build` (or `npx astro build`) first, and a Node that runs .ts files (22.18 or newer).
 */
import { readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import * as lib from '../src/lib/lesson-search.ts';

export { lib };

/** @param {string} [site] the build output folder (default: dist next to this repo's package.json) */
export function nodeEngine(site = fileURLToPath(new URL('../dist', import.meta.url))) {
  const root = resolve(site);
  const dir = resolve(root, 'pagefind');
  if (!existsSync(resolve(dir, 'pagefind.js'))) throw new Error(`No search index in ${dir}. Run \`npm run build\` first.`);
  // Pagefind's client downloads its files with fetch(); here they are read from disk.
  const diskFetch = async (/** @type {any} */ u) => {
    const s = String(u);
    const bytes = await readFile(s.startsWith('file:') ? fileURLToPath(s) : resolve(root, '.' + s));
    return new Response(bytes, { status: 200, headers: s.endsWith('.wasm') ? { 'content-type': 'application/wasm' } : {} });
  };
  globalThis.fetch = /** @type {any} */ (diskFetch);
  /** @type {Promise<any> | null} */ let pf = null;
  return /** @type {import('../src/lib/lesson-search.ts').Engine} */ ({
    index: async () => JSON.parse(await readFile(resolve(root, 'search-index.json'), 'utf8')),
    pagefind: () => (pf ??= (async () => {
      const m = await import(pathToFileURL(resolve(dir, 'pagefind.js')).href);
      await m.options({ basePath: pathToFileURL(dir + '/').href, baseUrl: '/' });
      return m;
    })()),
    pageMap: async () => (existsSync(resolve(dir, 'page-map.json')) ? JSON.parse(await readFile(resolve(dir, 'page-map.json'), 'utf8')) : null),
  });
}
