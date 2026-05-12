# Compass — Test Plan

*Last updated: 2026-05-12.*

---

## 1. Overview

**Scope:** `crm.py` CLI + SQLite schema. Does NOT cover LLM agent synthesis (that is a human-judgment review step).

**Test runner:** `pytest` + `uv run pytest tests/`

**Philosophy:** Tests verify behavior, not implementation. Every command has acli observable output or DB side-effect that can be asserted.

---

## 2. Test Structure

```
tests/
├── conftest.py          # Shared fixtures
├── test_cli.py          # CLI commands: init, seed, migrate, track, analyze, review, sql
├── test_schema.py       # Append-only triggers
└── test_e2e.py          # Full workflows through compass CLI
```

---

## 3. Fixtures (`conftest.py`)

| Fixture | Scope | Purpose |
|---|---|---|
| `tmp_dir` | function | Isolated working dir per test |
| `db_path` | function | Points `crm.py` at temp `crm.db` via env or CLI arg |
| `seeded_db` | function | Runs `compass init` + `compass seed` (reads `data/seed.sql`) |
| `journal_path` | function | Points `crm.py` journal at temp dir |

All tests run in temp directories. No side-effects on the real `crm.db`.

---

## 4. CLI Tests (`test_cli.py`)

### `compass init`

| ID | Case | Expected |
|---|---|---|
| C-01 | Run on fresh temp dir | Creates `crm.db`, all `data/` subdirs, `north_star.md`, `profile.md` |
| C-02 | Run twice | Idempotent — no error, no data loss |
| C-03 | `crm.db` already exists | Opens existing DB, does not overwrite |

### `compass seed`

| ID | Case | Expected |
|---|---|---|
| S-01 | Run without `init` first | Prints "No database. Run `compass init` first." |
| S-02 | Run without seed.sql | Prints "No seed data at data/seed.sql" |
| S-03 | Run after `init` | Reads `data/seed.sql`, applies via `executescript` |
| S-04 | Run twice | `INSERT OR IGNORE` — no duplicates |
| S-05 | Verify target tiers | 1 dream, 1 strong, 2 try (matches cold-start data) |
| S-06 | Verify lane stages | Correct stage per lane (e.g. `lane_bdy_l7` → `interview`) |
| S-07 | Verify touchpoint count per lane | Correct counts (L7: 6, L6: 1, HF: 1, Blog: 1, Friends: 1) |

Note: seed data lives in `data/seed.sql` — tests should verify the file is created by `init` and read correctly by `seed`.

### `compass track`

| ID | Case | Expected |
|---|---|---|
| T-01 | After `init` + `seed` | Writes raw line to `data/journal/<today>.md` |
| T-02 | `crm.db` does not exist | Still writes journal line (graceful degradation) |
| T-03 | Output mentions `/track` skill invocation | CLI output contains "Run `/track`" instruction |
| T-04 | Output lists existing active targets | Shows name, kind, tier, id prefix for each |
| T-05 | Empty or whitespace-only text | Handles gracefully (journal line may be empty-ish) |

### `compass analyze`

| ID | Case | Expected |
|---|---|---|
| A-01 | No DB | Prints "No database. Run `compass init` first." |
| A-02 | Invalid target_id | Prints "No target found with id: ..." |
| A-03 | Valid `target_bdy` after seed | Shows target header + all 2 lanes |
| A-04 | Lane with no touchpoints | Shows "(no touchpoints)" |
| A-05 | Lane with touchpoints | Shows all touchpoints with kind, summary, insights, next_step |
| A-06 | Output ends with skill invocation hint | "Run `/analyze <target_id>` in Claude Code for LLM synthesis" |

### `compass review`

| ID | Case | Expected |
|---|---|---|
| R-01 | No DB | Prints "No database." |
| R-02 | After seed | Shows 5 open lanes grouped by target |
| R-03 | Shows 20 most recent touchpoints | Sorted by `happened_at DESC` |
| R-04 | Output mentions `/review` skill | Ends with invocation hint |

### `compass sql`

