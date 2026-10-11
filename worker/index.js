// Biochemistrypedia edge worker.
//
// Everything is served as static assets from dist/ exactly as before; this script
// runs FIRST only for media paths (see run_worker_first in wrangler.jsonc). It adds
// HTTP byte-range support, which the static-asset server does not provide: Safari
// (macOS and iOS) refuses to play <video>, and is unreliable with <audio>, unless
// the server answers "Range: bytes=…" with 206 Partial Content.
const MEDIA_CACHE = 'public, max-age=86400, stale-while-revalidate=604800';

const TYPES = { mp4: 'video/mp4', vtt: 'text/vtt; charset=utf-8', jpg: 'image/jpeg', png: 'image/png', mp3: 'audio/mpeg', m4a: 'audio/mp4', webm: 'video/webm' };

// Media can also live in an R2 bucket bound as MEDIA (see wrangler.jsonc), under the same
// path it has on the site: /explainers/x/explainer.mp4 is the object "explainers/x/explainer.mp4".
// R2 answers byte ranges itself, so nothing is buffered. Returns null when there is no bucket,
// no such object, or anything goes wrong, and the caller falls back to the static assets, so
// a file can be in either place (or both) while media moves out of the repository.
async function fromBucket(request, env) {
  if (!env.MEDIA) return null;
  try {
    const key = decodeURIComponent(new URL(request.url).pathname).replace(/^\/+/, '');
    const head = request.method === 'HEAD';
    const obj = head ? await env.MEDIA.head(key) : await env.MEDIA.get(key, { range: request.headers });
    if (!obj) return null;
    const headers = new Headers();
    obj.writeHttpMetadata(headers);
    if (!headers.has('Content-Type')) headers.set('Content-Type', TYPES[key.split('.').pop().toLowerCase()] || 'application/octet-stream');
    headers.set('ETag', obj.httpEtag);
    headers.set('Accept-Ranges', 'bytes');
    headers.set('Cache-Control', MEDIA_CACHE);
    const r = obj.range;
    if (!head && r && request.headers.has('Range')) {
      const start = r.offset ?? Math.max(0, obj.size - r.suffix);
      const length = r.length ?? obj.size - start;
      headers.set('Content-Range', `bytes ${start}-${start + length - 1}/${obj.size}`);
      headers.set('Content-Length', String(length));
      return new Response(obj.body, { status: 206, headers });
    }
    headers.set('Content-Length', String(obj.size));
    return new Response(head ? null : obj.body, { status: 200, headers });
  } catch {
    return null;
  }
}

export default {
  async fetch(request, env) {
    if (request.method === 'GET' || request.method === 'HEAD') {
      const hit = await fromBucket(request, env);
      if (hit) return hit;
    }
    const res = await env.ASSETS.fetch(request);
    if (res.status !== 200 || (request.method !== 'GET' && request.method !== 'HEAD')) return res;

    const headers = new Headers(res.headers);
    headers.set('Accept-Ranges', 'bytes');
    headers.set('Cache-Control', MEDIA_CACHE);
    const range = request.headers.get('Range');
    const m = range && /^bytes=(\d*)-(\d*)$/.exec(range.trim());
    if (!m || (m[1] === '' && m[2] === '')) {
      return new Response(request.method === 'HEAD' ? null : res.body, { status: 200, headers });
    }

    const body = await res.arrayBuffer();
    const size = body.byteLength;
    let start, end;
    if (m[1] === '') {                 // suffix range: the last N bytes
      start = Math.max(0, size - Number(m[2]));
      end = size - 1;
    } else {
      start = Number(m[1]);
      end = m[2] === '' ? size - 1 : Math.min(Number(m[2]), size - 1);
    }
    if (start >= size || start > end) {
      headers.set('Content-Range', `bytes */${size}`);
      headers.delete('Content-Length');
      return new Response(null, { status: 416, headers });
    }
    headers.set('Content-Range', `bytes ${start}-${end}/${size}`);
    headers.set('Content-Length', String(end - start + 1));
    return new Response(request.method === 'HEAD' ? null : body.slice(start, end + 1), { status: 206, headers });
  },
};
