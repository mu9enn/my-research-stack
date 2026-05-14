# Skill: proposal-ranking

## Purpose

从候选 ideas 中形成 1-3 个深度 proposal 并排序。

## Inputs

- `ideas.json`
- `novelty_check.md`

## Outputs

- `runs/<run_id>/artifacts/ranked_proposals.md`
- `runs/<run_id>/artifacts/review_report.json`
- `runs/<run_id>/checkpoints/proposal-ranking.json`

## Procedure

1. 剔除不可执行或高撞题且无替代路线的 ideas。
2. 输出 top 1-3 proposal，附三维评分与排序理由。
3. 使用 reviewer-panel 给出反对意见与修订建议。

## Stop Conditions

- ranked proposals 数量在 1-3。
- 每个 proposal 包含 novelty/feasibility/impact 评分。

## Human Checkpoint

- 必需：人类审批最终 shortlist。

