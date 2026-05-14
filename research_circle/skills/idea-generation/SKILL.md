# Skill: idea-generation

## Purpose

基于 gap 生成 5-8 个候选 `idea_card`。

## Inputs

- `gap_analysis.md`
- `paper_bank.jsonl`

## Outputs

- `runs/<run_id>/artifacts/ideas.json`
- `runs/<run_id>/checkpoints/idea-generation.json`

## Procedure

1. 每个 idea 对应至少一个明确 gap。
2. 填写：假设、创新来源、方法草图、实验草图、风险、相似工作。
3. 计算初始三维评分：novelty/feasibility/impact。

## Stop Conditions

- ideas 数量在 5-8。
- 每个 idea 都有 `similar_work` 条目。

## Human Checkpoint

- 必需：由人类确认是否继续 novelty 检查。

