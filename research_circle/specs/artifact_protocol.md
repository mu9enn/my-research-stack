# Artifact Protocol (Research Circle v2 Run Contract)

## Run Root

Each run lives at:

`runs/<run_id>/`

`run_id` format:

`YYYYMMDD-HHMMSS-<slug>`

## Stage Layout

```
runs/<run_id>/
  run_meta.json
  checkpoints/
    intake.json
    frontier-radar.json
    literature-search.json
    literature-map.json
    gap-mining.json
    taste-audit.json
    abstraction-lift.json
    idea-tree-search.json
    claim-novelty-check.json
    proposal-tournament.json
    construct-validity-audit.json
    research-planning.json
    run-postmortem.json
  artifacts/
    research_brief.json
    source_bank.jsonl
    frontier_radar.md
    source_gap_report.md
    paper_bank.jsonl
    literature_map.md
    contradiction_map.md
    evidence_strength_table.md
    unsupported_claims.md
    gap_analysis.md
    taste_audit.md
    taste_scores.json
    problem_reframing_ladder.md
    route_candidates.md
    idea_tree.json
    idea_mutations.md
    route_comparison.md
    claim_graph.json
    collision_matrix.md
    safe_claims.md
    claims_to_avoid.md
    proposal_tournament.md
    reviewer_objections.json
    revision_actions.md
    ranked_proposals.md
    construct_validity_report.md
    experiment_thesis_alignment.json
    research_plan.md
    run_postmortem.md
  logs/
    tool_calls.log
```

## Canonical Stage Order

1. `intake`
2. `frontier-radar`
3. `literature-search`
4. `literature-map`
5. `gap-mining`
6. `taste-audit`
7. `abstraction-lift`
8. `idea-tree-search`
9. `claim-novelty-check`
10. `proposal-tournament`
11. `construct-validity-audit`
12. `research-planning`
13. `run-postmortem`

## Stage Requirements

- Mandatory stages:
  - `intake`
  - `literature-search`
  - `literature-map`
  - `gap-mining`
  - `taste-audit`
  - `abstraction-lift`
  - `idea-tree-search`
  - `claim-novelty-check`
  - `proposal-tournament`
  - `construct-validity-audit`
  - `research-planning`
- Optional (recommended) stages:
  - `frontier-radar`
  - `run-postmortem`

## Backward-Compatible Stage Aliases

These aliases are accepted by CLI and normalized into canonical stage ids:

- `literature-review` -> `literature-map`
- `idea-generation` -> `idea-tree-search`
- `novelty-check` -> `claim-novelty-check`
- `proposal-ranking` -> `proposal-tournament`

## Human Checkpoints

Human checkpoints remain required with richer structured payloads.

Minimum mandatory decision points:

- after `gap-mining`
- after `taste-audit`
- after `abstraction-lift`
- after `idea-tree-search`
- after `proposal-tournament`
- after `construct-validity-audit`

Checkpoint file shape:

```json
{
  "stage": "taste-audit",
  "decision": "approved",
  "note": "继续进入抽象提升",
  "taste_target": "main-track",
  "risk_preference": "balanced",
  "desired_abstraction_level": "framework",
  "must_not_be": [
    "benchmark-only",
    "minor-extension"
  ],
  "main_objection": "担心 claim defensibility 不够",
  "pivot_permission": "moderate",
  "updated_at": "2026-05-14T12:00:00Z"
}
```

Allowed `decision` values:

- `pending`
- `approved`
- `needs_revision`
- `blocked`

Recommended `taste_target` values:

- `workshop`
- `findings`
- `main-track`
- `representative-work`

Recommended `risk_preference` values:

- `conservative`
- `balanced`
- `aggressive`

Recommended `desired_abstraction_level` values:

- `phenomenon`
- `mechanism`
- `framework`
- `theory`
- `agenda`

Recommended `pivot_permission` values:

- `none`
- `moderate`
- `aggressive`

## Artifact Contracts

- `research_brief.json`: must satisfy `research_brief.schema.json`
- `paper_bank.jsonl`: each line satisfies `paper_bank_record.schema.json`
- `source_bank.jsonl`: each line satisfies `source_bank_record.schema.json`
- `taste_scores.json`: must satisfy `taste_scores.schema.json`
- `idea_tree.json`: must satisfy `idea_tree.schema.json`
- `claim_graph.json`: must satisfy `claim_graph.schema.json`
- `construct_validity_report.md` and `experiment_thesis_alignment.json`: `experiment_thesis_alignment.json` should satisfy `construct_validity_report.schema.json`
- `run_postmortem.md`: structured summary file; optional machine-readable extension may satisfy `run_postmortem.schema.json`

