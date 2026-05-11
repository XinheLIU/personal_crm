-- Compass schema. Idempotent. Re-run with `compass migrate` after edits.
-- All timestamps are ISO-8601 strings (UTC). UUIDs are generated in Python.

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS target (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    kind        TEXT NOT NULL CHECK (kind IN ('job', 'media', 'community', 'collaborator')),
    tier        TEXT NOT NULL DEFAULT 'try' CHECK (tier IN ('dream', 'strong', 'try', 'cold')),
    status      TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'dormant', 'closed')),
    notes_path  TEXT,
    created_at  TEXT NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_target_name_kind ON target(name, kind);
CREATE INDEX IF NOT EXISTS idx_target_status ON target(status);

CREATE TABLE IF NOT EXISTS lane (
    id          TEXT PRIMARY KEY,
    target_id   TEXT NOT NULL REFERENCES target(id) ON DELETE CASCADE,
    kind        TEXT NOT NULL CHECK (kind IN ('job_app', 'content', 'event', 'outreach')),
    title       TEXT NOT NULL,
    stage       TEXT NOT NULL DEFAULT 'open' CHECK (stage IN ('open','applied','screening','interview','offer','rejected','closed')),
    deadline    TEXT,
    asset_id    TEXT REFERENCES asset(id) ON DELETE SET NULL,
    status      TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'paused', 'closed')),
    created_at  TEXT NOT NULL,
    closed_at   TEXT
);

CREATE INDEX IF NOT EXISTS idx_lane_target ON lane(target_id);
CREATE INDEX IF NOT EXISTS idx_lane_status ON lane(status);
CREATE INDEX IF NOT EXISTS idx_lane_deadline ON lane(deadline) WHERE deadline IS NOT NULL;
CREATE UNIQUE INDEX IF NOT EXISTS idx_lane_target_title ON lane(target_id, title);

-- Append-only. Triggers below enforce no UPDATE / no DELETE.
CREATE TABLE IF NOT EXISTS touchpoint (
    id           TEXT PRIMARY KEY,
    lane_id      TEXT NOT NULL REFERENCES lane(id) ON DELETE RESTRICT,
    kind         TEXT NOT NULL CHECK (kind IN ('applied', 'call', 'message', 'post', 'meet', 'reply')),
    summary      TEXT NOT NULL,
    insights     TEXT,
    next_step    TEXT,
    happened_at  TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_touchpoint_lane ON touchpoint(lane_id);
CREATE INDEX IF NOT EXISTS idx_touchpoint_happened ON touchpoint(happened_at);

CREATE TRIGGER IF NOT EXISTS touchpoint_no_update
BEFORE UPDATE ON touchpoint
BEGIN
    SELECT RAISE(ABORT, 'touchpoint is append-only');
END;

CREATE TRIGGER IF NOT EXISTS touchpoint_no_delete
BEFORE DELETE ON touchpoint
BEGIN
    SELECT RAISE(ABORT, 'touchpoint is append-only');
END;

CREATE TABLE IF NOT EXISTS asset (
    id              TEXT PRIMARY KEY,
    name            TEXT NOT NULL,
    kind            TEXT NOT NULL CHECK (kind IN ('resume', 'blog', 'repo', 'talk', 'side_project')),
    stage           TEXT NOT NULL DEFAULT 'idea' CHECK (stage IN ('idea', 'prototype', 'public', 'maintained')),
    artifact_path   TEXT,
    last_touched_at TEXT
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_asset_name_kind ON asset(name, kind);

-- Append-only. Edits to data/retros/<iso>.md are user annotations, separate from this row.
CREATE TABLE IF NOT EXISTS retro_brief (
    id          TEXT PRIMARY KEY,
    period_iso  TEXT NOT NULL,
    content_md  TEXT NOT NULL,
    created_at  TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_retro_period ON retro_brief(period_iso);

CREATE TRIGGER IF NOT EXISTS retro_no_update
BEFORE UPDATE ON retro_brief
BEGIN
    SELECT RAISE(ABORT, 'retro_brief is append-only');
END;

CREATE TRIGGER IF NOT EXISTS retro_no_delete
BEFORE DELETE ON retro_brief
BEGIN
    SELECT RAISE(ABORT, 'retro_brief is append-only');
END;
