# Skill: idea-generation (Compatibility Alias)

## Purpose

兼容旧阶段名。执行逻辑迁移到 `idea-tree-search`，canonical stage 为 `idea-tree-search`。

## Inputs

- `route_candidates.md`
- `problem_reframing_ladder.md`
- `gap_analysis.md`

## Outputs

- `runs/<run_id>/artifacts/idea_tree.json`
- `runs/<run_id>/artifacts/idea_mutations.md`
- `runs/<run_id>/artifacts/route_comparison.md`

## Procedure

1. 使用 `skills/idea-tree-search/SKILL.md` 生成树状候选。
2. 不再以 flat `ideas.json` 作为 canonical 输出。

## Stop Conditions

- 与 `idea-tree-search` 一致。

## Human Checkpoint

- 必需。

