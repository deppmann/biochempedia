// AI feedback, layer 1 (/api/ai/*, /api/student/feedback, and class routes called from
// api.js). Off unless a teacher stores their own API key and turns AI on for a class.
//
// Rules that hold everywhere here:
//  - Calls bill to the teacher's key. Every call is metered in ai_calls, and a class's
//    monthly cap is checked before each call.
//  - The task and worked answer come from the site's own lesson data (/quiz/<slug>.json),
//    never from the browser. The student's nickname is never sent to a model.
//  - In 'hold' mode feedback waits for the teacher, who can release, edit or discard it.
//    In 'show' mode it goes straight to the student. The teacher sees every exchange.

import { getTeacher, getStudent } from './auth.js';
import { DAY, json, fail, clean, body, allow } from './util.js';
import { PROVIDERS, aiAvailable, encryptKey, decryptKey, complete, costMicro, feedbackPrompt, summaryPrompt, replyPrompt } from './ai.js';

const MODEL_RE = /^[A-Za-z0-9._:\-]{2,80}$/;

const monthStart = () => { const d = new Date(); return Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), 1); };

export async function monthSpendMicro(db, classId) {
  return (await db.prepare('SELECT COALESCE(SUM(cost_micro),0) AS s FROM ai_calls WHERE class_id=? AND created_at>=?').bind(classId, monthStart()).first()).s;
}

async function keyFor(env, db, teacherId, provider) {
  const row = await db.prepare('SELECT key_enc, key_iv FROM teacher_ai_keys WHERE teacher_id=? AND provider=?').bind(teacherId, provider).first();
  if (!row) return null;
  try { return await decryptKey(env, row); } catch { return null; }
}

/** Is AI usable for this class right now? Returns { ok, reason, apiKey } */
async function classAiReady(env, db, cls) {
  if (!aiAvailable(env)) return { ok: false, reason: 'AI feedback is not switched on for the site yet.' };
  if (!cls.ai_enabled || !cls.ai_provider || !cls.ai_model) return { ok: false, reason: 'AI feedback is off for this class.' };
  const apiKey = await keyFor(env, db, cls.teacher_id, cls.ai_provider);
  if (!apiKey) return { ok: false, reason: 'The teacher has no API key for this model.' };
  if ((await monthSpendMicro(db, cls.id)) >= cls.ai_cap_cents * 10_000) return { ok: false, reason: 'This class reached its AI spending limit for the month.' };
  return { ok: true, apiKey };
}

async function meteredCall(env, db, cls, purpose, apiKey, system, user, maxOut) {
  try {
    const r = await complete(env, cls.ai_provider, cls.ai_model, apiKey, system, user, maxOut);
    await db.prepare('INSERT INTO ai_calls (class_id, teacher_id, purpose, provider, model, tokens_in, tokens_out, cost_micro, ok, created_at) VALUES (?,?,?,?,?,?,?,?,1,?)')
      .bind(cls.id, cls.teacher_id, purpose, cls.ai_provider, cls.ai_model, r.tin, r.tout, costMicro(cls.ai_provider, cls.ai_model, r.tin, r.tout), Date.now()).run();
    if (!r.text) throw new Error('The model returned an empty reply.');
    return r.text;
  } catch (e) {
    await db.prepare('INSERT INTO ai_calls (class_id, teacher_id, purpose, provider, model, ok, created_at) VALUES (?,?,?,?,?,0,?)')
      .bind(cls.id, cls.teacher_id, purpose, cls.ai_provider, cls.ai_model, Date.now()).run();
    throw e;
  }
}

async function lessonData(env, request, slug) {
  try {
    const r = await env.ASSETS.fetch(new Request(new URL(`/quiz/${slug}.json`, request.url)));
    return r.ok ? await r.json() : null;
  } catch { return null; }
}

const answerText = (v) => [v.claim && `Claim: ${v.claim}`, v.evidence && `Evidence: ${v.evidence}`, v.reasoning && `Reasoning: ${v.reasoning}`, v.text]
  .filter(Boolean).join('\n');

