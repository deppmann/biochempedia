-- AI feedback, layer 1. Off by default; paid for by the teacher's own API key.
--
-- A teacher stores one key per provider (encrypted with the site's KEY_ENCRYPTION_KEY
-- secret; only the last four characters are kept in the clear). Each class chooses
-- whether AI feedback is on, which provider and model, whether feedback goes to
-- students right away or waits for the teacher's review, and a monthly spending cap.
-- Every model call is metered in ai_calls, so the teacher sees what it cost.
-- Feedback rows also carry notes a teacher writes by hand (source 'teacher', free).

CREATE TABLE IF NOT EXISTS teacher_ai_keys (
  teacher_id  INTEGER NOT NULL REFERENCES teachers(id) ON DELETE CASCADE,
  provider    TEXT NOT NULL CHECK (provider IN ('gemini','anthropic','openai')),
  key_enc     TEXT NOT NULL,       -- base64 AES-GCM ciphertext
  key_iv      TEXT NOT NULL,       -- base64 12-byte IV
  last4       TEXT NOT NULL,
  created_at  INTEGER NOT NULL,
  PRIMARY KEY (teacher_id, provider)
);

ALTER TABLE classes ADD COLUMN ai_enabled INTEGER NOT NULL DEFAULT 0;
ALTER TABLE classes ADD COLUMN ai_provider TEXT;
ALTER TABLE classes ADD COLUMN ai_model TEXT;
ALTER TABLE classes ADD COLUMN ai_mode TEXT NOT NULL DEFAULT 'hold';     -- 'hold' (teacher reviews first) | 'show'
ALTER TABLE classes ADD COLUMN ai_cap_cents INTEGER NOT NULL DEFAULT 500; -- monthly cap, US cents

CREATE TABLE IF NOT EXISTS feedback (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  class_id     TEXT NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
  student_id   INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
  lesson_slug  TEXT NOT NULL,
  kind         TEXT NOT NULL CHECK (kind IN ('cer','design','stuck','note')),
  item         TEXT NOT NULL DEFAULT '',
  answer       TEXT,                -- the student's answer the feedback is about
  draft        TEXT,                -- what the model wrote
  final        TEXT,                -- what the student sees (teacher may edit)
  status       TEXT NOT NULL CHECK (status IN ('held','released','discarded')),
  source       TEXT NOT NULL CHECK (source IN ('ai','teacher')),
  model        TEXT,
  created_at   INTEGER NOT NULL,
  released_at  INTEGER,
  seen_at      INTEGER
);
CREATE INDEX IF NOT EXISTS idx_feedback_class ON feedback(class_id, status);
CREATE INDEX IF NOT EXISTS idx_feedback_student ON feedback(student_id, lesson_slug);

CREATE TABLE IF NOT EXISTS ai_calls (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  class_id    TEXT REFERENCES classes(id) ON DELETE CASCADE,   -- null for a key test
  teacher_id  INTEGER REFERENCES teachers(id) ON DELETE CASCADE,
  purpose     TEXT NOT NULL,        -- feedback | summary | reply | test
  provider    TEXT NOT NULL,
  model       TEXT NOT NULL,
  tokens_in   INTEGER NOT NULL DEFAULT 0,
  tokens_out  INTEGER NOT NULL DEFAULT 0,
  cost_micro  INTEGER NOT NULL DEFAULT 0,   -- millionths of a US dollar
  ok          INTEGER NOT NULL DEFAULT 1,
  created_at  INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_ai_calls_class ON ai_calls(class_id, created_at);
