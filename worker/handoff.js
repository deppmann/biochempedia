// The one-time hand-off after the site's address changes (phase B in worker/host.js).
//
// Browser storage belongs to one origin: what a learner without an account saved on
// biochemistrypedia.com (progress, notebook, flashcard schedule, film marks, class code, answers)
// cannot be read from stemhop.com. So:
//   1. The old host serves /handoff/ (also as the first answer to a person following an old link).
//      Its script reads this site's keys from localStorage (src/lib/handoff-merge.mjs lists them).
//      Nothing there, and not signed in: it sets the bp_moved cookie and forwards at once.
//   2. Otherwise it posts them, as an ordinary top-level form post, to the new host's
//      /handoff/receive. A signed-in learner's session is carried too, as a one-time sign-in code
//      (two minutes, single use) from POST /api/learner/bridge/issue on the old host.
//   3. /handoff/receive accepts the post only with an Origin header naming the old host (a browser
//      sets it; another site cannot), redeems the sign-in code, and answers a page that reads what
//      the new host already holds for those keys, asks POST /handoff/merge what to write (newer data
//      is never overwritten), writes it, and goes on to the page the learner asked for.
// No database table and no stored copy: the data travels inside the browser's own request and is
// not kept on the server. A second run changes nothing. The old host's copy is left as it was.
import { HOSTS, MOVED_COOKIE, legacyOrigins } from './host.js';
import { mergeStorage, carried, MAX_BYTES } from '../src/lib/handoff-merge.mjs';
import { json, fail } from './util.js';

/** Only a path on this site: "/x/y?z#w", never "//evil.com" or "https://…". */
export function safePath(to) {
  const s = String(to || '');
  return /^\/(?![\/\\])[^\s]*$/.test(s) && s.length < 600 ? s : '/';
}

// JSON inside <script>: nothing in it can close the tag or break the line.
const embed = (x) => JSON.stringify(x).replace(/</g, '\\u003c').replace(/>/g, '\\u003e').replace(/&/g, '\\u0026').replace(/\u2028/g, '\\u2028').replace(/\u2029/g, '\\u2029');
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

const PAGE_HEADERS = {
  'Content-Type': 'text/html; charset=utf-8',
  'Cache-Control': 'no-store',
  'X-Robots-Tag': 'noindex',
  // Not no-referrer: with it a browser sends "Origin: null" on the form post, and /handoff/receive
  // could no longer tell the old host's post from anyone else's.
  'Referrer-Policy': 'strict-origin-when-cross-origin',
  'X-Content-Type-Options': 'nosniff',
  'X-Frame-Options': 'DENY',
};

function page(title, body, script, extraHead = '') {
  return `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex">
<title>${esc(title)}</title>${extraHead}
<style>body{font:17px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif;margin:0;color:#1d2433;background:#fbfaf7}main{max-width:34rem;margin:12vh auto;padding:0 1.25rem}h1{font-size:1.35rem;margin:0 0 .6rem}p{margin:.5rem 0}button{font:inherit;padding:.55rem 1.1rem;border-radius:.5rem;border:1px solid #1d2433;background:#1d2433;color:#fff;cursor:pointer}.quiet{color:#5b6475;font-size:.92rem}[hidden]{display:none}</style>
</head><body><main>${body}</main><script>${script}</script></body></html>`;
}

/** The old host's page: read this browser's data, carry it (and a signed-in session) to the new host. */
export function handoffPage(to, cfg = HOSTS) {
  const target = `https://${cfg.primary}`;
  const dest = target + safePath(to);
  const cfgJs = embed({ target, to: safePath(to), cookie: MOVED_COOKIE });
  const body = `<h1>Biochemistrypedia has a new address: ${esc(cfg.primary)}</h1>
<p id="msg">Taking you there now.</p>
<p class="quiet" id="more" hidden>What you saved in this browser (your progress, notebook, flashcards and films watched) comes with you. This happens once, and nothing leaves your browser except to go to the new address.</p>
<noscript><p><a href="${esc(dest)}">Continue to ${esc(cfg.primary)}</a></p></noscript>
<form id="f" method="post" action="${esc(target)}/handoff/receive" hidden><input type="hidden" name="data"><input type="hidden" name="to"><input type="hidden" name="signin"></form>`;
  const script = `(async function(){
var C=${cfgJs};var to=C.to+(location.hash||'');
var KEY=/^(biochempedia:|bcp-arcade:|bcp:|bp-)/,SKIP=/^biochempedia:learner:v1$|:probe$|:test$/;
function moved(){try{document.cookie=C.cookie+'=1; Path=/; Max-Age=31536000; SameSite=Lax'+(location.protocol==='https:'?'; Secure':'')}catch(e){}}
var items={},n=0;try{for(var i=0;i<localStorage.length;i++){var k=localStorage.key(i);if(k&&KEY.test(k)&&!SKIP.test(k)){var v=localStorage.getItem(k);if(v!==null){items[k]=v;n++}}}}catch(e){}
var signin='';
if(/(?:^|;\\s*)bp_signed_in=1/.test(document.cookie)){try{var r=await fetch('/api/learner/bridge/issue',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}',credentials:'same-origin'});if(r.ok){signin=(await r.json()).code||''}}catch(e){}}
moved();
if(!n&&!signin){location.replace(C.target+to);return}
document.getElementById('msg').textContent='Bringing what you saved here with you\\u2026';document.getElementById('more').hidden=false;
var f=document.getElementById('f');f.elements.data.value=JSON.stringify({v:1,items:items});f.elements.to.value=to;f.elements.signin.value=signin;f.submit();
})();`;
  return new Response(page('Biochemistrypedia has a new address', body, script, `<link rel="canonical" href="${esc(dest)}">`), { headers: PAGE_HEADERS });
}

