# Skill: literature-review

## Purpose

从 `paper_bank` 形成领域地图和问题分层。

## Inputs

- `paper_bank.jsonl`

## Outputs

- `runs/<run_id>/artifacts/literature_map.md`

## Procedure

1. 按任务、方法、评测、数据集聚类。
2. 提取每簇代表论文与核心结论。
3. 标注证据链（paper_id/url）。
4. 输出结构化地图：趋势、共识、分歧。

## Stop Conditions

- `literature_map.md` 至少包含 3 个主题簇。
- 每个主题簇至少 3 篇引用。

## Human Checkpoint

- 非强制。

