#!/usr/bin/env python3
"""compass — single-user local personal CRM. SQLite + markdown, no server."""

import argparse
import sqlite3
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SCHEMA_PATH = PROJECT_ROOT / "schema.sql"
DB_PATH = PROJECT_ROOT / "crm.db"
DATA_DIR = PROJECT_ROOT / "data"
JOURNAL_DIR = DATA_DIR / "journal"
TARGETS_DIR = DATA_DIR / "targets"
ASSETS_DIR = DATA_DIR / "assets"
RETROS_DIR = DATA_DIR / "retros"
NORTH_STAR_PATH = PROJECT_ROOT / "north_star.md"
PROFILE_PATH = PROJECT_ROOT / "profile.md"

_SEED_NORTH_STAR = """# North Star

Last updated: {date}

## This quarter's goals (1-3)

1. [Goal — what are you pursuing?]
2. [Goal]
3. [Goal]

## Success criteria

- [How will you know you've made progress?]

## NOT chasing right now

- [What are you explicitly putting aside?]
"""

_SEED_PROFILE = """# Profile

Last updated: {date}

## Who I am

[Your current role, focus, and what you offer the world.]

## Core skills

- [Skill]
- [Skill]
- [Skill]

## Next-stage goals

- [What you're building toward — shaped by market feedback over time.]
"""


def get_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def new_uuid():
    return str(uuid.uuid4())


# ---------------------------------------------------------------------------
# commands
# ---------------------------------------------------------------------------

def cmd_init():
    """Create directories, seed files, and apply schema."""
    for d in [JOURNAL_DIR, TARGETS_DIR, ASSETS_DIR, RETROS_DIR]:
        d.mkdir(parents=True, exist_ok=True)

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    if not NORTH_STAR_PATH.exists():
        NORTH_STAR_PATH.write_text(_SEED_NORTH_STAR.format(date=today))

    if not PROFILE_PATH.exists():
        PROFILE_PATH.write_text(_SEED_PROFILE.format(date=today))

    schema = SCHEMA_PATH.read_text()
    conn = get_db()
    conn.executescript(schema)
    conn.commit()
    conn.close()

    print("compass init complete.")
    print(f"  DB:       {DB_PATH}")
    print(f"  Journal:  {JOURNAL_DIR}")
    print(f"  North Star: {NORTH_STAR_PATH}")
    print(f"  Profile:  {PROFILE_PATH}")


def cmd_migrate():
    """Re-apply schema.sql idempotently."""
    schema = SCHEMA_PATH.read_text()
    conn = get_db()
    conn.executescript(schema)
    conn.commit()
    conn.close()
    print("migrate complete.")


