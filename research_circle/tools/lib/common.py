#!/usr/bin/env python3
"""Shared utilities for Full Circle atomic tools."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List

_TOKEN_RE = re.compile(r"[a-z0-9]+")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "")).strip()


def tokenize(text: str) -> List[str]:
    return _TOKEN_RE.findall((text or "").lower())


def jaccard_similarity(a: str, b: str) -> float:
    sa = set(tokenize(a))
    sb = set(tokenize(b))
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def relevance_from_query(query: str, title: str, abstract: str) -> float:
    score_title = jaccard_similarity(query, title)
    score_abstract = jaccard_similarity(query, abstract)
    score = 0.7 * score_title + 0.3 * score_abstract
    return max(0.0, min(1.0, round(score, 4)))


def safe_year(value: object, default: int = 1900) -> int:
    try:
        year = int(value)
        if year < 1900:
            return default
        return year
    except (TypeError, ValueError):
        return default


def normalize_record(record: Dict[str, object]) -> Dict[str, object]:
    result = dict(record)
    result["id"] = normalize_whitespace(str(result.get("id", "unknown")))
    result["title"] = normalize_whitespace(str(result.get("title", "")))
    result["abstract"] = normalize_whitespace(str(result.get("abstract", "")))
    result["venue"] = normalize_whitespace(str(result.get("venue", "Unknown")))
    result["url"] = normalize_whitespace(str(result.get("url", "")))
    result["source"] = normalize_whitespace(str(result.get("source", "unknown")))
    result["year"] = safe_year(result.get("year", 1900))

    authors = result.get("authors", [])
    if isinstance(authors, list):
        result["authors"] = [normalize_whitespace(str(a)) for a in authors if str(a).strip()]
    else:
        result["authors"] = []

    relevance = result.get("relevance", 0.0)
    try:
        relevance = float(relevance)
    except (TypeError, ValueError):
        relevance = 0.0
    result["relevance"] = max(0.0, min(1.0, round(relevance, 4)))

    evidence = result.get("evidence", [])
    if isinstance(evidence, list):
        result["evidence"] = [normalize_whitespace(str(e)) for e in evidence if str(e).strip()]
    else:
        result["evidence"] = []

    return result


def read_jsonl(path: Path) -> List[Dict[str, object]]:
    items: List[Dict[str, object]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            items.append(json.loads(line))
    return items


def write_jsonl(path: Path, items: Iterable[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for item in items:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

