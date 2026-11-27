// Download films and Side Hops audio into public/ from the live site, for a tool that needs the file on disk.
//
//   node scripts/fetch-media.mjs --only action-potential           # one lesson's films and Side Hops audio
//   node scripts/fetch-media.mjs --only action-potential --only gpcr
//   node scripts/fetch-media.mjs --only side-hops                  # all Side Hops audio
//   node scripts/fetch-media.mjs --all                             # everything (about 5.6 GB)
//   node scripts/fetch-media.mjs --only home/sizzle --dry-run      # list what would be fetched
//
// Films and Side Hops audio are not tracked in git. Every file is in R2 and listed in media-manifest.json
// (path, size, sha256); the site serves it at the same path. This fetches each listed file under the chosen
// folders, checks its sha256 against the manifest and writes it in place. A file already on disk
// with the right hash is left alone; one with another hash (a local re-render not yet uploaded)
// is also left alone unless --force is given. Posters and captions are in git and are not fetched.
// The site address can be changed with MEDIA_BASE_URL (default: the site's address, src/lib/site-host.mjs).
import { createHash } from 'node:crypto';
import { existsSync, mkdirSync, readFileSync, renameSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { SITE_ORIGIN } from '../src/lib/site-host.mjs';

const args = process.argv.slice(2);
const only = args.flatMap((a, i) => (a === '--only' && args[i + 1] ? [args[i + 1].replace(/^\/+|\/+$/g, '')] : []));
const all = args.includes('--all');
const dry = args.includes('--dry-run');
const force = args.includes('--force');
const BASE = (process.env.MEDIA_BASE_URL || SITE_ORIGIN).replace(/\/+$/, '');
const PARALLEL = Number(process.env.MEDIA_PARALLEL || 4);

if (!all && !only.length) {
  console.error('Usage: node scripts/fetch-media.mjs --only <slug> [--only <slug> ...] | --all  [--dry-run] [--force]');
  process.exit(2);
}
if (!existsSync('media-manifest.json')) {
  console.error('fetch-media: run from the repository root (media-manifest.json not found).');
  process.exit(2);
}
const manifest = JSON.parse(readFileSync('media-manifest.json', 'utf8'));
const sha = (buf) => createHash('sha256').update(buf).digest('hex');

const isFilm = (k) => k.startsWith('explainers/') && k.endsWith('.mp4');
const hopAudio = (k) => /^side-hops\/([^/]+)-card[1-9]\d*\.mp3$/.exec(k);
const matches = (k, s) => (isFilm(k) ? k.startsWith(`explainers/${s}/`) : s === 'side-hops' || hopAudio(k)?.[1] === s);
const wanted = Object.keys(manifest).filter((k) => (isFilm(k) || hopAudio(k)) && (all || only.some((s) => matches(k, s))));
const unmatched = only.filter((s) => !wanted.some((k) => matches(k, s)));
if (unmatched.length) console.error(`fetch-media: no film or Side Hops audio in media-manifest.json under: ${unmatched.join(', ')}`);

const todo = [];
let present = 0, differs = 0;
for (const key of wanted) {
  const file = join('public', key);
  if (existsSync(file)) {
    if (sha(readFileSync(file)) === manifest[key].sha256) { present++; continue; }
    if (!force) { differs++; console.log(`kept ${key}: local file differs from the manifest (a re-render not uploaded yet?); --force replaces it`); continue; }
  }
  todo.push(key);
}
const bytes = todo.reduce((n, k) => n + manifest[k].size, 0);
if (dry) {
  for (const k of todo) console.log('would fetch', k, (manifest[k].size / 1e6).toFixed(1) + ' MB');
  console.log(`would fetch ${todo.length} of ${wanted.length} files, ${(bytes / 1e6).toFixed(0)} MB (${present} already present)`);
  process.exit(unmatched.length ? 1 : 0);
}

let next = 0, failed = 0, got = 0;
const one = async (key) => {
  const res = await fetch(`${BASE}/${key}`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const buf = Buffer.from(await res.arrayBuffer());
  const h = sha(buf);
  if (h !== manifest[key].sha256) throw new Error(`sha256 ${h.slice(0, 12)} does not match the manifest ${manifest[key].sha256.slice(0, 12)} (${buf.length} bytes)`);
  const file = join('public', key);
  mkdirSync(dirname(file), { recursive: true });
  writeFileSync(file + '.part', buf);
  renameSync(file + '.part', file);
};
const worker = async () => {
  while (next < todo.length) {
    const key = todo[next++];
    try { await one(key); got++; console.log('fetched', key); }
    catch (e) { failed++; console.error('FAILED', key, e.message); }
  }
};
await Promise.all(Array.from({ length: PARALLEL }, worker));
console.log(`fetched ${got} of ${wanted.length} files, ${(bytes / 1e6).toFixed(0)} MB; ${present} already present${differs ? `, ${differs} kept with local changes` : ''}${failed ? `, ${failed} FAILED` : ''}`);
if (failed || unmatched.length) process.exitCode = 1;
