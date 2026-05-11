# TODOS

Last updated: 2026-05-11

---

## Infrastructure

### Orchestrator runtime decision

**What:** Choose and document the runtime backend for `crm.py`'s LLM invocation layer before building the orchestration step.

**Why:** When `crm.py` needs to invoke the LLM programmatically, the invocation pattern is unspecified. Options: ms-agent (ModelScope), opencode subprocess, or Anthropic SDK direct. Picking the wrong one means rewriting the invocation layer.

**Context:** Originally the #1 risk in the design doc (unverified Claude Code subprocess). Revised architecture defers it safely — skills work manually first. Must be resolved before build order step 3 (adding `track` to `crm.py`). Verify each candidate with a minimal end-to-end call before committing.

**Effort:** M
**Priority:** P1
**Depends on:** Skills built and validated manually (build order steps 1–4).

---

## CLI

### `compass import <file>` — batch import of historical time records

**What:** A batch import command that parses a structured time log (CSV, Toggl export, or daily markdown log) into touchpoints, bypassing the per-line LLM confirmation gate.

**Why:** Real historical data from actual work records creates a high-quality initial corpus for Analyzer and Strategist — more valuable than synthetic seed data. Unlocks the full Analyzer + Strategist loop without waiting weeks of daily tracking.

**Context:** Design doc §"Leveraging Historical Time Records" identifies this explicitly. Not in the current build order. Add only after core system works end-to-end. Consider `compass import --format toggl <file>` or `--format markdown <file>` to support multiple sources.

**Effort:** L
**Priority:** P3
**Depends on:** Core system working (`init`, `track`, `analyze`, `review`).

---

## Completed

<!-- Items moved here when shipped, with: **Completed:** vX.Y.Z.W (YYYY-MM-DD) -->
