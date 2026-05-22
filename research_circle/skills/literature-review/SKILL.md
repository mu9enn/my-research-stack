# Skill: literature-review (Compatibility Alias)

## Purpose

兼容旧阶段名。执行逻辑与 `literature-map` 相同，canonical stage 为 `literature-map`。

## Inputs

- `paper_bank.jsonl`
- `source_bank.jsonl`（可选）

## Outputs

- `runs/<run_id>/artifacts/literature_map.md`
- `runs/<run_id>/artifacts/contradiction_map.md`
- `runs/<run_id>/artifacts/evidence_strength_table.md`
- `runs/<run_id>/artifacts/unsupported_claims.md`

## Procedure

1. 使用 `skills/literature-map/SKILL.md` 的完整流程。
2. 在 checkpoint 中统一写入 `literature-map`。

## Stop Conditions

- 与 `literature-map` 完全一致。

## Human Checkpoint

- 推荐。

