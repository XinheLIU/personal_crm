# Compass — Personal CRM & Profile Companion

*Last updated: 2026-05-09.*

> A single-user system for what you're pursuing and what you're selling. Remembers every interaction with companies, projects, or people, surfaces where each target stands, and uses market feedback to iteratively refine your personal profile, resume, and next-stage goals.

*The directory is currently `~/personal-crm/`. To match the name: `mv ~/personal-crm ~/compass`. Names are convention.*

---

## 1. What this is

Most productivity tools track **tasks**. Compass tracks **targets** (companies you want to join, projects you want to ship, social networks/friends you want to cultivate) and **your profile** (what you "sell" to the world). Tasks are the wake of the boat; targets are where the boat is going, and your profile is the engine.

Fundamentally, this system is a unified triad: **Personal Management + CRM (Client/Target Management) + Asset Management**.

Three core agents drive this system:

- **Tracker** (formerly Logger) captures every interaction (a call, a reply, a post, a meet) into structured form, in seconds. (The Input Layer)
- **Analyzer** (formerly Companion) answers "where am I with X target?" — full timeline + what's overdue + what's next. It acts as your strategic CRM partner. (The CRM Layer)
- **Strategist** (formerly Weekly) conducts periodic reviews (复盘). It doesn't just look at one week; it extracts lessons from past goals, turns past reviews into valuable personal assets, iterates your profile, and decides next steps. (The Personal & Asset Management Layer)

It runs locally. SQLite for structured data, markdown for narrative, Claude Code as the runtime. No server, no cloud, no auth. Single user.

Current priority order: **求职 > 自媒体 > others**. Encoded as one line in one prompt; flip in 10 seconds when life shifts.

---

## 2. Design philosophy

1. **Targets, not tasks.** A target persists across weeks; a task is one move toward it. The system is target-shaped at every layer.
2. **You are the product (Sell out).** This system is built for individual value realization. You are constantly iterating what you offer the world based on market feedback.
3. **Iterative Profile.** Every interaction with a company or person is a signal. The system uses these signals to continuously update your personal profile, resume, and next-stage work and learning goals.
4. **Time is the only currency.** Where business CRMs track money, Compass tracks half-days. Every plan is denominated in half-days because that is what is actually scarce.
5. **Log first, organize later.** The only required habit is `/track`. The system stays useful for months with no other agent turned on.
6. **Milestone-driven Reviews (复盘).** Quarterly: `north_star.md`. Periodic/Milestone: `retro_brief`. Daily: track. Reviews aren't strictly bound to a 7-day week; they happen when a cycle or project completes, turning past targets into personal iteration assets.
7. **Append-only past, mutable future.** Touchpoints and review briefs are immutable — searchable, trustworthy. Stages and statuses (the "where are we" of a target) are mutable.
8. **The agent is a prompt.** Editing `prompts/strategist.md` is deploying a new strategist. No code change, no redeploy.
9. **Bias as policy.** "Job > media" is one line in one prompt. Reverse it in 10 seconds when life flips.
10. **The system earns its complexity.** New agent, new table, new column — only added when a `retro_brief` explicitly says it was missed last time.
11. **Single user, single device.** No auth, no sync, no cloud. Backup = `git init && git push` on the directory.
12. **Graceful degradation.** If every agent breaks, you still have a fully searchable journal of every interaction. That alone is worth using.

---

## 3. Agents

Three core agents. Each = one prompt file + one slash command + a thin SQL helper. No class hierarchy, no orchestrator, no asyncio. The CLI is a 200-line Python file that gathers data, calls Claude Code with the relevant skill, and applies any DB writes the LLM returns as JSON.

### 3.1 Tracker — captures every interaction

**Purpose.** Turn one free-text sentence into a structured `(target, lane, touchpoint)` row, without you clicking through forms.

**Trigger.** `compass track "..."` (which routes to slash command `/track`).

