-- An optional role on learner accounts, and an anonymous count of films played.
-- Database: biochempedia-classes, bound as CLASSES.
--
-- Both are for the owner's totals page (worker/admin.js, GET /api/admin/stats), which shows
-- counts only. The code ships before this migration: until it is applied the account page asks
-- no question and the film counter answers quietly and stores nothing.
--
-- 1. learners.role: "student", "parent" or "teacher", or NULL for not asked or not answered.
--    Asked once, optionally, when an account is made (13 and older, as before), and changeable
--    or clearable on the account page. Nothing else is asked: no age, grade or school. It is in
--    "Download my data" and goes when the account is deleted, because it is a column of the
--    learner's own row.
ALTER TABLE learners ADD COLUMN role TEXT CHECK (role IN ('student', 'parent', 'teacher'));

-- 2. film_counts: how many times each film was started, and watched to the end, per day.
--    These four columns are everything that is kept. There is no account, class, device,
--    address or time of day in a row, so a row cannot be tied to a viewer (worker/film-count.js).
CREATE TABLE IF NOT EXISTS film_counts (
  film_key  TEXT NOT NULL,                -- the film's file under /explainers/, as in src/lib/film-progress.ts
  day       TEXT NOT NULL,                -- YYYY-MM-DD, UTC
  started   INTEGER NOT NULL DEFAULT 0,
  watched   INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (film_key, day)
);
CREATE INDEX IF NOT EXISTS idx_film_counts_day ON film_counts(day);
