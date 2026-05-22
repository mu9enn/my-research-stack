# Skill: intake

## Purpose

将模糊研究方向收敛为可执行、可审计的 `research_brief`，并显式写出 taste 目标与风险偏好。

## Inputs

- 用户方向描述
- 资源/时间约束
- 目标会议或投稿档位
- 用户偏好（可选）：`taste_target`、`risk_preference`、`desired_abstraction_level`、`must_not_be`

## Outputs

- `runs/<run_id>/artifacts/research_brief.json`
- `runs/<run_id>/checkpoints/intake.json`

## Procedure

1. 抽取方向、约束、资源、目标 venue、禁止项。
2. 若缺关键字段，先给最小补全并写入显式假设。
3. 设置默认偏好：`taste_target=main-track`、`risk_preference=balanced`、`desired_abstraction_level=framework`。
4. 输出符合 `research_brief.schema.json` 的 JSON。

## Stop Conditions

- `research_brief.json` 存在且必填字段完整。
- taste/风险偏好字段已给出（来自用户或默认值）。

## Human Checkpoint

- 推荐：确认目标档位、风险偏好与 pivot 许可。

