from __future__ import annotations

import hashlib
import json
import math
import os
import signal
import subprocess
from pathlib import Path
from typing import Any, Dict, Tuple

from .state import StateError, StateStore, find_by_id, next_id, now_iso


def _inside(base: Path, candidate: Path, label: str) -> Path:
    base = base.resolve()
    candidate = candidate.resolve()
    try:
        candidate.relative_to(base)
    except ValueError as error:
        raise StateError("%s escapes its allowed directory" % label) from error
    return candidate


def _parse_metrics(path: Path, required: list) -> Dict[str, float]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise StateError("metrics file is missing or invalid JSON: %s" % error) from error
    if not isinstance(raw, dict):
        raise StateError("metrics file must contain a JSON object")
    metrics = {}
    for name in required:
        value = raw.get(name)
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(float(value)):
            raise StateError("required metric %s is missing or non-finite" % name)
        metrics[name] = float(value)
    return metrics


def _evaluate(experiment: Dict[str, Any], metrics: Dict[str, float]) -> str:
    evaluator = experiment["evaluator"]
    value = metrics[evaluator["primary_metric"]]
    baseline = float(evaluator["baseline"])
    delta = float(evaluator["minimum_delta"])
    if evaluator["direction"] == "maximize":
        return "improved" if value >= baseline + delta else "not_improved"
    return "improved" if value <= baseline - delta else "not_improved"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _tail(path: Path, limit: int = 4000) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    return text[-limit:]


def _code_provenance(project_dir: Path) -> Tuple[str, str]:
    try:
        revision = subprocess.run(
            ["git", "-C", str(project_dir), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        diff = subprocess.run(
            ["git", "-C", str(project_dir), "diff", "--binary", "HEAD"],
            check=True,
            capture_output=True,
        ).stdout
        return revision, hashlib.sha256(diff).hexdigest()
    except (OSError, subprocess.CalledProcessError):
        return "unversioned", "unversioned"


def _code_input_hashes(project_dir: Path, code_files: list) -> Dict[str, str]:
    hashes = {}
    for relative in code_files:
        path = _inside(project_dir, project_dir / relative, "code_file")
        if not path.is_file():
            raise StateError("declared code file does not exist: %s" % relative)
        hashes[relative] = _sha256(path)
    return hashes


def execute(store: StateStore, experiment_id: str = None) -> Tuple[str, int]:
    with store.lock():
        state = store.load_unlocked()
        pending = state.get("pending") or {}
        expected = pending.get("experiment_id") if pending.get("kind") == "execute" else None
        target_id = experiment_id or expected
        if not target_id or target_id != expected:
            raise StateError("no matching experiment is ready to execute")
        experiment = find_by_id(state["experiments"], target_id, "experiment")
        if experiment.get("resource_class") == "large" and not experiment.get("human_approved"):
            raise StateError("large-resource experiment requires human approval")
        project_dir = Path(state["project_dir"])
        workdir = _inside(project_dir, project_dir / experiment["workdir"], "workdir")
        code_revision, working_tree_hash = _code_provenance(project_dir)
        code_input_hashes = _code_input_hashes(project_dir, experiment["code_files"])
        attempt_id = next_id("attempt", state["attempts"])
        attempt_dir = store.run_dir / "attempts" / attempt_id
        attempt_dir.mkdir(parents=True, exist_ok=False)
        attempt = {
            "id": attempt_id,
            "experiment_id": target_id,
            "status": "starting",
            "started_at": now_iso(),
            "finished_at": None,
            "pid": None,
            "exit_code": None,
            "metrics": None,
            "evaluator_outcome": None,
            "error": None,
            "stdout_tail": "",
            "stderr_tail": "",
            "artifact_hashes": {},
            "output_dir": str(attempt_dir.relative_to(store.run_dir)),
        }
        state["attempts"].append(attempt)
        experiment["status"] = "running"
        state["pending"] = None
        (attempt_dir / "input.json").write_text(
            json.dumps(experiment, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        store.save_unlocked(state)

    metrics_path = _inside(attempt_dir, attempt_dir / experiment["metrics_file"], "metrics_file")
    command = [arg.replace("{output_dir}", str(attempt_dir)) for arg in experiment["command"]]
    stdout_path = attempt_dir / "stdout.log"
    stderr_path = attempt_dir / "stderr.log"
    process = None
    status = "failed"
    exit_code = 1
    error_text = None
    metrics = None
    evaluator_outcome = None

    try:
        with stdout_path.open("wb") as stdout, stderr_path.open("wb") as stderr:
            process = subprocess.Popen(
                command,
                cwd=str(workdir),
                stdout=stdout,
                stderr=stderr,
                shell=False,
                start_new_session=True,
            )
            with store.lock():
                running_state = store.load_unlocked()
                running_attempt = find_by_id(running_state["attempts"], attempt_id, "attempt")
                running_attempt["status"] = "running"
                running_attempt["pid"] = process.pid
                store.save_unlocked(running_state)
            try:
                exit_code = process.wait(timeout=experiment["timeout_seconds"])
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGTERM)
                try:
                    process.wait(timeout=3)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()
                status = "timed_out"
                exit_code = process.returncode if process.returncode is not None else -signal.SIGKILL
                error_text = "experiment exceeded timeout"
            else:
                if exit_code != 0:
                    status = "failed"
                    error_text = "experiment exited with code %d" % exit_code
                else:
                    try:
                        metrics = _parse_metrics(metrics_path, experiment["required_metrics"])
                        evaluator_outcome = _evaluate(experiment, metrics)
                        status = "completed"
                    except StateError as error:
                        status = "invalid_metrics"
                        error_text = str(error)
    except OSError as error:
        status = "failed"
        exit_code = 127
        error_text = "could not start experiment: %s" % error
    except BaseException:
        if process is not None and process.poll() is None:
            os.killpg(process.pid, signal.SIGTERM)
            process.wait()
        raise
    finally:
        with store.lock():
            final_state = store.load_unlocked()
            final_attempt = find_by_id(final_state["attempts"], attempt_id, "attempt")
            final_attempt.update(
                {
                    "status": status,
                    "finished_at": now_iso(),
                    "exit_code": exit_code,
                    "metrics": metrics,
                    "evaluator_outcome": evaluator_outcome,
                    "error": error_text,
                    "stdout_tail": _tail(stdout_path),
                    "stderr_tail": _tail(stderr_path),
                    "artifact_hashes": {
                        path.name: _sha256(path)
                        for path in (attempt_dir / "input.json", stdout_path, stderr_path, metrics_path)
                        if path.exists()
                    },
                    "code_revision": code_revision,
                    "working_tree_hash": working_tree_hash,
                    "code_input_hashes": code_input_hashes,
                }
            )
            final_experiment = find_by_id(final_state["experiments"], target_id, "experiment")
            final_experiment["status"] = status
            final_state["phase"] = "interpret"
            final_state["pending"] = {"kind": "result_decision", "attempt_id": attempt_id}
            store.save_unlocked(final_state)
    return attempt_id, exit_code
