# Compass — Frontend UI Implementation Plan

Last updated: 2026-05-12

---

## 1. Problem Statement

The current Compass system is fully CLI-driven. Non-technical users (or users
sharing Compass with someone) cannot:

- See all targets and their status at a glance without running SQL
- Edit target tier, lane stage, or deadlines without knowing the schema
- Browse touchpoint history for a lane
- Read/edit `north_star.md` and `profile.md` in a structured way

The AI-powered features (`track`, `analyze`, `review`) remain in the CLI.
The UI fills one gap: **data viewing and human-editing**. It is not the engine;
the engine stays Claude Code / opencode in the terminal.

---

## 2. Scope

### In scope — UI does this

| Capability | Notes |
|------------|-------|
| View all targets as cards (tier, kind, last touchpoint) | Dashboard |
| Drill into a target → lanes + touchpoints timeline | Target detail |
| Edit target: tier, status | Human curation only |
| Edit lane: stage, deadline, status | Human curation only |
| Add touchpoint manually (fallback path, no LLM) | For corrections only |
| View/edit `north_star.md` and `profile.md` | Plain textarea, save to disk |
| List retro briefs, view content | Read-only |

### Out of scope — stays in CLI

| Capability | Why |
|------------|-----|
| `compass track "..."` | LLM parsing; can't be replicated in UI without calling the LLM |
| `compass analyze <id>` | LLM synthesis; output appears in terminal |
| `compass review` | LLM strategy brief; output written to `data/retros/` |
| `compass init` / `migrate` | One-time ops; CLI is fine |

The UI is a **companion** to the CLI, not a replacement.

---

## 3. Architecture

### 3.1 Approach: minimal local Python server + single HTML page

```
Non-technical user
        │
        ▼
  Browser (localhost:7364)
        │  HTTP (fetch)
        ▼
  ui_server.py  ──────────  crm.db  (read + write)
  (Flask, ~250 lines)              ▲
        │                          │
        └── from db import get_db ─┘

  db.py  (shared DB access, ~25 lines)
        ── get_db(), DB_PATH, now_iso(), new_uuid()
```

`db.py` is extracted from `crm.py` so both `crm.py` and `ui_server.py` import
from it without dragging in each other's module-level side effects. `crm.py`
retains `PROJECT_ROOT`, `SCHEMA_PATH`, and the `_SEED_*` templates — only the
shared DB/utility functions move.

```
GET  /api/targets        → list active targets
GET  /api/targets/:id    → target + lanes + touchpoints
PATCH /api/targets/:id   → update tier / status
PATCH /api/lanes/:id     → update stage / deadline / status
POST  /api/touchpoints   → manual insert (no LLM)
GET  /api/files/:name    → read north_star.md / profile.md
PUT  /api/files/:name    → write north_star.md / profile.md
GET  /api/retros         → list retro_briefs
```

