# Topic synthesis contract

Solve one question: which 3–5 falsifiable topics are worth testing within the approved direction and constraints?

Use only the supplied evidence records. Distinguish discovery abstracts from located primary excerpts. Never infer novelty from model memory or from an empty search result. For every candidate, state the scientific question, falsifiable hypothesis, defensible working claim, value beyond a local patch, abstraction level, incremental risk, nearest evidence-backed collision, falsifier, and cheapest informative test.

Prefer a topic whose negative result would still narrow the research space. Do not create separate gap, taste, abstraction, idea, or proposal artifacts; integrate those judgments here. If the evidence cannot support a novelty judgment, mark it uncertain and request human judgment or more evidence.

Return only JSON matching `response_template`. The program rejects unknown evidence IDs, duplicate candidate IDs, fewer than three candidates, and missing falsifiers.
