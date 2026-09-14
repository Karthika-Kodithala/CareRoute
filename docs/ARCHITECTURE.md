# CareRoute Technical Architecture

```text
                         ┌────────────────────┐
                         │   React Frontend    │
                         │       Person 4      │
                         └─────────┬──────────┘
                                   │ HTTP/JSON
                                   ▼
                         ┌────────────────────┐
                         │    FastAPI API     │
                         │       Person 1     │
                         └─────────┬──────────┘
                                   │
                     ┌─────────────┼─────────────┐
                     ▼             ▼             ▼
              Patient State     Agent       Navigation
              + Change Detect   Logic        Decision
                     │             │
                     └──────┬──────┘
                            ▼
                  ┌────────────────────┐
                  │ RAG + Safety       │
                  │     Person 2       │
                  └─────────┬──────────┘
                            │
                            ▼
                  Structured Result
                            │
                            ▼
                  ┌────────────────────┐
                  │ Evaluation Trace   │
                  │     Person 3       │
                  └─────────┬──────────┘
                            │
                            ▼
                         PRISM
                            │
                            ▼
                  Failure → Root Cause
                            │
                            ▼
                    Engineering Fix
                            │
                            ▼
                         V2 → PRISM
```

## Critical architectural idea
CareRoute is stateful. A later message can change the patient's situation, so the agent must compare the old and new state and decide whether reassessment is required.

## PRISM loop
PRISM is not an afterthought. The evaluation output should feed directly into engineering decisions.
