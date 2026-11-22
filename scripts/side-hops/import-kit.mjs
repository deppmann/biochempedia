#!/usr/bin/env node
/**
 * Bring an approved Side Hops kit into the site.
 *
 *   node scripts/side-hops/import-kit.mjs <slug> <kit.json> <audio.mp3>
 *
 * Run it from the repository root. It writes src/data/side-hops/<slug>.json, copies the audio to
 * public/side-hops/<slug>.mp3 (git-ignored; scripts/upload-media.mjs sends it to R2), refreshes the
 * production record and runs scripts/check-side-hops.mjs. Run it again after any fix to the kit.
 *
 * Pictures (2026-11-21): a Side Hop whose kit entry has an `image` ({caption, alt}) takes its picture
 * from images/<n>.jpg next to kit.json, where n is its place in the kit's list (1, 2, 3). The file is
 * copied to public/side-hops/<slug>-<n>.jpg (git-ignored, sent to R2 like the audio).
 *
 * Source links that point at a machine-readable API are replaced by the page a reader can open.
 * A warning is printed when the recording's length does not fit the script, which usually means the
 * script changed after the audio was recorded.
 */
import { spawnSync } from 'node:child_process';
import { copyFileSync, existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { lessonHeadings } from './shared.mjs';

const NARRATION = 'an AI narrator voice (ElevenLabs, Jessica)';
/** Characters of script per second of finished audio. The recordings so far run from 13.0 to 14.2. */
const PACE = { low: 12.3, high: 14.3 };

const [slug, kitPath, audioPath] = process.argv.slice(2);
if (!slug || !kitPath || !audioPath) {
  console.error('Usage: node scripts/side-hops/import-kit.mjs <slug> <kit.json> <audio.mp3>');
  process.exit(2);
}
const lessonPath = `src/content/lessons/${slug}/lesson.mdx`;
for (const p of [lessonPath, kitPath, audioPath]) {
  if (!existsSync(p)) { console.error(`import-kit: ${p} not found (run from the repository root)`); process.exit(1); }
}

/** Length of an MP3 in seconds, by walking its frames (correct for constant and variable bit rates). */
function mp3Seconds(buf) {
  const RATES = { 3: [44100, 48000, 32000], 2: [22050, 24000, 16000], 0: [11025, 12000, 8000] };
  const KBPS_V1 = [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320];
  const KBPS_V2 = [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160];
  let i = 0;
  if (buf.toString('latin1', 0, 3) === 'ID3') i = 10 + ((buf[6] << 21) | (buf[7] << 14) | (buf[8] << 7) | buf[9]);
  let seconds = 0, first = true;
  while (i + 4 <= buf.length) {
    if (buf[i] !== 0xff || (buf[i + 1] & 0xe0) !== 0xe0) { i++; continue; }
    const version = (buf[i + 1] >> 3) & 3, layer = (buf[i + 1] >> 1) & 3;
    const rateIdx = (buf[i + 2] >> 4) & 15, freqIdx = (buf[i + 2] >> 2) & 3, padding = (buf[i + 2] >> 1) & 1;
    if (version === 1 || layer !== 1 || rateIdx === 0 || rateIdx === 15 || freqIdx === 3) { i++; continue; }
    const v1 = version === 3;
    const hz = RATES[version][freqIdx];
    const samples = v1 ? 1152 : 576;
    const size = Math.floor(((samples / 8) * (v1 ? KBPS_V1 : KBPS_V2)[rateIdx] * 1000) / hz) + padding;
    // The first frame of most encoders is an information header, not sound.
    const info = first && /Xing|Info/.test(buf.toString('latin1', i + 4, Math.min(i + 40, buf.length)));
    if (!info) seconds += samples / hz;
    first = false;
    i += size;
  }
  return seconds;
}

function readerUrl(url) {
  const pubmed = /^https:\/\/eutils\.ncbi\.nlm\.nih\.gov\/entrez\/eutils\/efetch\.fcgi\?.*\bid=(\d+)/.exec(url);
  if (pubmed) return `https://pubmed.ncbi.nlm.nih.gov/${pubmed[1]}/`;
  const pmc = /^https:\/\/www\.ebi\.ac\.uk\/europepmc\/webservices\/rest\/(PMC\d+)\/fullTextXML/.exec(url);
  if (pmc) return `https://pmc.ncbi.nlm.nih.gov/articles/${pmc[1]}/`;
  return url;
}

const kit = JSON.parse(readFileSync(kitPath, 'utf8'));
if (kit.slug !== slug) { console.error(`import-kit: the kit is for "${kit.slug}", not "${slug}"`); process.exit(1); }
const headings = lessonHeadings(readFileSync(lessonPath, 'utf8'));
const place = (h) => { const n = headings.indexOf(h.afterHeading); return n < 0 ? headings.length : n; };

/** Width and height of a JPEG, from its first start-of-frame marker. */
function jpegSize(buf) {
  let i = 2;
  while (i + 9 < buf.length) {
    if (buf[i] !== 0xff) { i++; continue; }
    const m = buf[i + 1], len = buf.readUInt16BE(i + 2);
    if (m >= 0xc0 && m <= 0xcf && ![0xc4, 0xc8, 0xcc].includes(m)) return { height: buf.readUInt16BE(i + 5), width: buf.readUInt16BE(i + 7) };
    i += 2 + len;
  }
  return null;
}

const kitDir = dirname(kitPath);
const pictures = [];
function picture(a, n) {
  if (!a.image) return {};
  const src = join(kitDir, 'images', `${n}.jpg`);
  if (!existsSync(src)) { console.error(`import-kit: Side Hop ${n} has an image entry but ${src} is missing`); process.exit(1); }
  const size = jpegSize(readFileSync(src));
  if (!size) { console.error(`import-kit: ${src} is not a JPEG`); process.exit(1); }
  const file = `side-hops/${slug}-${n}.jpg`;
  pictures.push([src, `public/${file}`]);
  const alt = a.image.alt.startsWith('AI-generated illustration:') ? a.image.alt : `AI-generated illustration: ${a.image.alt}`;
  return { image: { file, alt, caption: a.image.caption, ...size } };
}

let relinked = 0;
const hops = kit.asides.map((a, i) => ({
  afterHeading: a.after_heading,
  kind: a.kind,
  title: a.title,
  text: a.text,
  sources: (a.sources ?? []).map((s) => {
    const url = readerUrl(s.url);
    if (url !== s.url) relinked++;
    return { citation: s.citation, url };
  }),
  ...picture(a, i + 1),
})).sort((a, b) => place(a) - place(b));

const durationSec = Math.round(mp3Seconds(readFileSync(audioPath)) * 10) / 10;
const transcript = kit.audio.script.trim();
const now = new Date();
const updated = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;
const data = {
  slug, updated, hops,
  audio: { title: kit.audio.title, file: `side-hops/${slug}.mp3`, durationSec, narration: NARRATION, transcript },
};

mkdirSync('src/data/side-hops', { recursive: true });
mkdirSync('public/side-hops', { recursive: true });
writeFileSync(`src/data/side-hops/${slug}.json`, JSON.stringify(data, null, 1) + '\n');
copyFileSync(audioPath, `public/side-hops/${slug}.mp3`);
for (const [from, to] of pictures) copyFileSync(from, to);
console.log(`import-kit: ${slug}: ${hops.length} Side Hops, ${pictures.length} picture(s), ${durationSec} s of audio${relinked ? `, ${relinked} source link(s) changed to the reader's page` : ''}`);

const pace = transcript.length / durationSec;
if (pace < PACE.low || pace > PACE.high) {
  console.log(`WARNING: ${slug}: ${transcript.length} characters over ${durationSec} s is ${pace.toFixed(1)} per second (usual: ${PACE.low} to ${PACE.high}). The recording may not match this script; re-record it before shipping.`);
}

const record = spawnSync('node', ['scripts/production-record.mjs', 'derive'], { stdio: 'inherit' });
const check = spawnSync('node', ['scripts/check-side-hops.mjs'], { stdio: 'inherit' });
process.exit(record.status || check.status || 0);
