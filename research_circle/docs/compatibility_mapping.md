# Codex / Claude Code Compatibility Mapping

Canonical files live in `skills/` and `agents/`.

Claude Code mirrors are exposed under `.claude/skills` and `.claude/agents` through symbolic links.

## Behavior

- Stage logic text is identical across platforms.
- Only invocation style differs:
  - Codex: reference file paths directly.
  - Claude Code: invoke as project skills/agents.

## Canonical Skills

- `skills/intake/SKILL.md`
- `skills/literature-search/SKILL.md`
- `skills/literature-review/SKILL.md`
- `skills/gap-mining/SKILL.md`
- `skills/idea-generation/SKILL.md`
- `skills/novelty-check/SKILL.md`
- `skills/proposal-ranking/SKILL.md`
- `skills/research-planning/SKILL.md`

## Canonical Agents

- `agents/literature-scout.md`
- `agents/gap-analyst.md`
- `agents/idea-writer.md`
- `agents/novelty-critic.md`
- `agents/reviewer-panel.md`

