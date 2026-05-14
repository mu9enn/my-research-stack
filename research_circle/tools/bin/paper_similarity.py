#!/usr/bin/env python3
"""Atomic similarity scoring between free text and paper bank."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
from common import jaccard_similarity, read_jsonl  # noqa: E402


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Score similarity against paper bank.")
    p.add_argument("--text", required=True, help="Input text to compare")
    p.add_argument("--paper-bank", required=True)
    p.add_argument("--top-k", type=int, default=5)
    p.add_argument("--output", required=False)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    candidates = []
    for paper in read_jsonl(Path(args.paper_bank)):
        source_text = f"{paper.get('title', '')} {paper.get('abstract', '')}"
        score = jaccard_similarity(args.text, source_text)
        candidates.append(
            {
                "paper_id": paper.get("id"),
                "title": paper.get("title"),
                "url": paper.get("url"),
                "score": round(score, 4),
            }
        )

    top = sorted(candidates, key=lambda x: x["score"], reverse=True)[: max(1, args.top_k)]
    payload = {"query": args.text, "top_matches": top}

    if args.output:
        Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
