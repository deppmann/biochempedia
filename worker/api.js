// Teacher classes API (step 2a): /api/*
//
// Teachers self-register and own their classes. Students join a class with its code
// and a nickname (or a code from the teacher's roster); no email, no real name, no
// password. Lesson pages report what a joined student does; the teacher reads it as
// a morning brief. No AI model is called anywhere in here, so nothing here costs
// money beyond Cloudflare's own (free-tier) Worker and D1 usage.
//
// Security: HttpOnly SameSite=Lax cookies; every state-changing request must be
// JSON from this site's own origin (blocks cross-site form posts); fixed-window rate
// limits on sign-up, sign-in, join and answers; a teacher can only touch their own
// classes, and a student only their own answers.

import {
  sha256Hex, randomToken, humanCode, normCode, hashPassword, verifyPassword, attemptLogin,
  createTeacherSession, getTeacher, revokeTeacherSessions, createStudentSession, getStudent,
  cookie, readCookie, normalizeEmail, validEmail, TEACHER_COOKIE, STUDENT_COOKIE,
  TEACHER_SESSION_DAYS, STUDENT_SESSION_DAYS, MIN_PASSWORD_LENGTH,
} from './auth.js';
import { DAY, JOIN_MODES, SLUG, json, fail, clean, body, sameOrigin, clientKey, allow, mailOn, sendMail } from './util.js';
import { handleGroups } from './groups.js';

