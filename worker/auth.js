// Teacher and student auth for teacher classes. Ported from the grad expedition's
// auth.js (WebCrypto only, no dependencies) and opened up: anyone may register as a
// teacher; students never have passwords.
//
// Ground rules carried over:
//  - The database never holds a usable credential: passwords are PBKDF2 hashes,
//    session tokens, student codes, recovery codes and email links are stored as
//    their SHA-256 hex.
//  - Ten wrong passwords pause an account for fifteen minutes, and an unknown email
//    costs the same PBKDF2 time as a wrong password, so the form neither
//    brute-forces nor tells you which emails exist.
// Cloudflare's runtime caps WebCrypto PBKDF2 at 100k iterations (higher works in
// Node and fails only in production), hence 100k.

const ITERATIONS = 100_000;
const SALT_BYTES = 16;
const HASH_BITS = 256;
export const LOCKOUT_AFTER = 10;
export const LOCKOUT_MS = 15 * 60 * 1000;
export const MIN_PASSWORD_LENGTH = 10;
export const TEACHER_COOKIE = 'bp_teacher';
export const STUDENT_COOKIE = 'bp_student';
export const TEACHER_SESSION_DAYS = 30;
export const STUDENT_SESSION_DAYS = 365;

const enc = new TextEncoder();
const b64 = (bytes) => btoa(String.fromCharCode(...new Uint8Array(bytes)));
const unb64 = (s) => Uint8Array.from(atob(String(s)), (c) => c.charCodeAt(0));

export async function sha256Hex(input) {
  const d = await crypto.subtle.digest('SHA-256', enc.encode(input));
  return [...new Uint8Array(d)].map((b) => b.toString(16).padStart(2, '0')).join('');
}

export function randomToken(bytes = 32) {
  return [...crypto.getRandomValues(new Uint8Array(bytes))].map((x) => x.toString(16).padStart(2, '0')).join('');
}

// Codes people type: no 0/O, 1/I/L, 5/S, 8/B.
const ALPHABET = '234679ACDEFGHJKMNPQRTUVWXYZ';
export function humanCode(len) {
  const a = crypto.getRandomValues(new Uint8Array(len));
  return [...a].map((x) => ALPHABET[x % ALPHABET.length]).join('');
}
export const normCode = (s) => String(s || '').toUpperCase().replace(/[^A-Z0-9]/g, '');

function constantTimeEqual(a, b) {
  if (a.length !== b.length) return false;
  let diff = 0;
  for (let i = 0; i < a.length; i++) diff |= a[i] ^ b[i];
  return diff === 0;
}

async function pbkdf2(password, salt, iterations) {
  const key = await crypto.subtle.importKey('raw', enc.encode(password), 'PBKDF2', false, ['deriveBits']);
  return new Uint8Array(await crypto.subtle.deriveBits({ name: 'PBKDF2', hash: 'SHA-256', salt, iterations }, key, HASH_BITS));
}

export async function hashPassword(password) {
  const salt = crypto.getRandomValues(new Uint8Array(SALT_BYTES));
  return `pbkdf2$${ITERATIONS}$${b64(salt)}$${b64(await pbkdf2(password, salt, ITERATIONS))}`;
}

export async function verifyPassword(password, stored) {
  const [scheme, iterStr, saltB64, hashB64] = String(stored || '').split('$');
  const iterations = parseInt(iterStr, 10);
  if (scheme !== 'pbkdf2' || !(iterations >= ITERATIONS)) return false;
  let salt, expected;
  try { salt = unb64(saltB64); expected = unb64(hashB64); } catch { return false; }
  return constantTimeEqual(await pbkdf2(password, salt, iterations), expected);
}

export const burnPasswordCheck = (password) => pbkdf2(password, new Uint8Array(SALT_BYTES), ITERATIONS);

export function readCookie(request, name) {
  for (const part of (request.headers.get('Cookie') || '').split(';')) {
    const [k, ...v] = part.trim().split('=');
    if (k === name) return v.join('=');
  }
  return null;
}

export function cookie(name, value, request, maxAgeSec) {
  const secure = new URL(request.url).protocol === 'https:' ? '; Secure' : '';
  return `${name}=${value}; Path=/; HttpOnly; SameSite=Lax; Max-Age=${maxAgeSec}${secure}`;
}

