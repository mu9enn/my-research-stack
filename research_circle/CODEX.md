# Codex Entrypoint

When implementing or running Research Circle v2 tasks:

1. Load `skills/<stage>/SKILL.md` for canonical stage logic.
2. Use `agents/*.md` for role-specific critique and drafting.
3. Invoke only atomic tools from `tools/bin/*.py` when deterministic data operations are required.
4. Persist every stage output into `runs/<run_id>/` using `specs/artifact_protocol.md`.
5. Prefer canonical v2 stages; legacy stage names are compatibility aliases only.

Never re-encode workflow orchestration in Python scripts.

