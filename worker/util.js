// Shared helpers for the classes and groups APIs (worker/api.js, worker/groups.js).
import { sha256Hex } from './auth.js';

export const DAY = 86_400_000;
export const JOIN_MODES = ['open', 'approve', 'roster', 'locked'];
export const SLUG = /^[a-z0-9][a-z0-9-]{0,80}$/;

export const json = (body, status = 200, headers = {}) =>
  new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', ...headers } });
export const fail = (status, error, extra = {}) => json({ error, ...extra }, status);

export const clean = (s, max) => String(s ?? '').replace(/[\u0000-\u001f\u007f]/g, ' ').trim().slice(0, max);

export async function body(request) {
  try { return await request.json(); } catch { return null; }
}

/** Same-origin JSON only, for anything that changes state. */
export function sameOrigin(request) {
  const origin = request.headers.get('Origin');
  const host = new URL(request.url).origin;
  return (!origin || origin === host) && (request.headers.get('Content-Type') || '').startsWith('application/json');
}

export async function clientKey(request) {
  return sha256Hex(request.headers.get('CF-Connecting-IP') || 'local');
}

/** Fixed-window counter. Returns true while under `limit` per `windowMs`. */
export async function allow(db, key, limit, windowMs) {
  const now = Date.now();
  // Now and then, drop counters older than a day (the privacy page promises it).
  if (Math.random() < 0.02) await db.prepare('DELETE FROM rate_limits WHERE window_start < ?').bind(now - DAY).run();
  const row = await db.prepare('SELECT count, window_start FROM rate_limits WHERE key=?').bind(key).first();
  if (!row || now - row.window_start > windowMs) {
    await db.prepare('INSERT OR REPLACE INTO rate_limits (key, count, window_start) VALUES (?,1,?)').bind(key, now).run();
    return true;
  }
  if (row.count >= limit) return false;
  await db.prepare('UPDATE rate_limits SET count=count+1 WHERE key=?').bind(key).run();
  return true;
}

// ---- email (Resend). Without RESEND_API_KEY nothing is sent and callers fall back. ----
// Mail always comes from the site's own address, never a person's. A teacher's
// invitation shows their name ("Ms. Rivera via Biochemistrypedia") and replies go
// to them; putting their address in From would be blocked as spoofing.
export const mailOn = (env) => !!env.RESEND_API_KEY;

export async function sendMail(env, to, subject, text, { fromName, replyTo } = {}) {
  if (!mailOn(env)) return false;
  const site = env.MAIL_FROM || 'Biochemistrypedia <classes@biochemistrypedia.com>';
  const addr = /<([^>]+)>/.exec(site)?.[1] ?? site;
  const from = fromName ? `${clean(fromName, 60).replace(/[<>"]/g, '')} via Biochemistrypedia <${addr}>` : site;
  try {
    const r = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
      body: JSON.stringify({ from, to: [to], subject, text, ...(replyTo ? { reply_to: replyTo } : {}) }),
    });
    return r.ok;
  } catch { return false; }
}
