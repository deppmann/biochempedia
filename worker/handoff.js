// The one-time hand-off after the site's address changes (phase B in worker/host.js).
//
// Browser storage belongs to one origin: what a learner without an account saved on
// biochemistrypedia.com (progress, notebook, flashcard schedule, film marks, class code, answers)
// cannot be read from stemhop.com. So:
//   1. The old host serves /handoff/ (also as the first answer to a person following an old link).
//      Its script reads this site's keys from localStorage (src/lib/handoff-merge.mjs lists them).
//      Nothing there and not signed in: it marks the browser as moved and forwards at once.
//   2. Otherwise it posts them (multipart/form-data, so the store is not inflated by URL-encoding)
//      as an ordinary top-level form post to the new host's /handoff/receive. A signed-in learner's
//      session is carried too, as a one-time sign-in code (two minutes, single use) from
//      POST /api/learner/bridge/issue on the old host, over https only.
//   3. /handoff/receive accepts the post only with an Origin header naming the old host (a browser
//      sets it; another site cannot), redeems the sign-in code if the post came from an https page,
//      and answers a page that copies every key the new host lacks, asks POST /handoff/merge about the
//      keys both hold (newer data is never overwritten), writes the result, and only then goes back
//      through the old host's /handoff/done, which marks the browser as moved and forwards to the
//      page asked for. Anything failing on the way leaves the browser unmarked, so the hand-off is
//      offered again on the next old link; after one failed try it asks before trying again.
// No database table and no stored copy: the data travels inside the browser's own request and is
// not kept on the server. A second run changes nothing. The old host's copy is left as it was.
import { HOSTS, MOVED_COOKIE, legacyOrigins } from './host.js';
import { mergeStorage, MAX_BYTES, MAX_STORE_CHARS } from '../src/lib/handoff-merge.mjs';
import { json, fail } from './util.js';

/** Only a path on this site: "/x/y?z#w", never "//evil.com" or "https://…". */
export function safePath(to) {
  const s = String(to || '');
  return /^\/(?![\/\\])[^\s]*$/.test(s) && s.length < 600 ? s : '/';
}

// JSON inside <script>: nothing in it can close the tag or break the line.
const embed = (x) => JSON.stringify(x).replace(/</g, '\\u003c').replace(/>/g, '\\u003e').replace(/&/g, '\\u0026').replace(/\u2028/g, '\\u2028').replace(/\u2029/g, '\\u2029');
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');

const STYLE = 'body{font:17px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif;margin:0;color:#1d2433;background:#fbfaf7}main{max-width:34rem;margin:12vh auto;padding:0 1.25rem}h1{font-size:1.35rem;margin:0 0 .6rem}h2{font-size:1.1rem;margin:1.5rem 0 .4rem}p{margin:.5rem 0}button{font:inherit;padding:.55rem 1.1rem;border-radius:.5rem;border:1px solid #1d2433;background:#1d2433;color:#fff;cursor:pointer;margin:.25rem .5rem .25rem 0}button.ghost{background:transparent;color:#1d2433}input[type=text]{font:inherit;padding:.4rem .6rem;width:100%;box-sizing:border-box}label{display:block;margin:.5rem 0}fieldset{border:0;padding:0;margin:1rem 0;min-width:0}legend{padding:0;font-weight:600}.quiet{color:#5b6475;font-size:.92rem}[hidden]{display:none}';

async function sha256b64(text) {
  const d = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(text));
  return btoa(String.fromCharCode(...new Uint8Array(d)));
}

/**
 * A small page with one inline script and one inline style, under a strict CSP that allows exactly
 * those two (by hash), same-origin fetches, and form posts only to `formAction`.
 */
