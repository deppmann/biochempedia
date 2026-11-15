import { existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

/**
 * Films are not tracked in git: each is uploaded to R2 by scripts/upload-media.mjs and listed in
 * media-manifest.json, and the Worker serves /explainers/* from R2. A build (on Cloudflare, in CI,
 * in a fresh clone) has no .mp4 files on disk, so build-time code must ask the manifest whether a
 * film exists, never the file system. Build time only.
 */
let manifest: Record<string, { size: number; sha256: string }> | null = null;

/** True when a site path such as "/explainers/home/sizzle/explainer.mp4" is listed in media-manifest.json. */
export function filmInR2(src: string): boolean {
  if (!manifest) {
    const f = join(process.cwd(), 'media-manifest.json');
    manifest = existsSync(f) ? JSON.parse(readFileSync(f, 'utf8')) : {};
  }
  return Boolean(manifest![src.replace(/^\/+/, '')]);
}
