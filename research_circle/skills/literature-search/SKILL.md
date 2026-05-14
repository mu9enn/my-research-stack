# Skill: literature-search

## Purpose

使用 3 源（arXiv/Semantic Scholar/OpenAlex）构建初始 `paper_bank`。

## Inputs

- `research_brief.json`

## Outputs

- `runs/<run_id>/artifacts/paper_bank.jsonl`
- `runs/<run_id>/logs/tool_calls.log`

## Procedure

1. 基于方向生成 3-8 条检索 query。
2. 优先调用 `tools/bin/search_all_sources.sh` 执行三源检索、去重与归一化。
3. 合并并使用 `dedupe_papers.py` 去重。
4. 使用 `normalize_papers.py` 统一字段。
5. 保留 30-60 篇高相关论文。

## Stop Conditions

- `paper_bank.jsonl` 行数在 30-60。
- 至少两源返回成功结果；若一源失败需在 `search_errors.log` 记录原因。

## Human Checkpoint

- 非强制。