**Why not `viewer.html` + sql.js (the spec's §12 step 5 suggestion)?**
sql.js loads the entire DB into WASM memory and cannot write back to disk
without a round-trip through a download dialog or a Service Worker — too awkward
for a data-entry tool. A minimal local server makes writes trivial and shares
the same `get_db()` factory from `db.py`.

**Why not Streamlit?**
Streamlit is opinionated about layout and adds a dependency outside the current
stack. Flask is already implicitly in the Python stdlib neighborhood and keeps
the server to ~250 lines.

**Why not Electron / Tauri?**
Both require a build step. The design principle is zero build step.

### 3.2 Frontend

- Single `ui.html` file — no build step, no bundler, no npm
- Tailwind CSS via CDN (same pattern spec suggests for viewer.html)
- Alpine.js via CDN — 15 KB, provides reactivity without a framework
- Vanilla `fetch()` for all API calls
- No TypeScript, no JSX, no transpilation

### 3.3 Data flow

```
User edits tier in UI
        │
        ▼
PATCH /api/targets/:id  { "tier": "dream" }
        │
        ▼
ui_server.py → get_db() → UPDATE target SET tier=? WHERE id=?
        │
        ▼
200 OK  ──────────────→  Alpine.js re-renders card
```

Touchpoints remain append-only — the UI sends POST (insert), never PATCH/DELETE.
The append-only SQLite triggers are a backstop; the server also enforces this.

### 3.4 File layout

```
~/compass/
├── db.py                  # NEW: shared get_db(), DB_PATH, now_iso(), new_uuid()
├── ui_server.py           # NEW: Flask server, ~250 lines
├── ui.html                # NEW: Single-page app, ~500 lines
├── crm.py                 # MODIFIED: imports from db.py; adds `compass ui`
└── (everything else unchanged)
```

Three new files. `crm.py` refactored to import from `db.py`.

---

## 4. Pages / Views

### 4.1 Dashboard

```
┌─────────────────────────────────────────────────────────┐
│  compass                                [+ add target]  │
├─────────────────────────────────────────────────────────┤
│  DREAM          STRONG            TRY             COLD   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │字节跳动  │  │HuggingFc │  │My Blog   │           │
│  │ job      │  │ job      │  │ media    │           │
│  │2 lanes   │  │1 lane    │  │1 lane    │           │
│  │last: 3d  │  │last: 11d │  │last: 27d │           │
│  └──────────┘  └──────────┘  └──────────┘           │
└─────────────────────────────────────────────────────────┘
```

- Cards grouped by tier column (dream → strong → try → cold)
- Click card → Target Detail view
- Last touchpoint age shown (e.g., "3d ago") — red if >14 days

### 4.2 Target Detail

```
┌─────────────────────────────────────────────────────────┐
│  ← back    字节跳动    [job] [dream ▾]  [active ▾]    │
├─────────────────────────────────────────────────────────┤
│  Lane: L7 Staff Engineer (Go)     [interview] [active] │
│  ─────────────────────────────────────────────────────  │
│  2026-04-20  message   猎头Alice联系，推荐L7职位...      │
│  2026-04-22  call      与猎头Alice通话，了解团队...       │
│  2026-04-24  applied   正式提交L7申请...                 │
│  2026-04-28  call      第一轮技术面...                   │
│  2026-05-05  call      第二轮技术面...                   │
│  2026-05-08  message   三面定在周五...                   │
│                                                         │
│  Lane: L6 Senior Engineer (Go)    [applied] [active]   │
│  ─────────────────────────────────────────────────────  │
│  2026-04-25  applied   投递L6职位...                    │
└─────────────────────────────────────────────────────────┘
```

- Tier and status are inline dropdowns (PATCH on change)
- Lane stage is an inline dropdown (PATCH on change)
- Touchpoints shown chronologically (append-only — no edit/delete UI)

### 4.3 Files (north_star + profile)

```
┌─────────────────────────────────────────────────────────┐
│  Files         [North Star]  [Profile]                  │
├─────────────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────────────┐  │
│  │ # North Star                                      │  │
│  │                                                   │  │
│  │ ## This quarter's goals                           │  │
│  │ 1. Land staff engineering role...                 │  │
│  │                                                   │  │
│  └───────────────────────────────────────────────────┘  │
│                                              [Save]      │
└─────────────────────────────────────────────────────────┘
```

- Plain `<textarea>` — raw markdown, no WYSIWYG (non-technical users can read markdown)
- Auto-updates `Last updated:` line in the file on save
- File path is validated server-side (only `north_star.md` and `profile.md` allowed)

### 4.4 Retros

```
┌─────────────────────────────────────────────────────────┐
│  Review Briefs                                          │
├─────────────────────────────────────────────────────────┤
│  2026-05-10  Retro brief #1                    [view]  │
│  ─────────────────────────────────────────────────────  │
│  ## Retro — 2026-W19                                    │
│  ### What happened this cycle                          │
│  - Completed 2 rounds at ByteDance...                  │
│  ...                                                    │
└─────────────────────────────────────────────────────────┘
```

- List of retro_brief rows, newest first
- Click row to expand content_md inline
- Read-only (append-only invariant respected)

### 4.5 UI States (empty, error, loading)

**Loading state (all views):** Show a skeleton card grid (3 placeholder cards with
pulse animation) while the first fetch is in-flight. Tailwind's `animate-pulse` is
sufficient. No spinner.

**Empty dashboard:** When `/api/targets` returns `[]`, show a centered message:
"No targets yet. Run `compass track \"...\"` in the terminal to log your first interaction."
The terminal command is styled as a `<code>` block for copy-paste. No "+ add target" button
(targets are created as a side effect of `compass track`, not manually).

**Fetch failure:** When any API call fails (network error, 500, server down), show
an inline red banner at the top of the view: "Couldn't reach the server. Is
`uv run python ui_server.py` still running?" with a [Retry] button that re-fetches.

**PATCH conflict:** When a PATCH returns 400 (e.g., stage regression), show a toast
in the bottom-right corner that auto-dismisses after 4 seconds. The toast includes
the server's error message (e.g., "stage cannot go backwards (current: interview)").
The dropdown reverts to the previous value.

**Save success:** When a file PUT succeeds, show a brief green toast "Saved." that
auto-dismisses after 2 seconds. No toast on PATCH success (dropdown already reflects
the new value).

---

## 5. API Contract

All endpoints return JSON. Server is on `localhost:7364` (port configurable via
`COMPASS_UI_PORT` env var). Server binds to `127.0.0.1` only. No CORS needed —
`ui.html` is served from the same origin, so all `fetch()` calls are same-origin.

```
GET  /api/targets
     → [{ id, name, kind, tier, status, lane_count, last_touchpoint_at }]

GET  /api/targets/:id
     → { target, lanes: [{ ...lane, touchpoints: [...] }] }

PATCH /api/targets/:id
     body: { tier?, status? }   (only mutable fields accepted)
     → 200 | 400 (invalid tier/status value) | 404

PATCH /api/lanes/:id
     body: { stage?, deadline?, status? }
     Stage regression guard: server rejects PATCH if new stage ordinal < current.
     → 200 | 400 (regression or invalid) | 404

POST  /api/touchpoints
     body: { lane_id, kind, summary, insights?, next_step?, happened_at? }
     → 201 | 400 | 404

GET  /api/files/:name          name ∈ { north_star, profile }
     → { content: "..." }

PUT  /api/files/:name
     body: { content: "..." }
     Auto-updates "Last updated:" line before writing.
     → 200 | 400 (invalid name) | 500

GET  /api/retros
     → [{ id, period_iso, content_md, created_at }] newest-first
```

No authentication. The server binds to `127.0.0.1` only.

---

## 6. Tech Stack

| Layer | Choice | Reason |
|-------|--------|--------|
| Server | Flask (uv-managed) | ~250 lines, in Python, no new language; shares `get_db()` from crm.py |
| Frontend | Single `ui.html` | No build step; spec precedent (viewer.html) |
| CSS | Tailwind CDN | Same as spec suggestion; zero build |
| JS reactivity | Alpine.js CDN | 15 KB; avoids raw DOM manipulation without a framework |
| DB access | Shared `db.py` imported by both `crm.py` and `ui_server.py` | No module-level coupling; same pragma enforcement |

**Dependencies added:** `flask` (runtime), `pytest` (dev). Both uv-managed; confirmed in review.

---

## 7. Startup

No CLI integration needed. The server is self-contained:

```bash
uv run python ui_server.py                  # start on port 7364
COMPASS_UI_PORT=8080 uv run python ui_server.py  # custom port
```

`ui_server.py` calls `webbrowser.open("http://localhost:7364")` on startup
(suppress with `--no-open` flag). No `compass ui` subcommand — the CLI and
server are independent processes sharing only `db.py`.

---

## 8. Build Order

1. **Extract `db.py`** — move `get_db()`, `DB_PATH`, `now_iso()`, `new_uuid()` from
   `crm.py` into `db.py`. Update `crm.py` imports. Verify `compass init` + `compass sql` still work.
2. **`ui_server.py` skeleton** — Flask app, import from `db`, single `GET /` that
   serves `ui.html`. Verify it starts with `uv run python ui_server.py`.
3. **Dashboard endpoint** — `GET /api/targets` with lane count + last touchpoint date.
   Test with `compass sql` to verify data matches.
4. **`ui.html` dashboard view** — Tailwind + Alpine.js, card grid by tier column,
   fetch from `/api/targets` on load.
5. **Target detail endpoint** — `GET /api/targets/:id` with full lane+touchpoint graph.
6. **Target detail view** — timeline per lane, inline dropdowns for tier/stage.
7. **PATCH endpoints** — `PATCH /api/targets/:id`, `PATCH /api/lanes/:id`.
   Stage regression guard in server, not just DB trigger.
8. **Files view** — `GET/PUT /api/files/:name`, textarea + save button.
9. **Retros view** — `GET /api/retros`, expandable list.
10. **Manual POST touchpoint** — last; least critical path.

---

## 9. Failure Modes

| Scenario | Handling |
|----------|----------|
| `crm.db` not found on server start | Server prints error + exits with message "Run `compass init` first" |
| Stage regression via PATCH | Server returns 400 with message "stage cannot go backwards (current: interview)" |
| Write to append-only touchpoint | DB trigger raises ABORT; server returns 500 with message |
| File write fails (disk full, permissions) | Server returns 500; no partial write (write to temp file first) |
| User edits arbitrary file path via `/api/files/` | Server allowlist: only `north_star` and `profile` accepted |
| UI used while `compass track` is writing | SQLite's WAL mode handles concurrent reads/writes; no lock contention |

---

## 10. What Already Exists

| Existing piece | Reused |
|----------------|--------|
| `get_db()` in db.py | Extracted from crm.py; imported by both crm.py and ui_server.py |
| `schema.sql` / `crm.db` | Unchanged; server reads/writes it |
| `data/` directory layout | Unchanged |
| `north_star.md` / `profile.md` | Read and written by Files view |
| `data/retros/*.md` | Retro view reads from `retro_brief` table (DB row), not the markdown files |

---

## 11. NOT in Scope (explicit deferrals)

| Item | Rationale |
|------|-----------|
| LLM-powered track/analyze/review in the UI | AI engine stays in CLI; avoids duplicating prompt plumbing |
| Target creation via UI | `compass track` creates targets as a side effect; manual creation is edge case |
| Asset management UI | No lanes use assets in the seeded data yet; defer until a retro flags the gap |
| Mobile responsiveness | Single-user, single-device; desktop only for now |
| Auth / access control | Design principle: single user, no auth |
| Dark mode | Not requested |
| Markdown preview | Textarea is sufficient for editing north_star / profile |

---

## 13. Test Plan

Tests use `pytest` + Flask test client against a temporary `crm.db` seeded with
known data. No browser. Run with `uv run pytest test_ui.py`.

### Test cases

| # | Endpoint | Test | Verifies |
|---|----------|------|----------|
| 1 | `GET /api/targets` | Empty DB returns `[]` | Empty state JSON shape |
| 2 | `GET /api/targets` | Seeded DB returns targets with `lane_count` and `last_touchpoint_at` | JOIN correctness |
| 3 | `GET /api/targets/:id` | Valid ID returns `{target, lanes: [{...lane, touchpoints}]}` | Tree shape |
| 4 | `GET /api/targets/:id` | Unknown ID returns 404 + `{"error": "..."}` | Error shape |
| 5 | `PATCH /api/targets/:id` | Valid `{"tier": "dream"}` returns 200, DB reflects change | Write path |
| 6 | `PATCH /api/targets/:id` | Invalid field `{"kind": "job"}` returns 400 | Field allowlist |
| 7 | `PATCH /api/targets/:id` | Invalid value `{"tier": "unknown"}` returns 400 | CHECK constraint |
| 8 | `PATCH /api/targets/:id` | Unknown ID returns 404 | Not found |
| 9 | `PATCH /api/lanes/:id` | Valid `{"stage": "interview"}` returns 200 | Write path |
| 10 | `PATCH /api/lanes/:id` | Stage regression `{"stage": "open"}` when current=interview → 400 | Regression guard |
| 11 | `PATCH /api/lanes/:id` | Same stage `{"stage": "interview"}` when current=interview → 200 | Idempotent |
| 12 | `POST /api/touchpoints` | Valid body (all required fields) returns 201, DB has row | Manual insert |
| 13 | `POST /api/touchpoints` | Missing `summary` returns 400 | Required field validation |
| 14 | `GET /api/files/north_star` | Returns content of `north_star.md` | File read |
| 15 | `GET /api/files/unknown` | Returns 400 (name not in allowlist) | Allowlist enforcement |
| 16 | `PUT /api/files/north_star` | Writes content, `Last updated:` line updated | File write + date update |
| 17 | `GET /api/retros` | Empty DB returns `[]` | Empty state |
| 18 | `GET /api/retros` | Seeded DB returns rows newest-first | Sort order |

### db.py extraction regression

After extracting `db.py`, run the existing smoke checks:

```
compass init   → creates dirs + applies schema (verify crm.db exists)
compass seed   → inserts demo data (verify no import errors)
compass sql "SELECT COUNT(*) FROM target" → returns count
```

### Test fixture design

```python
@pytest.fixture
def client():
    """Create temp DB, seed with known data, return Flask test client."""
    import tempfile, os
    # Point db.DB_PATH to temp file
    # Run schema.sql
    # Insert one target, one lane, one touchpoint
    # Yield app.test_client()
    # Clean up temp file
```

---

## 14. Open Questions

1. **Port conflict**: `7364` is arbitrary. Should the server check if the port is
   in use and pick a different port or print a clear error?

2. **Browser auto-open**: `webbrowser.open()` works on macOS/Linux; Windows behavior
   varies. Acceptable for single-user local tool.

---

## GSTACK REVIEW REPORT

| Review | Trigger | Why | Runs | Status | Findings |
|--------|---------|-----|------|--------|----------|
| CEO Review | `/plan-ceo-review` | Scope & strategy | 0 | — | — |
| Codex Review | `/codex review` | Independent 2nd opinion | 0 | — | — |
| Eng Review | `/plan-eng-review` | Architecture & tests (required) | 1 | CLEAR | 6 issues, 0 critical gaps |
| Design Review | `/plan-design-review` | UI/UX gaps | 0 | — | — |

**VERDICT:** ENG CLEARED — ready to implement.
