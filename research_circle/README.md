# Full Circle MVP (Skill-First, Codex-First)

Full Circle is a research idea discovery MVP for `NLP/LLM/Agent` topics.

Core loop:

1. Research direction intake
2. Literature search (arXiv + Semantic Scholar + OpenAlex)
3. Literature review and gap mining
4. Idea generation
5. Novelty check (balanced filter)
6. Proposal ranking
7. Research planning (3 days / 2 weeks / 1 month)

## Design Principles

- Pipeline orchestration and decision logic live in Skills/Agents, not Python.
- Python is only used for atomic tools (search, normalization, dedupe, similarity, export).
- Artifacts are stage-based and file-based. Stage transitions happen through explicit files and human checkpoints.

## Repository Layout

- `skills/`: canonical workflow instructions (8 fixed skills)
- `agents/`: role definitions (5 fixed agents)
- `tools/`: atomic Python tools only
- `runs/`: stage artifacts for each run
- `references/`: SSH-cloned external projects (read-only reference)
- `specs/`: artifact protocol and JSON Schemas
- `docs/`: Codex entrypoint and Claude compatibility mapping

## Quick Start

### 1) Create run workspace

```bash
./bin/fc init-run --topic "Long-horizon LLM agent planning"
```

### 2) Check run status

```bash
./bin/fc status --run-id <run_id>
```

### 3) Record human checkpoint decision

```bash
./bin/fc checkpoint --run-id <run_id> --stage gap-mining --decision approved --note "继续 idea 生成"
```

### 4) Clone references via SSH

```bash
./bin/clone_references.sh
```

### 5) Run 3-source atomic retrieval (fail-soft)

```bash
./tools/bin/search_all_sources.sh \
  --query "llm agent planning" \
  --output-dir runs/<run_id>/artifacts \
  --max-results 20 \
  --top-k 60
```

## Schemas and Examples

- JSON Schemas: `specs/schemas/`
- Example payloads: `specs/examples/`

## Defaults

- Output language: Chinese
- Mode: Human-in-the-loop
- Retrieval size: 30-60 papers
- Platform: Codex-first, Claude Code compatible