const KINDS = ['quiz', 'idea', 'cer', 'done', 'stuck'];
const MAX_STUDENTS = 200;
const MAX_CLASSES = 40;
const RETENTION_DAYS = 400;   // a class with no activity for this long is deleted
const NICK = /^[\p{L}\p{N} .'\-]{1,24}$/u;

async function emailLink(env, db, request, teacherId, email, purpose) {
  const token = randomToken();
  const now = Date.now();
  await db.prepare('INSERT INTO email_tokens (token_hash, teacher_id, purpose, created_at, expires_at) VALUES (?,?,?,?,?)')
    .bind(await sha256Hex(token), teacherId, purpose, now, now + (purpose === 'verify' ? 7 : 1) * DAY).run();
  const origin = new URL(request.url).origin;
  if (purpose === 'verify') {
    return sendMail(env, email, 'Confirm your email for Biochemistrypedia classes',
      `Confirm this address to finish setting up your teacher account:\n\n${origin}/teach/verify/?t=${token}\n\nThe link works for 7 days. If you did not sign up, ignore this email.`);
  }
  return sendMail(env, email, 'Reset your Biochemistrypedia teacher password',
    `Choose a new password here:\n\n${origin}/teach/reset/?t=${token}\n\nThe link works for 24 hours and only once. If you did not ask for this, ignore this email; your password has not changed.`);
}

// ---- helpers -------------------------------------------------------------------
async function ownClass(db, teacher, id) {
  if (!teacher || !/^[A-Za-z0-9]{6,20}$/.test(id || '')) return null;
  return db.prepare('SELECT * FROM classes WHERE id=? AND teacher_id=?').bind(id, teacher.id).first();
}

async function newClassCode(db) {
  for (let i = 0; i < 8; i++) {
    const code = humanCode(6);
    if (!(await db.prepare('SELECT 1 FROM classes WHERE code=?').bind(code).first())) return code;
  }
  throw new Error('no code');
}

async function purgeStale(db) {
  await db.prepare('DELETE FROM rate_limits WHERE window_start < ?').bind(Date.now() - DAY).run();
  const cutoff = Date.now() - RETENTION_DAYS * DAY;
  const stale = (await db.prepare('SELECT id FROM classes WHERE last_activity_at < ?').bind(cutoff).all()).results || [];
  for (const c of stale) await deleteClass(db, c.id);
}

async function deleteClass(db, id) {
  await db.batch([
    db.prepare('DELETE FROM answers WHERE student_id IN (SELECT id FROM students WHERE class_id=?)').bind(id),
    db.prepare('DELETE FROM student_sessions WHERE student_id IN (SELECT id FROM students WHERE class_id=?)').bind(id),
    db.prepare('DELETE FROM students WHERE class_id=?').bind(id),
    db.prepare('DELETE FROM assignments WHERE class_id=?').bind(id),
    db.prepare('DELETE FROM classes WHERE id=?').bind(id),
  ]);
}

const touchClass = (db, id) => db.prepare('UPDATE classes SET last_activity_at=? WHERE id=?').bind(Date.now(), id).run();

function teacherCookie(token, request) { return cookie(TEACHER_COOKIE, token, request, TEACHER_SESSION_DAYS * 86400); }
function studentCookie(token, request) { return cookie(STUDENT_COOKIE, token, request, STUDENT_SESSION_DAYS * 86400); }

async function studentView(db, s) {
  const assignments = (await db.prepare('SELECT lesson_slug AS slug, due_date AS due FROM assignments WHERE class_id=? ORDER BY due_date IS NULL, due_date, assigned_at').bind(s.class_id).all()).results || [];
  const done = (await db.prepare("SELECT lesson_slug FROM answers WHERE student_id=? AND kind='done'").bind(s.id).all()).results || [];
  return {
    nickname: s.nickname, className: s.class_name, teacherName: s.teacher_name,
    pending: s.status === 'pending', assignments, done: done.map((d) => d.lesson_slug),
  };
}

// ---- the morning brief ------------------------------------------------------------
async function buildBrief(db, cls) {
  const students = (await db.prepare('SELECT id, nickname, status, created_at, last_seen_at FROM students WHERE class_id=? ORDER BY nickname').bind(cls.id).all()).results || [];
  const assignments = (await db.prepare('SELECT lesson_slug AS slug, due_date AS due, assigned_at FROM assignments WHERE class_id=? ORDER BY due_date IS NULL, due_date, assigned_at').bind(cls.id).all()).results || [];
  const rows = (await db.prepare(
    'SELECT a.* FROM answers a JOIN students s ON s.id = a.student_id WHERE s.class_id=?').bind(cls.id).all()).results || [];
  const nick = Object.fromEntries(students.map((s) => [s.id, s.nickname]));
  const active = students.filter((s) => s.status === 'active');
  const today = new Date().toISOString().slice(0, 10);

  const slugs = [...new Set([...assignments.map((a) => a.slug), ...rows.map((r) => r.lesson_slug)])];
  const lessons = {};
  for (const slug of slugs) {
    const mine = rows.filter((r) => r.lesson_slug === slug);
    const started = [...new Set(mine.map((r) => r.student_id))];
    const done = mine.filter((r) => r.kind === 'done').map((r) => r.student_id);
    const ideas = {};
    for (const r of mine.filter((x) => x.kind === 'idea')) {
      let v = {}; try { v = JSON.parse(r.value || '{}'); } catch { /* ignore */ }
      const it = (ideas[r.item] ??= { item: r.item, idea: v.idea || '', answer: v.answer || '', agree: 0, disagree: 0 });
      if (v.idea) it.idea = v.idea;
      if (v.answer) it.answer = v.answer;
      if (v.pick === 'agree') it.agree++; else if (v.pick === 'disagree') it.disagree++;
    }
    const quiz = {};
    for (const r of mine.filter((x) => x.kind === 'quiz')) {
      const q = (quiz[r.item] ??= { item: r.item, n: 0, correct: 0 });
      q.n++; if (r.correct) q.correct++;
    }
    const cers = mine.filter((r) => r.kind === 'cer').map((r) => {
      let v = {}; try { v = JSON.parse(r.value || '{}'); } catch { /* ignore */ }
      return { student: nick[r.student_id], item: r.item, task: v.task || '', claim: v.claim || '', evidence: v.evidence || '', reasoning: v.reasoning || '', at: r.updated_at };
    });
    const stuck = mine.filter((r) => r.kind === 'stuck' && r.value).map((r) => ({ student: nick[r.student_id], text: r.value, at: r.updated_at }));
    lessons[slug] = {
      started: started.length, done: done.length,
      notStarted: active.filter((s) => !started.includes(s.id)).map((s) => s.nickname),
      ideas: Object.values(ideas), quiz: Object.values(quiz).sort((a, b) => a.correct / a.n - b.correct / b.n), cers, stuck,
    };
  }

  // Who needs you: overdue and not started, low first-try accuracy, or a stuck note.
  const needs = [];
  for (const s of active) {
    const mine = rows.filter((r) => r.student_id === s.id);
    const reasons = [];
    const overdue = assignments.filter((a) => a.due && a.due < today && !mine.some((r) => r.lesson_slug === a.slug && r.kind === 'done'));
    if (overdue.length) reasons.push(`${overdue.length} overdue ${overdue.length === 1 ? 'lesson' : 'lessons'} not finished`);
    const q = mine.filter((r) => r.kind === 'quiz');
    const acc = q.length ? q.filter((r) => r.correct).length / q.length : null;
    if (q.length >= 4 && acc < 0.5) reasons.push(`${Math.round(acc * 100)}% right on first tries`);
    const st = mine.filter((r) => r.kind === 'stuck' && r.value);
    if (st.length) reasons.push(`left a stuck note`);
    if (reasons.length) needs.push({ student: s.nickname, reasons });
  }

  return {
    class: { id: cls.id, name: cls.name, code: cls.code, course: cls.course, joinMode: cls.join_mode, groupId: cls.group_id ?? null, shared: !!cls.shared_with_group },
    students: students.map((s) => ({ id: s.id, nickname: s.nickname, status: s.status, joined: s.created_at, lastSeen: s.last_seen_at })),
    assignments, lessons, needs,
  };
}

// ---- router -----------------------------------------------------------------------
export async function handleApi(request, env) {
  const db = env.CLASSES;
  if (!db) return fail(503, 'Teacher classes are not switched on yet.');
  const url = new URL(request.url);
  const path = url.pathname.replace(/\/+$/, '');
  const method = request.method;
  if (method !== 'GET' && !sameOrigin(request)) return fail(403, 'Bad request origin.');

  try {
    // Groups: /api/g/<slug> (public) and /api/groups/* (worker/groups.js).
    const grouped = await handleGroups(request, env, db, path, method, url);
    if (grouped) return grouped;

    // ---------- teacher account ----------
    if (path === '/api/teacher/signup' && method === 'POST') {
      if (!(await allow(db, 'signup:' + (await clientKey(request)), 5, 3600_000))) return fail(429, 'Too many sign-ups from here. Try again in an hour.');
      const b = await body(request);
      const email = normalizeEmail(b?.email);
      const name = clean(b?.name, 60);
      const password = String(b?.password || '');
      if (!validEmail(email)) return fail(400, 'Please enter a valid email address.');
      if (!name) return fail(400, 'Please enter the name your students know you by.');
      if (password.length < MIN_PASSWORD_LENGTH) return fail(400, `Use a password of at least ${MIN_PASSWORD_LENGTH} characters.`);
      if (!b?.agree) return fail(400, 'Please confirm the classroom rules.');
      if (await db.prepare('SELECT 1 FROM teachers WHERE email=?').bind(email).first()) return fail(409, 'An account with that email already exists. Sign in instead.');
      const recovery = `${humanCode(4)}-${humanCode(4)}-${humanCode(4)}`;
      const now = Date.now();
      const res = await db.prepare('INSERT INTO teachers (email, name, password_hash, recovery_hash, created_at, last_active_at) VALUES (?,?,?,?,?,?)')
        .bind(email, name, await hashPassword(password), await sha256Hex(normCode(recovery)), now, now).run();
      const id = res.meta.last_row_id;
      const mailed = await emailLink(env, db, request, id, email, 'verify');
      const token = await createTeacherSession(db, id);
      return json({ ok: true, recoveryCode: recovery, verificationSent: mailed, mailOn: mailOn(env) }, 201, { 'Set-Cookie': teacherCookie(token, request) });
    }

    if (path === '/api/teacher/login' && method === 'POST') {
      if (!(await allow(db, 'login:' + (await clientKey(request)), 40, 3600_000))) return fail(429, 'Too many tries from here. Try again later.');
      const b = await body(request);
      const r = await attemptLogin(db, b?.email, String(b?.password || ''));
      if (!r.ok) return fail(r.status, r.error);
      const token = await createTeacherSession(db, r.id);
      return json({ ok: true }, 200, { 'Set-Cookie': teacherCookie(token, request) });
    }

    if (path === '/api/teacher/logout' && method === 'POST') {
      const t = await getTeacher(db, request);
      if (t) await db.prepare('UPDATE teacher_sessions SET revoked_at=? WHERE token_hash=?').bind(Date.now(), await sha256Hex(t.token)).run();
      return json({ ok: true }, 200, { 'Set-Cookie': cookie(TEACHER_COOKIE, '', request, 0) });
    }

    if (path === '/api/teacher/me' && method === 'GET') {
      const t = await getTeacher(db, request);
      if (!t) return fail(401, 'Not signed in.');
      await purgeStale(db).catch(() => {});
      const classes = (await db.prepare(
        `SELECT c.id, c.name, c.course, c.code, c.join_mode AS joinMode, c.created_at AS created,
                c.group_id AS groupId, c.shared_with_group AS shared,
                (SELECT COUNT(*) FROM students s WHERE s.class_id=c.id AND s.status='active') AS students,
                (SELECT COUNT(*) FROM students s WHERE s.class_id=c.id AND s.status='pending') AS pending,
                (SELECT COUNT(*) FROM assignments a WHERE a.class_id=c.id) AS assignments
           FROM classes c WHERE c.teacher_id=? ORDER BY c.created_at`).bind(t.id).all()).results || [];
      return json({ name: t.name, email: t.email, verified: t.verified, mailOn: mailOn(env), classes });
    }

    if (path === '/api/teacher/resend-verify' && method === 'POST') {
      const t = await getTeacher(db, request);
      if (!t) return fail(401, 'Not signed in.');
      if (!(await allow(db, 'verify:' + t.id, 3, 3600_000))) return fail(429, 'We sent a few already. Check your spam folder, or try again in an hour.');
      return json({ ok: await emailLink(env, db, request, t.id, t.email, 'verify') });
    }

    if (path === '/api/teacher/verify' && method === 'POST') {
      const b = await body(request);
      const h = await sha256Hex(String(b?.token || ''));
      const row = await db.prepare("SELECT teacher_id FROM email_tokens WHERE token_hash=? AND purpose='verify' AND used_at IS NULL AND expires_at > ?").bind(h, Date.now()).first();
      if (!row) return fail(400, 'That link has expired or was already used.');
      await db.batch([
        db.prepare('UPDATE email_tokens SET used_at=? WHERE token_hash=?').bind(Date.now(), h),
        db.prepare('UPDATE teachers SET email_verified_at=? WHERE id=?').bind(Date.now(), row.teacher_id),
      ]);
      return json({ ok: true });
    }

    if (path === '/api/teacher/forgot' && method === 'POST') {
      if (!(await allow(db, 'forgot:' + (await clientKey(request)), 5, 3600_000))) return fail(429, 'Too many requests. Try again in an hour.');
      const b = await body(request);
      const email = normalizeEmail(b?.email);
      const t = validEmail(email) && await db.prepare('SELECT id FROM teachers WHERE email=?').bind(email).first();
      if (t && mailOn(env)) await emailLink(env, db, request, t.id, email, 'reset');
      // Same answer either way, so the form does not reveal who has an account.
      return json({ ok: true, mailOn: mailOn(env) });
    }

    if (path === '/api/teacher/reset' && method === 'POST') {
      if (!(await allow(db, 'reset:' + (await clientKey(request)), 10, 3600_000))) return fail(429, 'Too many tries. Try again in an hour.');
      const b = await body(request);
      const password = String(b?.password || '');
      if (password.length < MIN_PASSWORD_LENGTH) return fail(400, `Use a password of at least ${MIN_PASSWORD_LENGTH} characters.`);
      let teacherId = null;
      let newRecovery = null;
      if (b?.token) {
        const h = await sha256Hex(String(b.token));
        const row = await db.prepare("SELECT teacher_id FROM email_tokens WHERE token_hash=? AND purpose='reset' AND used_at IS NULL AND expires_at > ?").bind(h, Date.now()).first();
        if (!row) return fail(400, 'That link has expired or was already used.');
        await db.prepare('UPDATE email_tokens SET used_at=? WHERE token_hash=?').bind(Date.now(), h).run();
        teacherId = row.teacher_id;
      } else {
        // Recovery code: works once, then a new one is issued.
        const t = await db.prepare('SELECT id, recovery_hash FROM teachers WHERE email=?').bind(normalizeEmail(b?.email)).first();
        if (!t || !t.recovery_hash || t.recovery_hash !== await sha256Hex(normCode(b?.recoveryCode))) return fail(400, 'That email and recovery code did not match.');
        teacherId = t.id;
        newRecovery = `${humanCode(4)}-${humanCode(4)}-${humanCode(4)}`;
        await db.prepare('UPDATE teachers SET recovery_hash=? WHERE id=?').bind(await sha256Hex(normCode(newRecovery)), t.id).run();
      }
      await db.prepare('UPDATE teachers SET password_hash=?, failed_logins=0, locked_until=NULL WHERE id=?').bind(await hashPassword(password), teacherId).run();
      await revokeTeacherSessions(db, teacherId);
      const token = await createTeacherSession(db, teacherId);
      return json({ ok: true, recoveryCode: newRecovery }, 200, { 'Set-Cookie': teacherCookie(token, request) });
    }

    if (path === '/api/teacher/delete' && method === 'POST') {
      const t = await getTeacher(db, request);
      if (!t) return fail(401, 'Not signed in.');
      const b = await body(request);
      const row = await db.prepare('SELECT password_hash FROM teachers WHERE id=?').bind(t.id).first();
      if (!(await verifyPassword(String(b?.password || ''), row.password_hash))) return fail(403, 'Password did not match.');
      const classes = (await db.prepare('SELECT id FROM classes WHERE teacher_id=?').bind(t.id).all()).results || [];
      for (const c of classes) await deleteClass(db, c.id);
      // Groups where this teacher is the only admin: hand them to the longest-standing member,
      // or delete the group if nobody else is in it.
      const solo = (await db.prepare(
        `SELECT gm.group_id FROM group_members gm WHERE gm.teacher_id=? AND gm.role='admin'
           AND (SELECT COUNT(*) FROM group_members x WHERE x.group_id=gm.group_id AND x.role='admin' AND x.status='active') = 1`).bind(t.id).all()).results || [];
      for (const { group_id } of solo) {
        const heir = await db.prepare("SELECT teacher_id FROM group_members WHERE group_id=? AND teacher_id<>? AND status='active' ORDER BY joined_at LIMIT 1").bind(group_id, t.id).first();
        if (heir) await db.prepare("UPDATE group_members SET role='admin' WHERE group_id=? AND teacher_id=?").bind(group_id, heir.teacher_id).run();
        else await db.batch([
          db.prepare('DELETE FROM group_invites WHERE group_id=?').bind(group_id),
          db.prepare('DELETE FROM group_members WHERE group_id=?').bind(group_id),
          db.prepare('DELETE FROM groups WHERE id=?').bind(group_id),
        ]);
      }
      await db.prepare('DELETE FROM group_members WHERE teacher_id=?').bind(t.id).run();
      await db.batch([
        db.prepare('DELETE FROM teacher_sessions WHERE teacher_id=?').bind(t.id),
        db.prepare('DELETE FROM email_tokens WHERE teacher_id=?').bind(t.id),
        db.prepare('DELETE FROM teachers WHERE id=?').bind(t.id),
      ]);
      return json({ ok: true }, 200, { 'Set-Cookie': cookie(TEACHER_COOKIE, '', request, 0) });
    }

    // ---------- classes (teacher) ----------
    if (path === '/api/classes' && method === 'POST') {
      const t = await getTeacher(db, request);
      if (!t) return fail(401, 'Not signed in.');
      const b = await body(request);
      const name = clean(b?.name, 60);
      const course = String(b?.course || '');
      if (!name) return fail(400, 'Give the class a name, like "Biology, period 3".');
      if (!SLUG.test(course)) return fail(400, 'Pick a course.');
      const n = await db.prepare('SELECT COUNT(*) AS n FROM classes WHERE teacher_id=?').bind(t.id).first();
      if (n.n >= MAX_CLASSES) return fail(400, `You can have up to ${MAX_CLASSES} classes.`);
      const id = randomToken(6);
      const now = Date.now();
      // Optionally inside one of the teacher's groups, which supplies the default join mode.
      let groupId = null;
      let groupMode = null;
      if (b?.groupId) {
        const gm = await db.prepare("SELECT g.id, g.default_join_mode FROM group_members m JOIN groups g ON g.id=m.group_id WHERE m.group_id=? AND m.teacher_id=? AND m.status='active'").bind(String(b.groupId), t.id).first();
        if (!gm) return fail(400, 'You are not in that group.');
        groupId = gm.id;
        groupMode = gm.default_join_mode;
      }
      const mode = JOIN_MODES.includes(b?.joinMode) ? b.joinMode : groupMode ?? 'open';
      await db.prepare('INSERT INTO classes (id, teacher_id, name, course, code, join_mode, created_at, last_activity_at, group_id) VALUES (?,?,?,?,?,?,?,?,?)')
        .bind(id, t.id, name, course, await newClassCode(db), mode, now, now, groupId).run();
      return json({ ok: true, id }, 201);
    }

    let m = /^\/api\/classes\/([A-Za-z0-9]+)(?:\/(.*))?$/.exec(path);
    if (m) {
      const t = await getTeacher(db, request);
      if (!t) return fail(401, 'Not signed in.');
      const sub = m[2] || '';
      const cls = await ownClass(db, t, m[1]);
      if (!cls) {
        // A group admin may read (never change) the brief of a class its teacher shared with the group.
        if (sub === 'brief' && method === 'GET' && /^[A-Za-z0-9]{6,20}$/.test(m[1])) {
          const shared = await db.prepare(
            `SELECT c.* FROM classes c JOIN group_members gm ON gm.group_id=c.group_id
              WHERE c.id=? AND c.shared_with_group=1 AND gm.teacher_id=? AND gm.role='admin' AND gm.status='active'`).bind(m[1], t.id).first();
          if (shared) return json({ ...(await buildBrief(db, shared)), viewer: 'group-admin' });
        }
        return fail(404, 'No such class.');
      }

      if (sub === 'brief' && method === 'GET') return json({ ...(await buildBrief(db, cls)), viewer: 'owner' });

      if (sub === '' && method === 'PATCH') {
        const b = await body(request);
        const name = b?.name !== undefined ? clean(b.name, 60) : cls.name;
        const mode = JOIN_MODES.includes(b?.joinMode) ? b.joinMode : cls.join_mode;
        const course = b?.course !== undefined && SLUG.test(String(b.course)) ? String(b.course) : cls.course;
        if (!name) return fail(400, 'The class needs a name.');
        let groupId = cls.group_id;
        if (b?.groupId !== undefined) {
          groupId = b.groupId ? String(b.groupId) : null;
          if (groupId && !(await db.prepare("SELECT 1 FROM group_members WHERE group_id=? AND teacher_id=? AND status='active'").bind(groupId, t.id).first())) return fail(400, 'You are not in that group.');
        }
        const shared = groupId && (b?.shared !== undefined ? !!b.shared : !!cls.shared_with_group) ? 1 : 0;
        await db.prepare('UPDATE classes SET name=?, join_mode=?, course=?, group_id=?, shared_with_group=? WHERE id=?').bind(name, mode, course, groupId, shared, cls.id).run();
        return json({ ok: true });
      }
      if (sub === 'new-code' && method === 'POST') {
        await db.prepare('UPDATE classes SET code=? WHERE id=?').bind(await newClassCode(db), cls.id).run();
        return json({ ok: true });
      }
      if (sub === '' && method === 'DELETE') {
        await deleteClass(db, cls.id);
        return json({ ok: true });
      }
      if (sub === 'assignments' && method === 'PUT') {
        // Replace the whole assignment list: [{slug, due?}]
        const b = await body(request);
        const list = Array.isArray(b?.assignments) ? b.assignments.slice(0, 400) : null;
        if (!list) return fail(400, 'Bad list.');
        const rows = list.filter((a) => SLUG.test(String(a?.slug || ''))).map((a) => ({ slug: a.slug, due: /^\d{4}-\d{2}-\d{2}$/.test(a?.due || '') ? a.due : null }));
        const now = Date.now();
        const old = Object.fromEntries(((await db.prepare('SELECT lesson_slug, assigned_at FROM assignments WHERE class_id=?').bind(cls.id).all()).results || []).map((r) => [r.lesson_slug, r.assigned_at]));
        await db.batch([
          db.prepare('DELETE FROM assignments WHERE class_id=?').bind(cls.id),
          ...rows.map((r) => db.prepare('INSERT INTO assignments (class_id, lesson_slug, due_date, assigned_at) VALUES (?,?,?,?)').bind(cls.id, r.slug, r.due, old[r.slug] ?? now)),
        ]);
        await touchClass(db, cls.id);
        return json({ ok: true, count: rows.length });
      }
      if (sub === 'roster' && method === 'POST') {
        // Teacher-made roster: create students by nickname, return their codes once.
        const b = await body(request);
        const names = (Array.isArray(b?.nicknames) ? b.nicknames : []).map((n) => clean(n, 24)).filter((n) => NICK.test(n)).slice(0, 100);
        const count = await db.prepare('SELECT COUNT(*) AS n FROM students WHERE class_id=?').bind(cls.id).first();
        if (count.n + names.length > MAX_STUDENTS) return fail(400, `A class can have up to ${MAX_STUDENTS} students.`);
        const made = [];
        const skipped = [];
        for (const n of names) {
          if (await db.prepare('SELECT 1 FROM students WHERE class_id=? AND nickname=?').bind(cls.id, n).first()) { skipped.push(n); continue; }
          const code = humanCode(8);
          await db.prepare("INSERT INTO students (class_id, nickname, code_hash, status, created_at) VALUES (?,?,?,'active',?)")
            .bind(cls.id, n, await sha256Hex(code), Date.now()).run();
          made.push({ nickname: n, code });
        }
        return json({ ok: true, made, skipped });
      }
      m = /^students\/(\d+)(?:\/(approve|code))?$/.exec(sub);
      if (m) {
        const st = await db.prepare('SELECT id FROM students WHERE id=? AND class_id=?').bind(m[1], cls.id).first();
        if (!st) return fail(404, 'No such student.');
        if (m[2] === 'approve' && method === 'POST') {
          await db.prepare("UPDATE students SET status='active' WHERE id=?").bind(st.id).run();
          return json({ ok: true });
        }
        if (m[2] === 'code' && method === 'POST') {
          const code = humanCode(8);
          await db.batch([
            db.prepare('UPDATE students SET code_hash=? WHERE id=?').bind(await sha256Hex(code), st.id),
            db.prepare('DELETE FROM student_sessions WHERE student_id=?').bind(st.id),
          ]);
          return json({ ok: true, code });
        }
        if (!m[2] && method === 'DELETE') {
          await db.batch([
            db.prepare('DELETE FROM answers WHERE student_id=?').bind(st.id),
            db.prepare('DELETE FROM student_sessions WHERE student_id=?').bind(st.id),
            db.prepare('DELETE FROM students WHERE id=?').bind(st.id),
          ]);
          return json({ ok: true });
        }
      }
      return fail(404, 'Not found.');
    }

    // ---------- students ----------
    if (path === '/api/join/lookup' && method === 'POST') {
      if (!(await allow(db, 'join:' + (await clientKey(request)), 60, 3600_000))) return fail(429, 'Too many tries. Ask your teacher for help.');
      const b = await body(request);
      const cls = await db.prepare('SELECT c.name, c.join_mode, t.name AS teacher FROM classes c JOIN teachers t ON t.id=c.teacher_id WHERE c.code=?').bind(normCode(b?.code)).first();
      if (!cls) return fail(404, 'No class has that code. Check it with your teacher.');
      return json({ className: cls.name, teacher: cls.teacher, joinMode: cls.join_mode });
    }

    if (path === '/api/join' && method === 'POST') {
      if (!(await allow(db, 'join:' + (await clientKey(request)), 60, 3600_000))) return fail(429, 'Too many tries. Ask your teacher for help.');
      const b = await body(request);
      const cls = await db.prepare('SELECT c.*, t.email_verified_at FROM classes c JOIN teachers t ON t.id=c.teacher_id WHERE c.code=?').bind(normCode(b?.code)).first();
      if (!cls) return fail(404, 'No class has that code. Check it with your teacher.');
      // Once email is switched on, a class opens only after its teacher confirms their address.
      if (mailOn(env) && !cls.email_verified_at) return fail(403, 'Your teacher needs to confirm their email before students can join.');
      let student;
      let newCode = null;
      if (b?.studentCode) {
        // Coming back (another device, or a roster code from the teacher).
        student = await db.prepare('SELECT * FROM students WHERE class_id=? AND code_hash=?').bind(cls.id, await sha256Hex(normCode(b.studentCode))).first();
        if (!student) return fail(404, 'That student code does not match this class. Your teacher can give you a new one.');
      } else {
        if (cls.join_mode === 'roster') return fail(403, 'This class uses student codes from your teacher.');
        if (cls.join_mode === 'locked') return fail(403, 'This class is not taking new students. Ask your teacher.');
        const nickname = clean(b?.nickname, 24);
        if (!NICK.test(nickname)) return fail(400, 'Use 1 to 24 letters, numbers or spaces. A nickname or first name is fine; please not your full name.');
        if (await db.prepare('SELECT 1 FROM students WHERE class_id=? AND nickname=?').bind(cls.id, nickname).first()) {
          return fail(409, 'Someone in this class already has that nickname. If it is you, use your student code instead.');
        }
        const count = await db.prepare('SELECT COUNT(*) AS n FROM students WHERE class_id=?').bind(cls.id).first();
        if (count.n >= MAX_STUDENTS) return fail(403, 'This class is full.');
        newCode = humanCode(8);
        const res = await db.prepare('INSERT INTO students (class_id, nickname, code_hash, status, created_at) VALUES (?,?,?,?,?)')
          .bind(cls.id, nickname, await sha256Hex(newCode), cls.join_mode === 'approve' ? 'pending' : 'active', Date.now()).run();
        student = { id: res.meta.last_row_id };
      }
      await touchClass(db, cls.id);
      const token = await createStudentSession(db, student.id);
      const s = await getStudent(db, new Request(request.url, { headers: { Cookie: `${STUDENT_COOKIE}=${token}` } }));
      return json({ ok: true, studentCode: newCode, ...(await studentView(db, s)) }, 200, { 'Set-Cookie': studentCookie(token, request) });
    }

    if (path === '/api/student/me' && method === 'GET') {
      const s = await getStudent(db, request);
      if (!s) return fail(401, 'Not in a class on this device.');
      await db.prepare('UPDATE students SET last_seen_at=? WHERE id=?').bind(Date.now(), s.id).run();
      const slug = url.searchParams.get('lesson');
      const view = await studentView(db, s);
      if (slug && SLUG.test(slug)) {
        const st = await db.prepare("SELECT value FROM answers WHERE student_id=? AND lesson_slug=? AND kind='stuck'").bind(s.id, slug).first();
        view.stuck = st?.value || '';
      }
      return json(view);
    }

    if (path === '/api/student/answer' && method === 'POST') {
      const s = await getStudent(db, request);
      if (!s) return fail(401, 'Not in a class on this device.');
      if (s.status === 'pending') return fail(403, 'Waiting for your teacher to let you in.');
      if (!(await allow(db, 'ans:' + s.id, 1500, 3600_000))) return fail(429, 'Slow down a little.');
      const b = await body(request);
      const slug = String(b?.lesson || '');
      const kind = String(b?.kind || '');
      const item = clean(b?.item, 80);
      if (!SLUG.test(slug) || !KINDS.includes(kind)) return fail(400, 'Bad answer.');
      const now = Date.now();
      let value = null;
      if (kind === 'quiz') value = String(Number(b?.pick) || 0);
      if (kind === 'idea') value = JSON.stringify({ pick: b?.pick === 'agree' ? 'agree' : 'disagree', idea: clean(b?.idea, 400), answer: b?.answer === 'agree' ? 'agree' : 'disagree' });
      if (kind === 'cer') value = JSON.stringify({ task: clean(b?.task, 600), claim: clean(b?.claim, 1500), evidence: clean(b?.evidence, 1500), reasoning: clean(b?.reasoning, 1500) });
      if (kind === 'stuck') value = clean(b?.text, 1000);
      if (kind === 'done') value = b?.done === false ? null : '1';
      const correct = kind === 'quiz' || kind === 'idea' ? (b?.correct ? 1 : 0) : null;

      if (kind === 'quiz' || kind === 'idea') {
        await db.prepare('INSERT OR IGNORE INTO answers (student_id, lesson_slug, kind, item, value, correct, created_at, updated_at) VALUES (?,?,?,?,?,?,?,?)')
          .bind(s.id, slug, kind, item, value, correct, now, now).run();
      } else if (kind === 'done' && value === null) {
        await db.prepare("DELETE FROM answers WHERE student_id=? AND lesson_slug=? AND kind='done'").bind(s.id, slug).run();
      } else {
        await db.prepare(`INSERT INTO answers (student_id, lesson_slug, kind, item, value, correct, created_at, updated_at) VALUES (?,?,?,?,?,?,?,?)
                          ON CONFLICT (student_id, lesson_slug, kind, item) DO UPDATE SET value=excluded.value, updated_at=excluded.updated_at`)
          .bind(s.id, slug, kind, kind === 'cer' ? item : '', value, null, now, now).run();
      }
      await touchClass(db, s.class_id);
      return json({ ok: true });
    }

    if (path === '/api/student/leave' && method === 'POST') {
      const token = readCookie(request, STUDENT_COOKIE);
      if (token && /^[0-9a-f]{64}$/.test(token)) await db.prepare('DELETE FROM student_sessions WHERE token_hash=?').bind(await sha256Hex(token)).run();
      return json({ ok: true }, 200, { 'Set-Cookie': cookie(STUDENT_COOKIE, '', request, 0) });
    }

    return fail(404, 'Not found.');
  } catch (e) {
    console.error('api error', path, e && e.stack || e);
    return fail(500, 'Something went wrong. Please try again.');
  }
}