export async function htmlPage(title, body, script, { status = 200, headers = {}, formAction = null, extraHead = '' } = {}) {
  const csp = [
    "default-src 'none'",
    `script-src 'sha256-${await sha256b64(script)}'`,
    `style-src 'sha256-${await sha256b64(STYLE)}'`,
    "connect-src 'self'",
    "img-src 'self' data:",
    `form-action ${formAction || "'none'"}`,
    "base-uri 'none'",
    "frame-ancestors 'none'",
  ].join('; ');
  const h = new Headers({
    'Content-Type': 'text/html; charset=utf-8',
    'Cache-Control': 'no-store',
    'X-Robots-Tag': 'noindex',
    // Not no-referrer: with it a browser sends "Origin: null" on the form post, and /handoff/receive
    // could no longer tell the old host's post from anyone else's.
    'Referrer-Policy': 'strict-origin-when-cross-origin',
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'Content-Security-Policy': csp,
    ...headers,
  });
  const html = `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex">
<title>${esc(title)}</title><link rel="icon" href="data:,">${extraHead}<style>${STYLE}</style>
</head><body><main>${body}</main><script>${script}</script></body></html>`;
  return new Response(html, { status, headers: h });
}

// Shared by the old and new hosts' pages: the keys carried, and where failed tries are counted (on
// the old origin; never carried).
const CLIENT_KEYS = `var KEY=/^(biochempedia:|bcp-arcade:|bcp:|bp-)/,SKIP=/^biochempedia:learner:v1$|^biochempedia:handoff:|:probe$|:test$/,TRIES='biochempedia:handoff:tries';`;

/** The old host's page: read this browser's data, carry it (and a signed-in session) to the new host. */
export function handoffPage(to, cfg = HOSTS) {
  const target = `https://${cfg.primary}`;
  const dest = target + safePath(to);
  const C = embed({ target, to: safePath(to), cookie: MOVED_COOKIE, max: MAX_STORE_CHARS, host: cfg.primary });
  const body = `<h1>Biochemistrypedia has a new address: ${esc(cfg.primary)}</h1>
<p id="msg">Taking you there now.</p>
<p class="quiet" id="more" hidden>What you saved in this browser (your progress, notebook, flashcards and films watched) comes with you. This happens once. It goes from this browser straight to ${esc(cfg.primary)} and is not kept anywhere else.</p>
<p id="ask" hidden><button id="again" type="button">Try again</button><button id="skip" class="ghost" type="button">Continue without it</button><button id="save" class="ghost" type="button" hidden>Download a copy</button></p>
<noscript><p><a href="${esc(dest)}">Continue to ${esc(cfg.primary)}</a></p></noscript>
<form id="f" method="post" enctype="multipart/form-data" action="${esc(target)}/handoff/receive" hidden><input type="hidden" name="data"><input type="hidden" name="to"><input type="hidden" name="signin"></form>`;
  const script = `(async function(){
var C=${C};${CLIENT_KEYS}
var to=C.to+(location.hash||''),$=function(i){return document.getElementById(i)};
function moved(){try{document.cookie=C.cookie+'=1; Path=/; Max-Age=31536000; SameSite=Lax'+(location.protocol==='https:'?'; Secure':'')}catch(e){}}
function go(){location.replace(C.target+to)}
var items={},n=0;try{for(var i=0;i<localStorage.length;i++){var k=localStorage.key(i);if(k&&KEY.test(k)&&!SKIP.test(k)){var v=localStorage.getItem(k);if(v!==null){items[k]=v;n++}}}}catch(e){}
var signin='';
if(location.protocol==='https:'&&/(?:^|;\\s*)bp_signed_in=1/.test(document.cookie)){try{var r=await fetch('/api/learner/bridge/issue',{method:'POST',headers:{'Content-Type':'application/json'},body:'{}',credentials:'same-origin'});if(r.ok){signin=(await r.json()).code||''}}catch(e){}}
if(!n&&!signin){moved();go();return}
var data=JSON.stringify({v:1,items:items});
function send(){try{localStorage.setItem(TRIES,String((+localStorage.getItem(TRIES)||0)+1))}catch(e){}
$('msg').textContent='Bringing what you saved here with you\\u2026';$('more').hidden=false;$('ask').hidden=true;
var f=$('f');f.action=C.target+'/handoff/receive?to='+encodeURIComponent(to);f.elements.data.value=data;f.elements.to.value=to;f.elements.signin.value=signin;f.submit()}
$('skip').onclick=function(){moved();go()};$('again').onclick=send;
$('save').onclick=function(){var a=document.createElement('a');a.href=URL.createObjectURL(new Blob([data],{type:'application/json'}));a.download='biochemistrypedia-saved-in-this-browser.json';document.body.appendChild(a);a.click()};
if(data.length>C.max){$('msg').textContent='What this browser saved is too large to carry over automatically.';$('more').textContent='Download a copy to keep it, then continue to '+C.host+'. Signing in to an account there keeps your progress and notebook in sync from now on.';$('more').hidden=false;$('again').hidden=true;$('save').hidden=false;$('ask').hidden=false;return}
var tries=0;try{tries=+localStorage.getItem(TRIES)||0}catch(e){}
if(tries>0){$('msg').textContent='Last time, what you saved in this browser may not all have come across to '+C.host+'. Trying again is safe: nothing is doubled, and anything newer there is kept.';$('more').hidden=false;$('save').hidden=false;$('ask').hidden=false;return}
send();
})();`;
  return htmlPage('Biochemistrypedia has a new address', body, script, { formAction: target, extraHead: `<link rel="canonical" href="${esc(dest)}">` });
}

