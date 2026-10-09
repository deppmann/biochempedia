// Biochemistrypedia edge worker.
//
// Everything is served as static assets from dist/ exactly as before; this script
// runs FIRST only for media paths (see run_worker_first in wrangler.jsonc). It adds
// HTTP byte-range support, which the static-asset server does not provide: Safari
// (macOS and iOS) refuses to play <video>, and is unreliable with <audio>, unless
// the server answers "Range: bytes=…" with 206 Partial Content.
const MEDIA_CACHE = 'public, max-age=86400, stale-while-revalidate=604800';

export default {
  async fetch(request, env) {
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