**What it does:**
- Parses the sentence with `prompts/tracker.md`.
- Creates a new target / lane if needed; otherwise reuses existing ones.
- Appends a `touchpoint` with `summary`, `insights`, `next_step`.
- Advances `lane.stage` if the input clearly signals progression ("got an offer" → `Offer`).
- Always writes the raw line to today's `data/journal/<yyyy-mm-dd>.md`, even if the DB write fails.

**What it does NOT do:**
- Generate plans or recommendations (that is Analyzer / Strategist).
- Modify past touchpoints — append-only.
- Pick `tier` for new targets — that is a human call. New targets default to `try`.
- Summarize or grade the interaction's value.

**Failure mode.** If the LLM is down, the journal markdown is still written. Recovery = re-run `compass track` against the journal lines later.

### 3.2 Analyzer — per-target CRM and insight

**Purpose.** Answer "where am I with X?" — deep dive into a specific company, project, or person.

**Trigger.** `compass analyze <target_id>` → `/analyze`.

**What it does:**
- Loads one target's full graph: all lanes, all touchpoints, linked assets, the relevant section of `north_star.md`.
- Outputs: CRM status per lane, last meaningful interaction, what was promised, what's overdue, recommended next move.

**What it does NOT do:**
- Compare across targets ("which of my five offers is best?") — that is the Strategist.
- Mutate anything — read-only by design.
- Make up data — if there are 0 touchpoints, it says so.

**Failure mode.** The underlying SQL query alone usually gives you the raw timeline. The LLM layer adds synthesis, not data.

### 3.3 Strategist — periodic review, asset extraction, and planning

**Purpose.** Conduct milestone or periodic reviews (复盘), extract insights into personal assets, decide ≤5 actions for the coming cycle, and update your personal profile based on market feedback.

**Trigger.** `compass review` → `/review`.

**What it does:**
- Pulls touchpoints from the recent cycle + all open lanes.
- Reads `north_star.md` and your current `profile.md`.
- Runs Analyzer as a sub-agent on the top-N hot targets (recent activity OR upcoming deadline).
- Synthesizes a `retro_brief`: ≤5 actions, ≤8 half-days total, biased toward your priorities.
- **Asset Extraction:** Turns past goals and interactions into personal iteration assets (e.g., "Why did this project stall?").
- Extracts learnings from the market to suggest iterations to your `profile.md` (e.g., "Company X valued skill Y, update resume to highlight Y" or "Need to learn Z for next stage").
- Writes `data/retros/<iso>.md` and appends a row to `retro_brief`.

**What it does NOT do:**
- Generate daily TODOs — the brief is the prompt for your own day planning.
- Track in-week execution — `compass track` handles that.
- Assign — every action is a recommendation, not a command.
- Touch the past — never edits old briefs.

**Failure mode.** Without LLM synthesis, you still have the raw "open lanes + recent touchpoints" dump from the SQL pull. Plan from that.

---

## 4. Tables

Five tables plus one freeform markdown file (`north_star.md`).

### 4.1 `target` — who or what you're pursuing
A target is anything that takes more than one interaction to convert. A company you want to join. A community you want a foothold in. A reader segment for your blog. A potential collaborator.

- **Records:** name, kind (`job` / `media` / `community` / `collaborator`), tier (`dream` / `strong` / `try` / `cold`), status, `notes_path`, `created_at`.
- **Answers:** Who am I pursuing? How seriously? Are they active or dormant?
- **Does NOT hold:** the interactions (those are touchpoints), the threads of pursuit (those are lanes), the people inside the target (free text in `notes_path`, not a separate table).

### 4.2 `lane` — one thread of pursuit within a target
One target can have many lanes. ByteDance is one target; "L7 staff eng" and "L6 senior" are two lanes. Your blog is one target; each post is a lane.

- **Records:** `target_id`, kind (`job_app` / `content` / `event` / `outreach`), title, stage, deadline, optional `asset_id`, status.
- **Answers:** What concrete pursuit is this? What stage? What's due?
- **Does NOT hold:** the history (touchpoints), the strategy (north_star), the artifact (asset).

### 4.3 `touchpoint` — a single interaction
The atomic unit. Every call, reply, application, post, meet, mention.

