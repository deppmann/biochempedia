-- Groups (step 2b): a school, department or district with its own page at /g/<slug>/
-- and its own admins. Teachers join by invite link or by asking; admins approve.
-- Admins see members, classes and counts; they see a class's student answers only
-- when its teacher shares that class with the group.

CREATE TABLE IF NOT EXISTS groups (
  id                 TEXT PRIMARY KEY,
  slug               TEXT NOT NULL UNIQUE,      -- the page address: /g/<slug>/
  name               TEXT NOT NULL,
  about              TEXT NOT NULL DEFAULT '',
  email_domain       TEXT,                      -- e.g. school.k12.va.us; new members must match
  default_join_mode  TEXT NOT NULL DEFAULT 'open' CHECK (default_join_mode IN ('open','approve','roster','locked')),
  created_by         INTEGER REFERENCES teachers(id) ON DELETE SET NULL,
  created_at         INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS group_members (
  group_id    TEXT NOT NULL REFERENCES groups(id) ON DELETE CASCADE,
  teacher_id  INTEGER NOT NULL REFERENCES teachers(id) ON DELETE CASCADE,
  role        TEXT NOT NULL DEFAULT 'teacher' CHECK (role IN ('admin','teacher')),
  status      TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active','pending')),
  joined_at   INTEGER NOT NULL,
  PRIMARY KEY (group_id, teacher_id)
);
CREATE INDEX IF NOT EXISTS idx_gm_teacher ON group_members(teacher_id);

-- Invite links. Reusable up to max_uses until they expire or an admin revokes them.
CREATE TABLE IF NOT EXISTS group_invites (
  token_hash  TEXT PRIMARY KEY,
  group_id    TEXT NOT NULL REFERENCES groups(id) ON DELETE CASCADE,
  role        TEXT NOT NULL DEFAULT 'teacher' CHECK (role IN ('admin','teacher')),
  created_by  INTEGER REFERENCES teachers(id) ON DELETE SET NULL,
  created_at  INTEGER NOT NULL,
  expires_at  INTEGER NOT NULL,
  max_uses    INTEGER NOT NULL DEFAULT 50,
  uses        INTEGER NOT NULL DEFAULT 0,
  revoked_at  INTEGER,
  note        TEXT NOT NULL DEFAULT ''          -- who it was for, shown to admins only
);
CREATE INDEX IF NOT EXISTS idx_gi_group ON group_invites(group_id);

ALTER TABLE classes ADD COLUMN group_id TEXT REFERENCES groups(id) ON DELETE SET NULL;
ALTER TABLE classes ADD COLUMN shared_with_group INTEGER NOT NULL DEFAULT 0;
CREATE INDEX IF NOT EXISTS idx_classes_group ON classes(group_id);
