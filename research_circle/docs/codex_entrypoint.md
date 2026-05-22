# Codex Entrypoint Guide (v2)

## Start a run

```bash
./bin/fc init-run --topic "Domain-general research direction"
```

## Suggested interaction flow

1. Execute `skills/intake/SKILL.md` -> `research_brief.json`
2. (Recommended) Execute `skills/frontier-radar/SKILL.md` -> `frontier_radar.md`, `source_bank.jsonl`
3. Execute `skills/literature-search/SKILL.md` -> `paper_bank.jsonl`
4. Execute `skills/literature-map/SKILL.md` -> literature map + contradiction/evidence outputs
5. Continue stage by stage using canonical v2 workflow
6. Pause at required human checkpoints

## Canonical v2 stages

`intake -> frontier-radar -> literature-search -> literature-map -> gap-mining -> taste-audit -> abstraction-lift -> idea-tree-search -> claim-novelty-check -> proposal-tournament -> construct-validity-audit -> research-planning -> run-postmortem`

## Stage aliases accepted by CLI

- `literature-review` -> `literature-map`
- `idea-generation` -> `idea-tree-search`
- `novelty-check` -> `claim-novelty-check`
- `proposal-ranking` -> `proposal-tournament`

## Tool usage rule

Use only atomic tools in `tools/bin/` when a stage needs deterministic data operations.

