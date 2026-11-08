// Groups API (step 2b): schools, departments or districts with their own page at
// /g/<slug>/ and their own admins.
//
// Who can do what:
//  - Any teacher can make a group (and becomes its admin) or ask to join one.
//  - Admins approve or remove members, promote admins, set the allowed email domain
//    and class defaults, and make invite links. A group always keeps one admin.
//  - Admins see members, classes and counts. They see a class's student answers only
//    if its teacher shares that class with the group (handled in api.js).
//  - The public page shows the group's name, its description and its teachers' display
//    names. Never emails, never students.

import { sha256Hex, randomToken, getTeacher } from './auth.js';
import { DAY, JOIN_MODES, json, fail, clean, body, allow, clientKey, mailOn, sendMail } from './util.js';

const GSLUG = /^[a-z0-9](?:[a-z0-9-]{1,38}[a-z0-9])$/;
const RESERVED = new Set(['admin', 'api', 'teach', 'join', 'new', 'www', 'help', 'about', 'g', 'group', 'groups', 'login', 'signup']);
const DOMAIN = /^(?=.{3,190}$)[a-z0-9-]+(\.[a-z0-9-]+)+$/;
const MAX_GROUPS_MADE = 5;
const INVITE_DAYS = 14;

/** Does this teacher's email satisfy the group's domain rule? Verified addresses only once email is on. */
function domainOk(env, group, teacher) {
  if (!group.email_domain) return true;
  const e = String(teacher.email || '').toLowerCase();
  const d = group.email_domain;
  const matches = e.endsWith('@' + d) || e.endsWith('.' + d);
  return matches && (!mailOn(env) || teacher.verified);
}

async function membership(db, groupId, teacherId) {
  return db.prepare('SELECT role, status FROM group_members WHERE group_id=? AND teacher_id=?').bind(groupId, teacherId).first();
}

async function adminCount(db, groupId) {
  return (await db.prepare("SELECT COUNT(*) AS n FROM group_members WHERE group_id=? AND role='admin' AND status='active'").bind(groupId).first()).n;
}

async function addMember(db, groupId, teacherId, role, status) {
  await db.prepare(`INSERT INTO group_members (group_id, teacher_id, role, status, joined_at) VALUES (?,?,?,?,?)
                    ON CONFLICT (group_id, teacher_id) DO UPDATE SET status=excluded.status,
                    role=CASE WHEN group_members.role='admin' THEN 'admin' ELSE excluded.role END`)
    .bind(groupId, teacherId, role, status, Date.now()).run();
}