export const normalizeEmail = (e) => String(e || '').trim().toLowerCase();
export const validEmail = (e) => /^[^\s@]{1,64}@[^\s@]{1,190}\.[^\s@]{2,}$/.test(e);

// ---- teacher sessions ---------------------------------------------------------
export async function createTeacherSession(db, teacherId) {
  const token = randomToken();
  const now = Date.now();
  await db.prepare('DELETE FROM teacher_sessions WHERE expires_at < ?').bind(now).run().catch(() => {});
  await db.prepare('INSERT INTO teacher_sessions (teacher_id, token_hash, created_at, expires_at) VALUES (?,?,?,?)')
    .bind(teacherId, await sha256Hex(token), now, now + TEACHER_SESSION_DAYS * 86_400_000).run();
  return token;
}

export async function getTeacher(db, request) {
  const token = readCookie(request, TEACHER_COOKIE);
  if (!token || !/^[0-9a-f]{64}$/.test(token)) return null;
  const row = await db.prepare(
    `SELECT t.id, t.email, t.name, t.email_verified_at, s.expires_at
       FROM teacher_sessions s JOIN teachers t ON t.id = s.teacher_id
      WHERE s.token_hash = ? AND s.revoked_at IS NULL`).bind(await sha256Hex(token)).first();
  if (!row || row.expires_at < Date.now()) return null;
  return { id: row.id, email: row.email, name: row.name, verified: !!row.email_verified_at, token };
}

export async function revokeTeacherSessions(db, teacherId) {
  await db.prepare('UPDATE teacher_sessions SET revoked_at=? WHERE teacher_id=? AND revoked_at IS NULL').bind(Date.now(), teacherId).run();
}

const GENERIC = 'That email and password did not match.';

export async function attemptLogin(db, email, password) {
  const t = await db.prepare('SELECT id, password_hash, failed_logins, locked_until FROM teachers WHERE email = ?')
    .bind(normalizeEmail(email)).first();
  const now = Date.now();
  if (!t) { await burnPasswordCheck(password); return { ok: false, status: 401, error: GENERIC }; }
  if (t.locked_until && t.locked_until > now) {
    return { ok: false, status: 429, error: `Too many wrong passwords. Try again in ${Math.ceil((t.locked_until - now) / 60000)} minutes.` };
  }
  if (!(await verifyPassword(password, t.password_hash))) {
    const failed = (t.failed_logins || 0) + 1;
    if (failed >= LOCKOUT_AFTER) await db.prepare('UPDATE teachers SET failed_logins=0, locked_until=? WHERE id=?').bind(now + LOCKOUT_MS, t.id).run();
    else await db.prepare('UPDATE teachers SET failed_logins=? WHERE id=?').bind(failed, t.id).run();
    return { ok: false, status: 401, error: GENERIC };
  }
  await db.prepare('UPDATE teachers SET failed_logins=0, locked_until=NULL, last_active_at=? WHERE id=?').bind(now, t.id).run();
  return { ok: true, id: t.id };
}

// ---- student sessions ----------------------------------------------------------
export async function createStudentSession(db, studentId) {
  const token = randomToken();
  const now = Date.now();
  await db.prepare('INSERT INTO student_sessions (token_hash, student_id, created_at, expires_at) VALUES (?,?,?,?)')
    .bind(await sha256Hex(token), studentId, now, now + STUDENT_SESSION_DAYS * 86_400_000).run();
  return token;
}

export async function getStudent(db, request) {
  const token = readCookie(request, STUDENT_COOKIE);
  if (!token || !/^[0-9a-f]{64}$/.test(token)) return null;
  const row = await db.prepare(
    `SELECT st.id, st.nickname, st.status, st.class_id, c.name AS class_name, c.join_mode, t.name AS teacher_name, s.expires_at
       FROM student_sessions s JOIN students st ON st.id = s.student_id
       JOIN classes c ON c.id = st.class_id JOIN teachers t ON t.id = c.teacher_id
      WHERE s.token_hash = ?`).bind(await sha256Hex(token)).first();
  if (!row || row.expires_at < Date.now()) return null;
  return { ...row, token };
}
