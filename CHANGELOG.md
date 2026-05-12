# Changelog

All notable changes to Compass are documented here. Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [0.1.0.0] - 2026-05-11

### Added
- `CLAUDE.md` — project guidance for Claude Code: architecture invariants, schema summary, planned commands, and stack constraints
- `schema.sql` — idempotent SQLite schema with five tables (`target`, `lane`, `touchpoint`, `asset`, `retro_brief`), FK constraints, append-only triggers for `touchpoint` and `retro_brief`, and supporting indexes
- `TODOS.md` — initial backlog with two open items: orchestrator runtime decision and `compass import` batch ingestion command

---

## [0.1.1.0] - 2026-05-12

### Added
- `crm.py` — full CLI implementation: `init`, `migrate`, `track`, `analyze`, `review`, `seed`, `sql`
- `data/seed.sql` — cold-start demo data (ByteDance, Hugging Face, blog, coffee chats) with 10 touchpoints across 5 lanes
- `prompts/tracker.md`, `prompts/analyzer.md`, `prompts/strategist.md` — agent behavior prompts
- `.claude/skills/track/SKILL.md` — Claude Code `/track` skill
- `north_star.md` and `profile.md` — user-editable strategy and self-definition templates
- `AGENTS.md` — OpenCode-compatible agent instructions
- `docs/ideas/` — design doc moved from `docs/idea.md`
- `docs/ui-plan.md` — frontend UI implementation plan (Flask server + Alpine.js SPA)
- `docs/quick-start.md`, `docs/user-guide.md`, `docs/test-plan.md` — user and QA documentation

### Changed
- `docs/idea.md` moved to `docs/ideas/idea.md`
