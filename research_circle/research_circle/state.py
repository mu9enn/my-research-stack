from __future__ import annotations

import contextlib
import copy
import fcntl
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterator


SCHEMA_VERSION = 1
PHASES = {"topic", "experiment", "interpret", "human"}


class StateError(RuntimeError):
    pass


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def initial_state(
    run_id: str,
    direction: str,
    project_dir: Path,
    constraints: list,
    max_timeout_seconds: int,
) -> Dict[str, Any]:
    timestamp = now_iso()
    return {
        "schema_version": SCHEMA_VERSION,
        "run_id": run_id,
        "direction": direction,
        "project_dir": str(project_dir.resolve()),
        "constraints": constraints,
        "limits": {"max_timeout_seconds": max_timeout_seconds},
        "phase": "topic",
        "pending": {"kind": "topic_synthesis"},
        "human_reason": None,
        "created_at": timestamp,
        "updated_at": timestamp,
        "revision": 0,
        "applied_response_ids": [],
        "evidence": [],
        "discovery_runs": [],
        "topics": [],
        "selected_topic_id": None,
        "claims": [],
        "critics": [],
        "experiments": [],
        "attempts": [],
        "decisions": [],
        "paper_notes": [],
    }


def validate_state(state: Dict[str, Any]) -> None:
    required = {
        "schema_version",
        "run_id",
        "direction",
        "project_dir",
        "phase",
        "revision",
        "evidence",
        "topics",
        "claims",
        "experiments",
        "attempts",
        "decisions",
    }
    missing = sorted(required - set(state))
    if missing:
        raise StateError("state missing fields: " + ", ".join(missing))
    if state["schema_version"] != SCHEMA_VERSION:
        raise StateError("unsupported state schema version")
    if state["phase"] not in PHASES:
        raise StateError("invalid phase: %s" % state["phase"])
    if not isinstance(state["revision"], int) or state["revision"] < 0:
        raise StateError("revision must be a non-negative integer")
    for field in (
        "evidence",
        "topics",
        "claims",
        "experiments",
        "attempts",
        "decisions",
    ):
        if not isinstance(state[field], list):
            raise StateError("%s must be a list" % field)


class StateStore:
    def __init__(self, run_dir: Path):
        self.run_dir = run_dir.resolve()
        self.state_path = self.run_dir / "state.json"
        self.previous_path = self.run_dir / "state.prev.json"
        self.lock_path = self.run_dir / ".state.lock"

    @contextlib.contextmanager
    def lock(self) -> Iterator[None]:
        self.run_dir.mkdir(parents=True, exist_ok=True)
        with self.lock_path.open("a+", encoding="utf-8") as lock_file:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)

    def load_unlocked(self, recover: bool = False) -> Dict[str, Any]:
        try:
            state = json.loads(self.state_path.read_text(encoding="utf-8"))
            validate_state(state)
            return state
        except (OSError, ValueError, StateError) as error:
            if not recover:
                raise StateError("cannot load state: %s" % error) from error
            try:
                state = json.loads(self.previous_path.read_text(encoding="utf-8"))
                validate_state(state)
                return state
            except (OSError, ValueError, StateError) as previous_error:
                raise StateError(
                    "state and backup are unreadable: %s; %s" % (error, previous_error)
                ) from previous_error

    def save_unlocked(self, state: Dict[str, Any]) -> None:
        candidate = copy.deepcopy(state)
        candidate["revision"] = int(candidate.get("revision", 0)) + 1
        candidate["updated_at"] = now_iso()
        validate_state(candidate)
        payload = json.dumps(candidate, ensure_ascii=False, indent=2, sort_keys=True) + "\n"

        if self.state_path.exists():
            previous = self.state_path.read_bytes()
            self._atomic_bytes(self.previous_path, previous)
        self._atomic_bytes(self.state_path, payload.encode("utf-8"))
        state.clear()
        state.update(candidate)

    def restore_unlocked(self, state: Dict[str, Any]) -> None:
        """Restore a validated backup without rotating a corrupt current file over it."""
        candidate = copy.deepcopy(state)
        candidate["revision"] = int(candidate.get("revision", 0)) + 1
        candidate["updated_at"] = now_iso()
        validate_state(candidate)
        payload = json.dumps(candidate, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        self._atomic_bytes(self.state_path, payload.encode("utf-8"))
        state.clear()
        state.update(candidate)

    def create(self, state: Dict[str, Any]) -> None:
        with self.lock():
            if self.state_path.exists():
                raise StateError("run already exists: %s" % self.run_dir.name)
            self.save_unlocked(state)
            self._atomic_bytes(self.previous_path, self.state_path.read_bytes())

    def _atomic_bytes(self, destination: Path, payload: bytes) -> None:
        fd, tmp_name = tempfile.mkstemp(prefix=".%s." % destination.name, dir=str(self.run_dir))
        try:
            with os.fdopen(fd, "wb") as handle:
                handle.write(payload)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(tmp_name, destination)
            directory_fd = os.open(str(self.run_dir), os.O_RDONLY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
        finally:
            if os.path.exists(tmp_name):
                os.unlink(tmp_name)


def find_by_id(items: list, item_id: str, kind: str) -> Dict[str, Any]:
    for item in items:
        if item.get("id") == item_id:
            return item
    raise StateError("unknown %s id: %s" % (kind, item_id))


def next_id(prefix: str, items: list) -> str:
    return "%s-%04d" % (prefix, len(items) + 1)
