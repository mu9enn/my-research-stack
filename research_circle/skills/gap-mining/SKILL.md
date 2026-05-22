# Skill: gap-mining

## Purpose

识别可投稿导向的研究空白，并区分局部缺口与结构性缺口。

## Inputs

- `literature_map.md`
- `contradiction_map.md`
- `evidence_strength_table.md`
- `paper_bank.jsonl`

## Outputs

- `runs/<run_id>/artifacts/gap_analysis.md`
- `runs/<run_id>/checkpoints/gap-mining.json`

## Procedure

1. 提取候选 gaps，并按 `local | structural | field_defining` 分类。
2. 对每个 gap 给出：`why_now`、`who_cares`、证据与反例。
3. 评分：`abstraction_level`、`representative_work_potential`、`risk_of_being_incremental`。
4. 输出 top gaps shortlist，并标注哪些只是 benchmark/tool/dataset 缺口。

## Required Gap Fields

```json
{
  "gap_type": "local | structural | field_defining",
  "why_now": "",
  "who_cares": "",
  "abstraction_level": 1,
  "representative_work_potential": 1,
  "risk_of_being_incremental": 1
}
```

## Stop Conditions

- 至少产出 5 个 gap。
- 每个 gap 至少绑定 2 条证据。
- 每个 gap 均包含 required gap fields。

## Human Checkpoint

- 必需：由人类写入 `checkpoints/gap-mining.json` 决策后才能进入下一阶段。

