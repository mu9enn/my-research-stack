# Skill: literature-search

## Purpose

构建高相关 `paper_bank`，为 claim-level 推理提供可追溯论文证据池。

## Inputs

- `research_brief.json`
- `frontier_radar.md`（可选，推荐）
- `source_gap_report.md`（可选，推荐）

## Outputs

- `runs/<run_id>/artifacts/paper_bank.jsonl`
- `runs/<run_id>/logs/tool_calls.log`
- `runs/<run_id>/checkpoints/literature-search.json`

## Procedure

1. 基于 topic 与 frontier keywords 生成 3-12 条 query。
2. 优先调用 `tools/bin/search_all_sources.sh` 做三源检索、去重与归一化。
3. 保留 30-80 篇高相关论文，覆盖至少两类方法路线。
4. 记录检索失败原因与 coverage 风险。

## Stop Conditions

- `paper_bank.jsonl` 行数在 30-80。
- 至少两源返回成功结果；若一源失败需在 `search_errors.log` 记录原因。

## Human Checkpoint

- 非强制。

