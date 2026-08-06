# Experiment design contract

Solve one question: what is the smallest executable experiment that can materially update belief in the approved claim?

Use the approved topic, human-approved claim, prior attempts, repository location, constraints, and fixed resource limit. Declare every code file required by the experiment so the program can hash it. Define the command as an argv array, never shell syntax. The command may write results only through `{output_dir}` and must emit the declared metrics JSON.

Fix the primary metric, direction, baseline, and minimum meaningful delta before execution. Explain metric–claim alignment, baseline adequacy, confounds, and what a negative result would teach. For stochastic experiments, require meaningful replication; do not substitute “runs successfully” for construct validity.

Stop for human judgment when the experiment requires large resources, changes the research direction, or cannot distinguish the focal claim from obvious confounds. Return only JSON matching `response_template`; the program validates paths, timeout, claims, metrics, and evaluator fields before any process starts.
