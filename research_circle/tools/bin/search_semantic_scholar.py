#!/usr/bin/env python3
"""Atomic search tool for Semantic Scholar Graph API."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
from common import normalize_record, relevance_from_query, write_jsonl  # noqa: E402

API_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
FIELDS = "paperId,title,year,venue,abstract,url,authors"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Search papers from Semantic Scholar.")
    p.add_argument("--query", required=True)
    p.add_argument("--max-results", type=int, default=20)
    p.add_argument("--output", required=False)
    p.add_argument("--fail-soft", action="store_true", help="Write empty output on API error and exit 0.")
    return p.parse_args()


def fetch_semantic_scholar(query: str, max_results: int):
    params = urllib.parse.urlencode(
        {
            "query": query,
            "limit": max_results,
            "fields": FIELDS,
            "offset": 0,
        }
    )
    req = urllib.request.Request(f"{API_URL}?{params}")
    api_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY", "").strip()
    if api_key:
        req.add_header("x-api-key", api_key)

    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.loads(resp.read().decode("utf-8"))

    records = []
    for paper in payload.get("data", []):
        title = paper.get("title") or ""
        abstract = paper.get("abstract") or ""
        url = paper.get("url") or ""
        paper_id = paper.get("paperId") or "unknown"
        authors = [a.get("name", "").strip() for a in (paper.get("authors") or []) if a.get("name")]

        record = {
            "id": f"s2:{paper_id}",
            "source": "semantic_scholar",
            "title": title,
            "year": paper.get("year") or 1900,
            "venue": paper.get("venue") or "Unknown",
            "abstract": abstract,
            "url": url,
            "authors": authors,
            "relevance": relevance_from_query(query, title, abstract),
            "evidence": [f"query:{query}", f"source_url:{url or 'N/A'}"],
        }
        records.append(normalize_record(record))
    return records


def main() -> int:
    args = parse_args()
    had_error = False
    try:
        records = fetch_semantic_scholar(args.query, args.max_results)
    except Exception as err:
        if not args.fail_soft:
            raise
        had_error = True
        records = []
        print(
            json.dumps(
                {"source": "semantic_scholar", "status": "error", "error": str(err), "query": args.query},
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
    if args.output:
        write_jsonl(Path(args.output), records)
    else:
        print(json.dumps(records, ensure_ascii=False, indent=2))
    return 2 if had_error else 0


if __name__ == "__main__":
    raise SystemExit(main())
