// Which host serves the site, and what every other host of ours answers (src/lib/site-host.mjs).
//
// The worker only sees the paths in run_worker_first (wrangler.jsonc). Today those are media, /api/*
// and /g/*: page requests never reach this code. So:
//
// Phase A (PRIMARY_HOST is biochemistrypedia.com, today): any request of ours that does reach the
// worker on stemhop.com or www.stemhop.com (API, media, group pages) gets a 302 (307 for non-GET) to
// the same path on biochemistrypedia.com, so nobody signs in or syncs there. Pages are NOT redirected
// here while the worker does not run first for them: phase A for whole hosts is a Cloudflare Redirect
// Rule on the stemhop.com zone, and stemhop.com is not attached to the Worker until the switch.
// www.biochemistrypedia.com and plain http keep being served exactly as before.
//
// Phase B needs the worker to run first for every page ("/*", the worker-first-all-paths change);
// scripts/test-host.mjs refuses a phase B setting without it.
//
// Phase B (PRIMARY_HOST is stemhop.com): biochemistrypedia.com, its www, and www.stemhop.com answer
// with a 301 (308 for anything but GET and HEAD) to the same path and query on stemhop.com; the
// browser keeps any #fragment. Three things stay on the old host, because they must run there:
//   /.well-known/webauthn       passkeys made on biochemistrypedia.com keep working on stemhop.com
//                               (WebAuthn Related Origin Requests); served in both phases.
//   /handoff/                   the one-time move of what this browser saved (worker/handoff.js).
//                               A person following an old link (a browser navigation that has not
//                               been through it yet) gets this page first; it forwards at once.
//   /handoff/signin/ and the passkey sign-in API, for browsers without Related Origin Requests.
// Crawlers, link previews, files, feeds and every repeat visit get the plain 301.
//
// Not redirected after the switch: the folders run_worker_first leaves out (/_astro, /pagefind,
// /vendor, /figures, /scientists, /quiz, /flashcards, /helper-data) keep answering 200 on the old
// host, because the worker never sees them. That is deliberate. Old pages still open in a tab, or
// restored from the back/forward cache, load their hashed bundles, search index and card data from
// the old origin; a cross-origin redirect would break the module scripts and the search fetches (no
// CORS). The hand-off pages need none of these files (their style and script are inline). Hotlinked
// figures keep working. To move image-search results for figures to the new address, add a Redirect
// Rule on the biochemistrypedia.com zone for /figures/* and /scientists/* only (301 to the same path
// on stemhop.com): it runs before the worker and costs no requests. Widening run_worker_first to
// these folders instead would bill a worker request for every file a page loads.

import { PRIMARY_HOST, LEGACY_HOST, PASSKEY_RP_ID, KNOWN_HOSTS } from '../src/lib/site-host.mjs';

export const HOSTS = { primary: PRIMARY_HOST, legacy: LEGACY_HOST, rpId: PASSKEY_RP_ID, known: KNOWN_HOSTS };

// Set on the old host once the new host has taken this browser's data (or there was none), so later
// visits are a straight 301. A failed transfer leaves it unset, and the hand-off is offered again.
export const MOVED_COOKIE = 'bp_moved';

export const inFamily = (host, base) => host === base || host.endsWith('.' + base);
/** True once the primary host is no longer the old domain. */
export const switched = (cfg = HOSTS) => !inFamily(cfg.primary, cfg.legacy);
/** The old host's origins, as a browser would send them in Origin (http included: the site answers it). */
export const legacyOrigins = (cfg = HOSTS) =>
  cfg.known.filter((h) => inFamily(h, cfg.legacy)).flatMap((h) => [`https://${h}`, `http://${h}`]);

/** The site's own origin for links we write (emails, Google's redirect_uri). Off our hosts (local, preview), the request's. */
export function siteOrigin(url, cfg = HOSTS) {
  const u = typeof url === 'string' ? new URL(url) : url;
  return cfg.known.includes(u.hostname.toLowerCase()) ? `https://${cfg.primary}` : u.origin;
}

/** The /.well-known/webauthn document: every https origin of ours outside the RP ID's own domain. */
export function webauthnOrigins(cfg = HOSTS) {
  return cfg.known.filter((h) => !inFamily(h, cfg.rpId)).map((h) => `https://${h}`);
}

// What stays on the old host after the switch (see the header).
const OLD_HOST_PATHS = new Set([
  '/handoff/', '/handoff', '/handoff/signin/', '/handoff/signin', '/handoff/done',
  '/api/learner/passkey/login/options', '/api/learner/passkey/login/verify', '/api/learner/bridge/issue',
  '/api/learner/passkey/register/options', '/api/learner/passkey/register/verify',
]);

