// Upload the site's film files to the R2 bucket the edge worker reads (binding MEDIA).
//
//   node scripts/upload-media.mjs            # upload anything new or changed
//   node scripts/upload-media.mjs --dry-run  # list what would be uploaded
//   node scripts/upload-media.mjs --all      # upload everything again
//
// Each file under public/explainers/ becomes the object "explainers/<...>", the same path it
// has on the site, so no lesson has to change. A manifest of what was uploaded (path, size,
// sha256) is kept in media-manifest.json so a second run sends only what changed. Needs
// `wrangler login` once on this machine (run it from outside this folder). The bucket name is read from wrangler.jsonc.
import { execFile } from 'node:child_process';
import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join, relative, extname, resolve } from 'node:path';
import { tmpdir } from 'node:os';

const ROOT = 'public';
const DIRS = ['explainers'];
const TYPES = { '.mp4': 'video/mp4', '.vtt': 'text/vtt; charset=utf-8', '.jpg': 'image/jpeg', '.png': 'image/png', '.mp3': 'audio/mpeg' };
const MANIFEST = 'media-manifest.json';
const dry = process.argv.includes('--dry-run');
const all = process.argv.includes('--all');

const cfg = readFileSync('wrangler.jsonc', 'utf8').replace(/^\s*\/\/.*$/gm, '');
const bucket = (/"bucket_name"\s*:\s*"([^"]+)"/.exec(cfg) || [])[1] || process.env.MEDIA_BUCKET;
if (!bucket) { console.error('No r2_buckets entry in wrangler.jsonc and no MEDIA_BUCKET set.'); process.exit(1); }

const walk = (d) => readdirSync(d).flatMap((n) => {
  const p = join(d, n);
  return statSync(p).isDirectory() ? walk(p) : [p];
});
const files = DIRS.flatMap((d) => walk(join(ROOT, d))).filter((p) => TYPES[extname(p)]);
const seen = existsSync(MANIFEST) ? JSON.parse(readFileSync(MANIFEST, 'utf8')) : {};
// Find what is new or changed, then upload several files at a time.
const todo = [];
for (const p of files) {
  const key = relative(ROOT, p).split('\\').join('/');
  const buf = readFileSync(p);
  const sha = createHash('sha256').update(buf).digest('hex');
  if (!all && seen[key]?.sha256 === sha) continue;
  todo.push({ p, key, size: buf.length, sha });
}
const sent = todo.length;
const bytes = todo.reduce((n, f) => n + f.size, 0);
// Run wrangler from outside the repo: a project .env with an old CLOUDFLARE_API_TOKEN
// would otherwise override the `wrangler login` session.
const env = { ...process.env }; delete env.CLOUDFLARE_API_TOKEN;
const put = (f) => new Promise((done, fail) => {
  execFile('npx', ['wrangler', 'r2', 'object', 'put', `${bucket}/${f.key}`, '--file', resolve(f.p), '--content-type', TYPES[extname(f.p)], '--remote'],
    { cwd: tmpdir(), env }, (err, _out, stderr) => (err ? fail(new Error(`${f.key}: ${stderr || err.message}`)) : done()));
});
if (dry) for (const f of todo) console.log('would upload', f.key, (f.size / 1e6).toFixed(1) + ' MB');
else {
  let next = 0, failed = 0;
  const worker = async () => {
    while (next < todo.length) {
      const f = todo[next++];
      try {
        await put(f);
        seen[f.key] = { size: f.size, sha256: f.sha };
        writeFileSync(MANIFEST, JSON.stringify(seen, null, 1) + '\n');
        console.log('uploaded', f.key);
      } catch (e) { failed += 1; console.error('FAILED', e.message.split('\n')[0]); }
    }
  };
  await Promise.all(Array.from({ length: Number(process.env.MEDIA_PARALLEL || 8) }, worker));
  if (failed) { console.error(`${failed} upload(s) failed; run again to retry them.`); process.exitCode = 1; }
}
console.log(`${dry ? 'would upload' : 'uploaded'} ${sent} of ${files.length} files, ${(bytes / 1e6).toFixed(0)} MB, to ${bucket}`);
