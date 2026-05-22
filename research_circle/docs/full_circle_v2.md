# Full Circle v2 Workflow

Research Circle v2 is taste-first, claim-centric, and reframing-driven.

Canonical chain:

`intake -> frontier-radar -> literature-search -> literature-map -> gap-mining -> taste-audit -> abstraction-lift -> idea-tree-search -> claim-novelty-check -> proposal-tournament -> construct-validity-audit -> research-planning -> run-postmortem`

## Stage Definitions

## 0) intake

- Input: user direction, constraints, resource/time/venue preferences.
- Output: `research_brief.json`.
- Gate: brief complete and taste/risk preferences explicit.

## 1) frontier-radar (optional, recommended)

- Input: `research_brief.json`, seed queries.
- Output: `frontier_radar.md`, `source_bank.jsonl`, `source_gap_report.md`.
- Gate: source ecosystem coverage and expansion plan documented.

## 2) literature-search

- Input: `research_brief.json` (+ optional frontier artifacts).
- Output: `paper_bank.jsonl`.
- Gate: 30-80 papers; fail-soft retrieval logs preserved.

## 3) literature-map

- Input: `paper_bank.jsonl` (+ optional `source_bank.jsonl`).
- Output: `literature_map.md`, `contradiction_map.md`, `evidence_strength_table.md`, `unsupported_claims.md`.
- Gate: clustered map + contradiction coverage + unsupported claim list.

## 4) gap-mining

- Input: literature map artifacts.
- Output: `gap_analysis.md` with `local/structural/field_defining` gap types.
- Gate: evidence-backed gaps with abstraction and incremental-risk fields.
- Human checkpoint: required.

## 5) taste-audit

- Input: `literature_map.md`, `gap_analysis.md`, `research_brief.json`.
- Output: `taste_audit.md`, `taste_scores.json`.
- Gate: 10-dimension taste scoring and trigger rules applied.
- Human checkpoint: required.

## 6) abstraction-lift

- Input: `taste_audit.md`, `gap_analysis.md`, `literature_map.md`.
- Output: `problem_reframing_ladder.md`, `route_candidates.md`.
- Gate: 5-level reframing ladder + conservative/main/aggressive routes.
- Human checkpoint: required.

## 7) idea-tree-search

- Input: reframing and route artifacts.
- Output: `idea_tree.json`, `idea_mutations.md`, `route_comparison.md`.
- Gate: mandatory mutation coverage for strong candidates.
- Human checkpoint: required.

## 8) claim-novelty-check

- Input: `idea_tree.json`, literature and source artifacts.
- Output: `claim_graph.json`, `collision_matrix.md`, `safe_claims.md`, `claims_to_avoid.md`.
- Gate: claim-level status labels and safe rewrites complete.

## 9) proposal-tournament

- Input: idea tree + safe claims + taste scores.
- Output: `proposal_tournament.md`, `reviewer_objections.json`, `revision_actions.md`, `ranked_proposals.md`.
- Gate: multi-reviewer scoring and route comparison complete.
- Human checkpoint: required.

## 10) construct-validity-audit

- Input: ranked proposals and tournament outputs.
- Output: `construct_validity_report.md`, `experiment_thesis_alignment.json`.
- Gate: thesis-experiment alignment and required revisions explicit.
- Human checkpoint: required.

## 11) research-planning

- Input: ranked proposals + construct validity artifacts.
- Output: `research_plan.md`.
- Gate: 3-day/2-week/1-month plan includes required construct-validity revisions.

## 12) run-postmortem (optional, recommended)

- Input: full run artifacts/checkpoints/logs.
- Output: `run_postmortem.md`.
- Gate: pivot history, rejected ideas, claim rewrites, and system improvements recorded.

## Human Checkpoint Payload

Use structured checkpoint fields to guide pivots and risk posture:

- `taste_target`
- `risk_preference`
- `desired_abstraction_level`
- `must_not_be`
- `main_objection`
- `pivot_permission`

## Generic Example Topics

- Mechanism-level robustness for scientific information extraction pipelines.
- Cross-domain transferability of uncertainty-aware planning in autonomous systems.
- Benchmark construct validity for multi-step decision-making under partial observability.

