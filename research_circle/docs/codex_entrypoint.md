# Codex Entrypoint Guide

## Start a run

```bash
./bin/fc init-run --topic "NLP/LLM/Agent topic"
```

## Suggested interaction flow

1. Execute `skills/intake/SKILL.md` and produce `research_brief.json`
2. Execute `skills/literature-search/SKILL.md` and fill `paper_bank.jsonl`
   - Recommended atomic call:
     `./tools/bin/search_all_sources.sh --query \"<query>\" --output-dir runs/<run_id>/artifacts --max-results 20 --top-k 60`
3. Continue stage by stage, always reading/writing run artifacts
4. Pause for human checkpoints when required

## Tool usage rule

Use only atomic tools in `tools/bin/` when a stage needs deterministic data operations.
