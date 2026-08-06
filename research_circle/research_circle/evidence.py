from __future__ import annotations

import hashlib
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Callable, Dict, List, Tuple


USER_AGENT = "research-circle/3.0 (evidence-discovery)"


def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def local_evidence(path: Path, title: str, locator: str, url: str = "") -> Dict[str, Any]:
    resolved = path.resolve()
    text = resolved.read_text(encoding="utf-8")
    if not text.strip():
        raise ValueError("evidence file is empty")
    return {
        "title": title,
        "url": url,
        "locator": locator,
        "snippet": text.strip(),
        "content_hash": content_hash(text),
        "level": "primary_excerpt",
        "source": "local",
        "source_path": str(resolved),
    }


def _request(url: str, headers: Dict[str, str] = None, attempts: int = 2) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, **(headers or {})})
    last_error = None
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(request, timeout=25) as response:
                return response.read()
        except (OSError, urllib.error.HTTPError) as error:
            last_error = error
            if attempt + 1 < attempts:
                time.sleep(0.5 * (attempt + 1))
    raise last_error  # type: ignore[misc]


def _normalize(source: str, remote_id: str, title: str, url: str, abstract: str) -> Dict[str, Any]:
    compact = " ".join((abstract or "").split())
    return {
        "remote_id": "%s:%s" % (source, remote_id),
        "title": " ".join((title or "").split()),
        "url": url or "",
        "locator": "abstract",
        "snippet": compact,
        "content_hash": content_hash(compact),
        "level": "discovery_abstract",
        "source": source,
        "source_path": None,
    }


def search_arxiv(query: str, limit: int) -> List[Dict[str, Any]]:
    encoded = urllib.parse.quote("all:%s" % query)
    url = "https://export.arxiv.org/api/query?search_query=%s&start=0&max_results=%d&sortBy=relevance&sortOrder=descending" % (
        encoded,
        limit,
    )
    root = ET.fromstring(_request(url))
    namespace = {"atom": "http://www.w3.org/2005/Atom"}
    records = []
    for entry in root.findall("atom:entry", namespace):
        identifier = (entry.findtext("atom:id", default="", namespaces=namespace) or "").strip()
        records.append(
            _normalize(
                "arxiv",
                identifier.rsplit("/", 1)[-1] or "unknown",
                entry.findtext("atom:title", default="", namespaces=namespace) or "",
                identifier,
                entry.findtext("atom:summary", default="", namespaces=namespace) or "",
            )
        )
    return records


def search_openalex(query: str, limit: int) -> List[Dict[str, Any]]:
    params = urllib.parse.urlencode({"search": query, "per-page": limit})
    payload = json.loads(_request("https://api.openalex.org/works?%s" % params).decode("utf-8"))
    records = []
    for work in payload.get("results", []):
        inverted = work.get("abstract_inverted_index") or {}
        tokens = []
        for token, positions in inverted.items():
            tokens.extend((position, token) for position in positions)
        abstract = " ".join(token for _, token in sorted(tokens))
        location = work.get("primary_location") or {}
        work_id = (work.get("id") or "unknown").rsplit("/", 1)[-1]
        records.append(
            _normalize(
                "openalex",
                work_id,
                work.get("title") or "",
                location.get("landing_page_url") or work.get("doi") or "",
                abstract,
            )
        )
    return records


def search_semantic_scholar(query: str, limit: int) -> List[Dict[str, Any]]:
    params = urllib.parse.urlencode(
        {"query": query, "limit": limit, "offset": 0, "fields": "paperId,title,abstract,url"}
    )
    headers = {}
    api_key = os.environ.get("SEMANTIC_SCHOLAR_API_KEY", "").strip()
    if api_key:
        headers["x-api-key"] = api_key
    payload = json.loads(
        _request("https://api.semanticscholar.org/graph/v1/paper/search?%s" % params, headers=headers).decode("utf-8")
    )
    return [
        _normalize(
            "semantic_scholar",
            paper.get("paperId") or "unknown",
            paper.get("title") or "",
            paper.get("url") or "",
            paper.get("abstract") or "",
        )
        for paper in payload.get("data", [])
    ]


SEARCHERS: Dict[str, Callable[[str, int], List[Dict[str, Any]]]] = {
    "arxiv": search_arxiv,
    "openalex": search_openalex,
    "semantic_scholar": search_semantic_scholar,
}


def search_all(query: str, limit: int) -> Tuple[List[Dict[str, Any]], Dict[str, str], List[str]]:
    records: List[Dict[str, Any]] = []
    errors: Dict[str, str] = {}
    successful_sources: List[str] = []
    with ThreadPoolExecutor(max_workers=len(SEARCHERS)) as executor:
        futures = {executor.submit(searcher, query, limit): name for name, searcher in SEARCHERS.items()}
        for future in as_completed(futures):
            name = futures[future]
            try:
                records.extend(future.result())
                successful_sources.append(name)
            except Exception as error:  # Each source is deliberately fail-soft.
                errors[name] = "%s: %s" % (type(error).__name__, error)

    seen = set()
    unique = []
    for record in records:
        key = (" ".join(record["title"].lower().split()), record["url"])
        if key in seen or not record["snippet"]:
            continue
        seen.add(key)
        unique.append(record)
    unique.sort(key=lambda item: (item["source"], item.get("remote_id") or "", item["title"]))
    return unique, errors, sorted(successful_sources)
