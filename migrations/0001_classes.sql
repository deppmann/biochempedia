-- Teacher classes (step 2a). Database: biochempedia-classes, bound as CLASSES.
--
-- Privacy by design: teachers give an email (to sign in) and a display name.
-- Students give a nickname only: no email, no real name, no password. Each student
-- holds a personal student code (stored hashed) to get back in on another device.
-- Answers are what a student did in a lesson: first tries on quiz questions and
-- agree/disagree checks, claim-evidence-reasoning answers they chose to send,
-- "done" marks and stuck notes. Deleting a class deletes all of it.

CREATE TABLE IF NOT EXISTS teachers (
  id                INTEGER PRIMARY KEY AUTOINCREMENT,
  email             TEXT NOT NULL UNIQUE COLLATE NOCASE,
  name              TEXT NOT NULL,
  password_hash     TEXT NOT NULL,              -- pbkdf2$<iter>$<salt_b64>$<hash_b64>
  recovery_hash     TEXT,                       -- sha256 of the one-time recovery code
  email_verified_at INTEGER,
  failed_logins     INTEGER NOT NULL DEFAULT 0,
  locked_until      INTEGER,
  created_at        INTEGER NOT NULL,
  last_active_at    INTEGER
);

CREATE TABLE IF NOT EXISTS teacher_sessions (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  teacher_id  INTEGER NOT NULL REFERENCES teachers(id) ON DELETE CASCADE,
  token_hash  TEXT NOT NULL UNIQUE,
  created_at  INTEGER NOT NULL,
  expires_at  INTEGER NOT NULL,
  revoked_at  INTEGER
);
CREATE INDEX IF NOT EXISTS idx_tsess_teacher ON teacher_sessions(teacher_id);

-- Email links: verify an address, or reset a password. Single use, short lived.
CREATE TABLE IF NOT EXISTS email_tokens (
  token_hash  TEXT PRIMARY KEY,
  teacher_id  INTEGER NOT NULL REFERENCES teachers(id) ON DELETE CASCADE,
  purpose     TEXT NOT NULL CHECK (purpose IN ('verify','reset')),
  created_at  INTEGER NOT NULL,
  expires_at  INTEGER NOT NULL,
  used_at     INTEGER
);

CREATE TABLE IF NOT EXISTS classes (
  id               TEXT PRIMARY KEY,            -- random, used in teacher URLs
  teacher_id       INTEGER NOT NULL REFERENCES teachers(id) ON DELETE CASCADE,
  name             TEXT NOT NULL,
  course           TEXT NOT NULL,               -- a course slug, for the lesson picker
  code             TEXT NOT NULL UNIQUE,        -- what students type to join
  join_mode        TEXT NOT NULL DEFAULT 'open' CHECK (join_mode IN ('open','approve','roster','locked')),
  created_at       INTEGER NOT NULL,
  last_activity_at INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_classes_teacher ON classes(teacher_id);

CREATE TABLE IF NOT EXISTS assignments (
  class_id     TEXT NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
  lesson_slug  TEXT NOT NULL,
  due_date     TEXT,                            -- YYYY-MM-DD, optional
  assigned_at  INTEGER NOT NULL,
  PRIMARY KEY (class_id, lesson_slug)
);

CREATE TABLE IF NOT EXISTS students (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  class_id      TEXT NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
  nickname      TEXT NOT NULL COLLATE NOCASE,
  code_hash     TEXT NOT NULL,
  status        TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active','pending')),
  created_at    INTEGER NOT NULL,
  last_seen_at  INTEGER,
  UNIQUE (class_id, nickname)
);
CREATE INDEX IF NOT EXISTS idx_students_code ON students(class_id, code_hash);

CREATE TABLE IF NOT EXISTS student_sessions (
  token_hash  TEXT PRIMARY KEY,
  student_id  INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
  created_at  INTEGER NOT NULL,
  expires_at  INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_ssess_student ON student_sessions(student_id);

-- kind: quiz | idea  (first try only; later tries are ignored)
--       cer          (latest version the student sent)
--       done | stuck (one per lesson; stuck keeps the latest note)
CREATE TABLE IF NOT EXISTS answers (
  student_id   INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
  lesson_slug  TEXT NOT NULL,
  kind         TEXT NOT NULL CHECK (kind IN ('quiz','idea','cer','done','stuck')),
  item         TEXT NOT NULL DEFAULT '',
  value        TEXT,
  correct      INTEGER,
  created_at   INTEGER NOT NULL,
  updated_at   INTEGER NOT NULL,
  PRIMARY KEY (student_id, lesson_slug, kind, item)
);

-- Fixed-window counters for sign-up, sign-in, join and answer limits.
CREATE TABLE IF NOT EXISTS rate_limits (
  key           TEXT PRIMARY KEY,
  count         INTEGER NOT NULL,
  window_start  INTEGER NOT NULL
);
