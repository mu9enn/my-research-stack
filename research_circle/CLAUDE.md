# Full Circle: Project Memory

## Positioning

A-conference oriented research idea discovery copilot.

This project is not a local autonomous pipeline runner. The reasoning flow is controlled by skills/agents in interactive agent sessions.

## Non-Negotiable Rules

1. Do not implement orchestration logic in Python.
2. Use stage artifacts for handoff; do not rely on hidden context.
3. Keep novelty decisions evidence-backed with source links.
4. Human checkpoint is required at `gap-mining`, `idea-generation`, and `proposal-ranking`.

## Directory Contracts

- Canonical skills: `skills/*/SKILL.md`
- Canonical agents: `agents/*.md`
- Atomic tools only: `tools/bin/*.py`
- Artifact schemas: `specs/schemas/*.schema.json`

## Platform Mapping

- Codex: use `skills/` and `agents/` directly.
- Claude Code: consume mirrored files in `.claude/skills` and `.claude/agents`.