/**
 * The old host's passkey sign-in, for browsers without WebAuthn Related Origin Requests (where a
 * passkey made on biochemistrypedia.com cannot be used on stemhop.com directly). The passkey is
 * used here, on its own domain, which every browser allows; the hand-off page then carries the
 * session to the new host.
 */
export function signinPage(to, cfg = HOSTS) {
  const back = safePath(to || '/account/');
  const cfgJs = embed({ to: back, target: `https://${cfg.primary}` });
  const body = `<h1>Sign in with your passkey</h1>
<p>Your passkey belongs to biochemistrypedia.com, so on this browser it is used here, then you go straight back to ${esc(cfg.primary)}, signed in.</p>
<p><button id="go" type="button">Sign in with a passkey</button></p>
<p id="msg" class="quiet" role="status"></p>
<p class="quiet"><a href="https://${esc(cfg.primary)}${esc(back)}">Back to ${esc(cfg.primary)}</a></p>`;
  const script = `(function(){
var C=${cfgJs};var msg=document.getElementById('msg');
function b2a(s){s=s.replace(/-/g,'+').replace(/_/g,'/');while(s.length%4)s+='=';var b=atob(s),u=new Uint8Array(b.length);for(var i=0;i<b.length;i++)u[i]=b.charCodeAt(i);return u.buffer}
function a2b(buf){if(!buf)return undefined;var u=new Uint8Array(buf),s='';for(var i=0;i<u.length;i++)s+=String.fromCharCode(u[i]);return btoa(s).replace(/\\+/g,'-').replace(/\\//g,'_').replace(/=+$/,'')}
async function post(p,b){var r=await fetch('/api/learner'+p,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b||{}),credentials:'same-origin'});return{status:r.status,data:await r.json().catch(function(){return null})}}
document.getElementById('go').addEventListener('click',async function(){
msg.textContent='';
try{
var o=await post('/passkey/login/options');if(o.status!==200)throw new Error((o.data&&o.data.error)||'Sign-in is not available right now.');
var op=o.data.options;var pk={challenge:b2a(op.challenge),rpId:op.rpId,timeout:op.timeout,userVerification:op.userVerification,allowCredentials:[]};
var c=await navigator.credentials.get({publicKey:pk});
var resp={id:c.id,rawId:a2b(c.rawId),type:c.type,clientExtensionResults:c.getClientExtensionResults?c.getClientExtensionResults():{},authenticatorAttachment:c.authenticatorAttachment||undefined,
response:{clientDataJSON:a2b(c.response.clientDataJSON),authenticatorData:a2b(c.response.authenticatorData),signature:a2b(c.response.signature),userHandle:a2b(c.response.userHandle)}};
var v=await post('/passkey/login/verify',{response:resp});if(v.status!==200)throw new Error((v.data&&v.data.error)||'Sign-in failed.');
msg.textContent='Signed in. Taking you back\\u2026';location.replace('/handoff/?to='+encodeURIComponent(C.to));
}catch(e){msg.textContent=(e&&e.name==='NotAllowedError')?'No passkey was chosen. Try again, or sign in with Google on '+C.target.replace('https://','')+' if your account has it.':String(e&&e.message||e)}
});})();`;
  return new Response(page('Sign in with your passkey', body, script), { headers: PAGE_HEADERS });
}