- **Records:** `lane_id`, kind (`applied` / `call` / `message` / `post` / `meet` / `reply`), summary, insights, next_step, `happened_at`.
- **Answers:** What did I do, when, what did I learn, what did I commit to next?
- **Append-only.** Once written, never UPDATE or DELETE. The journal must be trustworthy.
- **Does NOT hold:** strategy or rollups — those are derived in Analyzer / Strategist.

### 4.4 `asset` & `profile.md` — what you offer the world
Your "shop": resume, blog, GitHub, talks, side projects, social accounts. Lanes link to assets (a job application uses a resume version; a blog post is part of your blog). Additionally, your `profile.md` serves as the core master document of who you are and what you offer.

- **Records:** name, kind (`resume` / `blog` / `repo` / `talk` / `side_project`), stage (`idea` / `prototype` / `public` / `maintained`), `artifact_path`, `last_touched_at`.
- **Answers:** What's in my shop? What's stale? What's mature enough to deploy? How is my profile evolving based on market feedback?
- **Does NOT hold:** the artifact itself (that is a file at `artifact_path`), or feedback on it (that lives in touchpoints linked to lanes that used the asset).

### 4.5 `retro_brief` — your review and decision history
The append-only trail of periodic syntheses (复盘).

- **Records:** `period_iso`, `content_md` (full text), `created_at`.
- **Answers:** What did I decide last cycle? What assets and lessons did I extract? Did I follow through? (Cross-reference touchpoints from that cycle.)
- **Does NOT hold:** edits — if you edit `data/retros/<iso>.md`, that is your annotation, separate from the immutable DB row.

### 4.6 `north_star.md` & `profile.md` — your strategy & self-definition (no DB)
Two single hand-written markdown files. Not tables.

- **north_star.md holds:** 1–3 goals for the current quarter, success criteria, what you are explicitly NOT chasing.
- **profile.md holds:** Your current personal "Sell out" proposition, core skills, and next-stage learning/work goals iteratively shaped by periodic feedback.
- **Answers:** When the strategist synthesis has to choose, what should it prefer? Who am I becoming?
- **Does NOT hold:** task lists, OKRs, KPIs. Direction only.

---

## 5. The iteration cycle

```
each day        compass track "..."        → touchpoint (+ upsert target/lane)

periodic        compass review             → reads recent cycle data
(e.g. weekly)                              → runs /analyze on hot targets
                                           → extracts lessons for assets/profile
                                           → ≤5 actions, ≤8 half-days
                                           → writes data/retros/<iso>.md
                                           → appends retro_brief

each quarter    edit north_star.md         → manual; rare
```

That is the entire rhythm. Reviews (复盘) turn raw logs into permanent assets. No daily standups, no arbitrary monthly reporting.

---

## 6. Stack

- Runtime: Claude Code (skills, slash commands, sub-agents)
- Structured store: SQLite `crm.db`
- Unstructured store: filesystem markdown + assets
- LLM: Claude via Claude Code
- CLI: one Python file `crm.py` (uv-run)
- MCP: official SQLite MCP server, mounted read-only on `crm.db`

No web server, no ORM, no auth, no Docker, no asyncio.

---

## 7. Layout

```
~/compass/                        # rename from ~/personal-crm/ if you like
├── crm.db
├── schema.sql
├── north_star.md
├── profile.md                    # the living personal profile and value proposition
├── crm.py                        # the CLI; binary on $PATH = `compass`
├── prompts/
│   ├── tracker.md
│   ├── analyzer.md
│   └── strategist.md
├── skills/
│   ├── track/SKILL.md
│   ├── analyze/SKILL.md
│   └── review/SKILL.md
└── data/
    ├── journal/<yyyy-mm-dd>.md
    ├── targets/<id>/notes.md
    ├── assets/<id>/
    └── retros/<iso>.md
```

---

## 8. Schema

