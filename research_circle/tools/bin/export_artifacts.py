#!/usr/bin/env python3
"""Atomic exporter for paper bank JSONL to Markdown."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
from common import read_jsonl  # noqa: E402


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Export artifacts into Markdown.")
    p.add_argument("--paper-bank", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--top-k", type=int, default=30)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    rows = read_jsonl(Path(args.paper_bank))
    rows = sorted(rows, key=lambda r: float(r.get("relevance", 0.0)), reverse=True)[: args.top_k]

    lines = ["# Paper Bank (Top Ranked)", "", "| ID | Year | Source | Title | Relevance |", "|---|---:|---|---|---:|"]
    for item in rows:
        title = str(item.get("title", "")).replace("|", " ")
        lines.append(
            f"| {item.get('id', '')} | {item.get('year', '')} | {item.get('source', '')} | [{title}]({item.get('url', '')}) | {item.get('relevance', 0.0):.4f} |"
        )

    Path(args.output).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
