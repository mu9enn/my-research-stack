#!/usr/bin/env python3
"""Atomic normalization tool for paper records."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
from common import normalize_record, read_jsonl, write_jsonl  # noqa: E402


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Normalize paper bank JSONL fields.")
    p.add_argument("--input", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--top-k", type=int, default=60)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    rows = [normalize_record(item) for item in read_jsonl(Path(args.input))]
    rows.sort(key=lambda r: (float(r.get("relevance", 0.0)), int(r.get("year", 1900))), reverse=True)
    rows = rows[: max(1, args.top_k)]
    write_jsonl(Path(args.output), rows)
    print(json.dumps({"normalized": len(rows)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
