-- Study helpers (worker/helper.js): the spend cap and the counts. Nothing about learners.
--
-- Same shape as router_budget (0004), kept separate so the helpers have their own caps:
-- one row per day ('d2026-11-14', Eastern time) and one per month ('m2026-11').
-- spent_micro is the cost so far in millionths of a US dollar, from the usage tokens the
-- API reports; reserved_micro is the worst case of calls in flight right now. No passage,
-- answer, highlight or reply is ever stored: the counts below are all the logging there is.
-- Until this table exists, GET /api/help answers 503 and no helper control is shown.
CREATE TABLE IF NOT EXISTS helper_budget (
  period          TEXT PRIMARY KEY,
  spent_micro     INTEGER NOT NULL DEFAULT 0,
  reserved_micro  INTEGER NOT NULL DEFAULT 0,
  calls           INTEGER NOT NULL DEFAULT 0,   -- model calls that returned
  errors          INTEGER NOT NULL DEFAULT 0,   -- model calls that failed
  blocked         INTEGER NOT NULL DEFAULT 0,   -- requests turned away at the cap
  dropped         INTEGER NOT NULL DEFAULT 0,   -- replies that failed the checks and were not shown
  tokens_in       INTEGER NOT NULL DEFAULT 0,   -- uncached input
  cache_read      INTEGER NOT NULL DEFAULT 0,
  cache_write     INTEGER NOT NULL DEFAULT 0,
  tokens_out      INTEGER NOT NULL DEFAULT 0
);
