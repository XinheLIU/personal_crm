---
name: personal-strategy-system
description: Use for full personal-development strategy synthesis, bottom-up personal OS planning, testing personal-development skills, forming a reusable strategy system, packaging strategy skills, or turning the user's personal evidence into concrete strategic assets and experiments. Orchestrates dns-opportunity-planning, personal-wardley-review, value-capture-rent-alpha, and effectual-leverage-roadmap in sequence.
---

# Personal Strategy System

> Last updated: 2026-05-30

## Output style

- Lead with the concrete direction and next artifact.
- Keep the default output short: 3-5 sections, one or two compact tables.
- Prefer assets, tests, and decisions over abstract career advice.
- State uncertainty as a testable assumption, not a long caveat.

## When to use

Use this skill when the user asks for:

- Personal development strategy, personal OS design, career/business direction, or a strategy system.
- A bottom-up workflow that starts from real personal evidence and produces reusable skills, methods, or assets.
- Testing, improving, or packaging the Personal OS skills into a coherent system.
- A full strategy pass across opportunity, capability terrain, value capture, and action roadmap.

This is the orchestration skill for the strategy pipeline:

```text
DNS/opportunity -> Wardley/self-review -> rent/Alpha capture -> leverage/effectuation roadmap
```

## Evidence to load

Read only the files needed for the user's request. Start with:

- `about-me/about-me.md` — identity, values, strategic tensions.
- `about-me/capabilities.md` — current capability inventory.
- `about-me/resume/resume-zh.md` or `about-me/resume/resume-en.md` — work-history facts when claims need verification.
- `self-review/action-plan.md` and `self-review/strategic-planning.md` — current direction and experiments.
- `user-next-step.md` — active todos and unresolved details.

Load principle files only when they affect the reasoning:

- `principles/dns-model.md` and `principles/opportunity-window.md` for opportunity timing.
- `principles/wardley-map.md` for capability terrain.
- `principles/economic-rent.md`, `principles/alpha-beta.md`, and `principles/value-capture.md` for capture design.
- `principles/effectuation.md` and `principles/business-leverage.md` for roadmap design.

Do not fabricate missing personal facts. If a claim is not supported by notes, mark it as an assumption or ask.

## Core workflow

1. **Frame the strategy question.**
   - Name the decision being made: direction, wedge, skill test, packaging boundary, or next action.
   - Separate current facts, user interpretation, and open assumptions.

2. **Run DNS opportunity planning.**
   - Generate 3-5 concrete opportunity hypotheses tied to the user's actual capabilities and relationships.
   - Score Demand / Narrative / Supply and judge the opportunity window.
   - Penalize opportunities that need authority, distribution, or delivery capacity the user does not control.

3. **Run personal Wardley review.**
   - Map buyer-visible capabilities and reusable assets.
   - Distinguish personal fast-loop capabilities from platform/status/relationship-dependent capabilities.
   - Identify what to own, productize, borrow, outsource, or stop over-investing in.

4. **Run value-capture / rent / Alpha design.**
   - Separate value creation from value capture.
   - Identify the capture point, rent type, proof asset, distribution path, and compounding loop.
   - Mark whether the Alpha is personally capturable now or requires borrowed leverage.

5. **Run effectual leverage roadmap.**
   - Start from bird-in-hand resources and affordable loss.
   - Choose one route: personal fast loop, platform/status leverage, relationship leverage, content/IP leverage, or deferral.
   - Produce small experiments that create reusable assets and real market signal.

6. **Package the learning loop.**
   - Convert the result into skill-system improvements: better prompts, test cases, principle notes, templates, or reusable assets.
   - Keep the near-term path explicit: develop and test personal-development skills first, form a strategy system, then package reusable skills later.

## Output format

Use this structure by default:

```markdown
## Recommendation

- Direction:
- Next artifact:
- Why now:

## Strategy Pipeline

| Stage | Verdict | Evidence | Decision |
|------|---------|----------|----------|
| DNS | | | |
| Wardley | | | |
| Rent / Alpha | | | |
| Effectuation | | | |

## Asset And Test Plan

| Asset / test | Purpose | Cost | Success signal | Kill or switch signal |
|--------------|---------|------|----------------|-----------------------|

## System Packaging

- Skill to improve:
- Test case to add:
- Principle or note to update:
- Packaging boundary:
```

## Failure modes / avoid

- Do not collapse the four-stage pipeline into generic advice.
- Do not recommend broad "AI transformation" positioning unless it has a concrete buyer, proof asset, and capture point.
- Do not make tool fluency the identity; use tools to express judgment.
- Do not package a skill before it has passed realistic personal test cases.
- Do not treat company-authorized work as personally capturable without naming the borrowed leverage.
- Do not add speculative structure; each new skill, file, or test should come from an observed strategy-system need.
