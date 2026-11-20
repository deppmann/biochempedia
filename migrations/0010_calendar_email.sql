-- Calendar email (/calendar/): the tables an opt-in email will need.
-- Database: biochempedia-classes, bound as CLASSES.
--
-- NOTHING USES THESE TABLES YET. No code reads or writes them, the site sends no calendar
-- email, and the opt-in button is switched off (src/lib/calendar/flags.ts, EMAIL_OPT_IN).
-- The migration is additive (two new tables, nothing altered), so applying it changes nothing
-- a visitor can see. It is here so the design is reviewed with the page it belongs to.
--
-- Before any calendar email can go out, the site's owner has to do and decide these, in order:
--   1. Apply this migration to the remote database.
--   2. Verify stemhop.com as a sending domain with the mail provider, set RESEND_API_KEY as a
--      Worker secret, and move MAIL_FROM (wrangler.jsonc) off the old domain.
--   3. Build the sending side (not in the repository yet): an HTML body and the
--      List-Unsubscribe and List-Unsubscribe-Post headers in sendMail (worker/util.js);
--      routes to ask, confirm, stop and move, each landing on a page with one button, so that
--      nothing acts when a mail scanner follows a link; a "triggers.crons" entry in
--      wrangler.jsonc and a scheduled() handler in worker/index.js; a daily send cap.
--   4. Rewrite /privacy/, which today says "We send no email", and list the teacher emails
--      on /teach/privacy/. Add these tables to the account export and to account deletion.
--   5. See a test email to his own address first. Only then set EMAIL_OPT_IN to true.
--
-- Who may be in this table: an adult who typed an address, ticked "18 or over" and then
-- confirmed from their inbox (role 'parent'); a teacher, by their confirmed teacher address
-- (role 'teacher'); a signed-in learner, 13 and over, by the address on their account
-- (role 'learner'). Never a student in a class, and never a child.
--
-- What is kept: the address (or a reference to the account that has one), the plan as
-- references only (which activities or which course, on which weekdays), a time zone, and
-- hashes of the confirm and stop tokens. Nothing about a child. Stopping deletes the row;
-- so does reaching the last email; an address that is never confirmed is deleted after a day.

CREATE TABLE IF NOT EXISTS email_subscriptions (
  id            TEXT PRIMARY KEY,                    -- random
  role          TEXT NOT NULL CHECK (role IN ('parent', 'teacher', 'learner')),
  -- Exactly one of these three says where the email goes.
  address       TEXT,                                -- a parent's typed address, lower-cased
  learner_id    TEXT REFERENCES learners(id) ON DELETE CASCADE,
  teacher_id    INTEGER REFERENCES teachers(id) ON DELETE CASCADE,
  class_id      TEXT REFERENCES classes(id) ON DELETE CASCADE,   -- teacher: which class plan
  plan_json     TEXT NOT NULL,                       -- references only: slugs in order, weekdays; no child data
  cadence       TEXT NOT NULL,                       -- 'two-days-before' | 'evening-before' | 'class-morning' | 'study-day'
  tz            TEXT NOT NULL,                       -- IANA zone, e.g. 'America/New_York', from the browser when asked
  adult         INTEGER NOT NULL DEFAULT 0,          -- 1 = ticked "I'm the grown-up here, 18 or over" (parents)
  confirm_hash  TEXT,                                -- hash of the double opt-in token; cleared on confirm
  stop_hash     TEXT NOT NULL,                       -- hash of the one-click unsubscribe token
  created_at    INTEGER NOT NULL,                    -- ms
  confirmed_at  INTEGER,                             -- null until the link in the confirming email is used
  sent_count    INTEGER NOT NULL DEFAULT 0,
  max_sends     INTEGER NOT NULL DEFAULT 8,          -- they stop by themselves
  last_sent_on  TEXT,                                -- 'YYYY-MM-DD' in tz
  CHECK ((address IS NOT NULL) + (learner_id IS NOT NULL) + (teacher_id IS NOT NULL) = 1)
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_esub_address ON email_subscriptions(address, role) WHERE address IS NOT NULL;
CREATE UNIQUE INDEX IF NOT EXISTS idx_esub_stop ON email_subscriptions(stop_hash);
CREATE INDEX IF NOT EXISTS idx_esub_confirm ON email_subscriptions(confirm_hash);
CREATE INDEX IF NOT EXISTS idx_esub_learner ON email_subscriptions(learner_id);
CREATE INDEX IF NOT EXISTS idx_esub_teacher ON email_subscriptions(teacher_id);

-- One row per email sent, so a retried run can never send the same day's email twice.
-- It holds no address and no content, and goes with its subscription.
CREATE TABLE IF NOT EXISTS email_sends (
  subscription_id  TEXT NOT NULL REFERENCES email_subscriptions(id) ON DELETE CASCADE,
  send_date        TEXT NOT NULL,                    -- 'YYYY-MM-DD' in the subscriber's zone
  kind             TEXT NOT NULL DEFAULT 'plan',     -- 'confirm' | 'plan'
  sent_at          INTEGER NOT NULL,                 -- ms
  PRIMARY KEY (subscription_id, send_date, kind)
);
