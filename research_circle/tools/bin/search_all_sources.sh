#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
TOOLS_DIR="$ROOT_DIR/tools/bin"

query=""
out_dir=""
max_results="20"
log_file=""
top_k="60"
success_count=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --query)
      query="$2"; shift 2 ;;
    --output-dir)
      out_dir="$2"; shift 2 ;;
    --max-results)
      max_results="$2"; shift 2 ;;
    --log-file)
      log_file="$2"; shift 2 ;;
    --top-k)
      top_k="$2"; shift 2 ;;
    *)
      echo "Unknown option: $1" >&2
      exit 1 ;;
  esac
done

if [[ -z "$query" || -z "$out_dir" ]]; then
  echo "--query and --output-dir are required" >&2
  exit 1
fi

mkdir -p "$out_dir"
if [[ -z "$log_file" ]]; then
  log_file="$out_dir/search_errors.log"
fi
: > "$log_file"

timestamp() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

run_source() {
  local source="$1"
  local cmd="$2"

  if eval "$cmd" 2>>"$log_file"; then
    success_count=$((success_count + 1))
    echo "$(timestamp) source=$source status=ok" >> "$log_file"
  else
    echo "$(timestamp) source=$source status=failed" >> "$log_file"
  fi
}

run_source "arxiv" "python3 '$TOOLS_DIR/search_arxiv.py' --query \"$query\" --max-results '$max_results' --fail-soft --output '$out_dir/arxiv_raw.jsonl'"
run_source "openalex" "python3 '$TOOLS_DIR/search_openalex.py' --query \"$query\" --max-results '$max_results' --fail-soft --output '$out_dir/openalex_raw.jsonl'"
run_source "semantic_scholar" "python3 '$TOOLS_DIR/search_semantic_scholar.py' --query \"$query\" --max-results '$max_results' --fail-soft --output '$out_dir/s2_raw.jsonl'"

python3 "$TOOLS_DIR/dedupe_papers.py" \
  --input "$out_dir/arxiv_raw.jsonl" \
  --input "$out_dir/openalex_raw.jsonl" \
  --input "$out_dir/s2_raw.jsonl" \
  --output "$out_dir/paper_bank_merged.jsonl"

python3 "$TOOLS_DIR/normalize_papers.py" \
  --input "$out_dir/paper_bank_merged.jsonl" \
  --output "$out_dir/paper_bank.jsonl" \
  --top-k "$top_k"

if [[ "$success_count" -lt 2 ]]; then
  echo "$(timestamp) stage=literature-search status=failed reason='fewer_than_two_sources_success'" >> "$log_file"
  echo "Expected at least two successful sources, got $success_count" >&2
  exit 3
fi

echo "paper_bank=$out_dir/paper_bank.jsonl"
echo "log_file=$log_file"
