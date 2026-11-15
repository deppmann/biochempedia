// The site's own address, in one place. Read by the build (astro.config.mjs `site`, and through it
// canonical tags, the sitemap, Open Graph, llms.txt, catalog.json, the agent Markdown, structured
// data, QR codes, Anki exports and share links) and by the Worker (worker/host.js: which host
// serves the site and where every other known host is sent; email links; Google sign-in).
//
// THE SWITCH is the one line below: set PRIMARY_HOST to 'stemhop.com', merge, and Workers Builds
// redeploys. Before that: stemhop.com attached to the Worker as a Custom Domain, the Google console
// listing it, and the worker running first for every page (run_worker_first "/*" in wrangler.jsonc;
// scripts/test-host.mjs fails a phase B setting without it). See the switch-day checklist.
//   PRIMARY_HOST = 'biochemistrypedia.com' (phase A): stemhop.com is sent here by a Redirect Rule on
//     its own zone; any request of ours that reaches the Worker there gets a 302 to the same path here.
//   PRIMARY_HOST = 'stemhop.com' (phase B): biochemistrypedia.com and its www answer with a 301 to the
//     same path on stemhop.com, except the one-time hand-off of browser-only progress (/handoff/)
//     and what passkeys need (/.well-known/webauthn and the sign-in bridge).
// A Worker var cannot reach the Astro build, so this is a module both import, not a wrangler var.
export const PRIMARY_HOST = 'biochemistrypedia.com';

// The site's first domain. After the switch it still serves the hand-off and the passkey pieces.
export const LEGACY_HOST = 'biochemistrypedia.com';

// The relying-party ID every learner passkey is registered to. Never change it: a passkey is bound
// to its RP ID for good. After the switch stemhop.com keeps using it through WebAuthn Related
// Origin Requests (/.well-known/webauthn on this host lists stemhop.com).
export const PASSKEY_RP_ID = 'biochemistrypedia.com';

// Every hostname that is this site. Any other host (localhost, a preview) is served as it is.
export const KNOWN_HOSTS = ['biochemistrypedia.com', 'www.biochemistrypedia.com', 'stemhop.com', 'www.stemhop.com'];

export const SITE_ORIGIN = `https://${PRIMARY_HOST}`;
