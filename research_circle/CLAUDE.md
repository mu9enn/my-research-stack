# Full Circle: Project Memory (v2)

## Positioning

Taste-first, claim-centric scientific exploration copilot.

This project is not a local autonomous pipeline runner. Reasoning flow is controlled by skills/agents in interactive sessions.

## Non-Negotiable Rules

1. Do not implement orchestration logic in Python.
2. Use stage artifacts for handoff; do not rely on hidden context.
3. Keep novelty decisions evidence-backed with source links.
4. Required human checkpoints for v2: `gap-mining`, `taste-audit`, `abstraction-lift`, `idea-tree-search`, `proposal-tournament`, `construct-validity-audit`.

## Directory Contracts

- Canonical skills: `skills/*/SKILL.md`
- Canonical agents: `agents/*.md`
- Atomic tools only: `tools/bin/*.py`
- Artifact schemas: `specs/schemas/*.schema.json`

## Platform Mapping

- Codex: use `skills/` and `agents/` directly.
- Claude Code: consume mirrors in `.claude/skills` and `.claude/agents`.

