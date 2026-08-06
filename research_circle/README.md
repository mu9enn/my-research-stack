# Research Circle

Research Circle is a small, evidence-driven research loop for PhD work. It keeps one canonical research state and separates responsibilities clearly:

- the researcher approves the direction, core claim, major pivots, large resource use, and submission;
- the model proposes topics and experiments, interprets evidence, and drafts scoped material;
- the program validates transitions, executes experiments, records immutable results, recovers interrupted runs, and renders the working paper record.

The loop is:

`evidence → candidate topics → human-approved claim → executable experiment → fixed evaluator → result decision → paper update → next experiment`

There are no permanent stage agents. Novelty, research quality (taste + abstraction), and validity critics are invoked only when risk requires them.

## Quick start

```bash
./bin/fc init \
  --run-id my-study \
  --direction "A falsifiable research direction" \
  --project /absolute/path/to/experiment-repo

./bin/fc evidence add \
  --run-id my-study \
  --file /absolute/path/to/source-excerpt.txt \
  --title "Primary source" \
  --locator "page 4, section 2"

./bin/fc next --run-id my-study
```

`fc next` returns one prompt packet and JSON response template. Apply the completed response, follow any human approval request, and execute only when the state asks for it:

```bash
./bin/fc apply --run-id my-study --response /path/to/response.json
./bin/fc approve --run-id my-study --topic-id topic-1
./bin/fc execute --run-id my-study
./bin/fc status --run-id my-study
```

Every run lives in `runs/<run_id>/`:

- `state.json`: the only authority for topic, claim, experiment, result, and decision state;
- `state.prev.json`: last valid recovery snapshot;
- `attempts/<attempt_id>/`: immutable input, stdout, stderr, and metrics;
- `paper.md`: generated research/paper material with evidence and attempt provenance.

## Evidence semantics

`fc evidence search` queries arXiv, OpenAlex, and Semantic Scholar concurrently. A partial response is retained with explicit coverage errors rather than discarded. Search abstracts are discovery evidence and trigger novelty review; use `evidence add` with a located source excerpt for claim-level support.

## Testing

```bash
pytest -q
```

The suite runs a real subprocess-backed toy experiment, positive and negative decision paths, execution failures, timeout, invalid metrics, critic routing, atomic state recovery, and interrupted-attempt retry.
