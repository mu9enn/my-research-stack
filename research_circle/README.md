# Research Circle v2 (Taste-first, Claim-centric, Reframing-driven)

Research Circle v2 is a domain-general scientific exploration system.

It upgrades the v1 linear MVP into a workflow that can actively audit research taste,
reframe shallow topics, check novelty at claim level, and validate whether experiments
actually support the thesis.

## Canonical Workflow

1. intake
2. frontier-radar (optional, recommended)
3. literature-search
4. literature-map
5. gap-mining
6. taste-audit
7. abstraction-lift
8. idea-tree-search
9. claim-novelty-check
10. proposal-tournament
11. construct-validity-audit
12. research-planning
13. run-postmortem (optional, recommended)

## Design Principles

- Orchestration and decision logic live in Skills/Agents, not Python.
- Python is only used for atomic tools (search, normalization, dedupe, similarity, export).
- Stage transitions are explicit and artifact-based.
- Human checkpoints remain required and now carry richer structured feedback.
- The framework is domain-general and should not be specialized to one research field.

## Repository Layout

- `skills/`: canonical workflow instructions
- `agents/`: role definitions
- `tools/`: atomic Python tools only
- `runs/`: stage artifacts for each run
- `references/`: SSH-cloned external projects (read-only reference)
- `specs/`: artifact protocol and JSON Schemas
- `docs/`: workflow and migration docs

## Quick Start

### 1) Create run workspace

```bash
./bin/fc init-run --topic "General scientific direction"
```

### 2) Check run status

```bash
./bin/fc status --run-id <run_id>
```

### 3) Record human checkpoint decision

```bash
./bin/fc checkpoint \
  --run-id <run_id> \
  --stage taste-audit \
  --decision approved \
  --note "允许中等强度 pivot" \
  --taste-target main-track \
  --risk-preference balanced \
  --desired-abstraction-level framework \
  --must-not-be "benchmark-only,minor-extension" \
  --pivot-permission moderate
```

### 4) Clone references via SSH

```bash
./bin/clone_references.sh
```

### 5) Run 3-source atomic retrieval (fail-soft)

```bash
./tools/bin/search_all_sources.sh \
  --query "general research query" \
  --output-dir runs/<run_id>/artifacts \
  --max-results 20 \
  --top-k 60
```

## Schemas and Examples

- JSON Schemas: `specs/schemas/`
- Example payloads: `specs/examples/`

## Backward-Compatible Stage Aliases

- `literature-review` -> `literature-map`
- `idea-generation` -> `idea-tree-search`
- `novelty-check` -> `claim-novelty-check`
- `proposal-ranking` -> `proposal-tournament`

## Defaults

- Output language: Chinese
- Mode: Human-in-the-loop
- Retrieval size: 30-80 papers
- Platform: Codex-first, Claude Code compatible

