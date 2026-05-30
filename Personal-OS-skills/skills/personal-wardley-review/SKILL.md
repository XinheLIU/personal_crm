---
name: personal-wardley-review
description: Use for self-review, personal strategy, personal positioning, Wardley mapping, SWOT, VRIO, capability review, and Socratic interviews that help the user understand their personal strategic terrain and decide what to own, outsource, productize, or stop doing. Include closure ability: what the user can test and compound personally, what requires employer/platform authority, and what needs industry status, credentials, senior relationships, or borrowed leverage.
---

# Personal Wardley Review

> Last updated: 2026-05-30

## Output style

- Default to short Markdown: 2-4 sections, one compact table when useful, 3-5 bullets per section.
- Lead with the strategic diagnosis; avoid long inventories unless the user asks.
- If an interview is needed, interview first and write the review after the interview, not before.

## When to use

Use this skill when the user asks for:

- Personal strategy, self-review, career positioning, capability diagnosis, or "what should I become?"
- Wardley map, SWOT, VRIO, resource review, personal moat, or personal PMF.
- A Socratic interview to reflect on the user's personal space, assets, and constraints.

This skill is the second stage of the strategy pipeline:

```text
DNS/opportunity -> Wardley/self-review -> rent/Alpha capture -> leverage/effectuation roadmap
```

Use it after a direction exists, or use it to clarify why no direction currently fits the user's terrain.

## Core workflow

1. **Collect evidence before judging.**
   - Read relevant files when available: `about-me/about-me.md`, `about-me/capabilities.md`, `resume/resume-zh.md`, `resume/resume-en.md`, `about-me/360-review*.md`, `user-next-step.md`, and related project notes.
   - Separate facts, self-interpretations, and hypotheses.

2. **Offer a Socratic interview before writing.**
   - If the user asks for an interview, Socratic reflection, or ambiguous self-review, first ask whether they want to actually do the interview now.
   - If they agree, ask one question per turn and wait for the answer before asking the next question.
   - Ask at most 3-5 pointed questions unless the user asks to continue.
   - Write the Wardley/SWOT/VRIO synthesis only after the interview is complete, or after the user explicitly says to skip the interview.
   - If the user only wants a direct review, do not interview; infer from files and include 3 optional reflection questions at the end.
   - Focus on: who pays, what the user naturally sees, what is commoditizing, what is uniquely hard to copy, and what work creates or drains energy.

3. **Build a personal Wardley map table.**
   - Vertical position: distance from the buyer/user outcome.
   - Horizontal position: Genesis, Custom-built, Product/Rental, Commodity/Utility.
   - Map capabilities, assets, relationships, delivery formats, tools, and identity claims.

4. **Map closure ability.**
   - Mark which capabilities can be tested and compounded personally with a small artifact, memo, template, prototype, or conversation.
   - Mark which capabilities require employer authority, proprietary data, team capacity, buyer access, or implementation context.
   - Mark which capabilities require industry status, credentials, senior relationships, or public reputation before they can capture value.
   - Ask whether the user is choosing a battlefield where their current ecology can win.

5. **Diagnose strategic moves.**
   - Own/build: high-value, close to user, early/custom, hard to copy.
   - Productize: repeated custom work that can move right into a reusable asset.
   - Buy/outsource: mature, standardized, low-user-visibility components.
   - Stop over-investing: commodity work used as a substitute for harder positioning.
   - Borrow leverage: when the component matters but cannot be closed personally yet.

6. **Combine with SWOT and VRIO.**
   - SWOT gives the current situation.
   - VRIO tests whether resources are valuable, rare, hard to imitate, and organizationally usable.
   - Wardley decides whether a capability should be owned, productized, rented, or ignored.

7. **Reflect back contradictions.**
   - Name mismatches between identity, evidence, market position, and current action.
   - Keep claims tied to evidence; if a claim is not supported by resume/project notes, mark it as a hypothesis.
   - Be explicit when a desired positioning is actually a status game that requires borrowed authority first.

## Questions to ask

Use these one by one during an interview, selected by context:

- Who is the real user or buyer of your work, and what outcome are they buying?
- Which part of your work is becoming cheap, common, or tool-assisted?
- Which part still requires judgment that others cannot copy quickly?
- What do people ask you for when the problem is ambiguous?
- What repeated custom work could become a product, method, checklist, template, or public asset?
- Which impressive capability is only a ticket to enter, not a source of advantage?
- Where are you using right-side work to avoid left-side uncertainty?
- Which battlefield can you personally close with your current ecology?
- Which battlefield requires employer brand, industry status, credentials, or a senior partner before value can be captured?

## Output format

Use this structure by default:

```markdown
## Diagnosis

- One-line diagnosis:
- Main tension:
- Strategic move:

## Wardley Map

| Component | Stage | Visibility | Closure | Move |
|-----------|-------|------------|---------|------|

## SWOT / VRIO

| Capability | SWOT/VRIO verdict | Action |
|------------|-------------------|--------|

## Next Reflection

- Question 1:
- Question 2:
- Question 3:
```

## Failure modes / avoid

- Do not treat technical difficulty as strategic value.
- Do not call something a personal asset if it depends entirely on the current employer's permission.
- Do not force every capability into a "moat"; some are just entry tickets.
- Do not skip the buyer/user question.
- Do not recommend a battlefield where the user cannot close, unless the strategic move is explicitly to borrow leverage.
- Do not let SWOT become a loose list; connect it to Wardley position and VRIO quality.

## Source notes

Primary sources:

- `principles/wardley-map.md` — value-chain visibility, evolution stages, own vs outsource logic.
- `about-me/`, `resume/`, `about-me/capabilities.md` — personal evidence when relevant.

Useful adjacent sources:

- `principles/dns-model.md` — market terrain.
- `principles/economic-rent.md` and `principles/alpha-beta.md` — value capture after the personal terrain is clear.
