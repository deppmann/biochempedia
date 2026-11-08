-- Flashcards in teacher classes. Database: biochempedia-classes, bound as CLASSES.
--
-- A teacher can tick "include flashcards" on an assigned lesson that has a deck. Then,
-- for a student in that class, the lesson page counts in the browser how many times
-- each card was marked "Again" and sends that running count (not an increment), so
-- a resend is harmless. The brief shows the three cards the class marked "Again" most.
-- No AI. Deleting a student or a class deletes their card marks too (worker/api.js
-- clears them explicitly, as it does answers).

ALTER TABLE assignments ADD COLUMN flashcards INTEGER NOT NULL DEFAULT 0;

CREATE TABLE IF NOT EXISTS card_marks (
  student_id   INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
  lesson_slug  TEXT NOT NULL,
  card_id      TEXT NOT NULL,
  again        INTEGER NOT NULL,              -- times this student marked the card "Again"
  updated_at   INTEGER NOT NULL,
  PRIMARY KEY (student_id, lesson_slug, card_id)
);
