#!/usr/bin/env python3

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any
from uuid import uuid4

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


def _new_run_id() -> str:
    return f"test-v2-{uuid4().hex[:10]}"


def test_cli_init_status_and_checkpoint_alias() -> None:
    run_id = _new_run_id()
    run_dir = ROOT / "runs" / run_id

    try:
        proc = run(["./bin/fc", "init-run", "--topic", "General systems research", "--run-id", run_id])
        assert "Created run" in proc.stdout

        run_meta = json.loads((run_dir / "run_meta.json").read_text(encoding="utf-8"))
        assert run_meta["workflow"] == "research-circle-v2"
        assert run_meta["stage_order"] == [
            "intake",
            "frontier-radar",
            "literature-search",
            "literature-map",
            "gap-mining",
            "taste-audit",
            "abstraction-lift",
            "idea-tree-search",
            "claim-novelty-check",
            "proposal-tournament",
            "construct-validity-audit",
            "research-planning",
            "run-postmortem",
        ]

        status = run(["./bin/fc", "status", "--run-id", run_id])
        assert "frontier-radar" in status.stdout
        assert "construct-validity-audit" in status.stdout
        assert "run-postmortem" in status.stdout

        ck = run(
            [
                "./bin/fc",
                "checkpoint",
                "--run-id",
                run_id,
                "--stage",
                "proposal-ranking",
                "--decision",
                "approved",
                "--note",
                "v1 alias accepted",
                "--taste-target",
                "representative-work",
                "--risk-preference",
                "aggressive",
                "--desired-abstraction-level",
                "theory",
                "--must-not-be",
                "benchmark-only,minor-extension",
                "--main-objection",
                "collision risk",
                "--pivot-permission",
                "aggressive",
            ]
        )
        assert "Checkpoint updated" in ck.stdout

        ck_payload = json.loads((run_dir / "checkpoints" / "proposal-tournament.json").read_text(encoding="utf-8"))
        assert ck_payload["stage"] == "proposal-tournament"
        assert ck_payload["decision"] == "approved"
        assert ck_payload["taste_target"] == "representative-work"
        assert ck_payload["risk_preference"] == "aggressive"
        assert ck_payload["desired_abstraction_level"] == "theory"
        assert ck_payload["must_not_be"] == ["benchmark-only", "minor-extension"]
        assert ck_payload["main_objection"] == "collision risk"
        assert ck_payload["pivot_permission"] == "aggressive"
    finally:
        shutil.rmtree(run_dir, ignore_errors=True)


def _validate(schema: dict[str, Any], payload: Any) -> list[str]:
    errors: list[str] = []

    def walk(node: Any, spec: dict[str, Any], path: str) -> None:
        node_type = spec.get("type")

        if node_type == "object":
            if not isinstance(node, dict):
                errors.append(f"{path}: expected object")
                return

            required = spec.get("required", [])
            for key in required:
                if key not in node:
                    errors.append(f"{path}.{key}: required")

            properties = spec.get("properties", {})
            for key, value in node.items():
                if key in properties:
                    walk(value, properties[key], f"{path}.{key}")
                elif spec.get("additionalProperties", True) is False:
                    errors.append(f"{path}.{key}: additional property not allowed")

        elif node_type == "array":
            if not isinstance(node, list):
                errors.append(f"{path}: expected array")
                return
            items_spec = spec.get("items")
            if isinstance(items_spec, dict):
                for idx, item in enumerate(node):
                    walk(item, items_spec, f"{path}[{idx}]")

        elif node_type == "string":
            if not isinstance(node, str):
                errors.append(f"{path}: expected string")
                return
            min_len = spec.get("minLength")
            if isinstance(min_len, int) and len(node) < min_len:
                errors.append(f"{path}: too short")

        elif node_type == "integer":
            if not isinstance(node, int) or isinstance(node, bool):
                errors.append(f"{path}: expected integer")
                return

        elif node_type == "number":
            if not isinstance(node, (int, float)) or isinstance(node, bool):
                errors.append(f"{path}: expected number")
                return

        elif node_type == "boolean":
            if not isinstance(node, bool):
                errors.append(f"{path}: expected boolean")
                return

        if "enum" in spec and node not in spec["enum"]:
            errors.append(f"{path}: not in enum")

        minimum = spec.get("minimum")
        maximum = spec.get("maximum")
        if isinstance(node, (int, float)) and not isinstance(node, bool):
            if minimum is not None and node < minimum:
                errors.append(f"{path}: below minimum")
            if maximum is not None and node > maximum:
                errors.append(f"{path}: above maximum")

    walk(payload, schema, "$")
    return errors


def _load_schema(name: str) -> dict[str, Any]:
    return json.loads((ROOT / "specs" / "schemas" / name).read_text(encoding="utf-8"))


