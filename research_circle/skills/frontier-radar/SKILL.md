# Skill: frontier-radar

## Purpose

构建 paper 之外的证据生态雷达，识别前沿信号、来源缺口和检索扩展方向。

## Inputs

- `research_brief.json`
- `seed_queries`
- 用户约束（可选）

## Outputs

- `runs/<run_id>/artifacts/frontier_radar.md`
- `runs/<run_id>/artifacts/source_bank.jsonl`
- `runs/<run_id>/artifacts/source_gap_report.md`
- `runs/<run_id>/checkpoints/frontier-radar.json`

## Procedure

1. 将 topic 拆解为 papers/docs/specs/repos/benchmarks/leaderboards/datasets 等多类 source query。
2. 记录 fast-moving frontier signals 与 emerging keywords。
3. 归档 primary sources 与 authority level，写入 `source_bank.jsonl`。
4. 输出 source gaps 和 recommended search expansions。

## Source Types (must cover)

- papers
- official docs
- technical specs
- GitHub repos
- benchmarks
- leaderboards
- datasets
- model cards
- dataset cards
- release notes
- standards documents
- security advisories
- primary lab blog posts
- competition reports

## Stop Conditions

- `frontier_radar.md` 完成 9 段结构化输出。
- `source_bank.jsonl` 每条记录满足 `source_bank_record.schema.json`。

## Human Checkpoint

- 推荐：确认 source coverage 是否满足方向需求。

