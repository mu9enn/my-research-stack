# v2 Test Plan

## Scenario 1: Happy Path (Canonical v2)

- Input a domain-general direction.
- Execute canonical stages through `research-planning`.
- Confirm mandatory artifacts exist and checkpoints are writable.

## Scenario 2: Stage Alias Compatibility

- Use `idea-generation` / `novelty-check` / `proposal-ranking` in checkpoint command.
- Expect normalization to `idea-tree-search` / `claim-novelty-check` / `proposal-tournament`.

## Scenario 3: Taste-first Gatekeeping

- Force low `representative_work_potential` in taste audit.
- Confirm abstraction-lift remains required before tournament ranking.

## Scenario 4: Claim Collision Pressure

- Inject high-collision claims into `claim_graph`.
- Expect explicit `weaken`/`unsafe` status and rewrite actions.

## Scenario 5: Construct Validity Correction

- Start with weak benchmark/metric alignment.
- Confirm `construct-validity-audit` produces required plan revisions.

## Scenario 6: Optional Stages

- Skip `frontier-radar` and `run-postmortem`.
- Confirm main pipeline is still valid while status marks them optional.

## Scenario 7: Atomic Tool Regression

- Keep dedupe/normalize/similarity behavior unchanged.
- Confirm no orchestration logic moved into Python tools.

