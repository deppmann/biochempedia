-- Learner accounts (worker/learner.js). Database: biochempedia-classes, bound as CLASSES.
--
-- An account is optional and only syncs what the browser already keeps (notebook and
-- progress) between a learner's own devices. 13 and older only. A learner signs in
-- with Google or with a passkey; there are no passwords. The database never holds a
-- usable credential: session tokens are stored as their SHA-256 hex, and a passkey is
-- only its public key. "Delete my account" removes every row below for that learner.

CREATE TABLE IF NOT EXISTS learners (
  id              TEXT PRIMARY KEY,               -- random, never shown
  display_name    TEXT NOT NULL,
  email           TEXT,                           -- from Google, only if verified; NULL for passkey-only
  google_sub      TEXT UNIQUE,                    -- Google's stable account id
  created_at      INTEGER NOT NULL,
  last_active_at  INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS learner_sessions (
  token_hash  TEXT PRIMARY KEY,
  learner_id  TEXT NOT NULL REFERENCES learners(id) ON DELETE CASCADE,
  created_at  INTEGER NOT NULL,
  expires_at  INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_lsess_learner ON learner_sessions(learner_id);

CREATE TABLE IF NOT EXISTS learner_passkeys (
  credential_id  TEXT PRIMARY KEY,                -- base64url, as the browser sends it
  learner_id     TEXT NOT NULL REFERENCES learners(id) ON DELETE CASCADE,
  public_key     TEXT NOT NULL,                   -- base64url COSE public key
  counter        INTEGER NOT NULL DEFAULT 0,
  transports     TEXT,                            -- JSON array, e.g. ["internal","hybrid"]
  created_at     INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_lpk_learner ON learner_passkeys(learner_id);

CREATE TABLE IF NOT EXISTS learner_data (
  learner_id     TEXT PRIMARY KEY REFERENCES learners(id) ON DELETE CASCADE,
  notebook_json  TEXT NOT NULL DEFAULT '{}',      -- { "<id>": item } as in src/lib/notebook.ts
  progress_json  TEXT NOT NULL DEFAULT '{}',      -- the biochempedia:progress:v1 object
  updated_at     INTEGER NOT NULL
);

-- Sign-in in progress: a WebAuthn challenge, or a Google state + PKCE verifier. The
-- browser holds the random id in a short-lived cookie; the row is used once and lives
-- ten minutes at most. learner_id is set when a signed-in learner adds a passkey or
-- links Google; display_name when a new learner signs up with a passkey.
CREATE TABLE IF NOT EXISTS learner_challenges (
  id            TEXT PRIMARY KEY,                 -- sha256 hex of the cookie value
  purpose       TEXT NOT NULL CHECK (purpose IN ('register','login','google')),
  challenge     TEXT NOT NULL,                    -- WebAuthn challenge, or the PKCE verifier
  learner_id    TEXT,
  display_name  TEXT,
  extra         TEXT,                             -- Google: JSON { nonce, ret }; register: the new user id
  created_at    INTEGER NOT NULL,
  expires_at    INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_lchal_exp ON learner_challenges(expires_at);
