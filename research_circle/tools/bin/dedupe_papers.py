#!/usr/bin/env python3
"""Atomic dedupe tool for paper records."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
from common import normalize_record, read_jsonl, write_jsonl  # noqa: E402


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Dedupe paper records by DOI/title.")
    p.add_argument("--input", action="append", required=True, help="Input JSONL file (repeatable)")
    p.add_argument("--output", required=True, help="Output JSONL file")
    return p.parse_args()


def title_key(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (title or "").lower())


def record_key(record: Dict[str, object]) -> str:
    doi = str(record.get("doi", "")).strip().lower()
    if doi:
        return f"doi:{doi}"
    return f"title:{title_key(str(record.get('title', '')))}"


def better(a: Dict[str, object], b: Dict[str, object]) -> Dict[str, object]:
    a_abs = len(str(a.get("abstract", "")))
    b_abs = len(str(b.get("abstract", "")))
    if b_abs > a_abs:
        return b
    return a


def main() -> int:
    args = parse_args()
    merged: Dict[str, Dict[str, object]] = {}

    for input_path in args.input:
        for record in read_jsonl(Path(input_path)):
            norm = normalize_record(record)
            key = record_key(norm)
            if key in merged:
                merged[key] = better(merged[key], norm)
            else:
                merged[key] = norm

    output_records = sorted(
        merged.values(),
        key=lambda x: (float(x.get("relevance", 0.0)), int(x.get("year", 1900))),
        reverse=True,
    )
    write_jsonl(Path(args.output), output_records)

    stats = {
        "input_files": args.input,
        "unique_records": len(output_records),
    }
    print(json.dumps(stats, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
