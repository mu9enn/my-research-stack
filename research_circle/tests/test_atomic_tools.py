#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, check=True)


def test_dedupe_and_normalize(tmp_path: Path) -> None:
    out = tmp_path / "deduped.jsonl"
    run(
        [
            "python3",
            "tools/bin/dedupe_papers.py",
            "--input",
            "tests/fixtures/sample_papers_a.jsonl",
            "--input",
            "tests/fixtures/sample_papers_b.jsonl",
            "--output",
            str(out),
        ]
    )

    lines = [json.loads(x) for x in out.read_text(encoding="utf-8").splitlines() if x.strip()]
    assert len(lines) == 3

    normalized = tmp_path / "normalized.jsonl"
    run(
        [
            "python3",
            "tools/bin/normalize_papers.py",
            "--input",
            str(out),
            "--output",
            str(normalized),
            "--top-k",
            "2",
        ]
    )
    norm_lines = [json.loads(x) for x in normalized.read_text(encoding="utf-8").splitlines() if x.strip()]
    assert len(norm_lines) == 2


def test_similarity(tmp_path: Path) -> None:
    result = tmp_path / "sim.json"
    run(
        [
            "python3",
            "tools/bin/paper_similarity.py",
            "--text",
            "long horizon agent planning",
            "--paper-bank",
            "tests/fixtures/sample_papers_a.jsonl",
            "--top-k",
            "1",
            "--output",
            str(result),
        ]
    )

    payload = json.loads(result.read_text(encoding="utf-8"))
    assert payload["top_matches"][0]["paper_id"] in {"arxiv:1", "arxiv:2"}


def test_cli_init_and_checkpoint() -> None:
    proc = run(["./bin/fc", "init-run", "--topic", "Test agent topic", "--run-id", "test-run-001"])
    assert "Created run" in proc.stdout

    status = run(["./bin/fc", "status", "--run-id", "test-run-001"])
    assert "gap-mining" in status.stdout

    ck = run(
        [
            "./bin/fc",
            "checkpoint",
            "--run-id",
            "test-run-001",
            "--stage",
            "gap-mining",
            "--decision",
            "approved",
            "--note",
            "ok",
        ]
    )
    assert "Checkpoint updated" in ck.stdout
