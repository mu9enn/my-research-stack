# Skill: literature-map

## Purpose

从 `paper_bank` 构建结构化文献版图，并显式输出矛盾证据与未被支撑的 claim。

## Inputs

- `paper_bank.jsonl`
- `source_bank.jsonl`（可选）

## Outputs

- `runs/<run_id>/artifacts/literature_map.md`
- `runs/<run_id>/artifacts/contradiction_map.md`
- `runs/<run_id>/artifacts/evidence_strength_table.md`
- `runs/<run_id>/artifacts/unsupported_claims.md`
- `runs/<run_id>/checkpoints/literature-map.json`

## Procedure

1. 按任务、方法、评测、数据集聚类，并给出代表性工作。
2. 标注每个簇的 primary/secondary evidence strength。
3. 输出文献间矛盾点和可能成因（数据、设定、指标、假设）。
4. 列出当前证据不足以支撑的高风险 claim。

## Stop Conditions

- `literature_map.md` 至少包含 3 个主题簇。
- 每个主题簇至少 3 篇引用。
- `contradiction_map.md` 至少包含 2 组冲突证据。

## Human Checkpoint

- 推荐：确认 evidence quality 与 coverage。

