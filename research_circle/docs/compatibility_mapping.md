# Codex / Claude Code Compatibility Mapping

Canonical files live in `skills/` and `agents/`.

Claude Code mirrors are exposed under `.claude/skills` and `.claude/agents` through symbolic links.

## Behavior

- Stage logic text is identical across platforms.
- Invocation style differs:
  - Codex: reference file paths directly.
  - Claude Code: invoke as project skills/agents.

## Canonical Skills (v2)

- `skills/intake/SKILL.md`
- `skills/frontier-radar/SKILL.md`
- `skills/literature-search/SKILL.md`
- `skills/literature-map/SKILL.md`
- `skills/gap-mining/SKILL.md`
- `skills/taste-audit/SKILL.md`
- `skills/abstraction-lift/SKILL.md`
- `skills/idea-tree-search/SKILL.md`
- `skills/claim-novelty-check/SKILL.md`
- `skills/proposal-tournament/SKILL.md`
- `skills/construct-validity-audit/SKILL.md`
- `skills/research-planning/SKILL.md`
- `skills/run-postmortem/SKILL.md`

## Backward-Compatible Skill Aliases

- `skills/literature-review/SKILL.md` -> `literature-map`
- `skills/idea-generation/SKILL.md` -> `idea-tree-search`
- `skills/novelty-check/SKILL.md` -> `claim-novelty-check`
- `skills/proposal-ranking/SKILL.md` -> `proposal-tournament`

## Canonical Agents

- `agents/literature-scout.md`
- `agents/gap-analyst.md`
- `agents/idea-writer.md`
- `agents/novelty-critic.md`
- `agents/reviewer-panel.md`
- `agents/taste-critic.md`
- `agents/abstraction-architect.md`
- `agents/novelty-prosecutor.md`
- `agents/frontier-scout.md`
- `agents/benchmark-validity-auditor.md`
- `agents/venue-reviewer.md`
- `agents/cross-domain-analogist.md`
- `agents/negative-result-planner.md`

