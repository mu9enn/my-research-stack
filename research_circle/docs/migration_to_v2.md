# Migration Guide: v1 -> v2

This guide explains how the original linear MVP maps to Research Circle v2.

## Mapping Table

| v1 stage | v2 stage | Change |
|---|---|---|
| intake | intake | Expanded with taste/risk preference fields |
| literature-search | literature-search | Kept; now can consume frontier outputs |
| literature-review | literature-map | Upgraded outputs: contradiction/evidence/unsupported claims |
| gap-mining | gap-mining | Adds gap taxonomy + abstraction/taste risk fields |
| idea-generation | idea-tree-search | Flat list -> tree search |
| novelty-check | claim-novelty-check | Idea-level -> claim-level novelty |
| proposal-ranking | proposal-tournament | Single scoring -> multi-reviewer tournament |
| research-planning | research-planning | Now must integrate construct-validity revisions |

## New Stages in v2

- `frontier-radar` (optional, recommended)
- `taste-audit` (required)
- `abstraction-lift` (required)
- `construct-validity-audit` (required)
- `run-postmortem` (optional, recommended)

## Required vs Optional

Required chain:

`intake -> literature-search -> literature-map -> gap-mining -> taste-audit -> abstraction-lift -> idea-tree-search -> claim-novelty-check -> proposal-tournament -> construct-validity-audit -> research-planning`

Optional (recommended):

- `frontier-radar`
- `run-postmortem`

## Artifact Renames and Additions

Key canonical renames:

- `literature-review` outputs now grouped under `literature-map` stage.
- `ideas.json` is replaced by `idea_tree.json`.
- `novelty_check.md` is replaced by `claim_graph.json` + claim novelty artifacts.
- `review_report.json` is replaced by `reviewer_objections.json` + `revision_actions.md` under tournament.

Major new artifacts include:

- `source_bank.jsonl`, `frontier_radar.md`, `source_gap_report.md`
- `contradiction_map.md`, `evidence_strength_table.md`, `unsupported_claims.md`
- `taste_audit.md`, `taste_scores.json`
- `problem_reframing_ladder.md`, `route_candidates.md`, `idea_mutations.md`
- `claim_graph.json`, `collision_matrix.md`, `safe_claims.md`, `claims_to_avoid.md`
- `construct_validity_report.md`, `experiment_thesis_alignment.json`
- `run_postmortem.md`

## CLI Compatibility

The v2 CLI accepts old stage names and normalizes them:

- `literature-review` -> `literature-map`
- `idea-generation` -> `idea-tree-search`
- `novelty-check` -> `claim-novelty-check`
- `proposal-ranking` -> `proposal-tournament`

## Migration Checklist

1. Update run-level docs and operating playbooks to canonical v2 stages.
2. Produce v2 artifacts in each stage handoff (instead of v1-only files).
3. Use structured checkpoint payload fields for taste/risk/pivot decisions.
4. Ensure ranking decisions happen after claim-level novelty and construct-validity audit.

