from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

from .contracts import (
    ContractError,
    validate_critic_response,
    validate_decision_response,
    validate_experiment_response,
    validate_topic_response,
)
from .evidence import local_evidence, search_all
from .prompts import packet_json
from .render import render_paper
from .runner import execute as execute_experiment
from .state import StateError, StateStore, find_by_id, initial_state, next_id, now_iso


ROOT = Path(__file__).resolve().parents[1]
RUNS_DIR = Path(os.environ.get("RESEARCH_CIRCLE_RUNS_DIR", str(ROOT / "runs"))).resolve()


def _slug(text: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return value[:48] or "research"


def _store(run_id: str) -> StateStore:
    if not run_id or "/" in run_id or "\\" in run_id or run_id in {".", ".."}:
        raise StateError("invalid run id")
    return StateStore(RUNS_DIR / run_id)


def _load_response(path: str) -> Dict[str, Any]:
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise ContractError("cannot read response JSON: %s" % error) from error
    if not isinstance(payload, dict):
        raise ContractError("response must be a JSON object")
    return payload


def _render(store: StateStore, state: Dict[str, Any]) -> None:
    render_paper(state, store.run_dir / "paper.md")


def cmd_init(args: argparse.Namespace) -> None:
    project = Path(args.project).resolve()
    if not project.is_dir():
        raise StateError("project directory does not exist: %s" % project)
    if len(args.direction.strip()) < 5:
        raise StateError("direction must contain at least five characters")
    run_id = args.run_id or "%s-%s" % (now_iso().replace(":", "").replace("+00:00", "Z"), _slug(args.direction))
    state = initial_state(run_id, args.direction.strip(), project, args.constraint or [], args.max_timeout)
    store = _store(run_id)
    store.create(state)
    _render(store, state)
    print(run_id)


def cmd_evidence_add(args: argparse.Namespace) -> None:
    store = _store(args.run_id)
    record = local_evidence(Path(args.file), args.title, args.locator, args.url or "")
    with store.lock():
        state = store.load_unlocked()
        existing = next((item for item in state["evidence"] if item["content_hash"] == record["content_hash"]), None)
        if existing:
            print(existing["id"])
            return
        record["id"] = next_id("evidence", state["evidence"])
        record["added_at"] = now_iso()
        state["evidence"].append(record)
        store.save_unlocked(state)
        _render(store, state)
    print(record["id"])


def cmd_evidence_search(args: argparse.Namespace) -> None:
    store = _store(args.run_id)
    with store.lock():
        state = store.load_unlocked()
        cached = next(
            (
                item
                for item in reversed(state["discovery_runs"])
                if item["query"] == args.query and item["limit"] == args.limit
            ),
            None,
        )
        if cached and not args.refresh:
            print(json.dumps(cached, ensure_ascii=False, indent=2, sort_keys=True))
            return
    records, errors, successful_sources = search_all(args.query, args.limit)
    with store.lock():
        state = store.load_unlocked()
        added = []
        for record in records:
            existing = next(
                (
                    item
                    for item in state["evidence"]
                    if item["content_hash"] == record["content_hash"]
                    or (record.get("remote_id") and item.get("remote_id") == record["remote_id"])
                ),
                None,
            )
            if existing:
                added.append(existing["id"])
                continue
            record["id"] = next_id("evidence", state["evidence"])
            record["added_at"] = now_iso()
            state["evidence"].append(record)
            added.append(record["id"])
        discovery = {
            "id": next_id("discovery", state["discovery_runs"]),
            "query": args.query,
            "limit": args.limit,
            "successful_sources": successful_sources,
            "errors": errors,
            "coverage": "complete" if len(successful_sources) == 3 else "partial",
            "evidence_ids": added,
            "created_at": now_iso(),
        }
        state["discovery_runs"].append(discovery)
        store.save_unlocked(state)
        _render(store, state)
    print(json.dumps(discovery, ensure_ascii=False, indent=2, sort_keys=True))


def cmd_next(args: argparse.Namespace) -> None:
    store = _store(args.run_id)
    with store.lock():
        state = store.load_unlocked()
    if state.get("pending", {}).get("kind") == "topic_synthesis" and not state["evidence"]:
        raise StateError("add or search evidence before topic synthesis")
    print(packet_json(state))


def _topic_critic_queue(state: Dict[str, Any], topic: Dict[str, Any]) -> List[str]:
    evidence = {item["id"]: item for item in state["evidence"]}
    refs = topic["novelty"]["evidence_ids"]
    queue = []
    if len(refs) < 2 or any(evidence[ref]["level"] != "primary_excerpt" for ref in refs):
        queue.append("novelty")
    if topic["incremental_risk"] == "high" or topic["abstraction_level"] == "phenomenon":
        queue.append("research_quality")
    return queue


def _set_critic(state: Dict[str, Any], critic_type: str, subject_id: str, remaining: List[str]) -> None:
    state["pending"] = {
        "kind": "critic",
        "critic_type": critic_type,
        "subject_id": subject_id,
        "remaining_critics": remaining,
    }


def _after_topic_reasoning(state: Dict[str, Any], topic: Dict[str, Any]) -> None:
    queue = _topic_critic_queue(state, topic)
    if queue:
        _set_critic(state, queue[0], topic["id"], queue[1:])
        state["phase"] = "topic"
    else:
        state["phase"] = "human"
        state["pending"] = None
        state["human_reason"] = "topic_approval"


def _after_experiment_reasoning(state: Dict[str, Any], experiment: Dict[str, Any]) -> None:
    if experiment["validity"]["risk"] == "high" or (experiment["stochastic"] and experiment["replications"] < 2):
        _set_critic(state, "validity", experiment["id"], [])
        state["phase"] = "experiment"
    elif experiment["resource_class"] == "large":
        state["phase"] = "human"
        state["pending"] = None
        state["human_reason"] = "large_resource:%s" % experiment["id"]
    else:
        state["phase"] = "experiment"
        state["pending"] = {"kind": "execute", "experiment_id": experiment["id"]}


def _apply_topic(state: Dict[str, Any], payload: Dict[str, Any]) -> None:
    evidence_ids = {item["id"] for item in state["evidence"]}
    validate_topic_response(payload, evidence_ids)
    existing = {item["id"] for item in state["topics"]}
    for candidate in payload["candidates"]:
        if candidate["id"] in existing:
            raise ContractError("topic id already exists: %s" % candidate["id"])
        candidate["status"] = "candidate"
        candidate["created_at"] = now_iso()
        state["topics"].append(candidate)
    state["recommended_topic_id"] = payload["recommended_id"]
    recommended = find_by_id(state["topics"], payload["recommended_id"], "topic")
    if payload["stop"]["needs_human"]:
        state["phase"] = "human"
        state["pending"] = None
        state["human_reason"] = "topic_uncertainty:%s" % payload["stop"]["reason"]
    else:
        _after_topic_reasoning(state, recommended)


def _apply_experiment(state: Dict[str, Any], payload: Dict[str, Any]) -> None:
    claim_ids = {item["id"] for item in state["claims"]}
    validate_experiment_response(
        payload,
        state["selected_topic_id"],
        claim_ids,
        state["limits"]["max_timeout_seconds"],
    )
    experiment = {key: value for key, value in payload.items() if key not in {"response_id", "type"}}
    experiment["id"] = next_id("experiment", state["experiments"])
    experiment["status"] = "planned"
    experiment["human_approved"] = experiment["resource_class"] == "small"
    experiment["created_at"] = now_iso()
    state["experiments"].append(experiment)
    _after_experiment_reasoning(state, experiment)


def _apply_critic(state: Dict[str, Any], payload: Dict[str, Any], pending: Dict[str, Any]) -> None:
    validate_critic_response(payload, pending["critic_type"], pending["subject_id"])
    record = {key: value for key, value in payload.items() if key != "response_id"}
    record["id"] = next_id("critic", state["critics"])
    record["created_at"] = now_iso()
    state["critics"].append(record)
    verdict = payload["verdict"]
    subject_id = pending["subject_id"]
    if verdict == "pass":
        remaining = pending.get("remaining_critics") or []
        if remaining:
            _set_critic(state, remaining[0], subject_id, remaining[1:])
            return
        if subject_id.startswith("experiment-"):
            _after_experiment_reasoning(state, find_by_id(state["experiments"], subject_id, "experiment"))
        else:
            state["phase"] = "human"
            state["pending"] = None
            state["human_reason"] = "topic_approval"
        return
    if verdict == "human":
        state["phase"] = "human"
        state["pending"] = None
        state["human_reason"] = "critic:%s:%s" % (payload["critic_type"], subject_id)
        return
    if subject_id.startswith("experiment-"):
        find_by_id(state["experiments"], subject_id, "experiment")["status"] = verdict
        state["phase"] = "experiment"
        state["pending"] = {"kind": "experiment_design"}
    else:
        find_by_id(state["topics"], subject_id, "topic")["status"] = verdict
        state["phase"] = "topic"
        state["pending"] = {"kind": "topic_synthesis"}


def _apply_decision(state: Dict[str, Any], payload: Dict[str, Any], pending: Dict[str, Any]) -> None:
    claim_ids = {item["id"] for item in state["claims"]}
    evidence_ids = {item["id"] for item in state["evidence"]}
    validate_decision_response(payload, pending["attempt_id"], claim_ids, evidence_ids)
    decision = {key: value for key, value in payload.items() if key not in {"response_id", "type", "paper_note"}}
    decision["id"] = next_id("decision", state["decisions"])
    decision["created_at"] = now_iso()
    state["decisions"].append(decision)
    for update in payload["claim_updates"]:
        claim = find_by_id(state["claims"], update["claim_id"], "claim")
        claim.setdefault("assessments", []).append(
            {
                "attempt_id": pending["attempt_id"],
                "assessment": update["assessment"],
                "reason": update["reason"],
                "created_at": now_iso(),
            }
        )
    state["paper_notes"].append(
        {
            "id": next_id("note", state["paper_notes"]),
            "attempt_id": pending["attempt_id"],
            "section": payload["paper_note"]["section"],
            "text": payload["paper_note"]["text"],
            "evidence_ids": payload["evidence_ids"],
            "claim_ids": [item["claim_id"] for item in payload["claim_updates"]],
            "created_at": now_iso(),
        }
    )
    action = payload["action"]
    if action in {"continue", "revise"}:
        state["phase"] = "experiment"
        state["pending"] = {"kind": "experiment_design"}
        state["human_reason"] = None
    elif action == "abandon":
        selected = find_by_id(state["topics"], state["selected_topic_id"], "topic")
        selected["status"] = "abandoned"
        state["selected_topic_id"] = None
        state["phase"] = "topic"
        state["pending"] = {"kind": "topic_synthesis"}
        state["human_reason"] = None
    else:
        state["phase"] = "human"
        state["pending"] = None
        state["human_reason"] = "major_pivot" if action == "pivot" else "result_judgment"


def cmd_apply(args: argparse.Namespace) -> None:
    payload = _load_response(args.response)
    store = _store(args.run_id)
    with store.lock():
        state = store.load_unlocked()
        response_id = payload.get("response_id")
        if response_id in state["applied_response_ids"]:
            raise ContractError("response_id was already applied")
        pending = state.get("pending") or {}
        kind = pending.get("kind")
        response_type = payload.get("type")
        expected = {
            "topic_synthesis": "topic_synthesis",
            "experiment_design": "experiment_design",
            "critic": "critic",
            "result_decision": "result_decision",
        }.get(kind)
        if not expected or response_type != expected:
            raise ContractError("response type %r does not match pending action %r" % (response_type, kind))
        if kind == "topic_synthesis":
            _apply_topic(state, payload)
        elif kind == "experiment_design":
            _apply_experiment(state, payload)
        elif kind == "critic":
            _apply_critic(state, payload, pending)
        else:
            _apply_decision(state, payload, pending)
        state["applied_response_ids"].append(response_id)
        store.save_unlocked(state)
        _render(store, state)
    print("applied %s at revision %d" % (response_id, state["revision"]))


def cmd_approve(args: argparse.Namespace) -> None:
    store = _store(args.run_id)
    with store.lock():
        state = store.load_unlocked()
        reason = state.get("human_reason") or ""
        if args.topic_id:
            if not reason.startswith("topic_") and not reason.startswith("critic:"):
                raise StateError("topic approval is not pending")
            topic = find_by_id(state["topics"], args.topic_id, "topic")
            for item in state["topics"]:
                if item["status"] == "candidate":
                    item["status"] = "rejected"
            topic["status"] = "approved"
            state["selected_topic_id"] = topic["id"]
            claim = {
                "id": next_id("claim", state["claims"]),
                "topic_id": topic["id"],
                "text": (args.claim or topic["claim"]).strip(),
                "status": "human_approved",
                "approved_at": now_iso(),
                "assessments": [],
            }
            if not claim["text"]:
                raise StateError("approved claim cannot be empty")
            state["claims"].append(claim)
            state["phase"] = "experiment"
            state["pending"] = {"kind": "experiment_design"}
            state["human_reason"] = None
        elif args.experiment_id:
            expected = "large_resource:%s" % args.experiment_id
            critic_override = reason == "critic:validity:%s" % args.experiment_id
            if reason != expected and not critic_override:
                raise StateError("this experiment is not awaiting resource approval")
            experiment = find_by_id(state["experiments"], args.experiment_id, "experiment")
            experiment["human_approved"] = True
            state.setdefault("human_decisions", []).append(
                {"kind": "experiment_approval", "experiment_id": experiment["id"], "reason": reason, "at": now_iso()}
            )
            state["phase"] = "experiment"
            state["pending"] = {"kind": "execute", "experiment_id": experiment["id"]}
            state["human_reason"] = None
        elif args.result_action:
            if reason != "result_judgment":
                raise StateError("result judgment is not pending")
            state.setdefault("human_decisions", []).append(
                {"kind": "result_action", "action": args.result_action, "at": now_iso()}
            )
            if args.result_action in {"continue", "revise"}:
                state["phase"] = "experiment"
                state["pending"] = {"kind": "experiment_design"}
            else:
                if state.get("selected_topic_id"):
                    find_by_id(state["topics"], state["selected_topic_id"], "topic")["status"] = "abandoned"
                state["selected_topic_id"] = None
                state["phase"] = "topic"
                state["pending"] = {"kind": "topic_synthesis"}
            state["human_reason"] = None
        elif args.pivot_direction:
            if reason != "major_pivot":
                raise StateError("major pivot approval is not pending")
            state.setdefault("human_decisions", []).append(
                {"kind": "pivot", "old_direction": state["direction"], "new_direction": args.pivot_direction, "at": now_iso()}
            )
            state["direction"] = args.pivot_direction.strip()
            state["selected_topic_id"] = None
            state["phase"] = "topic"
            state["pending"] = {"kind": "topic_synthesis"}
            state["human_reason"] = None
        else:
            raise StateError("approve requires a topic, experiment, result action, or pivot direction")
        store.save_unlocked(state)
        _render(store, state)
    print("approved at revision %d" % state["revision"])


def cmd_execute(args: argparse.Namespace) -> None:
    store = _store(args.run_id)
    attempt_id, exit_code = execute_experiment(store, args.experiment_id)
    with store.lock():
        state = store.load_unlocked()
        _render(store, state)
    print("%s exit=%d" % (attempt_id, exit_code))


def _pid_alive(pid: int) -> bool:
    if not pid:
        return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def cmd_resume(args: argparse.Namespace) -> None:
    store = _store(args.run_id)
    changed = False
    recovered = False
    with store.lock():
        try:
            state = store.load_unlocked()
        except StateError:
            state = store.load_unlocked(recover=True)
            recovered = True
        running = [item for item in state["attempts"] if item["status"] in {"starting", "running"}]
        for attempt in running:
            if _pid_alive(attempt.get("pid")):
                print("attempt still running: %s pid=%s" % (attempt["id"], attempt["pid"]))
                continue
            attempt["status"] = "interrupted"
            attempt["finished_at"] = now_iso()
            attempt["error"] = "runner process disappeared before terminal state"
            experiment = find_by_id(state["experiments"], attempt["experiment_id"], "experiment")
            experiment["status"] = "planned"
            state["phase"] = "experiment"
            state["pending"] = {"kind": "execute", "experiment_id": experiment["id"], "retry_of": attempt["id"]}
            changed = True
        if recovered:
            store.restore_unlocked(state)
            _render(store, state)
        elif changed:
            store.save_unlocked(state)
            _render(store, state)
    print("recovered backup" if recovered else ("resumed" if changed else "state is already consistent"))


def cmd_status(args: argparse.Namespace) -> None:
    store = _store(args.run_id)
    with store.lock():
        state = store.load_unlocked()
    summary = {
        "run_id": state["run_id"],
        "revision": state["revision"],
        "phase": state["phase"],
        "pending": state.get("pending"),
        "human_reason": state.get("human_reason"),
        "selected_topic_id": state.get("selected_topic_id"),
        "counts": {
            "evidence": len(state["evidence"]),
            "topics": len(state["topics"]),
            "claims": len(state["claims"]),
            "experiments": len(state["experiments"]),
            "attempts": len(state["attempts"]),
            "decisions": len(state["decisions"]),
        },
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))


