# Skill: idea-tree-search

## Purpose

把 idea generation 从平面列表升级为树状搜索，系统化探索 mutation 路径。

## Inputs

- `route_candidates.md`
- `problem_reframing_ladder.md`
- `gap_analysis.md`

## Outputs

- `runs/<run_id>/artifacts/idea_tree.json`
- `runs/<run_id>/artifacts/idea_mutations.md`
- `runs/<run_id>/artifacts/route_comparison.md`
- `runs/<run_id>/checkpoints/idea-tree-search.json`

## Procedure

1. 从每条路线生成 root idea node。
2. 对每个强候选至少生成以下 mutation：
   - local_extension
   - abstraction_lift
   - cross_domain_transfer
   - benchmark_first
   - theory_first
   - systems_first
3. 记录每个 node 的新增贡献、碰撞风险、kill reasons 与下一步变异方向。
4. 输出 route-level 比较，给出保守/主线/激进建议。

## Node Schema (must follow)

```json
{
  "idea_id": "",
  "parent_id": "",
  "mutation_type": "local_extension | abstraction_lift | cross_domain_transfer | benchmark_first | theory_first | systems_first | evaluation_first",
  "core_thesis": "",
  "problem_statement": "",
  "expected_contribution": "",
  "what_is_new": "",
  "what_is_not_new": "",
  "nearest_collision": [],
  "taste_score": {},
  "feasibility_score": {},
  "kill_reasons": [],
  "next_mutations": []
}
```

## Stop Conditions

- `idea_tree.json` 满足 `idea_tree.schema.json`。
- 每个强候选包含强制 mutation 类型。

## Human Checkpoint

- 必需：确认进入 claim-level novelty 检查的候选子树。