/** The old host, after the new host has taken the data: mark this browser as moved, then forward. */
export function doneResponse(request, to, cfg = HOSTS) {
  const secure = new URL(request.url).protocol === 'https:' ? '; Secure' : '';
  const script = `try{localStorage.removeItem('biochempedia:handoff:tries')}catch(e){}location.replace(${embed(`https://${cfg.primary}${safePath(to)}`)});`;
  return htmlPage('Moved', `<p>Done. Taking you to ${esc(cfg.primary)}\u2026</p>`, script, {
    headers: { 'Set-Cookie': `${MOVED_COOKIE}=1; Path=/; Max-Age=31536000; SameSite=Lax${secure}` },
  });
}

const B64 = `function b2a(s){s=s.replace(/-/g,'+').replace(/_/g,'/');while(s.length%4)s+='=';var b=atob(s),u=new Uint8Array(b.length);for(var i=0;i<b.length;i++)u[i]=b.charCodeAt(i);return u.buffer}
function a2b(buf){if(!buf)return undefined;var u=new Uint8Array(buf),s='';for(var i=0;i<u.length;i++)s+=String.fromCharCode(u[i]);return btoa(s).replace(/\\+/g,'-').replace(/\\//g,'_').replace(/=+$/,'')}
async function post(p,b){var r=await fetch('/api/learner'+p,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b||{}),credentials:'same-origin'});return{status:r.status,data:await r.json().catch(function(){return null})}}`;

/**
 * The old host's passkey page, for browsers without WebAuthn Related Origin Requests (where a
 * passkey for biochemistrypedia.com cannot be used, or made, on stemhop.com). Signing in and making
 * a new account both happen here, on the passkey's own domain, which every browser allows; the
 * hand-off page then carries the new session to the new host.
 *
 * The optional role question (worker/learner.js) is asked here too, or an answer given on the new
 * host's /account/ page would be lost on the way. It shows only when the account page sent the
 * visitor here with "#role=..." (which it does only once the server keeps roles), and only after
 * "I am 13 or older" is ticked. The answer rides in the fragment, which browsers never send to a
 * server, so it is in no request log; it reaches the server in the body of the sign-up request.
 */
