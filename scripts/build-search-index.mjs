#!/usr/bin/env node
/**
 * Builds the site search index: dist/pagefind/. Run by the pagefind-index integration in
 * astro.config.mjs once `astro build` has written dist/ (or by hand: node scripts/build-search-index.mjs dist).
 *
 * One Pagefind index holds two kinds of entry, each with a `type` filter:
 *  - the built pages marked data-pagefind-body: lesson pages (type lesson) and the math toolkit
 *    (type toolkit). Pagefind reads them from dist/ exactly as the CLI did; the settings that were
 *    in pagefind.yml are read from it here (the Node API does not read that file).
 *  - the typed records in dist/search-records.json (src/pages/search-records.json.ts): films with
 *    their whole narration, methods, Side Hops, flashcard decks and simulations. Each becomes a small
 *    HTML document (recordHtml in src/lib/search-records.mjs). The JSON file is then deleted, so it is
 *    never deployed.
 *
 * Prints how big the index is, so a growing index is noticed.
 */
import { readFile, rm, readdir, stat } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { join, resolve } from 'node:path';
import * as pagefind from 'pagefind';
import { recordHtml } from '../src/lib/search-records.mjs';

/** The few keys of pagefind.yml this site uses: exclude_selectors (a list) and force_language. */
export function readPagefindYml(text) {
  const cfg = { excludeSelectors: [] };
  let inList = false;
  for (const line of text.split('\n')) {
    if (/^\s*#/.test(line) || !line.trim()) continue;
    const key = /^([a-z_]+):\s*(.*)$/.exec(line);
    if (key) {
      inList = key[1] === 'exclude_selectors' && !key[2];
      if (key[1] === 'force_language' && key[2]) cfg.forceLanguage = key[2].replace(/^["']|["']$/g, '');
      continue;
    }
    const item = /^\s*-\s*(.+)$/.exec(line);
    if (inList && item) cfg.excludeSelectors.push(item[1].trim().replace(/^["']|["']$/g, ''));
  }
  return cfg;
}

async function dirSize(dir) {
  let bytes = 0;
  let files = 0;
  for (const e of await readdir(dir, { withFileTypes: true })) {
    const p = join(dir, e.name);
    if (e.isDirectory()) { const s = await dirSize(p); bytes += s.bytes; files += s.files; }
    else { bytes += (await stat(p)).size; files++; }
  }
  return { bytes, files };
}

export async function buildSearchIndex(site) {
  const root = resolve(site);
  const ymlPath = resolve('pagefind.yml');
  const cfg = existsSync(ymlPath) ? readPagefindYml(await readFile(ymlPath, 'utf8')) : { excludeSelectors: [] };
  const { index, errors } = await pagefind.createIndex(cfg);
  if (!index) throw new Error(`Pagefind could not start: ${errors.join('; ')}`);
  try {
    const pages = await index.addDirectory({ path: root });
    if (pages.errors?.length) throw new Error(pages.errors.join('; '));

    const recFile = join(root, 'search-records.json');
    let added = 0;
    const byType = {};
    if (existsSync(recFile)) {
      const { records } = JSON.parse(await readFile(recFile, 'utf8'));
      // Pagefind keeps one entry per URL (the hash does not count): a record must not share one with a
      // page or another record, or it silently replaces it (a Side Hop at /lessons/x/ would hide the lesson).
      const seen = new Set();
      for (const rec of records) {
        const key = rec.url.split('#')[0];
        if (seen.has(key) || /^\/lessons\/[^/?]+\/$/.test(key) || key === '/math-toolkit/') throw new Error(`search record URL ${rec.url} is not unique (it would replace a page or another record)`);
        seen.add(key);
      }
      for (const rec of records) {
        const r = await index.addHTMLFile({ url: rec.url, content: recordHtml(rec) });
        if (r.errors?.length) throw new Error(`search record ${rec.url}: ${r.errors.join('; ')}`);
        added++;
        byType[rec.type] = (byType[rec.type] ?? 0) + 1;
      }
      if (!process.env.KEEP_SEARCH_RECORDS) await rm(recFile);
    } else {
      console.warn('search: dist/search-records.json is missing; only pages are indexed.');
    }

    const out = join(root, 'pagefind');
    await rm(out, { recursive: true, force: true });
    const w = await index.writeFiles({ outputPath: out });
    if (w.errors?.length) throw new Error(w.errors.join('; '));
    const size = await dirSize(out);
    const kinds = Object.entries(byType).map(([k, n]) => `${n} ${k}`).join(', ');
    console.log(`search: ${pages.page_count} pages + ${added} records (${kinds}); dist/pagefind is ${(size.bytes / 1048576).toFixed(1)} MB in ${size.files} files, loaded a chunk at a time`);
  } finally {
    await pagefind.close();
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  buildSearchIndex(process.argv[2] || 'dist').catch((e) => { console.error(e); process.exit(1); });
}
