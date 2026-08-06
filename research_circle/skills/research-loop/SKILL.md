# Research Loop

Use this single skill to operate Research Circle. The Python CLI owns state, validation, execution, recovery, and rendering; the model supplies only structured scientific reasoning.

## Procedure

1. Create or inspect a run with `./bin/fc init` and `./bin/fc status`.
2. Add located source evidence with `./bin/fc evidence add`, or use `evidence search` for discovery only.
3. Call `./bin/fc next --run-id <id>` and solve exactly the returned task using its prompt and response template.
4. Save only the JSON response and apply it with `./bin/fc apply --run-id <id> --response <file>`.
5. When the CLI requests human approval, do not infer it. The researcher must call `fc approve` for the topic/claim, large experiment, or pivot.
6. When the CLI requests execution, call `fc execute`. Never reinterpret a missing metric or failed command as a scientific result.
7. Repeat `next → apply/execute` until the next scientific decision or human authority boundary.

## Authority boundaries

- Human: direction value, approved core claim, large resources, major pivot, submission.
- Model: topic proposals, evidence synthesis, experiment proposal, result interpretation, draft material.
- Program: canonical state, response validation, evaluator, subprocess, logs, recovery, provenance, paper rendering.

There are no stage agents. Novelty, research quality (taste + abstraction), and validity critics are invoked only when `fc next` requests them.