export function signinPage(url, cfg = HOSTS) {
  const q = new URL(url).searchParams;
  const back = safePath(q.get('to') || '/account/');
  const C = embed({ to: back, host: cfg.primary });
  const name = String(q.get('name') || '').slice(0, 40);
  const body = `<h1>Your passkey, on biochemistrypedia.com</h1>
<p>Passkeys made for this site belong to biochemistrypedia.com. This browser can only use them here, so you sign in (or make your passkey) on this page, then go straight back to ${esc(cfg.primary)}, signed in.</p>
<p><button id="go" type="button">Sign in with a passkey</button></p>
<form id="new"><h2>New here? Make a passkey</h2>
<label>A name to show on your account <input id="nm" type="text" maxlength="40" required value="${esc(name)}" autocomplete="nickname"></label>
<label><input id="age" type="checkbox"> I am 13 or older</label>
<fieldset id="rl" hidden><legend>One optional question: are you here as a student, a parent or a teacher?</legend>
<label><input type="radio" name="role" value="student"> A student</label>
<label><input type="radio" name="role" value="parent"> A parent or guardian</label>
<label><input type="radio" name="role" value="teacher"> A teacher or tutor</label>
<label><input type="radio" name="role" value="" checked> I'd rather not say</label>
<p class="quiet">It is about you, the person making the account: a parent answers as a parent. It is not a question about age or grade. Your answer is counted in totals with no names. It isn't shown to teachers or to anyone else, and you can change or clear it on your account page.</p></fieldset>
<button type="submit">Create account with a passkey</button></form>
<p id="msg" class="quiet" role="status"></p>
<p class="quiet">No passkey? On ${esc(cfg.primary)} you can sign in with Google instead. <a href="https://${esc(cfg.primary)}${esc(back)}">Back to ${esc(cfg.primary)}</a></p>`;
  const script = `(function(){
var C=${C};var msg=document.getElementById('msg');${B64}
var rl=document.getElementById('rl'),age=document.getElementById('age'),rm=/^#role=(student|parent|teacher|)$/.exec(location.hash||'');
if(rm){var pick=rl.querySelector('input[value="'+rm[1]+'"]');if(pick)pick.checked=true;age.addEventListener('change',function(){rl.hidden=!age.checked});rl.hidden=!age.checked}
function role(){if(!rm||rl.hidden)return null;var c=rl.querySelector('input:checked');return c&&c.value?c.value:null}
function back(){msg.textContent='Done. Taking you back\\u2026';location.replace('/handoff/?to='+encodeURIComponent(C.to))}
function oops(e){msg.textContent=(e&&e.name==='NotAllowedError')?'No passkey was chosen. Try again, or sign in with Google on '+C.host+'.':String(e&&e.message||e)}
document.getElementById('go').addEventListener('click',async function(){msg.textContent='';try{
var o=await post('/passkey/login/options');if(o.status!==200)throw new Error((o.data&&o.data.error)||'Sign-in is not available right now.');
var op=o.data.options;var c=await navigator.credentials.get({publicKey:{challenge:b2a(op.challenge),rpId:op.rpId,timeout:op.timeout,userVerification:op.userVerification,allowCredentials:[]}});
var resp={id:c.id,rawId:a2b(c.rawId),type:c.type,clientExtensionResults:c.getClientExtensionResults?c.getClientExtensionResults():{},authenticatorAttachment:c.authenticatorAttachment||undefined,
response:{clientDataJSON:a2b(c.response.clientDataJSON),authenticatorData:a2b(c.response.authenticatorData),signature:a2b(c.response.signature),userHandle:a2b(c.response.userHandle)}};
var v=await post('/passkey/login/verify',{response:resp});if(v.status!==200)throw new Error((v.data&&v.data.error)||'Sign-in failed.');back()}catch(e){oops(e)}});
document.getElementById('new').addEventListener('submit',async function(ev){ev.preventDefault();msg.textContent='';try{
var name=document.getElementById('nm').value.trim();if(!name)throw new Error('Please choose a name.');if(!document.getElementById('age').checked)throw new Error('Accounts are for people 13 and older.');
var o=await post('/passkey/register/options',{displayName:name,age13:true,role:role()});if(o.status!==200)throw new Error((o.data&&o.data.error)||'Sign-up is not available right now.');
var op=o.data.options;var c=await navigator.credentials.create({publicKey:{challenge:b2a(op.challenge),rp:op.rp,user:{id:b2a(op.user.id),name:op.user.name,displayName:op.user.displayName},pubKeyCredParams:op.pubKeyCredParams,timeout:op.timeout,attestation:op.attestation,authenticatorSelection:op.authenticatorSelection,
excludeCredentials:(op.excludeCredentials||[]).map(function(x){return{id:b2a(x.id),type:x.type,transports:x.transports}})}});
var resp={id:c.id,rawId:a2b(c.rawId),type:c.type,clientExtensionResults:c.getClientExtensionResults?c.getClientExtensionResults():{},authenticatorAttachment:c.authenticatorAttachment||undefined,
response:{clientDataJSON:a2b(c.response.clientDataJSON),attestationObject:a2b(c.response.attestationObject),transports:c.response.getTransports?c.response.getTransports():[]}};
var v=await post('/passkey/register/verify',{response:resp});if(v.status!==200)throw new Error((v.data&&v.data.error)||'The passkey could not be made.');back()}catch(e){oops(e)}});
})();`;
  return htmlPage('Your passkey, on biochemistrypedia.com', body, script);
}

