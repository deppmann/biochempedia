// Upload the site's film files to the R2 bucket the edge worker reads (binding MEDIA).
//
//   node scripts/upload-media.mjs            # upload anything new or changed
//   node scripts/upload-media.mjs --dry-run  # list what would be uploaded
//   node scripts/upload-media.mjs --all      # upload everything again
//
// Each file under public/explainers/ becomes the object "explainers/<...>", the same path it
// has on the site, so no lesson has to change. A manifest of what was uploaded (path, size,
// sha256) is kept in media-manifest.json so a second run sends only what changed. Needs
// `wrangler login` once on this machine. The bucket name is read from wrangler.jsonc.
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join, relative, extname } from 'node:path';

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
let sent = 0, bytes = 0;
for (const p of files) {
  const key = relative(ROOT, p).split('\\').join('/');
  const buf = readFileSync(p);
  const sha = createHash('sha256').update(buf).digest('hex');
  if (!all && seen[key]?.sha256 === sha) continue;
  sent += 1; bytes += buf.length;
  if (dry) { console.log('would upload', key, (buf.length / 1e6).toFixed(1) + ' MB'); continue; }
  execFileSync('npx', ['wrangler', 'r2', 'object', 'put', `${bucket}/${key}`, '--file', p, '--content-type', TYPES[extname(p)], '--remote'], { stdio: ['ignore', 'ignore', 'inherit'] });
  seen[key] = { size: buf.length, sha256: sha };
  writeFileSync(MANIFEST, JSON.stringify(seen, null, 1) + '\n');
  console.log('uploaded', key);
}
console.log(`${dry ? 'would upload' : 'uploaded'} ${sent} of ${files.length} files, ${(bytes / 1e6).toFixed(0)} MB, to ${bucket}`);
