# Person 2 — RAG + Safety

## Mission
Make CareRoute grounded, traceable and constrained.

## Start here
1. Read `docs/ARCHITECTURE.md`.
2. Read `docs/INTEGRATION_CONTRACT.md`.
3. Inspect `backend/app/rag/retrieval.py`.
4. Inspect `backend/app/safety/verifier.py`.
5. Create a small curated knowledge base.

## Own
- `backend/app/rag/`
- `backend/app/safety/`
- knowledge corpus
- grounding/safety tests

## Overnight scope
Do NOT build a huge medical search engine.

Use a small curated corpus that is sufficient for the demo scenarios and supports traceable sources.

## Interfaces
Retrieval:
`retrieve_guidance(query, patient_context, top_k=3)`

Verification:
`verify_response(response, patient_state, retrieved_context)`

## Verify against
- unsupported claims;
- diagnostic language;
- unsafe certainty;
- unsupported medication/prescription instructions;
- failure to respect configured escalation/navigation rules.

## Definition of done
- retrieval returns source metadata;
- verifier can catch an intentionally unsupported response;
- interfaces match shared schemas;
- tests exist.

## Do not own
Core agent/state, PRISM evaluation, frontend.

## Priority
1. Corpus
2. Retrieval
3. Source traceability
4. Verification
5. Tests