| ID | Case | Expected |
|---|---|---|
| Q-01 | No DB | "No database." |
| Q-02 | Valid SELECT | Pretty-printed table with headers and row count |
| Q-03 | Non-SELECT statement | SQLite rejects with error (read-only enforcement) |
| Q-04 | Empty result | Prints "(no results)" |
| Q-05 | Invalid SQL | Prints "Error: ..." with SQLite error message |

### `compass migrate`

| ID | Case | Expected |
|---|---|---|
| M-01 | After `init` + `seed` | Idempotent — touchpoints and data unchanged |
| M-02 | `schema.sql` updated | Re-running applies changes without dropping data |

---

## 5. Schema Tests (`test_schema.py`)

| ID | Case | Expected |
|---|---|---|
| SC-01 | `UPDATE touchpoint` | Raises `ABORT` trigger error: "touchpoint is append-only" |
| SC-02 | `DELETE FROM touchpoint` | Raises `ABORT` trigger error: "touchpoint is append-only" |
| SC-03 | `UPDATE retro_brief` | Raises `ABORT` trigger error: "retro_brief is append-only" |
| SC-04 | `DELETE FROM retro_brief` | Raises `ABORT` trigger error: "retro_brief is append-only" |
| SC-05 | `UPDATE` on existing target | Allowed (mutable future) |
| SC-06 | `UPDATE` lane stage | Allowed (mutable future) |
| SC-07 | Foreign key: delete target with lanes | CASCADE deletes lanes + touchpoints |
| SC-08 | Foreign key: delete lane with touchpoints | RESTRICT — cannot delete lane with touchpoints |
| SC-09 | `PRAGMA foreign_keys = OFF` | FK enforcement still works (ON required in `get_db()`) |

---

## 6. End-to-End Workflows (`test_e2e.py`)

These tests run the full `compass` CLI binary and assert observable outputs. No DB inspection — just CLI stdout/stderr + filesystem.

### `seed → analyze` pipeline

| ID | Case | Expected |
|---|---|---|
| E2E-01 | `init` → `seed` → `analyze target_bdy` | Output contains "字节跳动", "L7 Staff Engineer", 6 touchpoint entries |
| E2E-02 | `init` → `seed` → `analyze target_hf` | Output contains "Hugging Face", "ML Engineer", 1 touchpoint |
| E2E-03 | `init` → `seed` → `review` | Contains all 5 lanes, recent touchpoints from multiple targets |

### `journal degraded write` pipeline

| ID | Case | Expected |
|---|---|---|
| E2E-04 | Remove write permission on `crm.db`, run `track` | Journal file still written, no crash |
| E2E-05 | No `crm.db` at all, run `track` | Journal file written with raw text |

### `track → upsert` pipeline (requires LLM stub)

| ID | Case | Expected |
|---|---|---|
| E2E-06 | `track` new text matching existing target | Journal written, upsert hint printed (no LLM required for CLI output) |

### Real-data override pipeline

| ID | Case | Expected |
|---|---|---|
| E2E-07 | After seed, update target via SQL, re-run `analyze` | Shows updated data |

---

## 7. Not in Scope

| Area | Reason |
|---|---|
| LLM agent synthesis quality | Human judgment required — reviewed manually |
| `/track`, `/analyze`, `/review` skill outputs | Require running Claude Code / OpenCode with skills installed |
| Performance / load testing | Single-user, local; scale is bounded by human typing speed |
| Network / auth | No network calls, no auth in design |

---

## 8. Test Data

All test data uses the cold-start seed as baseline fixture (`seeded_db`).

For tests requiring non-seed data (e.g. E2E-06), use controlled strings that are unambiguous:
- Target: `E2E Test Target` (kind: job)
- Lane: `E2E Test Lane` (kind: job_app)
- Touchpoint: `E2E test touchpoint`

No reliance on external fixtures or randomness.

---

## 9. Acceptance Criteria

- All tests run under `uv run pytest tests/` with zero external dependencies beyond Python stdlib + pytest
- Tests are isolated — each runs in a temp dir, zero side-effects on real `crm.db`
- Append-only trigger tests MUST fail if triggers are accidentally dropped (run with and without triggers)
- CI gate: tests must pass before any `git commit` (pre-commit hook or CI action)
