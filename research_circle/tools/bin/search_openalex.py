#!/usr/bin/env python3
"""Atomic search tool for OpenAlex."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
from common import normalize_record, relevance_from_query, write_jsonl  # noqa: E402

API_URL = "https://api.openalex.org/works"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Search papers from OpenAlex.")
    p.add_argument("--query", required=True)
    p.add_argument("--max-results", type=int, default=20)
    p.add_argument("--output", required=False)
    p.add_argument("--fail-soft", action="store_true", help="Write empty output on API error and exit 0.")
    return p.parse_args()


def _venue_name(work: dict) -> str:
    primary = work.get("primary_location") or {}
    source = primary.get("source") or {}
    return source.get("display_name") or "Unknown"


def fetch_openalex(query: str, max_results: int):
    params = urllib.parse.urlencode({"search": query, "per-page": max_results})
    url = f"{API_URL}?{params}"
    with urllib.request.urlopen(url, timeout=30) as resp:
        payload = json.loads(resp.read().decode("utf-8"))

    results = []
    for work in payload.get("results", []):
        work_id = (work.get("id") or "unknown").rsplit("/", 1)[-1]
        title = work.get("title") or ""
        abstract = ""
        abstract_inverted = work.get("abstract_inverted_index")
        if isinstance(abstract_inverted, dict):
            tokens = []
            for token, positions in abstract_inverted.items():
                for pos in positions:
                    tokens.append((pos, token))
            abstract = " ".join(t for _, t in sorted(tokens, key=lambda x: x[0]))

        url = work.get("primary_location", {}).get("landing_page_url") or work.get("doi") or ""
        year = work.get("publication_year") or 1900
        authors = []
        for authorship in work.get("authorships", []):
            author = authorship.get("author", {})
            name = author.get("display_name")
            if name:
                authors.append(name)

        record = {
            "id": f"openalex:{work_id}",
            "source": "openalex",
            "title": title,
            "year": year,
            "venue": _venue_name(work),
            "abstract": abstract,
            "url": url,
            "authors": authors,
            "relevance": relevance_from_query(query, title, abstract),
            "evidence": [f"query:{query}", f"source_url:{url or 'N/A'}"],
        }
        results.append(normalize_record(record))
    return results


def main() -> int:
    args = parse_args()
    had_error = False
    try:
        records = fetch_openalex(args.query, args.max_results)
    except Exception as err:
        if not args.fail_soft:
            raise
        had_error = True
        records = []
        print(
            json.dumps(
                {"source": "openalex", "status": "error", "error": str(err), "query": args.query},
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
