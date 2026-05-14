#!/usr/bin/env python3
"""Atomic search tool for arXiv."""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "lib"))
from common import normalize_record, relevance_from_query, write_jsonl  # noqa: E402


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Search papers from arXiv API.")
    p.add_argument("--query", required=True)
    p.add_argument("--max-results", type=int, default=20)
    p.add_argument("--output", required=False)
    p.add_argument("--fail-soft", action="store_true", help="Write empty output on API error and exit 0.")
    return p.parse_args()


def fetch_arxiv(query: str, max_results: int):
    encoded = urllib.parse.quote(f"all:{query}")
    url = (
        "http://export.arxiv.org/api/query"
        f"?search_query={encoded}&start=0&max_results={max_results}&sortBy=relevance&sortOrder=descending"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "full-circle-mvp/0.1 (research-assistant)"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = resp.read()
            break
        except urllib.error.HTTPError as err:
            if err.code == 429 and attempt < 2:
                time.sleep(2 + attempt)
                continue
            raise

    root = ET.fromstring(data)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    entries = []
    for entry in root.findall("atom:entry", ns):
        identifier = (entry.findtext("atom:id", default="", namespaces=ns) or "").strip()
        title = (entry.findtext("atom:title", default="", namespaces=ns) or "").strip()
        summary = (entry.findtext("atom:summary", default="", namespaces=ns) or "").strip()
        published = (entry.findtext("atom:published", default="", namespaces=ns) or "")
        year = int(published[:4]) if len(published) >= 4 and published[:4].isdigit() else 1900
        authors = []
        for author in entry.findall("atom:author", ns):
            name = author.findtext("atom:name", default="", namespaces=ns)
            if name:
                authors.append(name.strip())

        arxiv_id = identifier.rsplit("/", 1)[-1] if identifier else "unknown"
        record = {
            "id": f"arxiv:{arxiv_id}",
            "source": "arxiv",
            "title": title,
            "year": year,
            "venue": "arXiv",
            "abstract": summary,
            "url": identifier,
            "authors": authors,
            "relevance": relevance_from_query(query, title, summary),
            "evidence": [f"query:{query}", f"source_url:{identifier}"],
        }
        entries.append(normalize_record(record))
    return entries


def main() -> int:
    args = parse_args()
    had_error = False
    try:
        entries = fetch_arxiv(args.query, args.max_results)
    except Exception as err:
        if not args.fail_soft:
            raise
        had_error = True
        entries = []
        print(
            json.dumps(
                {"source": "arxiv", "status": "error", "error": str(err), "query": args.query},
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )

    if args.output:
        write_jsonl(Path(args.output), entries)
    else:
        print(json.dumps(entries, ensure_ascii=False, indent=2))
    return 2 if had_error else 0


if __name__ == "__main__":
    raise SystemExit(main())
