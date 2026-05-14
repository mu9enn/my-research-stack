# Skill: intake

## Purpose

将模糊研究方向收敛成可执行的 `research_brief`。

## Inputs

- 用户方向描述
- 资源/时间约束
- 目标会议或投稿档位

## Outputs

- `runs/<run_id>/artifacts/research_brief.json`

## Procedure

1. 抽取方向、约束、资源、目标 venue、禁止项。
2. 若缺关键字段，给出最小补全建议并显式记录假设。
3. 输出符合 `research_brief.schema.json` 的 JSON。

## Stop Conditions

- `research_brief.json` 存在且字段完整。

## Human Checkpoint

- 非强制。