/** The new host's end: check where the post came from, carry the session, and hand the data to the page. */
export async function receive(request, env, cfg = HOSTS, redeemSignin = null) {
  const origin = request.headers.get('Origin') || '';
  if (!legacyOrigins(cfg).includes(origin)) {
    return new Response(page('Not moved', '<h1>That did not come from the old address</h1><p><a href="/">Go to the home page</a></p>', ''), { status: 403, headers: PAGE_HEADERS });
  }
  if (Number(request.headers.get('Content-Length') || 0) > MAX_BYTES) return retryPage(cfg, '/', 413);
  let form;
  try { form = await request.formData(); } catch { return retryPage(cfg, '/', 400); }
  const to = safePath(form.get('to'));
  let items = {};
  try {
    const d = JSON.parse(String(form.get('data') || '{}'));
    for (const [k, v] of Object.entries(d?.items || {})) if (carried(k) && typeof v === 'string') items[k] = v;
  } catch { return retryPage(cfg, to, 400); }
  const headers = new Headers(PAGE_HEADERS);
  const code = String(form.get('signin') || '');
  if (code && redeemSignin) for (const c of (await redeemSignin(code)) || []) headers.append('Set-Cookie', c);
  const script = `(function(){
var D=${embed({ to, items })};var keys=Object.keys(D.items),cur={};
keys.forEach(function(k){try{var v=localStorage.getItem(k);if(v!==null)cur[k]=v}catch(e){}});
function put(w){Object.keys(w).forEach(function(k){try{localStorage.setItem(k,w[k])}catch(e){}})}
function go(){location.replace(D.to)}
if(!keys.length){go();return}
fetch('/handoff/merge',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({current:cur,incoming:D.items}),credentials:'same-origin'})
.then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(r){put(r.write||{})})
.catch(function(){var w={};keys.forEach(function(k){if(!(k in cur))w[k]=D.items[k]});put(w)})
.then(go,go);
})();`;
  const body = `<h1>Welcome to ${esc(cfg.primary)}</h1><p>Putting what you saved in place\u2026</p><noscript><p><a href="${esc(to)}">Continue</a></p></noscript>`;
  return new Response(page(`Biochemistrypedia at ${cfg.primary}`, body, script), { headers });
}

function retryPage(cfg, to, status) {
  const old = `https://${cfg.legacy}/handoff/?to=${encodeURIComponent(to)}`;
  return new Response(page('Not moved', `<h1>Your saved work did not come across</h1><p>Nothing was lost: it is still in this browser at the old address. <a href="${esc(old)}">Try again</a>, or <a href="${esc(to)}">carry on without it</a>.</p>`, ''), { status, headers: PAGE_HEADERS });
}

/** POST /handoff/merge on the new host: same-origin JSON in, the keys to write out. Stores nothing. */
export async function mergeEndpoint(request) {
  const origin = request.headers.get('Origin');
  if ((origin && origin !== new URL(request.url).origin) || !(request.headers.get('Content-Type') || '').startsWith('application/json')) return fail(403, 'Bad request origin.');
  let text;
  try { text = await request.text(); } catch { return fail(400, 'Bad data.'); }
  if (text.length > MAX_BYTES * 2) return fail(413, 'Too big.');
  let b;
  try { b = JSON.parse(text); } catch { return fail(400, 'Bad data.'); }
  return json(mergeStorage(b?.current, b?.incoming));
}

/**
 * After the switch only: on the new host's /account/ page, a browser that cannot use a
 * biochemistrypedia.com passkey here (no Related Origin Requests) is shown the way to the old
 * host's sign-in page. Added at the edge, so the built page is the same in both phases.
 */
export function accountNote(res, cfg = HOSTS) {
  if (typeof HTMLRewriter === 'undefined' || !(res.headers.get('Content-Type') || '').includes('text/html')) return res;
  const link = `https://${cfg.legacy}/handoff/signin/?to=%2Faccount%2F`;
  const js = `(async function(){try{var c=window.PublicKeyCredential&&PublicKeyCredential.getClientCapabilities?await PublicKeyCredential.getClientCapabilities():null;if(c&&c.relatedOrigins===true)return}catch(e){}
var m=document.querySelector('main');if(!m)return;var p=document.createElement('p');p.className='bp-ror-note';p.style.cssText='margin:1rem 0;padding:.75rem 1rem;border:1px solid currentColor;border-radius:.5rem';
p.innerHTML='Made your passkey before the site moved, and this browser does not offer it here? <a href="${link}">Sign in with it on ${cfg.legacy}</a> and you will come straight back, signed in.';m.prepend(p)})();`;
  return new HTMLRewriter().on('body', { element(e) { e.append(`<script>${js}</script>`, { html: true }); } }).transform(res);
}