def cmd_render(args: argparse.Namespace) -> None:
    store = _store(args.run_id)
    with store.lock():
        state = store.load_unlocked()
        _render(store, state)
    print(store.run_dir / "paper.md")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="fc", description="Evidence-driven Research Circle")
    commands = parser.add_subparsers(dest="command", required=True)

    init = commands.add_parser("init")
    init.add_argument("--direction", required=True)
    init.add_argument("--project", required=True)
    init.add_argument("--run-id")
    init.add_argument("--constraint", action="append")
    init.add_argument("--max-timeout", type=int, default=3600)
    init.set_defaults(func=cmd_init)

    evidence = commands.add_parser("evidence")
    evidence_commands = evidence.add_subparsers(dest="evidence_command", required=True)
    add = evidence_commands.add_parser("add")
    add.add_argument("--run-id", required=True)
    add.add_argument("--file", required=True)
    add.add_argument("--title", required=True)
    add.add_argument("--locator", required=True)
    add.add_argument("--url")
    add.set_defaults(func=cmd_evidence_add)
    search = evidence_commands.add_parser("search")
    search.add_argument("--run-id", required=True)
    search.add_argument("--query", required=True)
    search.add_argument("--limit", type=int, default=10)
    search.add_argument("--refresh", action="store_true")
    search.set_defaults(func=cmd_evidence_search)

    for name, function in (("next", cmd_next), ("status", cmd_status), ("resume", cmd_resume), ("render", cmd_render)):
        command = commands.add_parser(name)
        command.add_argument("--run-id", required=True)
        command.set_defaults(func=function)

    apply_command = commands.add_parser("apply")
    apply_command.add_argument("--run-id", required=True)
    apply_command.add_argument("--response", required=True)
    apply_command.set_defaults(func=cmd_apply)

    approve = commands.add_parser("approve")
    approve.add_argument("--run-id", required=True)
    approve.add_argument("--topic-id")
    approve.add_argument("--claim")
    approve.add_argument("--experiment-id")
    approve.add_argument("--result-action", choices=["continue", "revise", "abandon"])
    approve.add_argument("--pivot-direction")
    approve.set_defaults(func=cmd_approve)

    execute = commands.add_parser("execute")
    execute.add_argument("--run-id", required=True)
    execute.add_argument("--experiment-id")
    execute.set_defaults(func=cmd_execute)
    return parser


def main(argv: List[str] = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
        if getattr(args, "max_timeout", 1) < 1:
            raise StateError("--max-timeout must be positive")
        args.func(args)
        return 0
    except (StateError, ContractError, ValueError) as error:
        print("error: %s" % error, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