// ---------------------------------------------------------------------------------
/** /api/ai/* (teacher keys) and /api/student/feedback. Returns null if not ours. */
export async function handleAi(request, env, db, path, method, url) {
  if (path === '/api/student/feedback') {
    const s = await getStudent(db, request);
    if (!s) return fail(401, 'Not in a class on this device.');
    if (method === 'GET') {
      const slug = url.searchParams.get('lesson');
      const rows = (await db.prepare(
        `SELECT id, lesson_slug AS lesson, kind, item, final AS text, source, released_at AS at FROM feedback
          WHERE student_id=? AND status='released' ${slug ? 'AND lesson_slug=?' : ''} ORDER BY released_at DESC LIMIT 50`)
        .bind(...(slug ? [s.id, slug] : [s.id])).all()).results || [];
      if (rows.length) await db.prepare(`UPDATE feedback SET seen_at=? WHERE student_id=? AND status='released' AND seen_at IS NULL ${slug ? 'AND lesson_slug=?' : ''}`).bind(...(slug ? [Date.now(), s.id, slug] : [Date.now(), s.id])).run();
      return json({ feedback: rows });
    }
    if (method !== 'POST') return fail(405, 'Method not allowed.');
    if (s.status === 'pending') return fail(403, 'Waiting for your teacher to let you in.');
    const cls = await db.prepare('SELECT * FROM classes WHERE id=?').bind(s.class_id).first();
    const ready = await classAiReady(env, db, cls);
    if (!ready.ok) return fail(403, ready.reason);
    if (!(await allow(db, `fb:${s.id}`, 15, 3600_000))) return fail(429, 'That is a lot of feedback requests. Try again in an hour.');
    const b = await body(request);
    const slug = String(b?.lesson || '');
    const item = clean(b?.item, 80);
    if (!/^[a-z0-9][a-z0-9-]{0,80}$/.test(slug) || !item) return fail(400, 'Bad request.');
    if (!(await allow(db, `fbi:${s.id}:${slug}:${item}`, 3, DAY))) return fail(429, 'You can ask for feedback on this answer three times a day.');
    const v = { claim: clean(b?.claim, 1500), evidence: clean(b?.evidence, 1500), reasoning: clean(b?.reasoning, 1500), text: clean(b?.text, 4000) };
    const answer = answerText(v);
    if (answer.replace(/\W/g, '').length < 15) return fail(400, 'Write a little more first, then ask for feedback.');
    const lesson = await lessonData(env, request, slug);
    const open = lesson?.open?.find((o) => o.item === item);
    if (!open) return fail(404, 'No feedback is set up for this part of the lesson.');
    const { system, user } = feedbackPrompt({ grade: lesson.grade, kind: open.kind, task: open.task, worked: open.worked, answer });
    let text;
    try { text = await meteredCall(env, db, cls, 'feedback', ready.apiKey, system, user, 2000); }
    catch (e) { return fail(502, `Feedback isn't available right now. ${e.message}`); }
    const now = Date.now();
    const show = cls.ai_mode === 'show';
    await db.prepare(`INSERT INTO feedback (class_id, student_id, lesson_slug, kind, item, answer, draft, final, status, source, model, created_at, released_at)
                      VALUES (?,?,?,?,?,?,?,?,?, 'ai', ?, ?, ?)`)
      .bind(cls.id, s.id, slug, open.kind, item, answer, text, show ? text : null, show ? 'released' : 'held', cls.ai_model, now, show ? now : null).run();
    return json(show ? { status: 'released', text } : { status: 'held' });
  }

  if (!path.startsWith('/api/ai/')) return null;
  const t = await getTeacher(db, request);
  if (!t) return fail(401, 'Not signed in.');

  if (path === '/api/ai/status' && method === 'GET') {
    const keys = (await db.prepare('SELECT provider, last4, created_at AS created FROM teacher_ai_keys WHERE teacher_id=? ORDER BY provider').bind(t.id).all()).results || [];
    return json({ available: aiAvailable(env), keys });
  }

  let m = /^\/api\/ai\/keys\/(gemini|anthropic|openai)(\/test)?$/.exec(path);
  if (m && !m[2] && method === 'PUT') {
    if (!aiAvailable(env)) return fail(503, 'AI feedback is not switched on for the site yet.');
    const b = await body(request);
    const key = String(b?.key || '').trim();
    if (!/^[A-Za-z0-9_\-.]{20,300}$/.test(key)) return fail(400, 'That does not look like an API key. Paste the whole key.');
    const enc = await encryptKey(env, key);
    await db.prepare(`INSERT INTO teacher_ai_keys (teacher_id, provider, key_enc, key_iv, last4, created_at) VALUES (?,?,?,?,?,?)
                      ON CONFLICT (teacher_id, provider) DO UPDATE SET key_enc=excluded.key_enc, key_iv=excluded.key_iv, last4=excluded.last4, created_at=excluded.created_at`)
      .bind(t.id, m[1], enc.key_enc, enc.key_iv, key.slice(-4), Date.now()).run();
    return json({ ok: true });
  }
  if (m && !m[2] && method === 'DELETE') {
    await db.batch([
      db.prepare('DELETE FROM teacher_ai_keys WHERE teacher_id=? AND provider=?').bind(t.id, m[1]),
      db.prepare('UPDATE classes SET ai_enabled=0 WHERE teacher_id=? AND ai_provider=?').bind(t.id, m[1]),
    ]);
    return json({ ok: true });
  }
  if (m && m[2] && method === 'POST') {
    if (!(await allow(db, `aitest:${t.id}`, 10, 3600_000))) return fail(429, 'Too many tests. Try again later.');
    const b = await body(request);
    const model = String(b?.model || '');
    if (!MODEL_RE.test(model)) return fail(400, 'Pick a model.');
    const apiKey = await keyFor(env, db, t.id, m[1]);
    if (!apiKey) return fail(404, 'No key saved for that provider.');
    try {
      const r = await complete(env, m[1], model, apiKey, 'Reply with the single word: ready', 'Are you ready?', 200);
      await db.prepare('INSERT INTO ai_calls (teacher_id, purpose, provider, model, tokens_in, tokens_out, cost_micro, ok, created_at) VALUES (?,?,?,?,?,?,?,1,?)')
        .bind(t.id, 'test', m[1], model, r.tin, r.tout, costMicro(m[1], model, r.tin, r.tout), Date.now()).run();
      return json({ ok: true, reply: r.text.slice(0, 40) });
    } catch (e) { return fail(400, e.message); }
  }
  return fail(404, 'Not found.');
}

