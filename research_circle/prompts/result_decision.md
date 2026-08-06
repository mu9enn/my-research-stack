# Result decision contract

Solve one question: given the immutable attempt record and the evaluator fixed before execution, should the project continue, revise, abandon, ask the researcher, or propose a major pivot?

First distinguish execution failure from a scientific negative result. Read raw status, logs, metrics, evaluator outcome, approved claims, and cited evidence. A single successful metric may support only the scoped working claim; it cannot silently strengthen or rewrite the human-approved claim. A failed command is diagnostic engineering information, not evidence against the hypothesis.

Choose exactly one action, explain the information gained, assess every affected claim, and produce one modest paper/research note with explicit provenance. Stop for human authority on major pivots or claim changes.

Return only JSON matching `response_template`. The program rejects unknown attempt, evidence, or claim IDs and does not accept an automatic rewrite of approved claim text.