def test_new_schema_positive_and_negative_examples() -> None:
    source_schema = _load_schema("source_bank_record.schema.json")
    taste_schema = _load_schema("taste_scores.schema.json")
    idea_tree_schema = _load_schema("idea_tree.schema.json")
    claim_graph_schema = _load_schema("claim_graph.schema.json")
    construct_schema = _load_schema("construct_validity_report.schema.json")
    postmortem_schema = _load_schema("run_postmortem.schema.json")

    source_ok = {
        "source_id": "src-001",
        "title": "Benchmark spec",
        "source_type": "technical_spec",
        "authority_level": "primary",
        "stability": "stable",
        "supports_claims": ["c1"],
    }
    assert not _validate(source_schema, source_ok)
    source_bad = dict(source_ok)
    source_bad["source_type"] = "whitepaper"
    assert _validate(source_schema, source_bad)

    taste_ok = {
        "problem_importance": 5,
        "abstraction_level": 4,
        "novelty_robustness": 4,
        "non_incrementality": 4,
        "external_validity": 4,
        "field_timing": 5,
        "theory_potential": 3,
        "benchmark_construct_validity": 4,
        "representative_work_potential": 4,
        "reviewer_defensibility": 4,
    }
    assert not _validate(taste_schema, taste_ok)
    taste_bad = dict(taste_ok)
    taste_bad["abstraction_level"] = 6
    assert _validate(taste_schema, taste_bad)

    idea_ok = {
        "nodes": [
            {
                "idea_id": "i-1",
                "parent_id": "",
                "mutation_type": "abstraction_lift",
                "core_thesis": "Mechanism-aware evaluation improves transfer.",
                "problem_statement": "Current tests under-specify mechanism.",
                "expected_contribution": "A mechanism-aware evaluation frame.",
                "what_is_new": "Mechanism-indexed evaluation protocol.",
                "what_is_not_new": "Not a new base model architecture.",
                "nearest_collision": ["paper-x"],
                "taste_score": {"importance": 4},
                "feasibility_score": {"resource_realism": 3},
                "kill_reasons": [],
                "next_mutations": ["theory_first"],
            }
        ]
    }
    assert not _validate(idea_tree_schema, idea_ok)
    idea_bad = {"nodes": [{"idea_id": "i-1"}]}
    assert _validate(idea_tree_schema, idea_bad)

    claim_ok = {
        "claims": [
            {
                "claim_id": "c-1",
                "claim_text": "Our protocol reveals hidden failure modes.",
                "claim_type": "empirical",
                "status": "safe",
                "collision_sources": ["paper-y"],
                "why_collision_matters": "prior work has adjacent setup",
                "safe_rewrite": "In our setting, protocol reveals additional failure modes.",
                "claims_to_avoid": ["first ever"],
                "related_work_positioning": "extends prior setup to broader conditions",
            }
        ]
    }
    assert not _validate(claim_graph_schema, claim_ok)
    claim_bad = {"claims": [{"claim_id": "c-1", "status": "green"}]}
    assert _validate(claim_graph_schema, claim_bad)

    construct_ok = {
        "core_thesis": "Causal intervention improves robustness diagnostics.",
        "main_experiment_tests_thesis": True,
        "metrics_support_claims": True,
        "benchmark_not_toy": True,
        "baseline_is_strong_enough": False,
        "failure_modes_are_diagnostic": True,
        "ablations_are_diagnostic": True,
        "negative_result_still_useful": True,
        "construct_validity_risks": ["baseline set too weak"],
        "required_plan_revisions": ["add two stronger baselines"],
    }
    assert not _validate(construct_schema, construct_ok)
    construct_bad = dict(construct_ok)
    construct_bad.pop("core_thesis")
    assert _validate(construct_schema, construct_bad)

    postmortem_ok = {
        "initial_topic": "Mechanism-aware robust evaluation",
        "major_pivots": ["benchmark question -> theory-backed object"],
        "rejected_ideas": [{"idea": "tool wrapper", "reason": "incremental"}],
        "successful_reframing": ["local metric issue -> construct-validity object"],
        "claim_rewrites": ["first -> in our setting"],
        "sources_that_changed_judgment": ["standard document A"],
        "workflow_failures": ["late reviewer simulation"],
        "system_improvement_suggestions": ["earlier tournament checkpoint"],
    }
    assert not _validate(postmortem_schema, postmortem_ok)
    postmortem_bad = dict(postmortem_ok)
    postmortem_bad.pop("major_pivots")
    assert _validate(postmortem_schema, postmortem_bad)


def test_research_brief_schema_has_optional_taste_fields() -> None:
    schema = _load_schema("research_brief.schema.json")
    props = schema["properties"]

    assert "taste_target" in props
    assert "risk_preference" in props
    assert "desired_abstraction_level" in props
    assert "must_not_be" in props
    assert "main_objection" in props
    assert "pivot_permission" in props


def test_artifact_protocol_contains_v2_core_contracts() -> None:
    text = (ROOT / "specs" / "artifact_protocol.md").read_text(encoding="utf-8")

    assert "frontier-radar" in text
    assert "literature-map" in text
    assert "claim-novelty-check" in text
    assert "proposal-tournament" in text
    assert "construct-validity-audit" in text
    assert "run-postmortem" in text

    assert "source_bank.jsonl" in text
    assert "taste_scores.json" in text
    assert "idea_tree.json" in text
    assert "claim_graph.json" in text
    assert "construct_validity_report.md" in text
    assert "run_postmortem.md" in text

    assert "taste_target" in text
    assert "risk_preference" in text
    assert "desired_abstraction_level" in text
    assert "must_not_be" in text
    assert "pivot_permission" in text

