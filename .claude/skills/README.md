# Skills (gstack runtime)

This folder is a **skills-only** copy: workflow `SKILL.md` files, `bin/` helpers, the headless **browse** CLI (`browse/dist/browse`), and `browse/src` (required at runtime so the CLI can start the server).

The `gstack` entry is a **symlink to `.`** so instructions that reference `.claude/skills/gstack/...` resolve correctly when the agent runs from your repo root.

## If browse fails to start

Dependencies live next to this tree. From this directory run:

```bash
bun install
```

That installs `diff` and `playwright` for the browse server. Playwright may still need browser binaries (`bunx playwright install chromium` if launches fail).

## Upstream

Full source, tests, and install automation live at [github.com/garrytan/gstack](https://github.com/garrytan/gstack).
