# CLAUDE.md

Last updated: 2026-05-11

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository status

This repo is **mid-scaffold**. Only the design doc (`docs/idea.md`) and `schema.sql` exist. The CLI (`crm.py`), prompts, skills, and data directories described below are **planned but not yet present**. When asked to implement, follow the build order in `docs/idea.md` §12. Do not invent files that the spec does not describe.

## What this project is (Compass)

Single-user, local personal CRM. Three agents driven by prompts + slash commands, backed by SQLite + markdown. Read `docs/idea.md` end-to-end before any non-trivial change — it is the source of truth for design intent, naming, and what each agent must NOT do.

- **Tracker** (`/track`): one free-text sentence → `(target, lane, touchpoint)` rows. Write-path.
- **Analyzer** (`/analyze`): per-target read-only timeline + recommendations.
- **Strategist** (`/review`): periodic 复盘 — synthesizes recent cycle, extracts assets, updates `profile.md`, writes a `retro_brief`.

The runtime is Claude Code itself. The CLI gathers data, calls a skill, and applies JSON-shaped DB writes the LLM returns. No server, no ORM, no asyncio.

## Architecture invariants (do not violate)

- **Targets, not tasks.** The data model is target-shaped at every layer. A `target` persists; a `lane` is one thread of pursuit within it; a `touchpoint` is one interaction on a lane.
- **Append-only past, mutable future.** `touchpoint` and `retro_brief` are enforced append-only via SQLite triggers (`touchpoint_no_update`, `touchpoint_no_delete`, `retro_no_update`, `retro_no_delete`). Never write code that bypasses these — re-do via a new row instead.
- **The agent is a prompt.** Behavior changes go in `prompts/<agent>.md`, not in Python. Adding a new slash command = drop a `skills/<name>/SKILL.md`. Code changes are a last resort.
- **Bias as policy.** Priority order ("求职 > 自媒体 > others") lives as one line in one prompt — flippable in seconds. Don't hard-code it.
- **The system earns its complexity.** New table / column / agent only when a `retro_brief` explicitly flags its absence. Push back on speculative additions.
- **Graceful degradation.** Even with the LLM down, `compass track` must still write the raw line to `data/journal/<yyyy-mm-dd>.md`. Don't gate writes on LLM success.
- **Single user, single device.** No auth, no sync, no cloud. Backup = `git push`.

## Schema (`schema.sql`)

Five tables. UUIDs generated in Python; all timestamps ISO-8601 UTC strings. `PRAGMA foreign_keys = ON;` is required on every connection — SQLite does not enforce FKs by default.

- `target` — name+kind unique; kind ∈ {job, media, community, collaborator}; tier ∈ {dream, strong, try, cold}.
- `lane` — belongs to a target (CASCADE delete); optional `asset_id` (SET NULL on asset delete); kind ∈ {job_app, content, event, outreach}.
- `touchpoint` — append-only; kind ∈ {applied, call, message, post, meet, reply}; carries `summary`, `insights`, `next_step`.
- `asset` — name+kind unique; kind ∈ {resume, blog, repo, talk, side_project}; stage ∈ {idea, prototype, public, maintained}.
- `retro_brief` — append-only; full `content_md` of each periodic review.

`schema.sql` is idempotent (`CREATE ... IF NOT EXISTS`). Re-run via `compass migrate` after edits — never write a migration script.

## Planned commands (per spec — implement when building `crm.py`)

```bash
compass init                  # create dirs + apply schema
compass migrate               # reapply schema.sql idempotently
compass track "..."           # → /track skill
compass analyze <target_id>   # → /analyze skill
compass review                # → /review skill
compass sql "<query>"         # raw read query
```

## Stack constraints

- Python via **uv** (no pip, no poetry, no global installs). Always isolated env.
- One CLI file (`crm.py`, ~200 lines target). No package layout, no class hierarchy.
- SQLite (`crm.db`, gitignored). Markdown for unstructured (`data/journal/`, `data/retros/`, `data/targets/<id>/notes.md`, `north_star.md`, `profile.md`).
- Official SQLite MCP server, mounted **read-only** on `crm.db`.
- Confirm before adding any dependency outside this stack.

## Conventions

- Don't commit unless explicitly told to. `*.db`, `*.sqlite*`, `.env*`, `.gstack/`, and `.claude/settings.local.json` are gitignored — keep it that way.
- When updating any `.md` file, also update its `Last updated:` line.
- The directory is currently `personal-crm/`; the product name is `compass`. Treat both as referring to the same thing.
