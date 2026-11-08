// Listen: render Kokoro narration clips for lesson paragraphs, upload them to R2, update the manifest.
//
//   npm run build                                     # writes .listen/<slug>.json (rehype-listen.mjs)
//   node scripts/listen-render.mjs                    # render missing clips, upload new ones, update the manifest
//   node scripts/listen-render.mjs --dry-run          # say what would be rendered and uploaded; change nothing
//   node scripts/listen-render.mjs --only action-potential   # one lesson (repeat --only for more)
//   node scripts/listen-render.mjs --no-upload        # render only; nothing is sent and the manifest is unchanged
//   node scripts/listen-render.mjs --only action-potential --no-upload --local-preview
//        # also copy that lesson's clips to public/listen/<slug>/ and list them in the manifest, so
//        # `astro dev` plays them. LOCAL TEST ONLY: delete public/listen/ (gitignored) and
//        # `git checkout src/data/listen-manifest.json` before committing.
//
// What it does:
//   1. Reads every .listen/<slug>.json ([{hash, text}] in reading order, written during the build).
//   2. Keeps lessons whose frontmatter `course:` is one of POLISHED (only fully polished courses
//      get Kokoro audio; the rest use the reader's device voice).
//   3. Renders each paragraph that has no clip yet with Kokoro-82M voice af_heart
//      (scripts/kokoro_say.py in ~/.venvs/kokoro), at most 5 Kokoro processes at once (Chris's
//      rule, so the Mac stays usable), then converts to mp3 at 64 kbps with ffmpeg:
//      listen-audio/<slug>/<hash>.mp3 (gitignored).
//   4. Uploads clips not yet in the bucket to R2 key listen/<slug>/<hash>.mp3, the same way
//      scripts/upload-media.mjs does (wrangler r2 object put, bucket from wrangler.jsonc, logged
//      with size and sha256 in media-manifest.json so a second run sends nothing twice).
//   5. Writes src/data/listen-manifest.json = { "<slug>": [hash, ...] }: the clips that are in the
//      bucket for the lesson's CURRENT text. The player plays those and uses the device voice for
//      the rest. The worker serves /listen/* from R2 (run_worker_first in wrangler.jsonc).
// Env: KOKORO_PARALLEL (default and maximum 5), KOKORO_PY (default ~/.venvs/kokoro/bin/python),
//      MEDIA_PARALLEL (uploads at once, default 8).
import { spawn, execFile } from 'node:child_process';
import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync, readdirSync, existsSync, mkdirSync, statSync, unlinkSync, copyFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { tmpdir, homedir, cpus } from 'node:os';
import { createInterface } from 'node:readline';

// Chris, 2026-11-06: never the device voice; every levelled-up course gets Kokoro. Lessons with no `course:` are Biochemistry.
import { POLISHED } from './listen-courses.mjs';
const LISTEN_DIR = '.listen';
const AUDIO_DIR = 'listen-audio';
const MANIFEST = 'src/data/listen-manifest.json';
const MEDIA_MANIFEST = 'media-manifest.json';
const KOKORO_PY = process.env.KOKORO_PY || join(homedir(), '.venvs/kokoro/bin/python');
const MAX_KOKORO = 5;

const argv = process.argv.slice(2);
const dry = argv.includes('--dry-run');
const noUpload = argv.includes('--no-upload');
const localPreview = argv.includes('--local-preview');
const only = argv.flatMap((a, i) => (a === '--only' && argv[i + 1] ? [argv[i + 1]] : []));
const parallel = Math.max(1, Math.min(MAX_KOKORO, Number(process.env.KOKORO_PARALLEL || MAX_KOKORO)));

if (!existsSync(LISTEN_DIR)) { console.error('No .listen/ folder. Run `npm run build` first.'); process.exit(1); }

// slug -> course, from each lesson's frontmatter.
const courseOf = {};
for (const dir of readdirSync('src/content/lessons')) {
  const f = join('src/content/lessons', dir, 'lesson.mdx');
  if (!existsSync(f)) continue;
  const fm = (/^---\n([\s\S]*?)\n---/.exec(readFileSync(f, 'utf8')) || [])[1] || '';
  const val = (k) => ((new RegExp(`^${k}:\\s*["']?([^"'\\n]+?)["']?\\s*$`, 'm').exec(fm)) || [])[1];
  courseOf[val('slug') || dir] = val('course') || 'biochemistry';
}

const lessons = readdirSync(LISTEN_DIR)
  .filter((n) => n.endsWith('.json'))
  .map((n) => ({ slug: n.slice(0, -5), blocks: JSON.parse(readFileSync(join(LISTEN_DIR, n), 'utf8')) }))
  .filter((l) => POLISHED.has(courseOf[l.slug]) && (!only.length || only.includes(l.slug)));
