# MVP Test Plan

## Scenario 1: Happy Path

- Input topic in NLP/LLM/Agent.
- Retrieve 30-60 papers from 3 sources.
- Produce 5-8 ideas and 1-3 deep proposals.

## Scenario 2: Novelty Collision

- Inject a high-similarity known paper.
- Expect downgrade/red flag and alternative direction suggestions.

## Scenario 3: Human Loop

- Edit outputs at `gap-mining`, `idea-generation`, `proposal-ranking`.
- Confirm pipeline can continue using updated artifacts.

## Scenario 4: Source Degradation

- Force one source failure.
- Confirm other sources continue and error is recorded.

## Scenario 5: Acceptance Focus

- Evaluate proposal executability and venue positioning clarity.

