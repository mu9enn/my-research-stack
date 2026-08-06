from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from .contracts import CRITIC_TEMPLATE, DECISION_TEMPLATE, EXPERIMENT_TEMPLATE, TOPIC_TEMPLATE


PROMPT_DIR = Path(__file__).resolve().parents[1] / "prompts"


def _load(name: str) -> str:
    return (PROMPT_DIR / (name + ".md")).read_text(encoding="utf-8")


def next_packet(state: Dict[str, Any]) -> Dict[str, Any]:
    pending = state.get("pending") or {}
    kind = pending.get("kind")
    base = {
        "run_id": state["run_id"],
        "revision": state["revision"],
        "direction": state["direction"],
        "constraints": state["constraints"],
    }
    if kind == "topic_synthesis":
        base.update(
            {
                "task": "topic_synthesis",
                "instructions": _load("topic_synthesis"),
                "evidence": state["evidence"],
                "response_template": TOPIC_TEMPLATE,
            }
        )
        return base
    if kind == "experiment_design":
        base.update(
            {
                "task": "experiment_design",
                "instructions": _load("experiment_design"),
                "approved_topic": _selected_topic(state),
                "approved_claims": state["claims"],
                "prior_attempts": state["attempts"],
                "response_template": EXPERIMENT_TEMPLATE,
            }
        )
        return base
    if kind == "result_decision":
        attempt_id = pending["attempt_id"]
        attempt = next(item for item in state["attempts"] if item["id"] == attempt_id)
        experiment = next(item for item in state["experiments"] if item["id"] == attempt["experiment_id"])
        base.update(
            {
                "task": "result_decision",
                "instructions": _load("result_decision"),
                "approved_topic": _selected_topic(state),
                "approved_claims": state["claims"],
                "experiment": experiment,
                "attempt": attempt,
                "evidence": state["evidence"],
                "response_template": DECISION_TEMPLATE,
            }
        )
        return base
    if kind == "critic":
        critic_type = pending["critic_type"]
        subject = _subject(state, pending["subject_id"])
        template = dict(CRITIC_TEMPLATE)
        template["critic_type"] = critic_type
        template["subject_id"] = pending["subject_id"]
        base.update(
            {
                "task": "critic",
                "critic_type": critic_type,
                "instructions": _load("critic"),
                "subject": subject,
                "evidence": state["evidence"],
                "response_template": template,
            }
        )
        return base
    if kind == "execute":
        return {
            **base,
            "task": "execute",
            "experiment_id": pending["experiment_id"],
            "instruction": "Run `fc execute --run-id %s`." % state["run_id"],
        }
    if state["phase"] == "human":
        return {**base, "task": "human_decision", "reason": state.get("human_reason")}
    return {**base, "task": "none", "instruction": "No pending action."}


def _selected_topic(state: Dict[str, Any]) -> Dict[str, Any]:
    selected = state.get("selected_topic_id")
    return next(item for item in state["topics"] if item["id"] == selected)


def _subject(state: Dict[str, Any], subject_id: str) -> Dict[str, Any]:
    for collection in ("topics", "experiments"):
        for item in state[collection]:
            if item["id"] == subject_id:
                return item
    raise KeyError(subject_id)


def packet_json(state: Dict[str, Any]) -> str:
    return json.dumps(next_packet(state), ensure_ascii=False, indent=2, sort_keys=True)
