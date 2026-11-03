-- Curiosity router (worker/curious.js): the spend cap and the counts. Nothing about visitors.
--
-- router_budget has one row per day ('d2026-10-30', Eastern time) and one per month
-- ('m2026-10'). spent_micro is the cost so far in millionths of a US dollar, worked out
-- from the usage tokens the API reports; reserved_micro is the worst-case cost of calls
-- that are in flight right now, so two requests arriving together cannot both squeeze
-- under the cap. The token and call counts are all the logging the router does.
CREATE TABLE IF NOT EXISTS router_budget (
  period          TEXT PRIMARY KEY,
  spent_micro     INTEGER NOT NULL DEFAULT 0,
  reserved_micro  INTEGER NOT NULL DEFAULT 0,
  calls           INTEGER NOT NULL DEFAULT 0,   -- model calls that returned
  errors          INTEGER NOT NULL DEFAULT 0,   -- model calls that failed
  blocked         INTEGER NOT NULL DEFAULT 0,   -- requests turned away at the cap
  tokens_in       INTEGER NOT NULL DEFAULT 0,   -- uncached input
  cache_read      INTEGER NOT NULL DEFAULT 0,
  cache_write     INTEGER NOT NULL DEFAULT 0,
  tokens_out      INTEGER NOT NULL DEFAULT 0
);

-- Only written when ROUTER_LOG_QUERIES is "1" (off by default), and pruned after 30 days.
-- The question text is the only thing in it: no IP, no hash, no identifier.
CREATE TABLE IF NOT EXISTS router_queries (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at  INTEGER NOT NULL,
  query       TEXT NOT NULL,
  picks       TEXT NOT NULL            -- the slugs returned, comma-separated
);
