# Codex entrypoint

Use `skills/research-loop/SKILL.md` as the only workflow instruction.

Always ask `./bin/fc next --run-id <id>` for the current task. Return JSON matching its template and commit it through `fc apply`; do not edit `state.json` or `paper.md` directly. Run experiments only when `pending.kind` is `execute`. Never infer human approval.
