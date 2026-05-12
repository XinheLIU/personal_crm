# Tracker

Last updated: 2026-05-11

Parse one free-text sentence into structured `(target, lane, touchpoint)` data. Return JSON the caller applies to the database. Read `schema.sql` for the full schema; what follows is the parsing contract.

## Data model (summary)

- **target** — who/what you're pursuing. `kind` ∈ {job, media, community, collaborator}. `tier` ∈ {dream, strong, try, cold}. Default tier for new targets: `try`.
- **lane** — one thread of pursuit within a target. `kind` ∈ {job_app, content, event, outreach}. `stage` ∈ {open, applied, screening, interview, offer, rejected, closed}. Default stage: `open`.
- **touchpoint** — one interaction. `kind` ∈ {applied, call, message, post, meet, reply}. `summary` (required, 1-2 sentences). `insights` and `next_step` (optional). Append-only — never update or delete.

A target can have many lanes. A lane can have many touchpoints.

## Parsing rules

1. **Identify the target.** Extract the company, project, community, or person from the text. Match against existing targets in the DB when possible (by name + kind). If no match, flag as new (upsert). New targets get `tier: "try"`, `status: "active"`.

2. **Identify the lane.** What specific thread of pursuit? For job targets, this is usually a role. For media, a piece of content. For community, an event or relationship. If this is a new thread, flag as new lane (upsert). If continuing an existing one, reference it.

3. **Classify the interaction (touchpoint kind):**
   - `applied` — submitted application, proposal, pitch
   - `call` — phone or video call
   - `message` — email, DM, text, any async written communication
   - `post` — published content (blog, social, repo)
   - `meet` — in-person or face-to-face meeting
   - `reply` — received a response from the other side

4. **Detect stage progression.** If the text signals a clear lane stage change, reflect it:
   - "applied to X" → stage: `applied`
   - "got an interview" / "screening call scheduled" → stage: `screening` or `interview`
   - "received an offer" → stage: `offer`
   - "got rejected" / "didn't get it" → stage: `rejected`
   - "finished" / "shipped" / "published" → stage: `closed`
   If unclear, leave stage unchanged.

5. **Write the touchpoint.** `summary` is 1-2 sentences capturing what happened. `insights` = what you learned (optional). `next_step` = what you committed to do next (optional).

## Ambiguity

If the text reasonably maps to 2+ different target/lane interpretations, return:

```json
{"choices": [<option1>, <option2>]}
```

## Output format

For a single clear interpretation:

```json
{
  "target":     {"upsert": true, "name": "...", "kind": "..."},
  "lane":       {"upsert": true, "title": "...", "kind": "...", "stage": "..."},
  "touchpoint": {"kind": "...", "summary": "...", "insights": "...", "next_step": "..."}
}
```

If the target/lane already exist and you're identifying them by name, `upsert: true` is correct — the CLI resolves duplicates via the unique index. Omit fields that aren't present in the text. `insights` and `next_step` are optional; omit them when they'd be empty strings.

## Examples

> "Applied to Google Cloud staff eng role"

```json
{
  "target": {"upsert": true, "name": "Google", "kind": "job"},
  "lane": {"upsert": true, "title": "Cloud staff eng", "kind": "job_app", "stage": "applied"},
  "touchpoint": {"kind": "applied", "summary": "Submitted application for staff eng role in Google Cloud."}
}
```

> "Had coffee with Alice from Stripe. She said the backend team is growing and uses Go. I'll send my resume by Friday."

```json
{
  "target": {"upsert": true, "name": "Stripe", "kind": "job"},
  "lane": {"upsert": true, "title": "Backend role (via Alice)", "kind": "job_app", "stage": "open"},
  "touchpoint": {
    "kind": "meet",
    "summary": "Coffee with Alice, a contact at Stripe.",
    "insights": "Backend team growing, uses Go.",
    "next_step": "Send resume by Friday."
  }
}
```

> "Published my static analysis blog post"

```json
{
  "target": {"upsert": true, "name": "My Blog", "kind": "media"},
  "lane": {"upsert": true, "title": "Static analysis post", "kind": "content", "stage": "closed"},
  "touchpoint": {"kind": "post", "summary": "Published blog post on static analysis."}
}
```

> "Got rejected from the Jane Street internship"

```json
{
  "target": {"upsert": true, "name": "Jane Street", "kind": "job"},
  "lane": {"upsert": true, "title": "Internship", "kind": "job_app", "stage": "rejected"},
  "touchpoint": {"kind": "reply", "summary": "Received rejection for internship application."}
}
```

## Rules

- Never invent data not present in the input.
- New targets always default to `tier: "try"`.
- Match against existing DB rows by name+kind before creating new ones — but if unsure, upsert by name is safe (the unique index on target(name, kind) handles dedup).
- Keep summaries factual and tight. No filler adjectives.
- When genuinely ambiguous, return choices. When slightly unclear, make your best call.