// ---------------------------------------------------------------------------------
/** Class-scoped AI routes for the class's own teacher. Returns null if not ours. */
export async function handleClassAi(request, env, db, cls, sub, method) {
  let m = /^feedback\/(\d+)$/.exec(sub);
  if (m && method === 'POST') {
    const b = await body(request);
    const row = await db.prepare('SELECT id, draft, final FROM feedback WHERE id=? AND class_id=?').bind(m[1], cls.id).first();
    if (!row) return fail(404, 'No such feedback.');
    if (b?.action === 'discard') {
      await db.prepare("UPDATE feedback SET status='discarded' WHERE id=?").bind(row.id).run();
      return json({ ok: true });
    }
    if (b?.action === 'release') {
      const text = clean(b?.text ?? row.draft ?? row.final, 3000);
      if (!text) return fail(400, 'The feedback is empty.');
      await db.prepare("UPDATE feedback SET status='released', final=?, released_at=COALESCE(released_at, ?) WHERE id=?").bind(text, Date.now(), row.id).run();
      return json({ ok: true });
    }
    return fail(400, 'Unknown action.');
  }

  if (sub === 'notes' && method === 'POST') {
    // A note the teacher writes (free, no AI): to one student, about one lesson.
    const b = await body(request);
    const text = clean(b?.text, 3000);
    const slug = String(b?.lesson || '');
    const st = await db.prepare('SELECT id FROM students WHERE id=? AND class_id=?').bind(Number(b?.studentId) || 0, cls.id).first();
    if (!st || !text || !/^[a-z0-9][a-z0-9-]{0,80}$/.test(slug)) return fail(400, 'Pick a student and write a note.');
    const now = Date.now();
    await db.prepare(`INSERT INTO feedback (class_id, student_id, lesson_slug, kind, item, final, status, source, created_at, released_at)
                      VALUES (?,?,?,?,?,?,'released','teacher',?,?)`).bind(cls.id, st.id, slug, b?.kind === 'stuck' ? 'stuck' : 'note', '', text, now, now).run();
    return json({ ok: true });
  }

  if ((sub === 'ai/summary' || sub === 'ai/reply') && method === 'POST') {
    const ready = await classAiReady(env, db, cls);
    if (!ready.ok) return fail(403, ready.reason);
    if (!(await allow(db, `aisum:${cls.id}`, 30, 3600_000))) return fail(429, 'Too many requests. Try again in a while.');
    const b = await body(request);
    const slug = String(b?.lesson || '');
    if (!/^[a-z0-9][a-z0-9-]{0,80}$/.test(slug)) return fail(400, 'Bad lesson.');
    const lesson = await lessonData(env, request, slug);
    if (sub === 'ai/summary') {
      const item = clean(b?.item, 80);
      const open = lesson?.open?.find((o) => o.item === item);
      if (!open) return fail(404, 'No written task with that id in this lesson.');
      const rows = (await db.prepare(
        `SELECT a.value FROM answers a JOIN students s ON s.id=a.student_id WHERE s.class_id=? AND a.lesson_slug=? AND a.kind='cer' AND a.item=?`).bind(cls.id, slug, item).all()).results || [];
      const answers = rows.map((r) => { try { return answerText(JSON.parse(r.value)); } catch { return ''; } }).filter((x) => x.trim()).slice(0, 60);
      if (answers.length < 2) return fail(400, 'Summaries need at least two answers.');
      const { system, user } = summaryPrompt({ grade: lesson.grade, task: open.task, answers });
      try { return json({ text: await meteredCall(env, db, cls, 'summary', ready.apiKey, system, user, 3000) }); }
      catch (e) { return fail(502, e.message); }
    }
    const st = await db.prepare(
      `SELECT a.value FROM answers a JOIN students s ON s.id=a.student_id WHERE s.class_id=? AND s.id=? AND a.lesson_slug=? AND a.kind='stuck'`).bind(cls.id, Number(b?.studentId) || 0, slug).first();
    if (!st?.value) return fail(404, 'No stuck note from that student for this lesson.');
    const { system, user } = replyPrompt({ grade: lesson?.grade ?? 13, lesson: lesson?.title ?? slug, note: st.value });
    try { return json({ text: await meteredCall(env, db, cls, 'reply', ready.apiKey, system, user, 1500) }); }
    catch (e) { return fail(502, e.message); }
  }
  return null;
}

