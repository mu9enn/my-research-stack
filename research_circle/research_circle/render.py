from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List


def _refs(values: List[str]) -> str:
    return ", ".join("`%s`" % value for value in values) if values else "none"


def render_paper(state: Dict[str, Any], destination: Path) -> None:
    lines = [
        "# Working Research Record",
        "",
        "> Generated from `state.json`. Edit the canonical state through `fc`; do not treat this file as authority.",
        "",
        "## Direction",
        "",
        state["direction"],
        "",
    ]

    selected = None
    for topic in state["topics"]:
        if topic["id"] == state.get("selected_topic_id"):
            selected = topic
            break
    if selected:
        lines.extend(
            [
                "## Approved Topic",
                "",
                "**%s**" % selected["title"],
                "",
                selected["question"],
                "",
                "Topic evidence: %s" % _refs(selected["novelty"]["evidence_ids"]),
                "",
            ]
        )

    if state["claims"]:
        lines.extend(["## Human-Approved Claims", ""])
        for claim in state["claims"]:
            lines.append("- `%s` — %s" % (claim["id"], claim["text"]))
            for assessment in claim.get("assessments", []):
                lines.append(
                    "  - `%s` from `%s`: %s"
                    % (assessment["assessment"], assessment["attempt_id"], assessment["reason"])
                )
        lines.append("")

    if state["evidence"]:
        lines.extend(["## Evidence Inventory", ""])
        for evidence in state["evidence"]:
            locator = evidence.get("locator") or "unlocated"
            lines.append(
                "- `%s` — %s (%s; %s; sha256 `%s`)"
                % (evidence["id"], evidence["title"], evidence["level"], locator, evidence["content_hash"][:12])
            )
        lines.append("")

    if state["attempts"]:
        lines.extend(["## Experiment Ledger", ""])
        for attempt in state["attempts"]:
            lines.append("### %s" % attempt["id"])
            lines.append("")
            lines.append("- Experiment: `%s`" % attempt["experiment_id"])
            lines.append("- Execution status: `%s`" % attempt["status"])
            if attempt.get("code_revision"):
                lines.append(
                    "- Code provenance: revision `%s`; working tree `%s`"
                    % (attempt["code_revision"][:12], attempt["working_tree_hash"][:12])
                )
            if attempt.get("code_input_hashes"):
                code_hashes = [
                    "%s=%s" % (name, value[:12])
                    for name, value in sorted(attempt["code_input_hashes"].items())
                ]
                lines.append("- Declared code hashes: %s" % ", ".join(code_hashes))
            if attempt.get("evaluator_outcome"):
                lines.append("- Fixed evaluator: `%s`" % attempt["evaluator_outcome"])
            if attempt.get("metrics"):
                pairs = ["%s=%s" % (key, value) for key, value in sorted(attempt["metrics"].items())]
                lines.append("- Metrics: %s" % ", ".join(pairs))
            if attempt["status"] not in {"completed"}:
                lines.append("- Interpretation guard: execution failure is not scientific evidence.")
            if attempt.get("artifact_hashes"):
                hashes = ["%s=%s" % (name, value[:12]) for name, value in sorted(attempt["artifact_hashes"].items())]
                lines.append("- Artifact hashes: %s" % ", ".join(hashes))
            lines.append("- Raw provenance: `%s`" % attempt["output_dir"])
            lines.append("")

    if state["paper_notes"]:
        lines.extend(["## Evidence-Backed Draft Material", ""])
        for note in state["paper_notes"]:
            lines.append("### %s" % note["section"].replace("_", " ").title())
            lines.append("")
            lines.append(note["text"])
            lines.append("")
            lines.append(
                "Provenance: attempt `%s`; evidence %s; claims %s."
                % (note["attempt_id"], _refs(note["evidence_ids"]), _refs(note["claim_ids"]))
            )
            lines.append("")

    destination.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
