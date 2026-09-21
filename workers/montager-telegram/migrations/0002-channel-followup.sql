-- Apply once after checking PRAGMA table_info(updates); before deploying the new Worker.
-- Zero defaults exclude historical registrations and pending historical updates.
ALTER TABLE updates ADD COLUMN confirmation_sent INTEGER NOT NULL DEFAULT 0 CHECK(confirmation_sent IN (0,1));
ALTER TABLE updates ADD COLUMN followup_required INTEGER NOT NULL DEFAULT 0 CHECK(followup_required IN (0,1));
