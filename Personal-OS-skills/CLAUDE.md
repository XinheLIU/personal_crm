# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Last updated: 2026-05-30

## What this repo is

A skill development and test-case folder inside Compass. It has two layers:

1. **Skills** (`/skills/`) — strategic AI skills loaded by Claude Code and Codex via symlinks from `.claude/skills` and `.codex/skills`. This is the canonical location for all skill definitions.
2. **Test case** — a personal knowledge OS for 刘昕和 (Xinhe Liu) that serves as the primary test case for those skills. No code, no build system — all Markdown.

## Repo structure

- `skills/` — canonical skill definitions. `.claude/skills` and `.codex/skills` are both symlinks here.
  - `personal-strategy-system/` — orchestration skill for the full bottom-up personal strategy workflow
  - `dns-opportunity-planning/` — strategic planning, opportunity sizing, D/N/S analysis
  - `personal-wardley-review/` — self-review, capability mapping, SWOT/VRIO
  - `value-capture-rent-alpha/` — value capture design, economic rent, moat design
  - `effectual-leverage-roadmap/` — tactical roadmap, low-cost experiments, leverage selection
  - `messy-to-mece/` — distill messy notes into MECE topic files
  - `README.md` — skill directory intro
  - `TESTING.md` — test prompts and pass criteria for each skill
- `about-me/` — personal identity and capability map. `capabilities.md` is the authoritative skill inventory; `about-me.md` is values/identity reflection.
- `resume/` — `resume-zh.md` and `resume-en.md` are the source-of-truth for work history. Do not change these unless explicitly asked.
- `动势经历/` — detailed records of work at 动势科技: projects, responsibilities, business solutions, team management.
- `self-review/` — MECE four-part self-review. Each file owns a distinct layer:
  - `self-analysis.md` — WHO: identity, core pattern, strengths
  - `360-review-principles.md` — HOW OTHERS SEE YOU: 6 perspectives (self/manager/peer/report/client/market)
  - `strategic-planning.md` — WHERE TO GO: market mismatches, Alpha/Beta, Wardley map, blind spots, recommended position
  - `action-plan.md` — WHAT TO DO: 4 phases, experiments, operating rules
- `principles/` — reference frameworks: Alpha/Beta, economic rent, Wardley map, DNS model, effectuation, leverage, opportunity window, value capture.
- `user-next-step.md` — active todo list and items needing follow-up.

## Key conventions

- When updating any Markdown file, update the `Last updated:` date near the top.
- Do not commit to git unless explicitly told to.
- Use `uv` for any Python tooling, not `pip`.
- `capabilities.md` must stay reconciled with the resume — claims there should be verifiable from resume experience. When in doubt, interview the user rather than assume.
- `user-next-step.md` is the place to park items that need user input or future detail (e.g., "fill in OpenClaw details").
- Resume files are the ground truth for dates, roles, and achievements. `about-me/` files are derived from them, not the other way around.
- The near-term development path is bottom-up: test personal-development skills on real personal evidence, form a strategy system, then package reusable skills.