for (const s of only) if (!lessons.some((l) => l.slug === s)) console.warn(`--only ${s}: no .listen/${s}.json for a lesson in ${[...POLISHED].join(', ')}`);

const clipPath = (slug, hash) => join(AUDIO_DIR, slug, `${hash}.mp3`);
const keyOf = (slug, hash) => `listen/${slug}/${hash}.mp3`;
const media = existsSync(MEDIA_MANIFEST) ? JSON.parse(readFileSync(MEDIA_MANIFEST, 'utf8')) : {};

const toRender = lessons.flatMap((l) => l.blocks.filter((b) => !existsSync(clipPath(l.slug, b.hash))).map((b) => ({ ...b, slug: l.slug })));
const words = toRender.reduce((n, b) => n + b.text.split(/\s+/).length, 0);
console.log(`${lessons.length} lesson(s), ${lessons.reduce((n, l) => n + l.blocks.length, 0)} paragraphs; ${toRender.length} clip(s) to render (~${words} words, ~${(words / 160).toFixed(0)} min of audio)`);

// ---- 1. Render with Kokoro -------------------------------------------------------------------
const run = (cmd, args) => new Promise((done, fail) => execFile(cmd, args, (err, _o, se) => (err ? fail(new Error(se || err.message)) : done())));
let audioSec = 0, renderWall = 0, rendered = 0, renderFailed = 0;

async function render() {
  if (!toRender.length) return;
  if (!existsSync(KOKORO_PY)) throw new Error(`Kokoro python not found at ${KOKORO_PY}`);
  const n = Math.min(parallel, toRender.length);
  const threads = String(Math.max(1, Math.floor(cpus().length / n)));
  const env = { ...process.env, OMP_NUM_THREADS: threads, MKL_NUM_THREADS: threads, TOKENIZERS_PARALLELISM: 'false', PYTHONWARNINGS: 'ignore' };
  const tmp = join(tmpdir(), `listen-${process.pid}`);
  mkdirSync(tmp, { recursive: true });
  let next = 0;
  const t0 = Date.now();
  const converts = [];
  const worker = () => new Promise((done) => {
    const py = spawn(KOKORO_PY, ['scripts/kokoro_say.py'], { env, stdio: ['pipe', 'pipe', 'pipe'] });
    let current = null, stderr = '';
    py.stderr.on('data', (d) => { stderr = (stderr + d).slice(-2000); });
    const send = () => {
      if (next >= toRender.length) { current = null; py.stdin.end(); return; }
      current = toRender[next++];
      current.wav = join(tmp, `${current.slug}-${current.hash}.wav`);
      py.stdin.write(JSON.stringify({ text: current.text, out: current.wav }) + '\n');
    };
    createInterface({ input: py.stdout }).on('line', (line) => {
      let msg; try { msg = JSON.parse(line); } catch { return; }      // ignore anything Kokoro prints
      if (msg.ready) return send();
      const job = current;
      if (msg.error || !job) { renderFailed += 1; console.error('FAILED', job?.slug, job?.hash, msg.error); return send(); }
      audioSec += msg.seconds;
      const mp3 = clipPath(job.slug, job.hash);
      mkdirSync(join(AUDIO_DIR, job.slug), { recursive: true });
      converts.push(run('ffmpeg', ['-y', '-loglevel', 'error', '-i', job.wav, '-ac', '1', '-codec:a', 'libmp3lame', '-b:a', '64k', mp3])
        .then(() => { unlinkSync(job.wav); rendered += 1; if (rendered % 10 === 0) console.log(`  ${rendered}/${toRender.length} clips`); })
        .catch((e) => { renderFailed += 1; console.error('ffmpeg FAILED', mp3, e.message.split('\n')[0]); }));
      send();
    });
    py.on('close', (code) => {
      if (current) { renderFailed += 1; console.error(`Kokoro exited (${code}) during ${current.slug}/${current.hash}: ${stderr.trim().split('\n').pop()}`); }
      done();
    });
  });
  console.log(`rendering with ${n} Kokoro process(es), ${threads} thread(s) each`);
  await Promise.all(Array.from({ length: n }, worker));
  await Promise.all(converts);
  renderWall = (Date.now() - t0) / 1000;
  console.log(`rendered ${rendered} clip(s), ${(audioSec / 60).toFixed(1)} min of audio, in ${renderWall.toFixed(0)} s` +
    (audioSec ? ` = ${(renderWall / (audioSec / 60)).toFixed(1)} s of rendering per minute of audio` : '') +
    (renderFailed ? `; ${renderFailed} FAILED (run again to retry)` : ''));
}

