#!/usr/bin/env node
/**
 * Bring an approved Side Hops kit into the site.
 *
 *   node scripts/side-hops/import-kit.mjs <slug> <kit.json> [cards-dir]
 *   node scripts/side-hops/import-kit.mjs <slug> --from-site <cards-dir>
 *
 * Run from the repository root. The kit form reads clips from audio/cards next to kit.json by
 * default, and copies pictures from images/<n>.jpg. The --from-site form attaches clips to
 * existing site data in its current card order, preserving the card content and pictures.
 * Media is copied to public/side-hops/ (git-ignored, uploaded to R2 by ship_pr.sh).
 */
import { spawnSync } from 'node:child_process';
import { copyFileSync, existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { lessonHeadings, problemsIn } from './shared.mjs';

const [slug, input, clipsDir, ...extra] = process.argv.slice(2);
const fromSite = input === '--from-site';
if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(slug ?? '') || !input || (fromSite && !clipsDir) || extra.length) {
  console.error('Usage: node scripts/side-hops/import-kit.mjs <slug> <kit.json> [cards-dir] | <slug> --from-site <cards-dir>');
  process.exit(2);
}
const lessonPath = `src/content/lessons/${slug}/lesson.mdx`;
const dataPath = `src/data/side-hops/${slug}.json`;
const inputPath = fromSite ? dataPath : input;
const kitDir = dirname(inputPath);
const cardsDir = clipsDir ?? join(kitDir, 'audio', 'cards');
for (const p of [lessonPath, inputPath]) {
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

const kit = JSON.parse(readFileSync(inputPath, 'utf8'));
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

const clips = [];
function audio(card, n) {
  const name = `${slug}-card${n}`;
  const file = `side-hops/${name}.mp3`;
  const source = join(cardsDir, `${name}.mp3`);
  const record = join(cardsDir, `${name}.record.json`);
  if (!existsSync(source)) throw new Error(`import-kit: missing clip ${source}`);
  if (existsSync(record)) {
    const r = JSON.parse(readFileSync(record, 'utf8'));
    if (r.slug !== slug || r.card !== n || r.title !== card.title || r.text !== card.text ||
        r.engine !== 'kokoro' || r.voice !== 'af_heart' || !r.check?.complete) {
      throw new Error(`import-kit: ${record} does not describe a verified Kokoro af_heart recording of this card`);
    }
  }
  const durationSec = Math.round(mp3Seconds(readFileSync(source)) * 10) / 10;
  if (!durationSec) throw new Error(`import-kit: no audio frames in ${source}`);
  clips.push([source, `public/${file}`]);
  return { file, durationSec };
}

const hops = fromSite
  ? kit.hops.map((h, i) => ({ ...h, audio: audio(h, i + 1) }))
  : kit.asides.map((a, i) => ({
      afterHeading: a.after_heading,
      kind: a.kind,
      title: a.title,
      text: a.text,
      sources: (a.sources ?? []).map((s) => ({ citation: s.citation, url: readerUrl(s.url) })),
      ...picture(a, i + 1),
      audio: audio(a, i + 1),
    })).sort((a, b) => place(a) - place(b));
const now = new Date();
const updated = fromSite ? kit.updated : `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;
const data = { slug, updated, hops };

const media = [...pictures, ...clips];
const manifest = JSON.parse(readFileSync('media-manifest.json', 'utf8'));
const incoming = new Set(media.map(([, destination]) => destination));
const problems = problemsIn(data, {
  fileSlug: slug,
  headings,
  audioFound: (file) => incoming.has(`public/${file}`) || existsSync(`public/${file}`) || Boolean(manifest[file]),
});
if (problems.length) {
  for (const problem of problems) console.error(`import-kit: ${problem}`);
  process.exit(1);
}
mkdirSync('src/data/side-hops', { recursive: true });
mkdirSync('public/side-hops', { recursive: true });
for (const [from, to] of media) copyFileSync(from, to);
writeFileSync(dataPath, JSON.stringify(data, null, 1) + '\n');
console.log(`import-kit: ${slug}: ${hops.length} Side Hops, ${clips.length} card clips, ${pictures.length} picture(s) copied`);

for (const args of [['scripts/production-record.mjs', 'derive'], ['scripts/check-side-hops.mjs']]) {
  const result = spawnSync(process.execPath, args, { stdio: 'inherit' });
  if (result.error) throw result.error;
  if (result.status !== 0) process.exit(result.status ?? 1);
}