export async function handleGroups(request, env, db, path, method, url) {
  // ---------- public page data ----------
  let m = /^\/api\/g\/([a-z0-9-]+)$/.exec(path);
  if (m && method === 'GET') {
    const g = await db.prepare('SELECT id, slug, name, about, email_domain FROM groups WHERE slug=?').bind(m[1]).first();
    if (!g) return fail(404, 'No group has that address.');
    const teachers = (await db.prepare(
      `SELECT t.name FROM group_members gm JOIN teachers t ON t.id=gm.teacher_id
        WHERE gm.group_id=? AND gm.status='active' ORDER BY t.name`).bind(g.id).all()).results || [];
    return json({ slug: g.slug, name: g.name, about: g.about, domain: g.email_domain || null, teachers: teachers.map((t) => t.name) });
  }

  if (path === '/api/groups/invite-info' && method === 'GET') {
    const t = url.searchParams.get('t') || '';
    if (!/^[0-9a-f]{64}$/.test(t)) return fail(400, 'That invitation link is not complete.');
    const inv = await db.prepare(
      `SELECT g.name, g.slug, g.email_domain, i.role, i.expires_at, i.uses, i.max_uses, i.revoked_at
         FROM group_invites i JOIN groups g ON g.id=i.group_id WHERE i.token_hash=?`).bind(await sha256Hex(t)).first();
    const valid = inv && !inv.revoked_at && inv.expires_at > Date.now() && inv.uses < inv.max_uses;
    if (!valid) return fail(410, 'This invitation has expired or was withdrawn. Ask for a new one.');
    return json({ group: inv.name, slug: inv.slug, role: inv.role, domain: inv.email_domain || null });
  }

  // Everything below needs a signed-in teacher.
  if (!path.startsWith('/api/groups')) return null;
  const teacher = await getTeacher(db, request);
  if (!teacher) return fail(401, 'Not signed in.');

  if (path === '/api/groups/mine' && method === 'GET') {
    const rows = (await db.prepare(
      `SELECT g.id, g.slug, g.name, gm.role, gm.status,
              (SELECT COUNT(*) FROM group_members x WHERE x.group_id=g.id AND x.status='active') AS members,
              (SELECT COUNT(*) FROM group_members x WHERE x.group_id=g.id AND x.status='pending') AS pending,
              (SELECT COUNT(*) FROM classes c WHERE c.group_id=g.id) AS classes
         FROM group_members gm JOIN groups g ON g.id=gm.group_id WHERE gm.teacher_id=? ORDER BY g.name`).bind(teacher.id).all()).results || [];
    return json({ groups: rows });
  }

  if (path === '/api/groups' && method === 'POST') {
    if (mailOn(env) && !teacher.verified) return fail(403, 'Confirm your email first, then make a group.');
    const made = await db.prepare('SELECT COUNT(*) AS n FROM groups WHERE created_by=?').bind(teacher.id).first();
    if (made.n >= MAX_GROUPS_MADE) return fail(400, `You can make up to ${MAX_GROUPS_MADE} groups.`);
    const b = await body(request);
    const name = clean(b?.name, 80);
    const slug = String(b?.slug || '').toLowerCase();
    if (!name) return fail(400, 'Give the group a name, like "Albemarle High School Science".');
    if (!GSLUG.test(slug) || RESERVED.has(slug)) return fail(400, 'The address needs 3 to 40 lowercase letters, numbers or dashes.');
    if (await db.prepare('SELECT 1 FROM groups WHERE slug=?').bind(slug).first()) return fail(409, 'That address is taken. Try another.');
    const domain = String(b?.emailDomain || '').trim().toLowerCase().replace(/^@/, '');
    if (domain && !DOMAIN.test(domain)) return fail(400, 'The email domain should look like school.k12.va.us.');
    if (domain && !teacher.email.toLowerCase().endsWith('@' + domain) && !teacher.email.toLowerCase().endsWith('.' + domain)) {
      return fail(400, 'Your own email must be on that domain.');
    }
    const id = randomToken(6);
    await db.batch([
      db.prepare('INSERT INTO groups (id, slug, name, about, email_domain, created_by, created_at) VALUES (?,?,?,?,?,?,?)')
        .bind(id, slug, name, clean(b?.about, 600), domain || null, teacher.id, Date.now()),
      db.prepare("INSERT INTO group_members (group_id, teacher_id, role, status, joined_at) VALUES (?,?,'admin','active',?)").bind(id, teacher.id, Date.now()),
    ]);
    return json({ ok: true, id, slug }, 201);
  }

  if (path === '/api/groups/join' && method === 'POST') {
    if (!(await allow(db, 'gjoin:' + (await clientKey(request)), 30, 3600_000))) return fail(429, 'Too many tries. Try again later.');
    const b = await body(request);
    const h = await sha256Hex(String(b?.token || ''));
    const inv = await db.prepare('SELECT * FROM group_invites WHERE token_hash=?').bind(h).first();
    if (!inv || inv.revoked_at || inv.expires_at < Date.now() || inv.uses >= inv.max_uses) return fail(410, 'This invitation has expired or was withdrawn. Ask for a new one.');
    const g = await db.prepare('SELECT * FROM groups WHERE id=?').bind(inv.group_id).first();
    if (!domainOk(env, g, teacher)) {
      return fail(403, mailOn(env) && !teacher.verified
        ? 'Confirm your email first: this group only accepts confirmed addresses.'
        : `This group only accepts teachers with an @${g.email_domain} email.`);
    }
    await addMember(db, g.id, teacher.id, inv.role, 'active');
    await db.prepare('UPDATE group_invites SET uses=uses+1 WHERE token_hash=?').bind(h).run();
    return json({ ok: true, id: g.id, slug: g.slug, name: g.name });
  }

  m = /^\/api\/groups\/by-slug\/([a-z0-9-]+)\/request$/.exec(path);
  if (m && method === 'POST') {
    const g = await db.prepare('SELECT * FROM groups WHERE slug=?').bind(m[1]).first();
    if (!g) return fail(404, 'No such group.');
    const mem = await membership(db, g.id, teacher.id);
    if (mem) return json({ ok: true, status: mem.status });
    if (!domainOk(env, g, teacher)) {
      return fail(403, mailOn(env) && !teacher.verified
        ? 'Confirm your email first: this group only accepts confirmed addresses.'
        : `This group only accepts teachers with an @${g.email_domain} email.`);
    }
    await addMember(db, g.id, teacher.id, 'teacher', 'pending');
    return json({ ok: true, status: 'pending' });
  }

  m = /^\/api\/groups\/([A-Za-z0-9]+)(?:\/(.*))?$/.exec(path);
  if (!m) return fail(404, 'Not found.');
  const g = await db.prepare('SELECT * FROM groups WHERE id=?').bind(m[1]).first();
  if (!g) return fail(404, 'No such group.');
  const mem = await membership(db, g.id, teacher.id);
  if (!mem || mem.status !== 'active') return fail(404, 'No such group.');
  const isAdmin = mem.role === 'admin';
  const sub = m[2] || '';

  if (sub === '' && method === 'GET') {
    const members = (await db.prepare(
      `SELECT t.id, t.name, t.email, gm.role, gm.status, gm.joined_at AS joined
         FROM group_members gm JOIN teachers t ON t.id=gm.teacher_id WHERE gm.group_id=? ORDER BY gm.status DESC, t.name`).bind(g.id).all()).results || [];
    const classes = (await db.prepare(
      `SELECT c.id, c.name, c.course, c.shared_with_group AS shared, t.name AS teacher, c.teacher_id AS teacherId,
              (SELECT COUNT(*) FROM students s WHERE s.class_id=c.id AND s.status='active') AS students,
              (SELECT COUNT(*) FROM assignments a WHERE a.class_id=c.id) AS assignments
         FROM classes c JOIN teachers t ON t.id=c.teacher_id WHERE c.group_id=? ORDER BY t.name, c.name`).bind(g.id).all()).results || [];
    const out = {
      id: g.id, slug: g.slug, name: g.name, about: g.about, emailDomain: g.email_domain || '', defaultJoinMode: g.default_join_mode,
      role: mem.role, me: teacher.id, mailOn: mailOn(env),
      // Teachers in the group see each other's names; admins also see emails and requests.
      members: members.filter((x) => isAdmin || x.status === 'active').map((x) => ({ id: x.id, name: x.name, email: isAdmin ? x.email : undefined, role: x.role, status: x.status, joined: x.joined })),
      classes: classes.filter((c) => isAdmin || c.teacherId === teacher.id),
    };
    if (isAdmin) {
      out.invites = ((await db.prepare(
        'SELECT token_hash, role, note, uses, max_uses, expires_at FROM group_invites WHERE group_id=? AND revoked_at IS NULL AND expires_at > ? ORDER BY created_at DESC').bind(g.id, Date.now()).all()).results || [])
        .map((i) => ({ id: i.token_hash.slice(0, 16), role: i.role, note: i.note, uses: i.uses, maxUses: i.max_uses, expires: i.expires_at }));
    }
    return json(out);
  }

  if (sub === 'leave' && method === 'POST') {
    if (isAdmin && (await adminCount(db, g.id)) <= 1) return fail(400, 'You are the only admin. Make someone else an admin first, or delete the group.');
    await db.batch([
      db.prepare('DELETE FROM group_members WHERE group_id=? AND teacher_id=?').bind(g.id, teacher.id),
      db.prepare('UPDATE classes SET group_id=NULL, shared_with_group=0 WHERE group_id=? AND teacher_id=?').bind(g.id, teacher.id),
    ]);
    return json({ ok: true });
  }

  if (!isAdmin) return fail(403, 'Only the group\'s admins can do that.');

  if (sub === '' && method === 'PATCH') {
    const b = await body(request);
    const name = b?.name !== undefined ? clean(b.name, 80) : g.name;
    const about = b?.about !== undefined ? clean(b.about, 600) : g.about;
    const slug = b?.slug !== undefined ? String(b.slug).toLowerCase() : g.slug;
    const mode = JOIN_MODES.includes(b?.defaultJoinMode) ? b.defaultJoinMode : g.default_join_mode;
    let domain = b?.emailDomain !== undefined ? String(b.emailDomain).trim().toLowerCase().replace(/^@/, '') : (g.email_domain || '');
    if (!name) return fail(400, 'The group needs a name.');
    if (!GSLUG.test(slug) || RESERVED.has(slug)) return fail(400, 'The address needs 3 to 40 lowercase letters, numbers or dashes.');
    if (slug !== g.slug && await db.prepare('SELECT 1 FROM groups WHERE slug=?').bind(slug).first()) return fail(409, 'That address is taken.');
    if (domain && !DOMAIN.test(domain)) return fail(400, 'The email domain should look like school.k12.va.us.');
    await db.prepare('UPDATE groups SET name=?, about=?, slug=?, email_domain=?, default_join_mode=? WHERE id=?')
      .bind(name, about, slug, domain || null, mode, g.id).run();
    return json({ ok: true, slug });
  }

  if (sub === '' && method === 'DELETE') {
    await db.batch([
      db.prepare('UPDATE classes SET group_id=NULL, shared_with_group=0 WHERE group_id=?').bind(g.id),
      db.prepare('DELETE FROM group_invites WHERE group_id=?').bind(g.id),
      db.prepare('DELETE FROM group_members WHERE group_id=?').bind(g.id),
      db.prepare('DELETE FROM groups WHERE id=?').bind(g.id),
    ]);
    return json({ ok: true });
  }

  if (sub === 'invites' && method === 'POST') {
    if (!(await allow(db, 'ginv:' + teacher.id, 30, 3600_000))) return fail(429, 'That is a lot of invitations. Try again in an hour.');
    const b = await body(request);
    const role = b?.role === 'admin' ? 'admin' : 'teacher';
    const token = randomToken();
    const now = Date.now();
    await db.prepare('INSERT INTO group_invites (token_hash, group_id, role, created_by, created_at, expires_at, max_uses, note) VALUES (?,?,?,?,?,?,?,?)')
      .bind(await sha256Hex(token), g.id, role, teacher.id, now, now + INVITE_DAYS * DAY, role === 'admin' ? 3 : 50, clean(b?.note, 120)).run();
    const link = `${new URL(request.url).origin}/teach/invite/?t=${token}`;
    // Optional emails: from the site's address, with the inviting teacher's name and reply-to.
    const emails = (Array.isArray(b?.emails) ? b.emails : []).map((e) => String(e).trim().toLowerCase()).filter((e) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e)).slice(0, 30);
    let sent = 0;
    for (const to of emails) {
      const ok = await sendMail(env, to, `${teacher.name} invited you to ${g.name} on Biochemistrypedia`,
        `${teacher.name} invited you to join ${g.name}, a group of teachers using free Biochemistrypedia classes.\n\nJoin here (the link works for ${INVITE_DAYS} days):\n${link}\n\nYou'll need a free teacher account; the link walks you through it.\n\nReplies to this email go to ${teacher.name}.`,
        { fromName: teacher.name, replyTo: teacher.email });
      if (ok) sent++;
    }
    return json({ ok: true, link, sent, mailOn: mailOn(env) });
  }

  m = /^invites\/([0-9a-f]{16})$/.exec(sub);
  if (m && method === 'DELETE') {
    await db.prepare("UPDATE group_invites SET revoked_at=? WHERE group_id=? AND substr(token_hash,1,16)=?").bind(Date.now(), g.id, m[1]).run();
    return json({ ok: true });
  }

  m = /^members\/(\d+)$/.exec(sub);
  if (m && method === 'POST') {
    const tid = Number(m[1]);
    const target = await membership(db, g.id, tid);
    if (!target) return fail(404, 'No such member.');
    const b = await body(request);
    const action = String(b?.action || '');
    const admins = await adminCount(db, g.id);
    if (action === 'approve') await db.prepare("UPDATE group_members SET status='active', joined_at=? WHERE group_id=? AND teacher_id=?").bind(Date.now(), g.id, tid).run();
    else if (action === 'make-admin') await db.prepare("UPDATE group_members SET role='admin' WHERE group_id=? AND teacher_id=?").bind(g.id, tid).run();
    else if (action === 'make-teacher') {
      if (target.role === 'admin' && admins <= 1) return fail(400, 'A group needs at least one admin.');
      await db.prepare("UPDATE group_members SET role='teacher' WHERE group_id=? AND teacher_id=?").bind(g.id, tid).run();
    } else if (action === 'remove') {
      if (target.role === 'admin' && target.status === 'active' && admins <= 1) return fail(400, 'A group needs at least one admin.');
      await db.batch([
        db.prepare('DELETE FROM group_members WHERE group_id=? AND teacher_id=?').bind(g.id, tid),
        db.prepare('UPDATE classes SET group_id=NULL, shared_with_group=0 WHERE group_id=? AND teacher_id=?').bind(g.id, tid),
      ]);
    } else return fail(400, 'Unknown action.');
    return json({ ok: true });
  }

  return fail(404, 'Not found.');
}
