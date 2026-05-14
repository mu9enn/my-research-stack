# Atomic Tools

These scripts are intentionally atomic and non-orchestrating.

## Search

- `tools/bin/search_arxiv.py`
- `tools/bin/search_semantic_scholar.py`
- `tools/bin/search_openalex.py`
- `tools/bin/search_all_sources.sh` (3-source fail-soft wrapper + dedupe + normalize)

## Transform

- `tools/bin/dedupe_papers.py`
- `tools/bin/normalize_papers.py`
- `tools/bin/paper_similarity.py`
- `tools/bin/export_artifacts.py`

## Example

```bash
./tools/bin/search_all_sources.sh \
  --query "llm agent planning" \
  --output-dir /tmp/fc-search \
  --max-results 20 \
  --top-k 60
```

## Environment Variables

- `SEMANTIC_SCHOLAR_API_KEY`: optional, recommended for higher rate limit.

## Failure Semantics

- `search_*.py --fail-soft` writes empty output on source failure and exits with code `2`.
- `search_all_sources.sh` continues on source failures but exits with code `3` when fewer than 2 sources succeed.
