# Skill Testing Guide

Last updated: 2026-05-30

These skills are not executable programs — the right test is a **trigger + behavior test**: give prompts that should clearly activate each skill, then check whether the response follows that skill's output contract.

---

## 1. Personal Strategy System

```text
Use the personal-strategy-system skill. Based on about-me/about-me.md, about-me/capabilities.md, self-review/action-plan.md, self-review/strategic-planning.md, and user-next-step.md, run the full bottom-up personal strategy workflow. Use DNS opportunity planning, personal Wardley review, value capture/rent/Alpha design, and effectual leverage roadmap in order. Output concrete strategy assets, tests, next actions, and what should be improved in the Personal OS skills before packaging.
```

Pass criteria:
- Output has `Strategy Pipeline`
- Uses all four stages: DNS, Wardley, Rent / Alpha, Effectuation
- Produces concrete assets/tests, not abstract career advice
- Explicitly mentions the bottom-up path: test personal-development skills first, form the strategy system, then package reusable skills
- Converges on a portable asset such as `AI Agent 场景价值评估矩阵 v0.1`

---

## 2. DNS Opportunity Planning

```text
Use the DNS opportunity planning skill. Based on about-me/about-me.md, about-me/capabilities.md, rank 3-5 strategic opportunities for me. Focus on AI Agent, data science, O2O/pharma/ToB, and personal asset building. Output D/N/S scores, opportunity-window judgment, resource fit, and next tests.
```

Pass criteria:
- Output has `Opportunity Ranking`
- Distinguishes Demand / Narrative / Supply
- Does not recommend generic "AI agent" positioning
- Likely ranks "AI Agent 场景价值评估矩阵 / AI-native business decision loops" near the top

---

## 3. Personal Wardley Review

```text
Use the personal Wardley review skill. Based on about-me/about-me.md and about-me/capabilities.md, build a personal Wardley map for my capabilities. Identify what I should own/build, productize, outsource, or stop over-investing in. Include SWOT/VRIO synthesis and Socratic reflection questions.
```

Pass criteria:
- Output has a `Personal Wardley Map` table
- Tool fluency / prompt / framework usage lands on the right side
- Business diagnosis, Agent evaluation, causal/data loop design lands closer to the left side
- Warns against making tool fluency the identity

---

## 4. Value Capture / Rent / Alpha

```text
Use the value-capture-rent-alpha skill. Assume my current strategic direction is: helping enterprise/growth teams identify, design, and evaluate AI-native business decision loops. Based on about-me/capabilities.md and self-review/action-plan.md, design my value-capture system: offer, buyer, capture point, rent type, proof asset, distribution, pricing logic, and compounding loop.
```

Pass criteria:
- Separates value creation from value capture
- Identifies plausible rent types: information rent, reputation rent, method/IP rent, relationship rent
- Does not say "just do consulting"
- Produces concrete assets: scorecard, diagnostic matrix, case note, benchmark, template

---

## 5. Effectual Leverage Roadmap

```text
Use the effectual leverage roadmap skill. Based on self-review/action-plan.md and about-me/about-me.md, turn my direction into a 30-day action plan. Use bird-in-hand, affordable loss, leverage type, experiment sequence, success signal, kill signal, and decision checkpoints. Assume I can spend 20 hours, 0 budget, and some reputation risk.
```

Pass criteria:
- Output has `Bird-in-Hand Inventory`, `Affordable Loss`, `Leverage Choice`, and `Roadmap`
- First action is small: matrix/template/article/interviews, not building a big product
- Includes the `AI Agent 场景价值评估矩阵 v0.1` idea
- Defines success/kill signals

---

## End-to-End Test

```text
Run the full four-skill workflow based on about-me/about-me.md, about-me/capabilities.md, and self-review/action-plan.md. First choose strategic opportunities with DNS, then do personal Wardley review, then design value capture with rent/Alpha, then produce an effectual leverage roadmap. Keep it concise and make the final recommendation actionable.
```

Expected final recommendation should converge roughly to:

```text
Build a portable personal asset around AI Agent scene/value evaluation:
AI Agent 场景价值评估矩阵 v0.1
+ 10 scenario examples
+ 3 feedback interviews
+ 1 public/private memo
```

If the skill names are not mentioned or required section formats are not followed, the trigger descriptions in the SKILL.md files may need to be strengthened.
