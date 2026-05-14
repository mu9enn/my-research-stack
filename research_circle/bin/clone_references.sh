#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REF_DIR="$ROOT_DIR/references"
LOCKFILE="$REF_DIR/LOCKFILE.md"

mkdir -p "$REF_DIR"
export GIT_SSH_COMMAND="${GIT_SSH_COMMAND:-ssh -o BatchMode=yes -o StrictHostKeyChecking=accept-new}"

repos=(
  "AI-Researcher|git@github.com:NoviScl/AI-Researcher.git|topic_to_proposal_ranking"
  "SciPIP|git@github.com:cheerss/SciPIP.git|literature_grounded_idea_proposer"
  "agent-research-skills|git@github.com:lingzhi227/agent-research-skills.git|skill_decomposition_patterns"
  "academic-research-skills|git@github.com:Imbad0202/academic-research-skills.git|quality_gates_and_review"
  "paper-qa|git@github.com:Future-House/paper-qa.git|paper_rag_and_citation_grounding"
)

for row in "${repos[@]}"; do
  IFS='|' read -r name url purpose <<< "$row"
  if [[ "$url" != git@github.com:* ]]; then
    echo "Refuse non-SSH URL: $url" >&2
    exit 1
  fi

  target="$REF_DIR/$name"
  if [[ -d "$target/.git" ]]; then
    echo "Updating $name"
    git -C "$target" fetch --all --prune
    default_branch="$(git -C "$target" remote show origin | awk '/HEAD branch/ {print $NF}')"
    git -C "$target" checkout "$default_branch"
    git -C "$target" pull --ff-only origin "$default_branch"
  else
    echo "Cloning $name"
    git clone --depth 1 "$url" "$target"
  fi

done

{
  echo "# References LOCKFILE"
  echo
  echo "Updated: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  echo
  echo "| Name | SSH URL | Commit | Purpose |"
  echo "|---|---|---|---|"

  for row in "${repos[@]}"; do
    IFS='|' read -r name url purpose <<< "$row"
    commit="$(git -C "$REF_DIR/$name" rev-parse HEAD)"
    echo "| $name | $url | $commit | $purpose |"
  done
} > "$LOCKFILE"

echo "Wrote lockfile: $LOCKFILE"
