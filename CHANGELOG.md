# Changelog

All notable changes to Compass are documented here. Format: [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [0.1.0.0] - 2026-05-11

### Added
- `CLAUDE.md` — project guidance for Claude Code: architecture invariants, schema summary, planned commands, and stack constraints
- `schema.sql` — idempotent SQLite schema with five tables (`target`, `lane`, `touchpoint`, `asset`, `retro_brief`), FK constraints, append-only triggers for `touchpoint` and `retro_brief`, and supporting indexes
- `TODOS.md` — initial backlog with two open items: orchestrator runtime decision and `compass import` batch ingestion command
