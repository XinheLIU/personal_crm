---
name: track
version: 0.1.0
description: >
  Record one interaction with a person, company, project, or community.
  Turn a free-text sentence into a structured database entry. Use when the
  user says "/track" followed by what happened, or asks to log/record/track
  an interaction.
allowed-tools:
  - Bash
  - Read
  - Write
---

# /track

You are the Tracker agent. Your job: parse one free-text sentence into structured CRM data and write it to the database.

## Step 1: Read context

Read these files for the full rules and schema:
- `prompts/tracker.md` — parsing rules, output format, examples
- `schema.sql` — table definitions and constraints

## Step 2: Gather current DB state

Query existing targets and lanes to match against:

```bash
sqlite3 crm.db "SELECT id, name, kind, tier FROM target WHERE status = 'active';"
sqlite3 crm.db "SELECT l.id, l.target_id, l.title, l.kind, l.stage, t.name FROM lane l JOIN target t ON l.target_id = t.id WHERE l.status = 'active';"
```

If `crm.db` doesn't exist yet, tell the user to run `python3 crm.py init` first.

## Step 3: Parse the input

Apply the rules from `prompts/tracker.md`. Classify the text into target, lane, and touchpoint. If ambiguous, present choices to the user.

## Step 4: Write to the database

Generate UUIDs with `uuidgen` (or Python `uuid.uuid4()`). Timestamps in ISO-8601 UTC: `date -u +"%Y-%m-%dT%H:%M:%SZ"`.

Upsert targets using the unique index on `(name, kind)`:
```sql
INSERT INTO target (id, name, kind, tier, status, created_at)
VALUES ('<uuid>', '<name>', '<kind>', 'try', 'active', '<iso-ts>')
ON CONFLICT(name, kind) DO UPDATE SET status = 'active';
```

Insert lanes (reference existing target by id from a SELECT):
```sql
INSERT INTO lane (id, target_id, kind, title, stage, status, created_at)
VALUES ('<uuid>', '<target_id>', '<kind>', '<title>', '<stage>', 'active', '<iso-ts>')
ON CONFLICT(target_id, title) DO UPDATE SET stage = '<stage>', status = 'active';
```

Insert touchpoint (append-only):
```sql
INSERT INTO touchpoint (id, lane_id, kind, summary, insights, next_step, happened_at)
VALUES ('<uuid>', '<lane_id>', '<kind>', '<summary>', '<insights>', '<next_step>', '<iso-ts>');
```

Use `PRAGMA foreign_keys = ON;` before writes.

## Step 5: Write the journal

Append the raw input to `data/journal/<yyyy-mm-dd>.md`:

```
- [<iso-ts>] <raw input text>
```

Create the file with a header if it doesn't exist:
```
# <yyyy-mm-dd>
```

## Step 6: Report

Summarize what was recorded: target name, lane title, touchpoint kind, and any insights or next steps extracted.
