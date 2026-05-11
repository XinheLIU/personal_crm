# TODOS

Last updated: 2026-05-11

---

## Orchestrator runtime decision

**What:** Choose and document the runtime backend for `crm.py`'s LLM invocation layer before building the orchestration step.

**Why:** The build architecture is "skills first, human validates manually, then automate." When `crm.py` needs to invoke the LLM programmatically, the invocation pattern is currently unspecified. Options: ms-agent (ModelScope), opencode subprocess, or Anthropic SDK direct. Picking the wrong one means rewriting the invocation layer.

**Pros:** Forces the decision at the right time (after skills are validated). Prevents building on an unverified assumption.

**Cons:** Blocks `crm.py` automation step until a runtime is chosen and tested.

**Context:** Originally the #1 risk in the design doc (unverified Claude Code subprocess). Revised architecture defers it safely — skills work manually first. Must be resolved before build order step 3 (adding `track` to `crm.py`). Verify each candidate with a minimal end-to-end call before committing.

**Depends on:** Skills built and validated manually (build order steps 1-4).

---

## `compass import <file>` — batch import of historical time records

**What:** A batch import command that parses a structured time log (CSV, toggl export, or daily markdown log) into touchpoints, bypassing the per-line LLM confirmation gate.

**Why:** `seed.py` provides synthetic test data. This is different: real historical data from actual work records. If you have weeks of structured time logs, importing them creates a high-quality initial corpus for Analyzer and Strategist — more valuable than synthetic seed data.

**Pros:** Unlocks the full Analyzer + Strategist loop without waiting two weeks of daily tracking. Strategist's budget calibration becomes meaningful immediately.

**Cons:** Requires knowing the format of your time records first. Format varies (Toggl CSV, manual daily log, etc.). Parser is custom per format.

**Context:** Design doc §"Leveraging Historical Time Records" identifies this explicitly. Not in the current build order. Add only after core system works end-to-end. Consider as `compass import --format toggl <file>` or `--format markdown <file>` to support multiple sources.

**Depends on:** Core system working (`init`, `track`, `analyze`, `review`).
