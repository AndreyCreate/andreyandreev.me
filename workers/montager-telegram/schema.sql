CREATE TABLE IF NOT EXISTS queue (
 position INTEGER PRIMARY KEY CHECK(position > 0),
 telegram_id INTEGER NOT NULL UNIQUE CHECK(telegram_id > 0),
 source TEXT NOT NULL CHECK(source IN ('site','reel','other')),
 created_at INTEGER NOT NULL DEFAULT(unixepoch())
);
CREATE TABLE IF NOT EXISTS updates (
 update_id INTEGER PRIMARY KEY,
 telegram_id INTEGER NOT NULL,
 sent INTEGER NOT NULL DEFAULT 0 CHECK(sent IN (0,1)),
 confirmation_sent INTEGER NOT NULL DEFAULT 0 CHECK(confirmation_sent IN (0,1)),
 followup_required INTEGER NOT NULL DEFAULT 0 CHECK(followup_required IN (0,1)),
 lease TEXT,
 lease_until INTEGER NOT NULL DEFAULT 0
);