def cmd_track(text: str):
    """Write raw line to today's journal. LLM parsing is handled by the /track skill."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    journal_path = JOURNAL_DIR / f"{today}.md"
    ts = now_iso()

    if not journal_path.exists():
        journal_path.write_text(f"# {today}\n\n")

    entry = f"- [{ts}] {text}\n"
    with open(journal_path, "a") as f:
        f.write(entry)

    # Print context the /track skill would need
    print(f"Journaled to {journal_path}")
    print(f"Run `/track {text}` in Claude Code to parse into structured DB rows.")

    # Print existing targets/lanes for reference
    if DB_PATH.exists():
        conn = get_db()
        targets = conn.execute(
            "SELECT id, name, kind, tier FROM target WHERE status = 'active' ORDER BY name"
        ).fetchall()
        if targets:
            print("\nExisting active targets:")
            for t in targets:
                print(f"  [{t['kind']}] {t['name']} ({t['tier']}) — {t['id'][:8]}...")
        conn.close()
    else:
        print("\nNo database yet. Run `compass init` first.")


def cmd_analyze(target_id: str):
    """Read-only timeline for one target. LLM synthesis via /analyze skill."""
    if not DB_PATH.exists():
        print("No database. Run `compass init` first.")
        return

    conn = get_db()

    target = conn.execute("SELECT * FROM target WHERE id = ?", (target_id,)).fetchone()
    if not target:
        print(f"No target found with id: {target_id}")
        conn.close()
        return

    lanes = conn.execute(
        "SELECT * FROM lane WHERE target_id = ? ORDER BY created_at", (target_id,)
    ).fetchall()

    print(f"Target: {target['name']} ({target['kind']}) — {target['tier']} / {target['status']}")
    print(f"Created: {target['created_at']}")
    print()

    for lane in lanes:
        print(f"  Lane: {lane['title']} ({lane['kind']}) — {lane['stage']} / {lane['status']}")
        if lane["deadline"]:
            print(f"    Deadline: {lane['deadline']}")

        touchpoints = conn.execute(
            "SELECT * FROM touchpoint WHERE lane_id = ? ORDER BY happened_at",
            (lane["id"],),
        ).fetchall()

        if touchpoints:
            for tp in touchpoints:
                print(f"    [{tp['happened_at']}] {tp['kind']}: {tp['summary']}")
                if tp["insights"]:
                    print(f"      insights: {tp['insights']}")
                if tp["next_step"]:
                    print(f"      next_step: {tp['next_step']}")
        else:
            print("    (no touchpoints)")

        print()

    conn.close()
    print("Run `/analyze <target_id>` in Claude Code for LLM synthesis and recommendations.")


def cmd_review():
    """Dump open lanes + recent touchpoints. LLM synthesis via /review skill."""
    if not DB_PATH.exists():
        print("No database. Run `compass init` first.")
        return

    conn = get_db()

    open_lanes = conn.execute("""
        SELECT l.id, l.title, l.kind, l.stage, l.status, l.deadline,
               t.name AS target_name, t.kind AS target_kind, t.tier
        FROM lane l
        JOIN target t ON l.target_id = t.id
        WHERE l.status = 'active'
        ORDER BY t.tier, l.deadline
    """).fetchall()

    print("=== Open Lanes ===\n")
    for lane in open_lanes:
        print(f"  [{lane['target_kind']}] {lane['target_name']} ({lane['tier']})")
        print(f"    Lane: {lane['title']} — {lane['stage']}")
        if lane["deadline"]:
            print(f"    Deadline: {lane['deadline']}")
        print()

    recent = conn.execute("""
        SELECT tp.happened_at, tp.kind, tp.summary,
               l.title AS lane_title, t.name AS target_name
        FROM touchpoint tp
        JOIN lane l ON tp.lane_id = l.id
        JOIN target t ON l.target_id = t.id
        ORDER BY tp.happened_at DESC
        LIMIT 20
    """).fetchall()

    print("=== Recent Touchpoints (last 20) ===\n")
    for tp in recent:
        print(f"  [{tp['happened_at']}] {tp['target_name']} / {tp['lane_title']}")
        print(f"    {tp['kind']}: {tp['summary']}")
        print()

    conn.close()
    print("Run `/review` in Claude Code for full LLM synthesis and retro_brief generation.")


SEED_SQL_PATH = DATA_DIR / "seed.sql"


def cmd_seed():
    """Inject cold-start seed data from data/seed.sql so Analyzer and Strategist have content immediately."""
    if not DB_PATH.exists():
        print("No database. Run `compass init` first.")
        return
    if not SEED_SQL_PATH.exists():
        print(f"No seed data at {SEED_SQL_PATH}. Run `compass init` first.")
        return

    conn = get_db()
    conn.executescript(SEED_SQL_PATH.read_text())
    conn.commit()
    conn.close()
    print("Cold-start data seeded. Run `compass review` or /analyze on any target to see it in action.")


def cmd_sql(query: str):
    """Run a read-only SQL query and print results."""
    if not DB_PATH.exists():
        print("No database. Run `compass init` first.")
        return

    conn = get_db()
    try:
        rows = conn.execute(query).fetchall()
        if not rows:
            print("(no results)")
        else:
            cols = rows[0].keys()
            widths = [len(c) for c in cols]
            for row in rows:
                for i, val in enumerate(row):
                    widths[i] = max(widths[i], len(str(val)))

            header = " | ".join(c.ljust(widths[i]) for i, c in enumerate(cols))
            sep = "-+-".join("-" * widths[i] for i in range(len(cols)))
            print(header)
            print(sep)
            for row in rows:
                print(" | ".join(str(v).ljust(widths[i]) for i, v in enumerate(row)))
            print(f"\n({len(rows)} row(s))")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        prog="compass",
        description="Single-user local personal CRM. SQLite + markdown, no server.",
    )
    sub = parser.add_subparsers(dest="command", help="Available commands")

    sub.add_parser("init", help="Create directories, seed files, and apply schema")
    sub.add_parser("seed", help="Inject cold-start demo data (targets + lanes + touchpoints)")
    sub.add_parser("migrate", help="Re-apply schema.sql idempotently")

    p_track = sub.add_parser("track", help="Record an interaction (journal + structured)")
    p_track.add_argument("text", help="Free-text description of the interaction")

    p_analyze = sub.add_parser("analyze", help="Show timeline for one target")
    p_analyze.add_argument("target_id", help="Target UUID (or prefix)")

    sub.add_parser("review", help="Dump open lanes and recent touchpoints")

    p_sql = sub.add_parser("sql", help="Run a read-only SQL query")
    p_sql.add_argument("query", help="SQL SELECT statement")

    args = parser.parse_args()

    if args.command == "init":
        cmd_init()
    elif args.command == "seed":
        cmd_seed()
    elif args.command == "migrate":
        cmd_migrate()
    elif args.command == "track":
        cmd_track(args.text)
    elif args.command == "analyze":
        cmd_analyze(args.target_id)
    elif args.command == "review":
        cmd_review()
    elif args.command == "sql":
        cmd_sql(args.query)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
