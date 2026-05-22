# Skill: research-planning

## Purpose

将 shortlist proposal 转成可执行研究计划，并强制吸收 construct validity 审计结果。

## Inputs

- `ranked_proposals.md`
- `proposal_tournament.md`
- `reviewer_objections.json`
- `construct_validity_report.md`
- `experiment_thesis_alignment.json`

## Outputs

- `runs/<run_id>/artifacts/research_plan.md`
- `runs/<run_id>/checkpoints/research-planning.json`

## Procedure

1. 为 top proposal 生成 3天 / 2周 / 1月计划。
2. 将 construct validity 风险映射到具体修订任务（benchmark、metric、baseline、ablation）。
3. 明确负结果 fallback 的可发表价值与分析产出。
4. 输出资源预算、里程碑、回退方案。

## Stop Conditions

- 计划覆盖所有时间窗口与里程碑。
- construct validity 的 required revisions 已映射进执行计划。
- 至少一个失败回退路径可形成可解释结果。

## Human Checkpoint

- 推荐：计划确认后开始实验执行。

