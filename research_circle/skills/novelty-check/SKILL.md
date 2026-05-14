# Skill: novelty-check

## Purpose

执行平衡过滤：保留边界案例，但必须标注撞题风险与证据。

## Inputs

- `ideas.json`
- `paper_bank.jsonl`

## Outputs

- `runs/<run_id>/artifacts/novelty_check.md`

## Procedure

1. 对每个 idea 检索高相似论文（标题/摘要/方法关键词）。
2. 计算相似度并判定风险等级：red/amber/green。
3. red/amber 案例提供替代方向建议。
4. 记录证据链接（source URL + paper_id）。

## Stop Conditions

- 所有 ideas 均完成风险标签。
- red/amber ideas 均有替代建议。

## Human Checkpoint

- 非强制。

