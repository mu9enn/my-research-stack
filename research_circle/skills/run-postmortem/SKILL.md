# Skill: run-postmortem

## Purpose

沉淀本轮 run 的关键决策、失败经验和成功重构，形成可复用 taste 资产。

## Inputs

- 全部 artifacts
- checkpoints
- decision logs

## Outputs

- `runs/<run_id>/artifacts/run_postmortem.md`
- `runs/<run_id>/checkpoints/run-postmortem.json`

## Procedure

1. 记录 initial topic 与 major pivots。
2. 汇总 rejected ideas 及拒绝原因。
3. 汇总 successful reframing、claim rewrites、改变判断的关键 sources。
4. 给出 workflow failures 与 system improvement suggestions。

## Stop Conditions

- `run_postmortem.md` 覆盖关键决策链与改进建议。
- 可追溯回答“为什么这条路线被选中”。

## Human Checkpoint

- 推荐：run 收尾与后续路线确认。

