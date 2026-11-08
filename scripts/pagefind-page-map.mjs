#!/usr/bin/env node
/**
 * Writes dist/pagefind/page-map.json: { "<Pagefind result id>": "<lesson slug>" }.
 *
 * Why: a Pagefind search result carries its score and the positions of the matched words, but not
 * the page's URL; the URL is in the page's fragment, one more download. The lesson search ranks the
 * top ~60 results (adjacent matched words, title evidence) before it downloads any fragment, so it
 * needs to know which lesson each result is. This map is read here with Pagefind's own client, so it
 * does not depend on the index file format, and it is a few kilobytes.
 *
 * Run by the Pagefind integration in astro.config.mjs right after the index is built:
 *   node scripts/pagefind-page-map.mjs dist
 * If it is missing the search still works: it fetches the fragments of the top results instead.
 */
import { readFile, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const site = resolve(process.argv[2] || 'dist');
const dir = resolve(site, 'pagefind');
// Pagefind's client loads its files with fetch(); here they come from disk.
globalThis.fetch = async (u) => {
  const s = String(u);
  const bytes = await readFile(s.startsWith('file:') ? fileURLToPath(s) : resolve(site, '.' + s));
  return new Response(bytes, { status: 200, headers: s.endsWith('.wasm') ? { 'content-type': 'application/wasm' } : {} });
};
const pf = await import(pathToFileURL(resolve(dir, 'pagefind.js')).href);
await pf.options({ basePath: pathToFileURL(dir + '/').href, baseUrl: '/' });
const all = await pf.search(null);
const map = {};
for (const r of all.results) {
  const d = await r.data();
  const slug = /\/lessons\/([^/?#]+)/.exec(d.url)?.[1];
  if (slug) map[r.id] = slug;
}
await writeFile(resolve(dir, 'page-map.json'), JSON.stringify(map));
console.log(`page-map.json: ${Object.keys(map).length} lessons`);
