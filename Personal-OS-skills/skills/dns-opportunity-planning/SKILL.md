---
name: dns-opportunity-planning
description: Use for strategic planning, opportunity search or sizing, market timing, D/N/S analysis, opportunity-window diagnosis, and advising the user based on what they are doing, who they have recently interacted with, what assets they have, and what resources they can mobilize. Challenge broad enterprise AI, organization redesign, or consulting-heavy opportunities when they cannot close with the user's current ecology; abstract surface trends into bottom-layer capabilities and classify the route as personal fast loop, platform/status leverage, relationship leverage, content/IP leverage, or not now.
---

# DNS Opportunity Planning

> Last updated: 2026-05-30

## Output style

- Default to short Markdown: 2-4 sections, one compact table when useful, 3-5 bullets per section.
- Lead with the recommendation; put supporting diagnosis after it.
- Do not produce exhaustive strategy reports unless the user explicitly asks.

## When to use

Use this skill when the user asks for:

- Strategic direction, market entry, opportunity discovery, or opportunity sizing.
- D/N/S, Demand/Narrative/Supply, opportunity window, trend timing, or "is it too early / too late?"
- Suggestions based on the user's current work, recent contacts in context, personal assets, or resource constraints.

This skill is the first stage of the strategy pipeline:

```text
DNS/opportunity -> Wardley/self-review -> rent/Alpha capture -> leverage/effectuation roadmap
```

If the user already has a strategic direction, skip broad opportunity search and use this skill to test timing and fit.

## Core workflow

1. **Ground in context first.**
   - Read relevant current notes if available: active file, `about-me/`, `resume/`, `capabilities.md`, `user-next-step.md`, and recent conversation context.
   - Extract: current activities, assets, skills, constraints, relationships, and any recently mentioned people or organizations.

2. **Define candidate opportunities.**
   - Prefer 3-5 concrete opportunity hypotheses.
   - Phrase each as: `for [buyer/user], use [resource/capability] to solve [urgent problem] through [offer/channel]`.
   - Do not list generic trends unless they connect to the user's actual resources.

3. **Run a scope sanity check.**
   - Penalize opportunities that are too large, consulting-heavy, status-dependent, or impossible for one person to close.
   - Treat "enterprise AI transformation" and "organization redesign" as long-term narratives unless the user already has authority, distribution, and delivery capacity.
   - Abstract each surface opportunity into its bottom-layer capability, e.g. `AI agent project` -> `judging which business decisions should be systemized, automated, modeled, or left human`.
   - Ask: can this create a closed loop with current resources, or does it require borrowed leverage?

4. **Score D/N/S timing.**
   - **D / Demand**: who pays, budget migration, painful urgency, tolerance for imperfect products.
   - **N / Narrative**: whether the market has a legitimate name, social proof, capital/media attention, and career/business legitimacy.
   - **S / Supply**: how crowded the field is, whether competitors have standardized the offer, and whether price competition is emerging.

5. **Judge the opportunity window.**
   - Too early: dominant category is not formed; education cost is high.
   - Best window: dominant category exists, but dominant design is not locked.
   - Too late: dominant design is locked; new entrants need exceptional differentiation.

6. **Add capability/resource fit and route classification.**
   - Score whether the user's capability is stable, transferable, and defensible.
   - Include resource fit from: time, money, credibility, data, distribution, team, tools, and relationships.
   - If recent contacts are in context, identify which opportunities they can validate, unlock, or distort.
   - Classify each opportunity route:
     - `personal fast loop`: can be tested with a small artifact, interview, memo, template, or prototype.
     - `platform/status leverage`: requires employer brand, industry authority, credentials, senior role, or stronger institutional context.
     - `relationship leverage`: requires a partner who owns domain trust, buyer access, or implementation capacity.
     - `content/IP leverage`: can compound through standards, frameworks, writing, templates, or tools.
     - `not now`: too broad, too status-dependent, or too hard to close.

7. **Recommend next tests.**
   - Each test should reduce uncertainty in demand, narrative, supply, or resource fit.
   - Prefer low-cost interviews, landing pages, paid pilots, public writing, prototype demos, or partner conversations.
   - For platform/status opportunities, recommend job/company selection criteria instead of fake personal experiments.

## Questions to ask

Ask only when the answer is not already in repo notes or conversation context:

- Who is the buyer or decision-maker you can actually reach within 30 days?
- What asset do you have that would still matter if common AI/tools became cheap?
- Which recent contact could validate demand, provide distribution, or become a first partner?
- What loss is acceptable for the next test: time, money, reputation, relationship capital?
- Are you optimizing for cash now, capability accumulation, or future position?
- Does this opportunity close personally, or does it require borrowed platform/status/relationship leverage?
- What is the bottom-layer capability underneath the surface trend?

## Output format

Use this structure by default:

```markdown
## Recommendation

- Direction:
- Why:
- Tradeoff:

## Opportunity Ranking

| Rank | Opportunity | D/N/S | Window | Route | Next test |
|------|-------------|-------|--------|-------|-----------|

## Key Diagnosis

- Resource fit:
- Main risk:
- Scope check:

## Next Tests

| Test | Tests what | Cost | Success signal | Kill signal |
|------|------------|------|----------------|-------------|
```

## Failure modes / avoid

- Do not recommend opportunities just because the market is hot.
- Do not confuse strong narrative with real demand.
- Do not let broad enterprise AI / organization redesign consulting pass as a first wedge unless the user has authority, status, distribution, and delivery capacity.
- Do not stop at the surface trend; name the bottom-layer capability that could form Alpha.
- Do not dismiss a crowded market without checking whether the user has a sharp wedge.
- Do not fabricate recent contacts or resources; mark unknowns and ask.
- Do not produce a strategy without a next test that can falsify it.

## Source notes

Primary sources:

- `principles/dns-model.md` — D/N/S curves, stages, capability fit.
- `principles/opportunity-window.md` — dominant category vs dominant design timing.

Useful adjacent sources:

- `principles/alpha-beta.md` — Alpha requires the right window and differentiated action.
- `principles/effectuation.md` — use when uncertainty is high and the next step should start from current means.
