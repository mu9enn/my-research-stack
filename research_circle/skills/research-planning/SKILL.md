# Skill: research-planning

## Purpose

将 shortlist proposal 转成可执行研究计划。

## Inputs

- `ranked_proposals.md`
- `review_report.json`

## Outputs

- `runs/<run_id>/artifacts/research_plan.md`
- `runs/<run_id>/checkpoints/research-planning.json`

## Procedure

1. 为 top proposal 生成 3天 / 2周 / 1月计划。
2. 定义最小可行实验、资源预算、里程碑、回退方案。
3. 将 reviewer 高优先级 objection 映射到执行动作。

## Stop Conditions

- 计划包含所有时间窗口与里程碑。
- 至少一个失败回退路径。

## Human Checkpoint

- 推荐：由人类确认后开始实际实验执行。

