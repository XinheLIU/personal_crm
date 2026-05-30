# Skills

Last updated: 2026-05-30

Strategic AI skills for personal career and business thinking. Both `.claude/skills` and `.codex/skills` are symlinks pointing here — single source of truth.

`personal-strategy-system` is the orchestration layer. The four core strategy skills form its workflow: DNS sets strategic direction → Wardley maps your capability terrain → Value Capture designs how rent flows to you → Effectuation turns it into a concrete action plan.

## The Skills

### 1. `personal-strategy-system/`

**When:** You want the full bottom-up personal strategy workflow, or you are testing and packaging the Personal OS skills into a coherent strategy system.

Orchestrates DNS, Wardley, Value Capture, and Effectuation in sequence. Loads personal evidence from `about-me/`, `self-review/`, `principles/`, and `user-next-step.md`. Outputs concrete strategy assets, tests, next actions, and skill-system improvements.

---

### 2. `dns-opportunity-planning/`

**When:** You want to evaluate or rank strategic opportunities — career moves, business directions, personal bets.

Analyzes opportunities across three dimensions: Demand (is there real pull?), Narrative (is the story strong?), Supply (how crowded is it?). Diagnoses the opportunity window (too early / best entry / crowded / closing) and maps fit against your current resources. Outputs ranked opportunities with D/N/S scores and suggested next tests.

---

### 3. `personal-wardley-review/`

**When:** You want to understand your capability terrain — what to own, productize, outsource, or stop over-investing in.

Builds a personal Wardley map: places your capabilities on a visibility-to-buyer × evolution-stage grid. Combines with SWOT/VRIO analysis. Uses Socratic interview questions to surface blind spots. Distinguishes what you can compound personally from what requires employer platform, industry status, or borrowed leverage.

---

### 4. `value-capture-rent-alpha/`

**When:** Strategic direction is clear and you want to design how value flows back to you.

Separates value creation from value capture. Identifies which rent types apply (information rent, reputation rent, method/IP rent, relationship rent). Designs the full capture system: offer, buyer, capture point, proof assets, distribution, pricing logic, and compounding loop. Flags when capture requires institutional authority or senior relationships rather than personal action.

---

### 5. `effectual-leverage-roadmap/`

**When:** You have a direction and need a concrete action plan with low downside.

Uses effectuation (bird-in-hand, affordable loss) rather than goal-first planning. Selects a leverage route: personal fast loop, platform/status leverage, relationship leverage, or content/IP leverage. Outputs a sequenced roadmap with success signals, kill signals, and decision checkpoints. Revises previous strategic thinking once a direction is set.

---

### 6. `messy-to-mece/`

**When:** You have a dense, mixed-topic markdown file (journal, stream-of-consciousness notes) and want it distilled into clean, MECE topic files.

Reads the source file, identifies distinct topics, and writes each into a separate file in a sibling subfolder. Includes a post-delivery reflection loop that proposes improvements to the skill itself.

---

## Testing

See [TESTING.md](TESTING.md) for test prompts and pass criteria for each skill.
