# Skill: novelty-check (Compatibility Alias)

## Purpose

兼容旧阶段名。执行逻辑迁移到 `claim-novelty-check`，canonical stage 为 `claim-novelty-check`。

## Inputs

- `idea_tree.json`
- `literature_map.md`
- `source_bank.jsonl`

## Outputs

- `runs/<run_id>/artifacts/claim_graph.json`
- `runs/<run_id>/artifacts/collision_matrix.md`
- `runs/<run_id>/artifacts/safe_claims.md`
- `runs/<run_id>/artifacts/claims_to_avoid.md`

## Procedure

1. 使用 `skills/claim-novelty-check/SKILL.md` 的 claim-level 审查流程。
2. 不再将 `novelty_check.md` 作为 canonical 输出。

## Stop Conditions

- 与 `claim-novelty-check` 一致。

## Human Checkpoint

- 推荐。