/** The new host's end: check where the post came from, carry the session, and hand the data to the page. */
export async function receive(request, env, cfg = HOSTS, redeemSignin = null) {
  const origin = request.headers.get('Origin') || '';
  if (!legacyOrigins(cfg).includes(origin)) {
    return htmlPage('Not moved', '<h1>That did not come from the old address</h1><p><a href="/">Go to the home page</a></p>', '', { status: 403 });
  }
  // The page asked for also rides in the query string (the old host's page puts it there), so a
  // failure before the form is read can still offer the way on.
  const asked = safePath(new URL(request.url).searchParams.get('to'));
  if (Number(request.headers.get('Content-Length') || 0) > MAX_BYTES) return retryPage(origin, asked, 413);
  let form;
  try { form = await request.formData(); } catch { return retryPage(origin, asked, 400); }
  const to = safePath(form.get('to'));
  const data = form.get('data');
  if (typeof data !== 'string' || data.length > MAX_BYTES || data[0] !== '{') return retryPage(origin, to, 400);
  const cookies = [];
  // A sign-in code is honoured only from an https page: on plain http it could have been read or
  // planted on the way. The data is still taken (it is the browser's own, and is only merged).
  const code = String(form.get('signin') || '');
  if (code && redeemSignin && origin.startsWith('https://')) cookies.push(...((await redeemSignin(code)) || []));
  // The store goes into the page untouched except for "<", so a large one costs one pass, not a parse.
  const raw = data.replace(/</g, '\\u003c');
  const script = `(function(){
var C=${embed({ to, done: `${origin}/handoff/done?to=${encodeURIComponent(to)}` })};${CLIENT_KEYS}
var inc={},cur={},both={},w={};
try{inc=JSON.parse(document.getElementById('d').textContent).items||{}}catch(e){location.replace(C.to);return}
Object.keys(inc).forEach(function(k){if(!KEY.test(k)||SKIP.test(k)||typeof inc[k]!=='string')return;var v=null;try{v=localStorage.getItem(k)}catch(e){}
if(v===null)w[k]=inc[k];else if(v!==inc[k]){cur[k]=v;both[k]=inc[k]}});
function put(x){Object.keys(x).forEach(function(k){localStorage.setItem(k,x[k])})}
function finish(){location.replace(C.done)}
function stay(){location.replace(C.to)}
try{put(w)}catch(e){stay();return}
if(!Object.keys(both).length){finish();return}
fetch('/handoff/merge',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({current:cur,incoming:both}),credentials:'same-origin'})
.then(function(r){if(!r.ok)throw 0;return r.json()}).then(function(r){try{put(r.write||{})}catch(e){stay();return}finish()}).catch(stay);
})();`;
  const body = `<h1>Welcome to ${esc(cfg.primary)}</h1><p>Putting what you saved in place\u2026</p><noscript><p><a href="${esc(to)}">Continue</a></p></noscript><script type="application/json" id="d">${raw}</script>`;
  const res = await htmlPage(`Biochemistrypedia at ${cfg.primary}`, body, script);
  for (const c of cookies) res.headers.append('Set-Cookie', c);
  return res;
}

