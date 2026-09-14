# Person 4 — Frontend + Demo

## Mission
Make the CareRoute reasoning and PRISM improvement visible in one strong demo.

## Start here
1. Read `docs/ARCHITECTURE.md`.
2. Read `docs/DEMO_SCRIPT.md`.
3. Run frontend.
4. Run backend.
5. Confirm the mock chat works.
6. Replace placeholders only after P1/P3 provide final contracts/results.

## Own
- `frontend/`
- chat interface
- patient-state visualization
- navigation display
- source/safety display
- PRISM evidence panel

## Main screen
Show:
Conversation | Live Patient State
Then:
Navigation + safety/sources
Then:
PRISM V1/V2 evidence

## Killer interaction
1. Patient says: "I'm feeling dizzy."
2. State shows dizziness.
3. Patient says: "I actually fainted earlier."
4. State-change indicator appears.
5. Navigation visibly reassesses.
6. PRISM evidence shows why V1 failed and how V2 improved.

## Important
Do not hard-code fake PRISM numbers.

Use the actual results supplied by Person 3.

## Definition of done
- chat works;
- state changes are visible;
- navigation is clear;
- safety/source status is visible;
- PRISM before/after evidence is visible;
- demo scenario is deterministic.

## Do not own
Agent logic, RAG internals, evaluation calculations.

## Priority
1. Chat
2. State visualization
3. Navigation
4. Demo flow
5. PRISM evidence
6. Visual polish
