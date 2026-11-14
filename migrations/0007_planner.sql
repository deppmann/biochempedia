-- Study planner (worker/planner.js): the spend cap, saved learner plans, and teachers'
-- class resource lists. Database: biochempedia-classes, bound as CLASSES.
--
-- Until this migration is applied the planner reports itself off (503) and the pages hide
-- their entry points, so the code can ship first.
--
-- What a person types or uploads to make a plan is sent to the model once and never stored.
-- Only a plan someone chooses to save is kept: catalog references (lesson slugs and the films,
-- simulations and method films picked in each), the person's own title and notes, and, for a
-- learner's plan, the goal fields they filled in, so the plan can be re-planned later.

-- One row per day ('d2026-11-14', Eastern) and per month ('m2026-11'), as router_budget.
CREATE TABLE IF NOT EXISTS planner_budget (
  period          TEXT PRIMARY KEY,
  spent_micro     INTEGER NOT NULL DEFAULT 0,
  reserved_micro  INTEGER NOT NULL DEFAULT 0,
  calls           INTEGER NOT NULL DEFAULT 0,
  errors          INTEGER NOT NULL DEFAULT 0,
  blocked         INTEGER NOT NULL DEFAULT 0,
  tokens_in       INTEGER NOT NULL DEFAULT 0,
  cache_read      INTEGER NOT NULL DEFAULT 0,
  cache_write     INTEGER NOT NULL DEFAULT 0,
  tokens_out      INTEGER NOT NULL DEFAULT 0
);

-- A learner's saved study plans (a few per account). Deleted with the account.
CREATE TABLE IF NOT EXISTS learner_plans (
  id          TEXT PRIMARY KEY,                   -- random
  learner_id  TEXT NOT NULL REFERENCES learners(id) ON DELETE CASCADE,
  title       TEXT NOT NULL,
  notes       TEXT NOT NULL DEFAULT '',
  goal_json   TEXT NOT NULL,                      -- { goal, weeks, hours, known, level }
  plan_json   TEXT NOT NULL,                      -- { summary, sections: [{ label, focus, gap, items: [refs] }], gaps }
  start_at    INTEGER NOT NULL,                   -- week 1 starts here (ms)
  created_at  INTEGER NOT NULL,
  updated_at  INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_lplans_learner ON learner_plans(learner_id);

-- A teacher's syllabus matched to the site, saved to one of their classes. Anyone with the
-- link can open it (students need no account), like a class's assigned lessons.
CREATE TABLE IF NOT EXISTS class_resource_lists (
  id          TEXT PRIMARY KEY,                   -- random, in the shareable link
  class_id    TEXT NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
  teacher_id  INTEGER NOT NULL REFERENCES teachers(id) ON DELETE CASCADE,
  title       TEXT NOT NULL,
  note        TEXT NOT NULL DEFAULT '',
  items_json  TEXT NOT NULL,                      -- { sections: [{ label, gap, items: [refs] }] }
  created_at  INTEGER NOT NULL,
  updated_at  INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_crl_class ON class_resource_lists(class_id);
