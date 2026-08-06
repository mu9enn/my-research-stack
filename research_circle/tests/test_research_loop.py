from __future__ import annotations

import json
import os
import signal
import subprocess
import time
from pathlib import Path

import pytest

from research_circle import evidence as evidence_module
from research_circle.contracts import ContractError, validate_experiment_response
from research_circle.state import StateStore, initial_state


ROOT = Path(__file__).resolve().parents[1]
FC = ROOT / "bin" / "fc"
TOY_PROJECT = ROOT / "tests" / "fixtures" / "toy_experiment"
EVIDENCE_DIR = ROOT / "tests" / "fixtures" / "evidence"


def invoke(runs_dir: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    env = dict(os.environ)
    env["RESEARCH_CIRCLE_RUNS_DIR"] = str(runs_dir)
    return subprocess.run(
        [str(FC), *args],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=check,
    )


def write_json(path: Path, payload: dict) -> Path:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def topic_payload(response_id: str = "topic-response-1", *, high_risk: bool = False) -> dict:
    candidates = []
    for index in range(1, 4):
        candidates.append(
            {
                "id": "topic-%d" % index,
                "title": "Mechanism test %d" % index,
                "question": "Does intervention %d improve a fixed diagnostic?" % index,
                "hypothesis": "The intervention changes the diagnostic score.",
                "claim": "In the toy setting, the intervention improves the diagnostic score.",
                "why_valuable": "It separates a mechanism from aggregate behavior.",
                "abstraction_level": "mechanism",
                "incremental_risk": "high" if high_risk and index == 1 else "low",
                "novelty": {
                    "status": "plausible",
                    "evidence_ids": ["evidence-0001", "evidence-0002"],
                    "uncertainty": "The fixture covers only a scoped toy setting.",
                },
                "falsifier": "A score at or below the fixed baseline plus delta.",
                "smallest_test": "Run the deterministic toy experiment once.",
                "risks": ["toy external validity"],
            }
        )
    return {
        "response_id": response_id,
        "type": "topic_synthesis",
        "direction_summary": "Mechanism-aware evaluation in a deterministic fixture.",
        "candidates": candidates,
        "recommended_id": "topic-1",
        "stop": {"needs_human": False, "reason": ""},
    }


def experiment_payload(
    response_id: str = "experiment-response-1",
    *,
    effect: float = 0.2,
    extra_args=None,
    timeout: int = 10,
    validity_risk: str = "low",
) -> dict:
    command = ["python3", "experiment.py", "--output", "{output_dir}/metrics.json", "--effect", str(effect)]
    command.extend(extra_args or [])
    return {
        "response_id": response_id,
        "type": "experiment_design",
        "topic_id": "topic-1",
        "hypothesis": "The intervention raises score by at least 0.1.",
        "claim_ids": ["claim-0001"],
        "code_files": ["experiment.py"],
        "command": command,
        "workdir": ".",
        "timeout_seconds": timeout,
        "metrics_file": "metrics.json",
        "required_metrics": ["score"],
        "evaluator": {
            "primary_metric": "score",
            "direction": "maximize",
            "baseline": 0.5,
            "minimum_delta": 0.1,
        },
        "validity": {
            "metric_claim_alignment": "The score directly operationalizes the scoped claim.",
            "baseline_rationale": "0.5 is emitted by the no-effect fixture.",
            "confounds": [],
            "negative_result_value": "It rejects the proposed intervention in this setting.",
            "risk": validity_risk,
        },
        "resource_class": "small",
        "stochastic": False,
        "replications": 1,
    }


def decision_payload(action: str, assessment: str, response_id: str = "decision-response-1") -> dict:
    return {
        "response_id": response_id,
        "type": "result_decision",
        "attempt_id": "attempt-0001",
        "action": action,
        "rationale": "The fixed evaluator changed belief in the scoped claim.",
        "evidence_ids": ["evidence-0001", "evidence-0002"],
        "claim_updates": [
            {
                "claim_id": "claim-0001",
                "assessment": assessment,
                "reason": "The attempt is interpreted only within the toy setting.",
            }
        ],
        "paper_note": {
            "section": "results",
            "text": "The deterministic toy experiment is reported with its fixed evaluator and scoped limitation.",
        },
    }


def bootstrap(tmp_path: Path, *, high_risk: bool = False) -> Path:
    runs = tmp_path / "runs"
    invoke(runs, "init", "--direction", "Mechanism-aware toy evaluation", "--project", str(TOY_PROJECT), "--run-id", "demo")
    for name, title in (("mechanism.txt", "Mechanism evidence"), ("evaluation.txt", "Evaluator evidence")):
        invoke(
            runs,
            "evidence",
            "add",
            "--run-id",
            "demo",
            "--file",
            str(EVIDENCE_DIR / name),
            "--title",
            title,
            "--locator",
            "fixture paragraph 1",
        )
    response = write_json(tmp_path / "topics.json", topic_payload(high_risk=high_risk))
    invoke(runs, "apply", "--run-id", "demo", "--response", str(response))
    return runs


def approve_and_design(tmp_path: Path, *, effect=0.2, extra_args=None, timeout=10) -> Path:
    runs = bootstrap(tmp_path)
    invoke(runs, "approve", "--run-id", "demo", "--topic-id", "topic-1")
    response = write_json(
        tmp_path / "experiment.json",
        experiment_payload(effect=effect, extra_args=extra_args, timeout=timeout),
    )
    invoke(runs, "apply", "--run-id", "demo", "--response", str(response))
    return runs


def load_state(runs: Path) -> dict:
    return json.loads((runs / "demo" / "state.json").read_text(encoding="utf-8"))


def test_positive_end_to_end_updates_next_step_and_paper(tmp_path: Path) -> None:
    runs = approve_and_design(tmp_path, effect=0.2)
    execution = invoke(runs, "execute", "--run-id", "demo")
    assert "attempt-0001 exit=0" in execution.stdout
    state = load_state(runs)
    assert state["attempts"][0]["status"] == "completed"
    assert state["attempts"][0]["evaluator_outcome"] == "improved"
    assert "experiment.py" in state["attempts"][0]["code_input_hashes"]
    decision = write_json(tmp_path / "decision.json", decision_payload("continue", "supported"))
    invoke(runs, "apply", "--run-id", "demo", "--response", str(decision))
    state = load_state(runs)
    assert state["pending"] == {"kind": "experiment_design"}
    paper = (runs / "demo" / "paper.md").read_text(encoding="utf-8")
    assert "score=0.7" in paper
    assert "attempt-0001" in paper
    assert "evidence-0001" in paper
    assert "Declared code hashes" in paper


def test_next_returns_one_prompt_and_validated_template(tmp_path: Path) -> None:
    runs = tmp_path / "runs"
    invoke(runs, "init", "--direction", "Mechanism-aware toy evaluation", "--project", str(TOY_PROJECT), "--run-id", "demo")
    blocked = invoke(runs, "next", "--run-id", "demo", check=False)
    assert blocked.returncode == 2
    assert "add or search evidence" in blocked.stderr
    invoke(
        runs,
        "evidence",
        "add",
        "--run-id",
        "demo",
        "--file",
        str(EVIDENCE_DIR / "mechanism.txt"),
        "--title",
        "Mechanism evidence",
        "--locator",
        "fixture paragraph 1",
    )
    packet = json.loads(invoke(runs, "next", "--run-id", "demo").stdout)
    assert packet["task"] == "topic_synthesis"
    assert packet["response_template"]["type"] == "topic_synthesis"
    assert "Use only the supplied evidence" in packet["instructions"]


def test_cli_entrypoint_works_outside_repository(tmp_path: Path) -> None:
    result = subprocess.run([str(FC), "--help"], cwd=tmp_path, text=True, capture_output=True, check=True)
    assert "Evidence-driven Research Circle" in result.stdout


def test_negative_result_can_revise_without_overwriting_claim(tmp_path: Path) -> None:
    runs = approve_and_design(tmp_path, effect=-0.1)
    invoke(runs, "execute", "--run-id", "demo")
    state = load_state(runs)
    original_claim = state["claims"][0]["text"]
    assert state["attempts"][0]["evaluator_outcome"] == "not_improved"
    decision = write_json(tmp_path / "decision.json", decision_payload("revise", "weakened"))
    invoke(runs, "apply", "--run-id", "demo", "--response", str(decision))
    state = load_state(runs)
    assert state["claims"][0]["text"] == original_claim
    assert state["claims"][0]["assessments"][0]["assessment"] == "weakened"
    assert state["phase"] == "experiment"


def test_model_can_escalate_result_but_human_resolves_action(tmp_path: Path) -> None:
    runs = approve_and_design(tmp_path, effect=0.0)
    invoke(runs, "execute", "--run-id", "demo")
    decision = decision_payload("ask_human", "inconclusive")
    response = write_json(tmp_path / "decision.json", decision)
    invoke(runs, "apply", "--run-id", "demo", "--response", str(response))
    state = load_state(runs)
    assert state["human_reason"] == "result_judgment"
    invoke(runs, "approve", "--run-id", "demo", "--result-action", "revise")
    state = load_state(runs)
    assert state["pending"] == {"kind": "experiment_design"}
    assert state["human_decisions"][0]["action"] == "revise"


@pytest.mark.parametrize(
    "extra_args,timeout,expected",
    [(["--fail"], 10, "failed"), (["--invalid"], 10, "invalid_metrics"), (["--sleep", "2"], 1, "timed_out")],
)
def test_runner_failure_modes_are_recorded(tmp_path: Path, extra_args, timeout, expected) -> None:
    runs = approve_and_design(tmp_path, extra_args=extra_args, timeout=timeout)
    invoke(runs, "execute", "--run-id", "demo", check=True)
    state = load_state(runs)
    assert state["attempts"][0]["status"] == expected
    assert state["attempts"][0]["evaluator_outcome"] is None
    assert state["pending"]["kind"] == "result_decision"
    paper = (runs / "demo" / "paper.md").read_text(encoding="utf-8")
    assert "execution failure is not scientific evidence" in paper


def test_missing_executable_is_a_recorded_failure_not_a_traceback(tmp_path: Path) -> None:
    runs = approve_and_design(tmp_path)
    store = StateStore(runs / "demo")
    with store.lock():
        state = store.load_unlocked()
        state["experiments"][0]["command"] = ["definitely-not-a-real-executable", "{output_dir}"]
        store.save_unlocked(state)
    result = invoke(runs, "execute", "--run-id", "demo")
    assert result.returncode == 0
    state = load_state(runs)
    assert state["attempts"][0]["status"] == "failed"
    assert "could not start experiment" in state["attempts"][0]["error"]


def test_risk_critic_is_advisory_and_routes_to_human(tmp_path: Path) -> None:
    runs = bootstrap(tmp_path, high_risk=True)
    state = load_state(runs)
    assert state["pending"]["kind"] == "critic"
    assert state["pending"]["critic_type"] == "research_quality"
    critic = {
        "response_id": "critic-response-1",
        "type": "critic",
        "critic_type": "research_quality",
        "subject_id": "topic-1",
        "verdict": "pass",
        "issues": ["Scoped external validity"],
        "required_changes": [],
        "rationale": "The mechanism-level question remains informative.",
    }
    response = write_json(tmp_path / "critic.json", critic)
    invoke(runs, "apply", "--run-id", "demo", "--response", str(response))
    state = load_state(runs)
    assert state["phase"] == "human"
    assert state["human_reason"] == "topic_approval"
    assert state["critics"][0]["subject_id"] == "topic-1"


def test_large_resource_experiment_requires_explicit_human_approval(tmp_path: Path) -> None:
    runs = bootstrap(tmp_path)
    invoke(runs, "approve", "--run-id", "demo", "--topic-id", "topic-1")
    payload = experiment_payload()
    payload["resource_class"] = "large"
    response = write_json(tmp_path / "large.json", payload)
    invoke(runs, "apply", "--run-id", "demo", "--response", str(response))
    state = load_state(runs)
    assert state["phase"] == "human"
    assert state["human_reason"] == "large_resource:experiment-0001"
    blocked = invoke(runs, "execute", "--run-id", "demo", check=False)
    assert blocked.returncode == 2
    invoke(runs, "approve", "--run-id", "demo", "--experiment-id", "experiment-0001")
    invoke(runs, "execute", "--run-id", "demo")
    assert load_state(runs)["attempts"][0]["status"] == "completed"


def test_duplicate_and_out_of_order_responses_are_rejected(tmp_path: Path) -> None:
    runs = bootstrap(tmp_path)
    response = tmp_path / "topics.json"
    duplicate = invoke(runs, "apply", "--run-id", "demo", "--response", str(response), check=False)
    assert duplicate.returncode == 2
    assert "already applied" in duplicate.stderr
    wrong = write_json(tmp_path / "wrong.json", experiment_payload())
    result = invoke(runs, "apply", "--run-id", "demo", "--response", str(wrong), check=False)
    assert result.returncode == 2
    assert "does not match pending action" in result.stderr


def test_resume_marks_orphaned_attempt_and_preserves_attempt_id(tmp_path: Path) -> None:
    runs = approve_and_design(tmp_path)
    store = StateStore(runs / "demo")
    with store.lock():
        state = store.load_unlocked()
        state["attempts"].append(
            {
                "id": "attempt-0001",
                "experiment_id": "experiment-0001",
                "status": "running",
                "started_at": "2026-01-01T00:00:00+00:00",
                "finished_at": None,
                "pid": 99999999,
                "exit_code": None,
                "metrics": None,
                "evaluator_outcome": None,
                "error": None,
                "output_dir": "attempts/attempt-0001",
            }
        )
        state["pending"] = None
        store.save_unlocked(state)
    invoke(runs, "resume", "--run-id", "demo")
    state = load_state(runs)
    assert state["attempts"][0]["status"] == "interrupted"
    assert state["pending"]["retry_of"] == "attempt-0001"
    invoke(runs, "execute", "--run-id", "demo")
    state = load_state(runs)
    assert [item["id"] for item in state["attempts"]] == ["attempt-0001", "attempt-0002"]
    assert state["attempts"][1]["status"] == "completed"


def test_state_backup_recovers_last_valid_revision(tmp_path: Path) -> None:
    store = StateStore(tmp_path / "run")
    state = initial_state("run", "Direction", TOY_PROJECT, [], 10)
    store.create(state)
    with store.lock():
        loaded = store.load_unlocked()
        loaded["constraints"].append("bounded")
        store.save_unlocked(loaded)
    store.state_path.write_text("{broken", encoding="utf-8")
    with store.lock():
        recovered = store.load_unlocked(recover=True)
    assert recovered["revision"] == 1


def test_cli_resume_restores_corrupt_state_from_backup(tmp_path: Path) -> None:
    runs = bootstrap(tmp_path)
    state_path = runs / "demo" / "state.json"
    state_path.write_text("{broken", encoding="utf-8")
    result = invoke(runs, "resume", "--run-id", "demo")
    assert "recovered backup" in result.stdout
    restored = load_state(runs)
    assert restored["run_id"] == "demo"
    assert restored["revision"] >= 3


def test_real_runner_interruption_is_resumable(tmp_path: Path) -> None:
    runs = approve_and_design(tmp_path, extra_args=["--sleep", "2"], timeout=10)
    env = dict(os.environ)
    env["RESEARCH_CIRCLE_RUNS_DIR"] = str(runs)
    parent = subprocess.Popen(
        [str(FC), "execute", "--run-id", "demo"],
        cwd=ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    child_pid = None
    deadline = time.time() + 5
    while time.time() < deadline:
        state = load_state(runs)
        if state["attempts"] and state["attempts"][0].get("pid"):
            child_pid = state["attempts"][0]["pid"]
            break
        time.sleep(0.05)
    assert child_pid is not None
    parent.kill()
    parent.wait(timeout=5)
    try:
        os.killpg(child_pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    deadline = time.time() + 3
    while time.time() < deadline:
        try:
            os.kill(child_pid, 0)
        except OSError:
            break
        time.sleep(0.05)
    invoke(runs, "resume", "--run-id", "demo")
    state = load_state(runs)
    assert state["attempts"][0]["status"] == "interrupted"
    assert state["pending"]["retry_of"] == "attempt-0001"
    invoke(runs, "execute", "--run-id", "demo")
    state = load_state(runs)
    assert state["attempts"][1]["id"] == "attempt-0002"
    assert state["attempts"][1]["status"] == "completed"


def test_contract_rejects_path_escape_and_shell_placeholder() -> None:
    payload = experiment_payload()
    payload["workdir"] = "../outside"
    with pytest.raises(ContractError, match="workdir"):
        validate_experiment_response(payload, "topic-1", {"claim-0001"}, 100)
    payload = experiment_payload()
    payload["command"] = ["python3", "{project_dir}/bad.py"]
    with pytest.raises(ContractError, match="placeholder"):
        validate_experiment_response(payload, "topic-1", {"claim-0001"}, 100)


def test_search_is_partial_and_fail_soft(monkeypatch) -> None:
    monkeypatch.setattr(
        evidence_module,
        "SEARCHERS",
        {
            "ok": lambda query, limit: [
                {
                    "remote_id": "ok:1",
                    "title": "  Paper  ",
                    "url": "https://example.test/1",
                    "locator": "abstract",
                    "snippet": "Evidence",
                    "content_hash": "hash",
                    "level": "discovery_abstract",
                    "source": "ok",
                    "source_path": None,
                },
                {
                    "remote_id": "ok:duplicate",
                    "title": "  Paper  ",
                    "url": "https://example.test/1",
                    "locator": "abstract",
                    "snippet": "Duplicate",
                    "content_hash": "hash-2",
                    "level": "discovery_abstract",
                    "source": "ok",
                    "source_path": None,
                },
            ],
            "bad": lambda query, limit: (_ for _ in ()).throw(RuntimeError("rate limited")),
        },
    )
    records, errors, successful = evidence_module.search_all("query", 2)
    assert [item["remote_id"] for item in records] == ["ok:1"]
    assert "rate limited" in errors["bad"]
    assert successful == ["ok"]


def test_retrieval_normalization_and_structure_reduction() -> None:
    record = evidence_module._normalize("source", "1", "  A   title ", "https://example.test", "  many\n spaces ")
    assert record["title"] == "A title"
    assert record["snippet"] == "many spaces"
    assert not list((ROOT / "agents").glob("*.md"))
    assert [path.parent.name for path in (ROOT / "skills").glob("*/SKILL.md")] == ["research-loop"]