// ---- 2. Upload to R2, as scripts/upload-media.mjs does ----------------------------------------
const cfg = readFileSync('wrangler.jsonc', 'utf8').replace(/^\s*\/\/.*$/gm, '');
const bucket = (/"bucket_name"\s*:\s*"([^"]+)"/.exec(cfg) || [])[1] || process.env.MEDIA_BUCKET;
const wranglerEnv = { ...process.env }; delete wranglerEnv.CLOUDFLARE_API_TOKEN;   // see upload-media.mjs
const put = (f) => new Promise((done, fail) => {
  execFile('npx', ['wrangler', 'r2', 'object', 'put', `${bucket}/${f.key}`, '--file', resolve(f.p), '--content-type', 'audio/mpeg', '--remote'],
    { cwd: tmpdir(), env: wranglerEnv }, (err, _o, stderr) => (err ? fail(new Error(`${f.key}: ${stderr || err.message}`)) : done()));
});

function pendingUploads() {
  const todo = [];
  for (const l of lessons) for (const b of l.blocks) {
    const p = clipPath(l.slug, b.hash);
    if (!existsSync(p)) continue;
    const key = keyOf(l.slug, b.hash);
    const buf = readFileSync(p);
    const sha = createHash('sha256').update(buf).digest('hex');
    if (media[key]?.sha256 === sha) continue;
    todo.push({ p, key, size: buf.length, sha });
  }
  return todo;
}

async function upload(todo) {
  if (!bucket) throw new Error('No r2_buckets entry in wrangler.jsonc and no MEDIA_BUCKET set.');
  let i = 0, failed = 0;
  const worker = async () => {
    while (i < todo.length) {
      const f = todo[i++];
      try {
        await put(f);
        media[f.key] = { size: f.size, sha256: f.sha };
        writeFileSync(MEDIA_MANIFEST, JSON.stringify(media, null, 1) + '\n');
      } catch (e) { failed += 1; console.error('FAILED', e.message.split('\n')[0]); }
    }
  };
  await Promise.all(Array.from({ length: Number(process.env.MEDIA_PARALLEL || 8) }, worker));
  console.log(`uploaded ${todo.length - failed} of ${todo.length} clip(s) to ${bucket}`);
  if (failed) process.exitCode = 1;
}

// ---- 3. Manifest -------------------------------------------------------------------------------
function writeManifest(extra = () => false) {
  const man = existsSync(MANIFEST) ? JSON.parse(readFileSync(MANIFEST, 'utf8')) : {};
  for (const l of lessons) {
    const hashes = l.blocks.map((b) => b.hash).filter((h) => media[keyOf(l.slug, h)] || extra(l.slug, h));
    if (hashes.length) man[l.slug] = hashes; else delete man[l.slug];
  }
  const sorted = Object.fromEntries(Object.keys(man).sort().map((k) => [k, man[k]]));
  writeFileSync(MANIFEST, JSON.stringify(sorted, null, 1) + '\n');
  console.log(`wrote ${MANIFEST}: ${Object.values(sorted).reduce((n, h) => n + h.length, 0)} clip(s) in ${Object.keys(sorted).length} lesson(s)`);
}

if (dry) {
  for (const b of toRender.slice(0, 20)) console.log('would render', clipPath(b.slug, b.hash), `"${b.text.slice(0, 60)}…"`);
  if (toRender.length > 20) console.log(`  … and ${toRender.length - 20} more`);
  const ups = pendingUploads();
  const uploadable = ups.length + toRender.length;
  console.log(noUpload ? 'would not upload (--no-upload)' : `would upload ${uploadable} clip(s) (${ups.length} already rendered, ${toRender.length} after rendering) to ${bucket} under listen/<slug>/<hash>.mp3, then update ${MANIFEST}`);
  process.exit(0);
}

await render();
if (!noUpload) {
  const todo = pendingUploads();
  if (todo.length) await upload(todo); else console.log('nothing new to upload');
  writeManifest();
} else {
  console.log('not uploading (--no-upload); the manifest lists only clips that are in the bucket');
}
if (localPreview) {
  let copied = 0;
  for (const l of lessons) for (const b of l.blocks) {
    const p = clipPath(l.slug, b.hash);
    if (!existsSync(p)) continue;
    mkdirSync(join('public/listen', l.slug), { recursive: true });
    copyFileSync(p, join('public/listen', l.slug, `${b.hash}.mp3`)); copied += 1;
  }
  writeManifest((slug, h) => existsSync(clipPath(slug, h)));
  console.warn(`LOCAL PREVIEW: copied ${copied} clip(s) to public/listen/ and listed them in ${MANIFEST}.\n` +
    `  Before committing: rm -rf public/listen && git checkout ${MANIFEST}`);
}
// Size of what is on disk, for the record.
const mb = lessons.flatMap((l) => l.blocks.map((b) => clipPath(l.slug, b.hash))).filter(existsSync).reduce((n, p) => n + statSync(p).size, 0) / 1e6;
console.log(`clips on disk for these lessons: ${mb.toFixed(1)} MB`);
