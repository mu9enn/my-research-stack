# Skill: gap-mining

## Purpose

识别可投稿导向的研究空白，并产出可验证 gap 列表。

## Inputs

- `literature_map.md`
- `paper_bank.jsonl`

## Outputs

- `runs/<run_id>/artifacts/gap_analysis.md`
- `runs/<run_id>/checkpoints/gap-mining.json`

## Procedure

1. 识别方法、设定、评测、资源四类空白。
2. 给出每个 gap 的证据论文与反例。
3. 标记 gap 风险级别（高/中/低）。
4. 形成 top gaps shortlist。

## Stop Conditions

- 至少产出 5 个 gap。
- 每个 gap 至少绑定 2 条证据。

## Human Checkpoint

- 必需：由人类写入 `checkpoints/gap-mining.json` 决策后才能进入下一阶段。

