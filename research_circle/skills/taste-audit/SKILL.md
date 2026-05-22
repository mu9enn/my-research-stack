# Skill: taste-audit

## Purpose

独立审查 topic 的 research taste，决定是否触发抽象提升与问题重构。

## Inputs

- `literature_map.md`
- `gap_analysis.md`
- `frontier_radar.md`（可选，推荐）
- `research_brief.json`

## Outputs

- `runs/<run_id>/artifacts/taste_audit.md`
- `runs/<run_id>/artifacts/taste_scores.json`
- `runs/<run_id>/checkpoints/taste-audit.json`

## Procedure

1. 按 10 维 rubric 打分并写出证据。
2. 回答强制问题：
   - 是局部补丁还是结构性问题？
   - 是否只是 benchmark/tool/demo？
   - 是否存在更高抽象层？
   - 能否形成长期研究议程？
   - 顶会 reviewer 最可能如何拒稿？
3. 应用决策规则：
   - `representative_work_potential <= 3` -> 触发 `abstraction-lift`
   - `abstraction_level <= 3` -> 触发 `abstraction-lift`
   - `reviewer_defensibility <= 3` -> 在 proposal 比选前强制 `claim-novelty-check`

## Score Dimensions

- problem_importance
- abstraction_level
- novelty_robustness
- non_incrementality
- external_validity
- field_timing
- theory_potential
- benchmark_construct_validity
- representative_work_potential
- reviewer_defensibility

## Stop Conditions

- `taste_scores.json` 满足 `taste_scores.schema.json`。
- `taste_audit.md` 包含评分证据、拒稿风险、触发规则结果。

## Human Checkpoint

- 必需：确认 risk 偏好与是否允许 pivot。