```sql
target(id TEXT PRIMARY KEY, name, kind, tier, status,
       notes_path, created_at)

lane(id TEXT PRIMARY KEY, target_id, kind, title, stage,
     deadline, asset_id, status, created_at, closed_at)

touchpoint(id TEXT PRIMARY KEY, lane_id, kind, summary,
           insights, next_step, happened_at)
-- append-only

asset(id TEXT PRIMARY KEY, name, kind, stage,
      artifact_path, last_touched_at)

retro_brief(id TEXT PRIMARY KEY, period_iso, content_md, created_at)
-- append-only
```

UUIDs generated in Python. ISO-8601 timestamps. `touchpoint` and `retro_brief` are append-only.

---

## 9. CLI

```bash
compass init                        # create dirs + apply schema
compass migrate                     # reapply schema.sql idempotently
compass track "..."                 # → /track
compass analyze <target_id>         # → /analyze
compass review                      # → /review
compass sql "<query>"               # raw read query
```

Each verb opens `crm.db`, gathers context, invokes Claude Code with the matching skill, and commits the JSON-shaped DB writes the skill returns.

---

## 10. Tracker contract

Input: free-text journal sentence.

Output JSON the CLI applies to the DB:

```json
{
  "target":     {"upsert": true, "name": "...", "kind": "..."},
  "lane":       {"upsert": true, "title": "...", "kind": "...", "stage": "..."},
  "touchpoint": {"kind": "...", "summary": "...", "insights": "...", "next_step": "..."}
}
```

First 50 entries: confirm with user before commit. After that: auto-commit, but log the JSON to that day's journal md.

If interpretation is ambiguous, return `{"choices": [<option1>, <option2>]}` and ask before writing.

---

## 11. Evolution

- Edit `prompts/*.md` to change agent behavior — no code change.
- Drop a new `skills/<name>/SKILL.md` to add `/name`.
- Schema change: edit `schema.sql`, run `compass migrate` (idempotent CREATE/ALTER).
- A new agent earns a slot only after a `retro_brief` explicitly flags its absence.

---

## 12. Build order

1. `schema.sql` + `compass init` + `prompts/tracker.md` + `skills/track/SKILL.md` — `/track` works.
2. Two weeks of daily `compass track` only, nothing else.
3. `prompts/strategist.md` + `skills/review/SKILL.md` — minimal synthesis: dump open lanes and ask.
4. `prompts/analyzer.md` + `skills/analyze/SKILL.md` — only after a retro brief asks for it.
5. `viewer.html` (sql.js + Tailwind CDN, no build step) — only after ≥50 touchpoints in DB.

---

## 13. The Future Vision: A True Hybrid-Data Agent

While Compass starts as a local, prompt-driven tool, its architectural trajectory is moving toward a highly autonomous, context-aware AI agent capable of mastering both complex structured and unstructured data. 

**Where this system is heading:**

1. **Passive Omnichannel Capture (Unstructured → Structured):**
   Instead of manually invoking `/track`, the future Tracker will act as a continuous background sensor. It will passively ingest unstructured streams—emails, browser sessions, chat logs, and calendar events—and autonomously synthesize them into structured `touchpoint` records and CRM updates without human intervention.

2. **Complex Hybrid Memory System:**
   The boundary between SQLite tables and Markdown files will blur. Compass will evolve into a hybrid memory engine combining relational databases (for status and timelines), vector databases (for semantic search of past ideas, lessons, and industry reports), and Knowledge Graphs (mapping complex relationship networks between people, companies, and skills).

3. **Proactive Market Intelligence:**
   The Analyzer and Strategist won't just look inward at your past data. They will ingest external, unstructured market data (industry trends, job descriptions, tech news) and cross-reference it against your `profile.md`. The agent will proactively suggest new targets ("Company X is expanding in your field, I've drafted an outreach email") rather than waiting for you to find them.

4. **The Ultimate "Digital Twin" for Value Realization:**
   Ultimately, Compass becomes more than a tracking system; it becomes your personal proxy and "Digital Twin". With deep historical context of every interaction, a perfect understanding of your goals (`north_star.md`), and your evolving assets (`profile.md`), the agent will autonomously tailor your resume for specific opportunities, draft context-perfect communications, and continuously iterate your "Sell out" proposition against real-world market feedback.
