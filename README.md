# CareRoute — ForgeAI Hackathon Starter Repo

## Mission
CareRoute is an AI patient-navigation agent. It maintains an evolving patient state, detects missing or changed information, asks targeted questions, reassesses the situation, retrieves grounded guidance, verifies safety, and produces a structured next-step recommendation.

**It does not diagnose.**

## ForgeAI loop
BUILD V1 → OBSERVE WITH PRISM → IDENTIFY FAILURE → ENGINEER FIX → BUILD V2 → PROVE IMPROVEMENT

## Team ownership

### Person 1 — Agent + Patient State
Owns:
- FastAPI orchestration
- Patient-state model/persistence
- Fact extraction
- Missing-information detection
- State-change detection
- Reassessment
- Navigation orchestration

### Person 2 — RAG + Safety
Owns:
- Curated knowledge base
- Retrieval
- Source traceability
- Grounding checks
- Safety verification
- Unsupported-claim detection

### Person 3 — PRISM + Evaluation
Owns:
- Failure-oriented scenarios
- Evaluation traces
- Metrics
- V1 baseline
- Root-cause analysis
- V2 comparison
- PRISM evidence

### Person 4 — Frontend + Demo
Owns:
- React UI
- Chat
- Live patient-state visualization
- Navigation result
- Safety/source display
- PRISM evidence panel

## Integration rule
All four people integrate through `shared/schemas/`. Do not silently change API contracts. If a contract must change, update the shared schema first and tell the team.

## Recommended branches
- `person1-agent-state`
- `person2-rag-safety`
- `person3-prism-eval`
- `person4-frontend`

## MVP
A fragmented multi-turn patient scenario must:
1. persist structured state;
2. detect new/changed critical information;
3. trigger reassessment;
4. retrieve grounded guidance;
5. perform safety verification;
6. return navigation;
7. emit an evaluation trace;
8. be replayable for V1/V2 comparison.

## Safety boundary
This is a navigation prototype, not a diagnostic or treatment system. Do not claim to diagnose, prescribe, or replace clinicians.

## Quick start

### Backend
```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

The frontend expects the backend at `http://localhost:8000` unless `VITE_API_BASE_URL` is changed.

## Important
The starter contains interfaces, mocks, schemas and placeholders—not the finished CareRoute intelligence. Implement the four ownership areas independently, then integrate.
