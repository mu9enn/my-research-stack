# Artifact Protocol (Run Directory Contract)

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
    literature-review.json
    gap-mining.json
    idea-generation.json
    proposal-ranking.json
    research-planning.json
  artifacts/
    research_brief.json
    paper_bank.jsonl
    literature_map.md
    gap_analysis.md
    ideas.json
    novelty_check.md
    ranked_proposals.md
    research_plan.md
    review_report.json
  logs/
    tool_calls.log
```

## Stage Order

1. `intake`
2. `literature-search`
3. `literature-review`
4. `gap-mining`
5. `idea-generation`
6. `novelty-check`
7. `proposal-ranking`
8. `research-planning`

## Human Checkpoints

Required manual decision points:

- after `gap-mining`
- after `idea-generation`
- after `proposal-ranking`

Checkpoint file shape:

```json
{
  "stage": "gap-mining",
  "decision": "approved",
  "note": "继续 idea 生成",
  "updated_at": "2026-05-14T12:00:00Z"
}
```

Allowed `decision` values:

- `approved`
- `needs_revision`
- `blocked`

## Artifact Contracts

- `research_brief.json`: must satisfy `research_brief.schema.json`
- `paper_bank.jsonl`: each line satisfies `paper_bank_record.schema.json`
- `ideas.json`: array of `idea_card.schema.json`
- `review_report.json`: must satisfy `review_report.schema.json`
- `ranked_proposals.md`: contains scored shortlist (novelty/feasibility/impact)
- `research_plan.md`: includes 3-day, 2-week, 1-month execution blocks

