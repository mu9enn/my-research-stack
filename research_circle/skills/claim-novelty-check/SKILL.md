# Skill: claim-novelty-check

## Purpose

从 idea-level novelty 升级为 claim-level novelty，逐条 claim 审查碰撞与防御性。

## Inputs

- `idea_tree.json`
- `literature_map.md`
- `source_bank.jsonl`
- `paper_bank.jsonl`

## Outputs

- `runs/<run_id>/artifacts/claim_graph.json`
- `runs/<run_id>/artifacts/collision_matrix.md`
- `runs/<run_id>/artifacts/safe_claims.md`
- `runs/<run_id>/artifacts/claims_to_avoid.md`
- `runs/<run_id>/checkpoints/claim-novelty-check.json`

## Procedure

1. 将候选 proposal 拆解为 claim graph。
2. 对每条 claim 检索最近碰撞证据并标注安全级别。
3. 对 `unsafe` 与 `weaken` claims 给出可防御重写。
4. 输出 reviewer attack points 与 related-work positioning。

## Claim Status Labels

- `safe`
- `weaken`
- `unsafe`
- `already_covered`
- `needs_search`

## Stop Conditions

- `claim_graph.json` 满足 `claim_graph.schema.json`。
- `safe_claims.md`、`claims_to_avoid.md` 完整覆盖主线 proposal。

## Human Checkpoint

- 推荐：对于高风险 claim 先做人类复核再进 proposal tournament。

