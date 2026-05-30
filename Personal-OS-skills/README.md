# Personal OS Skills

Last updated: 2026-05-30

A skill development and test-case folder for building personal strategic AI skills inside Compass.

## Provenance

This folder was absorbed into the root `personal-crm` repo from:

- Remote: `git@github.com:XinheLIU/Personal-Experience.git`
- Commit: `8f923f8`

Root Git now owns this folder. The original nested `.git/` metadata should not be restored unless the folder is intentionally split back into a separate repo.

## Two-layer structure

### Layer 1: Skills (`/skills/`)

The strategic skills Claude Code and Codex use in this repo. Both `.claude/skills` and `.codex/skills` are symlinks pointing to `/skills/` — single source of truth.

| Skill | When to use |
| --- | --- |
| `personal-strategy-system/` | Orchestrate the full personal strategy workflow and package skill-system learnings |
| `dns-opportunity-planning/` | Strategic planning, opportunity sizing, D/N/S analysis |
| `personal-wardley-review/` | Self-review, capability mapping, SWOT/VRIO |
| `value-capture-rent-alpha/` | Value capture design, economic rent, moat design |
| `effectual-leverage-roadmap/` | Tactical roadmap, low-cost experiments, leverage selection |
| `messy-to-mece/` | Distill messy notes into MECE topic files |

See [skills/README.md](skills/README.md) for details and [skills/TESTING.md](skills/TESTING.md) for test prompts and pass criteria.

### Layer 2: Test case content

The personal knowledge OS that serves as the primary test case for the skills above.

| Directory | Contents |
| --- | --- |
| `about-me/` | Identity, values, capability inventory (`capabilities.md` is authoritative) |
| `principles/` | Reference frameworks: Alpha/Beta, economic rent, Wardley, DNS, effectuation, leverage |
| `self-review/` | MECE four-part self-review (who / how others see you / where to go / what to do) |
| `resume/` | Source-of-truth work history (`resume-zh.md`, `resume-en.md`) |
| `动势经历/` | Detailed project and team records from 动势科技 |
| `user-next-step.md` | Active follow-up list and missing details |

## Symlink setup

```text
skills/                    ← canonical skill definitions
.claude/skills → ../skills
.codex/skills  → ../skills
```

Both Claude Code and Codex load skills from the same `/skills/` directory.
