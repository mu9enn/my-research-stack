# Skill: proposal-ranking (Compatibility Alias)

## Purpose

兼容旧阶段名。执行逻辑迁移到 `proposal-tournament`，canonical stage 为 `proposal-tournament`。

## Inputs

- `idea_tree.json`
- `safe_claims.md`
- `taste_scores.json`

## Outputs

- `runs/<run_id>/artifacts/proposal_tournament.md`
- `runs/<run_id>/artifacts/reviewer_objections.json`
- `runs/<run_id>/artifacts/revision_actions.md`
- `runs/<run_id>/artifacts/ranked_proposals.md`

## Procedure

1. 使用 `skills/proposal-tournament/SKILL.md` 的多评审对抗流程。
2. 不再使用 `novelty/feasibility/impact` 三维作为唯一排序标准。

## Stop Conditions

- 与 `proposal-tournament` 一致。

## Human Checkpoint

- 必需。