function retryPage(origin, to, status) {
  const old = `${origin}/handoff/?to=${encodeURIComponent(to)}`;
  return htmlPage('Not moved yet', `<h1>Your saved work did not come across this time</h1><p>Nothing was lost: it is still saved in this browser at the old address, and it will be offered again the next time you open an old link.</p><p><a href="${esc(to)}">Continue to the page you asked for</a> or <a href="${esc(old)}">try again now</a>.</p>`, '', { status });
}

/**
 * /handoff/receive threw (worker/index.js catches it): the same way on, so the learner is never left
 * on a bare error page. (A request the platform itself stops, such as one over the CPU limit, still
 * shows Cloudflare's error page; the next old link offers the hand-off again, as nothing was marked.)
 */
export function receiveFailed(request, cfg = HOSTS) {
  const origin = request.headers.get('Origin') || '';
  const old = legacyOrigins(cfg).includes(origin) ? origin : `https://${cfg.legacy}`;
  return retryPage(old, safePath(new URL(request.url).searchParams.get('to')), 500);
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

/** The script added to the new host's /account/ page (see accountNote). */
export function accountScript(cfg = HOSTS) {
  const C = embed({ old: `https://${cfg.legacy}/handoff/signin/`, legacy: cfg.legacy });
  return `(async function(){try{var c=window.PublicKeyCredential&&PublicKeyCredential.getClientCapabilities?await PublicKeyCredential.getClientCapabilities():null;if(c&&c.relatedOrigins===true)return}catch(e){}
var C=${C};
function role(){var f=document.querySelector('[data-role-new][data-role-on]');if(!f)return '';var c=f.querySelector('input:checked');return '#role='+encodeURIComponent(c&&!f.hidden?c.value:'')}
function link(x){return C.old+'?to=%2Faccount%2F'+(x?'&name='+encodeURIComponent(x):'')+role()}
var m=document.querySelector('main');if(m){var p=document.createElement('p');p.className='tc-note bp-ror-note';p.appendChild(document.createTextNode('On this browser, passkeys for this site are used on '+C.legacy+'. Signing in or making one takes you there and straight back. '));var a=document.createElement('a');a.href=link('');a.textContent='Go there';a.addEventListener('click',function(){a.href=link('')});p.appendChild(a);m.prepend(p)}
document.addEventListener('click',function(e){var t=e.target&&e.target.closest&&e.target.closest('[data-pk-login],[data-add-pk]');if(!t)return;e.preventDefault();e.stopImmediatePropagation();
if(t.hasAttribute('data-pk-login')){location.href=link('');return}
var out=document.querySelector('[data-add-err]')||document.querySelector('[data-add-msg]');if(out)out.textContent='This browser cannot add a passkey for this site here. Link Google instead, or add a passkey from a newer browser.'},true);
document.addEventListener('submit',function(e){var f=e.target;if(!f||!f.matches||!f.matches('[data-pk-new]'))return;e.preventDefault();e.stopImmediatePropagation();
var n='';try{n=String(new FormData(f).get('displayName')||'').trim()}catch(x){}location.href=link(n)},true);
})();`;
}

/**
 * After the switch only: on the new host's /account/ page, a browser that cannot use or make a
 * biochemistrypedia.com passkey here (no Related Origin Requests) is sent to the old host's passkey
 * page for signing in and for making a new account, instead of the page's own buttons failing.
 * "Add a passkey" to an account already signed in explains itself and points to Google. Added at the
 * edge, so the built page is the same in both phases. (The site's pages set no CSP.)
 */
export function accountNote(res, cfg = HOSTS) {
  if (typeof HTMLRewriter === 'undefined' || !(res.headers.get('Content-Type') || '').includes('text/html')) return res;
  const js = accountScript(cfg);
  return new HTMLRewriter().on('body', { element(e) { e.append(`<script>${js}</script>`, { html: true }); } }).transform(res);
}
