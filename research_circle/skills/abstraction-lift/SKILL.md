# Skill: abstraction-lift

## Purpose

将低层 topic 提升为更高抽象层研究对象，并产出多路线方案。

## Inputs

- `taste_audit.md`
- `gap_analysis.md`
- `literature_map.md`

## Outputs

- `runs/<run_id>/artifacts/problem_reframing_ladder.md`
- `runs/<run_id>/artifacts/route_candidates.md`
- `runs/<run_id>/checkpoints/abstraction-lift.json`

## Procedure

1. 构建 reframing ladder：
   - Level 0: Surface phenomenon
   - Level 1: Mechanism
   - Level 2: General object
   - Level 3: Theoretical framing
   - Level 4: Field-level agenda
2. 生成三条路线：`Conservative`、`Main-track`、`Aggressive`。
3. 每条路线必须描述：core thesis、变化点、novelty potential、risk、resource need、likely venue、representative-work potential、优劣权衡。

## Stop Conditions

- `problem_reframing_ladder.md` 至少 5 层。
- `route_candidates.md` 包含三条路线并完整填充 required sections。

## Human Checkpoint

- 必需：确认是否允许主线 pivot。

