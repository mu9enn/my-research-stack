# Codex Entrypoint

When implementing or running Full Circle tasks:

1. Load `skills/<stage>/SKILL.md` for stage logic.
2. Use `agents/*.md` for role-specific critique or drafting.
3. Invoke only atomic tools from `tools/bin/*.py` when data operations are required.
4. Persist every stage output into `runs/<run_id>/` using the protocol in `specs/artifact_protocol.md`.

Never re-encode stage orchestration in Python scripts.
