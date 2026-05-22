# Skill: construct-validity-audit

## Purpose

审查实验设计是否真正支撑论文 thesis，避免“实验清楚但 claim 不成立”。

## Inputs

- `ranked_proposals.md`
- `research_plan.md`（若已存在则增量审计）
- `proposal_tournament.md`

## Outputs

- `runs/<run_id>/artifacts/construct_validity_report.md`
- `runs/<run_id>/artifacts/experiment_thesis_alignment.json`
- `runs/<run_id>/checkpoints/construct-validity-audit.json`

## Core Checks

- main experiment tests thesis
- metrics support claims
- benchmark not toy
- baseline strong enough
- failure modes diagnostic
- ablations diagnostic
- negative result still useful

## Procedure

1. 对每条 shortlisted proposal 提取 `core_thesis`。
2. 审计实验-claim 对齐、指标有效性、baseline 强度与可诊断性。
3. 输出高风险 construct validity 缺陷及 required plan revisions。

## Stop Conditions

- `experiment_thesis_alignment.json` 满足 `construct_validity_report.schema.json`。
- `construct_validity_report.md` 包含每条 proposal 的风险与修订动作。

## Human Checkpoint

- 必需：通过后再进入 final research planning。

