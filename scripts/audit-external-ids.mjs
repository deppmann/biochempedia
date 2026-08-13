#!/usr/bin/env node
/**
 * External-ID resolution audit (network; run weekly by CI, or by hand).
 *
 * The build verifies every LOCAL reference, but nothing verifies that a
 * remote accession still resolves — a retracted PDB entry, a pulled YouTube
 * video, or a moved PhET sim would rot silently. This script re-resolves
 * every external ID the lessons reference, live, against the same providers
 * the site loads from. It was last run by hand on 2026-08-12 (all 378 unique
 * IDs resolved); this makes that audit repeatable.
 *
 * Sources checked: RCSB PDB entries, PubChem CIDs, YouTube videos (oEmbed),
 * PhET sim URLs, Spotify shows/episodes (oEmbed).
 *
 * Run: node scripts/audit-external-ids.mjs
 * Exit 1 if anything fails to resolve after one retry.
 */
import { readdir, readFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { join } from 'node:path';

const LESSONS = join(process.cwd(), 'src', 'content', 'lessons');
const DELAY_MS = 250; // be polite to the providers
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

// ---- Collect IDs from every lesson's frontmatter --------------------------
const rcsb = new Set();
const pubchem = new Set();
const youtube = new Set();
const phet = new Set();
const spotify = new Set();

for (const dir of (await readdir(LESSONS, { withFileTypes: true })).filter((d) => d.isDirectory())) {
  const file = join(LESSONS, dir.name, 'lesson.mdx');
  if (!existsSync(file)) continue;
  const text = await readFile(file, 'utf8');

  // structures: `source: "rcsb"` / `source: "pubchem"` followed by `id: "..."`.
  let lastSource = null;
  for (const line of text.split('\n')) {
    const src = line.match(/^\s*source:\s*["']?(rcsb|pubchem)["']?\s*$/);
    if (src) { lastSource = src[1]; continue; }
    const id = line.match(/^\s*id:\s*["']?([A-Za-z0-9]+)["']?\s*$/);
    if (id && lastSource) {
      (lastSource === 'rcsb' ? rcsb : pubchem).add(id[1]);
      lastSource = null;
    }
  }
  for (const m of text.matchAll(/^\s*youtubeId:\s*["']?([A-Za-z0-9_-]{11})["']?\s*$/gm)) youtube.add(m[1]);
  for (const m of text.matchAll(/https:\/\/phet\.colorado\.edu[^\s"']+/g)) phet.add(m[0]);
  for (const m of text.matchAll(/https:\/\/open\.spotify\.com[^\s"']+/g)) spotify.add(m[0]);
}

// ---- Resolvers -------------------------------------------------------------
const UA = { 'user-agent': 'biochemistrypedia.com integrity audit (deppmann lab)' };
async function ok(url, opts = {}) {
  const res = await fetch(url, { redirect: 'follow', headers: UA, ...opts });
  return res.ok;
}
const checks = [
  ...[...rcsb].map((id) => ({ kind: 'rcsb', id, url: `https://data.rcsb.org/rest/v1/core/entry/${id}` })),
  ...[...pubchem].map((id) => ({ kind: 'pubchem', id, url: `https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/${id}/property/Title/JSON` })),
  ...[...youtube].map((id) => ({ kind: 'youtube', id, url: `https://www.youtube.com/oembed?url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3D${id}&format=json` })),
  ...[...phet].map((u) => ({ kind: 'phet', id: u, url: u })),
  ...[...spotify].map((u) => ({ kind: 'spotify', id: u, url: `https://open.spotify.com/oembed?url=${encodeURIComponent(u)}` })),
];

console.log(`audit-external-ids: ${rcsb.size} PDB · ${pubchem.size} PubChem · ${youtube.size} YouTube · ${phet.size} PhET · ${spotify.size} Spotify (${checks.length} unique)`);

const failed = [];
for (const c of checks) {
  let good = false;
  try { good = await ok(c.url); } catch { good = false; }
  if (!good) {
    await sleep(1500); // one retry, after a beat — transient 5xx/ratelimit shouldn't page anyone
    try { good = await ok(c.url); } catch { good = false; }
  }
  if (!good) failed.push(c);
  await sleep(DELAY_MS);
}

if (failed.length) {
  console.error(`\n✗ audit-external-ids: ${failed.length} of ${checks.length} external IDs no longer resolve:\n`);
  for (const c of failed) console.error(`  [${c.kind}] ${c.id}\n      ↳ ${c.url}`);
  console.error('\n  Each of these is cited in a live lesson. Verify by hand, then fix or replace the reference.\n');
  process.exit(1);
}
console.log(`✓ audit-external-ids: all ${checks.length} external IDs resolve.`);