/** For the brief: AI settings, spend, and every non-discarded feedback row. */
export async function briefAi(env, db, cls) {
  const rows = (await db.prepare(
    `SELECT f.id, f.lesson_slug AS lesson, f.kind, f.item, f.answer, f.draft, f.final, f.status, f.source, f.created_at AS at, f.released_at AS releasedAt, f.seen_at AS seenAt,
            f.student_id AS studentId, s.nickname AS student
       FROM feedback f JOIN students s ON s.id=f.student_id WHERE f.class_id=? AND f.status<>'discarded' ORDER BY f.created_at DESC LIMIT 400`).bind(cls.id).all()).results || [];
  const hasKey = cls.ai_provider ? !!(await db.prepare('SELECT 1 FROM teacher_ai_keys WHERE teacher_id=? AND provider=?').bind(cls.teacher_id, cls.ai_provider).first()) : false;
  return {
    ai: {
      available: aiAvailable(env), enabled: !!cls.ai_enabled, provider: cls.ai_provider, model: cls.ai_model, mode: cls.ai_mode,
      capCents: cls.ai_cap_cents, spentMicro: await monthSpendMicro(db, cls.id), hasKey,
    },
    feedback: rows,
  };
}

export const studentAiOn = async (env, db, classId) => {
  const cls = await db.prepare('SELECT * FROM classes WHERE id=?').bind(classId).first();
  return cls ? (await classAiReady(env, db, cls)).ok : false;
};

export { PROVIDERS, MODEL_RE };
