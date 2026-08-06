from __future__ import annotations

import math
import os
from pathlib import Path
from typing import Any, Dict, Iterable, List


class ContractError(ValueError):
    pass


def _require_object(value: Any, path: str) -> Dict[str, Any]:
    if not isinstance(value, dict):
        raise ContractError("%s must be an object" % path)
    return value


def _require_list(value: Any, path: str, minimum: int = 0, maximum: int = None) -> list:
    if not isinstance(value, list):
        raise ContractError("%s must be a list" % path)
    if len(value) < minimum:
        raise ContractError("%s requires at least %d items" % (path, minimum))
    if maximum is not None and len(value) > maximum:
        raise ContractError("%s allows at most %d items" % (path, maximum))
    return value


def _require_string(value: Any, path: str, minimum: int = 1) -> str:
    if not isinstance(value, str) or len(value.strip()) < minimum:
        raise ContractError("%s must be a non-empty string" % path)
    return value.strip()


def _require_enum(value: Any, path: str, allowed: Iterable[str]) -> str:
    value = _require_string(value, path)
    allowed_set = set(allowed)
    if value not in allowed_set:
        raise ContractError("%s must be one of %s" % (path, sorted(allowed_set)))
    return value


def _require_number(value: Any, path: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ContractError("%s must be numeric" % path)
    number = float(value)
    if not math.isfinite(number):
        raise ContractError("%s must be finite" % path)
    return number


def _require_bool(value: Any, path: str) -> bool:
    if not isinstance(value, bool):
        raise ContractError("%s must be boolean" % path)
    return value


def _keys(obj: Dict[str, Any], required: Iterable[str], path: str) -> None:
    missing = [key for key in required if key not in obj]
    if missing:
        raise ContractError("%s missing fields: %s" % (path, ", ".join(missing)))


def _validate_response_id(payload: Dict[str, Any]) -> None:
    _require_string(payload.get("response_id"), "response_id")


def validate_topic_response(payload: Dict[str, Any], evidence_ids: set) -> None:
    payload = _require_object(payload, "response")
    _validate_response_id(payload)
    _require_enum(payload.get("type"), "type", ["topic_synthesis"])
    _require_string(payload.get("direction_summary"), "direction_summary")
    candidates = _require_list(payload.get("candidates"), "candidates", 3, 5)
    seen = set()
    for index, raw in enumerate(candidates):
        path = "candidates[%d]" % index
        candidate = _require_object(raw, path)
        _keys(
            candidate,
            [
                "id",
                "title",
                "question",
                "hypothesis",
                "claim",
                "why_valuable",
                "abstraction_level",
                "incremental_risk",
                "novelty",
                "falsifier",
                "smallest_test",
                "risks",
            ],
            path,
        )
        candidate_id = _require_string(candidate["id"], path + ".id")
        if candidate_id in seen:
            raise ContractError("duplicate candidate id: %s" % candidate_id)
        seen.add(candidate_id)
        for field in ("title", "question", "hypothesis", "claim", "why_valuable", "falsifier", "smallest_test"):
            _require_string(candidate[field], path + "." + field)
        _require_enum(
            candidate["abstraction_level"],
            path + ".abstraction_level",
            ["phenomenon", "mechanism", "framework", "theory", "agenda"],
        )
        _require_enum(candidate["incremental_risk"], path + ".incremental_risk", ["low", "medium", "high"])
        novelty = _require_object(candidate["novelty"], path + ".novelty")
        _keys(novelty, ["status", "evidence_ids", "uncertainty"], path + ".novelty")
        _require_enum(novelty["status"], path + ".novelty.status", ["plausible", "collision", "uncertain"])
        refs = _require_list(novelty["evidence_ids"], path + ".novelty.evidence_ids", 1)
        for ref in refs:
            if ref not in evidence_ids:
                raise ContractError("%s references unknown evidence: %s" % (path, ref))
        _require_string(novelty["uncertainty"], path + ".novelty.uncertainty")
        _require_list(candidate["risks"], path + ".risks")
    recommended = _require_string(payload.get("recommended_id"), "recommended_id")
    if recommended not in seen:
        raise ContractError("recommended_id must name a candidate")
    stop = _require_object(payload.get("stop"), "stop")
    _keys(stop, ["needs_human", "reason"], "stop")
    _require_bool(stop["needs_human"], "stop.needs_human")
    if stop["needs_human"]:
        _require_string(stop["reason"], "stop.reason")


def validate_critic_response(payload: Dict[str, Any], expected_type: str, subject_id: str) -> None:
    payload = _require_object(payload, "response")
    _validate_response_id(payload)
    _require_enum(payload.get("type"), "type", ["critic"])
    _require_enum(payload.get("critic_type"), "critic_type", ["novelty", "research_quality", "validity"])
    if payload["critic_type"] != expected_type:
        raise ContractError("critic_type does not match pending critic")
    if _require_string(payload.get("subject_id"), "subject_id") != subject_id:
        raise ContractError("subject_id does not match pending subject")
    _require_enum(payload.get("verdict"), "verdict", ["pass", "revise", "reject", "human"])
    _require_list(payload.get("issues"), "issues")
    _require_list(payload.get("required_changes"), "required_changes")
    _require_string(payload.get("rationale"), "rationale")


def validate_experiment_response(
    payload: Dict[str, Any],
    selected_topic_id: str,
    claim_ids: set,
    max_timeout_seconds: int,
) -> None:
    payload = _require_object(payload, "response")
    _validate_response_id(payload)
    _require_enum(payload.get("type"), "type", ["experiment_design"])
    if _require_string(payload.get("topic_id"), "topic_id") != selected_topic_id:
        raise ContractError("experiment topic_id is not the approved topic")
    _require_string(payload.get("hypothesis"), "hypothesis")
    refs = _require_list(payload.get("claim_ids"), "claim_ids", 1)
    for ref in refs:
        if ref not in claim_ids:
            raise ContractError("unknown claim id: %s" % ref)
    code_files = _require_list(payload.get("code_files"), "code_files", 1)
    for index, code_file in enumerate(code_files):
        code_path = _require_string(code_file, "code_files[%d]" % index)
        if os.path.isabs(code_path) or ".." in Path(code_path).parts:
            raise ContractError("code_files must stay inside the project directory")
    command = _require_list(payload.get("command"), "command", 1)
    for index, arg in enumerate(command):
        text = _require_string(arg, "command[%d]" % index)
        remainder = text.replace("{output_dir}", "")
        if "{" in remainder or "}" in remainder:
            raise ContractError("only {output_dir} is an allowed command placeholder")
    workdir = _require_string(payload.get("workdir"), "workdir")
    if os.path.isabs(workdir) or ".." in Path(workdir).parts:
        raise ContractError("workdir must stay inside the project directory")
    timeout = payload.get("timeout_seconds")
    if not isinstance(timeout, int) or isinstance(timeout, bool) or timeout < 1 or timeout > max_timeout_seconds:
        raise ContractError("timeout_seconds must be within the run limit")
    metrics_file = _require_string(payload.get("metrics_file"), "metrics_file")
    if os.path.isabs(metrics_file) or ".." in Path(metrics_file).parts:
        raise ContractError("metrics_file must stay inside the attempt output directory")
    required_metrics = _require_list(payload.get("required_metrics"), "required_metrics", 1)
    for index, metric in enumerate(required_metrics):
        _require_string(metric, "required_metrics[%d]" % index)
    evaluator = _require_object(payload.get("evaluator"), "evaluator")
    _keys(evaluator, ["primary_metric", "direction", "baseline", "minimum_delta"], "evaluator")
    primary = _require_string(evaluator["primary_metric"], "evaluator.primary_metric")
    if primary not in required_metrics:
        raise ContractError("primary_metric must be in required_metrics")
    _require_enum(evaluator["direction"], "evaluator.direction", ["maximize", "minimize"])
    _require_number(evaluator["baseline"], "evaluator.baseline")
    delta = _require_number(evaluator["minimum_delta"], "evaluator.minimum_delta")
    if delta < 0:
        raise ContractError("minimum_delta must be non-negative")
    validity = _require_object(payload.get("validity"), "validity")
    _keys(
        validity,
        ["metric_claim_alignment", "baseline_rationale", "confounds", "negative_result_value", "risk"],
        "validity",
    )
    _require_string(validity["metric_claim_alignment"], "validity.metric_claim_alignment")
    _require_string(validity["baseline_rationale"], "validity.baseline_rationale")
    _require_list(validity["confounds"], "validity.confounds")
    _require_string(validity["negative_result_value"], "validity.negative_result_value")
    _require_enum(validity["risk"], "validity.risk", ["low", "medium", "high"])
    _require_enum(payload.get("resource_class"), "resource_class", ["small", "large"])
    stochastic = _require_bool(payload.get("stochastic"), "stochastic")
    replications = payload.get("replications")
    if not isinstance(replications, int) or isinstance(replications, bool) or replications < 1:
        raise ContractError("replications must be a positive integer")
    if not stochastic and replications != 1:
        raise ContractError("deterministic experiments must use one replication")


def validate_decision_response(payload: Dict[str, Any], attempt_id: str, claim_ids: set, evidence_ids: set) -> None:
    payload = _require_object(payload, "response")
    _validate_response_id(payload)
    _require_enum(payload.get("type"), "type", ["result_decision"])
    if _require_string(payload.get("attempt_id"), "attempt_id") != attempt_id:
        raise ContractError("attempt_id does not match the pending attempt")
    _require_enum(payload.get("action"), "action", ["continue", "revise", "abandon", "ask_human", "pivot"])
    _require_string(payload.get("rationale"), "rationale")
    refs = _require_list(payload.get("evidence_ids"), "evidence_ids")
    for ref in refs:
        if ref not in evidence_ids:
            raise ContractError("unknown evidence id: %s" % ref)
    updates = _require_list(payload.get("claim_updates"), "claim_updates", 1)
    for index, update_raw in enumerate(updates):
        update = _require_object(update_raw, "claim_updates[%d]" % index)
        _keys(update, ["claim_id", "assessment", "reason"], "claim_updates[%d]" % index)
        if update["claim_id"] not in claim_ids:
            raise ContractError("unknown claim id: %s" % update["claim_id"])
        _require_enum(update["assessment"], "claim_updates[%d].assessment" % index, ["supported", "weakened", "refuted", "inconclusive"])
        _require_string(update["reason"], "claim_updates[%d].reason" % index)
    paper_note = _require_object(payload.get("paper_note"), "paper_note")
    _keys(paper_note, ["section", "text"], "paper_note")
    _require_enum(paper_note["section"], "paper_note.section", ["related_work", "methods", "results", "limitations", "next_steps"])
    _require_string(paper_note["text"], "paper_note.text")


TOPIC_TEMPLATE = {
    "response_id": "unique-id",
    "type": "topic_synthesis",
    "direction_summary": "",
    "candidates": [
        {
            "id": "topic-1",
            "title": "",
            "question": "",
            "hypothesis": "",
            "claim": "",
            "why_valuable": "",
            "abstraction_level": "mechanism",
            "incremental_risk": "low",
            "novelty": {"status": "plausible", "evidence_ids": ["evidence-id"], "uncertainty": ""},
            "falsifier": "",
            "smallest_test": "",
            "risks": [],
        }
    ],
    "recommended_id": "topic-1",
    "stop": {"needs_human": False, "reason": ""},
}

EXPERIMENT_TEMPLATE = {
    "response_id": "unique-id",
    "type": "experiment_design",
    "topic_id": "approved-topic-id",
    "hypothesis": "",
    "claim_ids": ["claim-id"],
    "code_files": ["experiment.py"],
    "command": ["python3", "experiment.py", "--output", "{output_dir}/metrics.json"],
    "workdir": ".",
    "timeout_seconds": 300,
    "metrics_file": "metrics.json",
    "required_metrics": ["score"],
    "evaluator": {"primary_metric": "score", "direction": "maximize", "baseline": 0.0, "minimum_delta": 0.0},
    "validity": {
        "metric_claim_alignment": "",
        "baseline_rationale": "",
        "confounds": [],
        "negative_result_value": "",
        "risk": "low",
    },
    "resource_class": "small",
    "stochastic": False,
    "replications": 1,
}

CRITIC_TEMPLATE = {
    "response_id": "unique-id",
    "type": "critic",
    "critic_type": "novelty",
    "subject_id": "topic-or-experiment-id",
    "verdict": "pass",
    "issues": [],
    "required_changes": [],
    "rationale": "",
}

DECISION_TEMPLATE = {
    "response_id": "unique-id",
    "type": "result_decision",
    "attempt_id": "attempt-id",
    "action": "continue",
    "rationale": "",
    "evidence_ids": [],
    "claim_updates": [{"claim_id": "claim-id", "assessment": "inconclusive", "reason": ""}],
    "paper_note": {"section": "results", "text": ""},
}
