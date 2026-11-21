-- How each learner session was made. Database: biochempedia-classes, bound as CLASSES.
--
-- The owner's totals page (worker/admin.js) opens for the owner's own Google account. Being
-- signed in to an account that HOLDS that Google identity is not enough: on a shared computer a
-- Google identity could end up on somebody else's account, and every session of that account
-- (a phone, a passkey) would then pass. So the page looks at how THIS session was made. These
-- three columns record it when a session starts (worker/learner.js startSession):
--
--   method        'google' or 'passkey'; NULL for sessions made before this migration, and for
--                 sessions carried across the address change (those never open the owner's page)
--   google_sub    for a Google sign-in: Google's account number from that sign-in
--   google_email  for a Google sign-in: the address Google vouched for (email_verified) then
--
-- Nothing new is learned about anyone: the same sub and email are already on the learner's row.
-- They go when the session ends, and with the account. Until this migration is applied, sessions
-- are made exactly as before and the owner's page stays shut for account sign-in (the ADMIN_TOKEN
-- secret, if set, still works).
ALTER TABLE learner_sessions ADD COLUMN method TEXT CHECK (method IN ('google', 'passkey'));
ALTER TABLE learner_sessions ADD COLUMN google_sub TEXT;
ALTER TABLE learner_sessions ADD COLUMN google_email TEXT;
