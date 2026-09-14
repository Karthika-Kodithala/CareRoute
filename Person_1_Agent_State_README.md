# Person 1 — Agent + Patient State

## Mission
Build CareRoute's core stateful agent and orchestration.

## Start here
1. Read `docs/ARCHITECTURE.md`.
2. Read `docs/INTEGRATION_CONTRACT.md`.
3. Run backend.
4. Run `pytest`.
5. Test `POST /api/chat`.
6. Replace the mock logic in `app/agents/care_agent.py`.

## Own
- `backend/app/agents/`
- `backend/app/core/`
- `backend/app/models/`
- `backend/app/services/`
- `backend/app/api/`
- relevant backend tests

## First implementation
Build:
`message → fact extraction → state update → state-change detection → reassessment → navigation`

## Key requirement
Do NOT rely only on raw conversation history. Maintain an explicit structured state.

Example:
`"I'm dizzy."` → `dizziness=true`

Later:
`"I fainted this morning."` → `fainting=true`

The second message must be able to trigger reassessment.

## Output
Every request must return:
- patient_state
- state_changes
- missing_information
- navigation
- safety
- sources
- trace_id
- response

## Definition of done
- multi-turn state persists;
- late critical information is detected;
- reassessment can be triggered;
- API follows shared schema;
- tests cover late information, contradiction and missing information.

## Do not own
RAG/safety internals, PRISM evaluation, frontend.

## Priority
1. State model
2. State updates
3. Change detection
4. Reassessment
5. API
6. Tests