/** A page address (a directory, an .html file or no extension), as opposed to a file. */
export function isPagePath(pathname) {
  if (pathname.startsWith('/api/')) return false;
  const last = pathname.slice(pathname.lastIndexOf('/') + 1);
  return last === '' || last.endsWith('.html') || !/\.[A-Za-z0-9]{1,8}$/.test(last);
}

const BOT = /bot|crawl|spider|slurp|archiver|facebookexternalhit|embedly|preview|whatsapp|telegram|discord|slack|linkedin|twitter|pinterest|bluesky|mastodon|curl|wget|python|go-http|java\/|okhttp|httpclient|headless|lighthouse/i;

/**
 * A person's browser opening a page (not a crawler, a link preview, or a script).
 * Browsers send Fetch Metadata (Sec-Fetch-*) only to secure origins. On plain http there is none, so
 * there a navigation is recognised by what browsers do send with one: Upgrade-Insecure-Requests: 1
 * and an Accept that asks for HTML (checked in Chrome, 2026-11-15; inferred for Safari and Firefox,
 * which send both on navigations too). Crawlers, curl and link previews still fail the User-Agent test.
 */
export function isBrowserNavigation(request) {
  const h = request.headers;
  const ua = h.get('User-Agent') || '';
  if (!ua || BOT.test(ua)) return false;
  const mode = h.get('Sec-Fetch-Mode');
  if (mode) return mode === 'navigate' && h.get('Sec-Fetch-Dest') === 'document';
  return new URL(request.url).protocol === 'http:' && h.get('Upgrade-Insecure-Requests') === '1' && /\btext\/html\b/.test(h.get('Accept') || '');
}

const hasCookie = (request, name) => new RegExp(`(?:^|;\\s*)${name}=`).test(request.headers.get('Cookie') || '');

/**
 * Decide what a request gets, from its host, path and headers alone.
 *   { kind: 'pass' }                       serve the site as usual
 *   { kind: 'redirect', status, location }
 *   { kind: 'webauthn' }                   the /.well-known/webauthn document
 *   { kind: 'handoff', to }                the old host's hand-off page; `to` is the path to land on
 *   { kind: 'signin' }                     the old host's passkey sign-in page
 *   { kind: 'done', to }                   the old host marks the browser as moved, then forwards
 *   { kind: 'receive' } / { kind: 'merge' } the new host's end of the hand-off
 */
export function route(request, cfg = HOSTS) {
  const url = new URL(request.url);
  const host = url.hostname.toLowerCase();
  const path = url.pathname;
  if (!cfg.known.includes(host)) return { kind: 'pass' };
  if (path === '/.well-known/webauthn' && host === cfg.rpId) return { kind: 'webauthn' };
  const safe = request.method === 'GET' || request.method === 'HEAD';
  const location = `https://${cfg.primary}${path}${url.search}`;

  if (!switched(cfg)) {
    // Phase A. The old domain (apex, www, http) is served as it always was; the new one points here.
    if (host === cfg.primary || inFamily(host, cfg.legacy)) return { kind: 'pass' };
    return { kind: 'redirect', status: safe ? 302 : 307, location };
  }

  // Phase B.
  if (host === cfg.primary) {
    if (path === '/handoff/receive' && request.method === 'POST') return { kind: 'receive' };
    if (path === '/handoff/merge' && request.method === 'POST') return { kind: 'merge' };
    return { kind: 'pass' };
  }
  if (inFamily(host, cfg.legacy)) {
    if (OLD_HOST_PATHS.has(path)) {
      if (path.startsWith('/api/')) return { kind: 'pass' };
      if (!safe) return { kind: 'redirect', status: 308, location };
      if (path.startsWith('/handoff/signin')) return { kind: 'signin' };
      if (path === '/handoff/done') return { kind: 'done', to: url.searchParams.get('to') || '/' };
      return { kind: 'handoff', to: url.searchParams.get('to') || '/' };
    }
    if (request.method === 'GET' && isPagePath(path) && isBrowserNavigation(request) && !hasCookie(request, MOVED_COOKIE)) {
      return { kind: 'handoff', to: path + url.search };
    }
  }
  return { kind: 'redirect', status: safe ? 301 : 308, location };
}

// no-store even on a 301: browsers otherwise keep a 301 for good, and a remembered 301 would skip the
// hand-off page for someone who has not been through it. Crawlers still read 301 as a permanent move.
export const redirectResponse = (status, location) =>
  new Response(null, { status, headers: { Location: location, 'Cache-Control': 'no-store' } });
