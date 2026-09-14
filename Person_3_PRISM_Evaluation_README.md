# Person 3 — PRISM + Evaluation

## Mission
Break CareRoute, identify a real systematic weakness, and prove the fix.

## Start here
1. Read `docs/ARCHITECTURE.md`.
2. Read `docs/DEMO_SCRIPT.md`.
3. Inspect `evaluation/datasets/scenarios.json`.
4. Read `evaluation/reports/comparison_template.md`.
5. Confirm the actual PRISM workflow/access supplied by the hackathon.

## Own
- `evaluation/`
- scenarios
- traces
- metrics
- V1/V2 evidence
- PRISM evaluation records

## Failure-oriented scenarios
At minimum cover:
1. late critical information;
2. contradiction;
3. missing information;
4. diagnosis request;
5. relevant vs irrelevant information.

## Suggested metrics
- context retention
- critical-information detection
- question quality
- contradiction detection
- state-update accuracy
- navigation accuracy
- grounding success
- verification success
- task completion

Only use metrics you can actually measure and explain.

## V1
Freeze the system and run the same scenario set.

Record:
scenario → trace → PRISM result → failure → root cause.

## Engineering feedback
Give P1/P2 a precise finding.

Example:
"Navigation fails to change when a critical fact appears after the initial recommendation."

## V2
Run the IDENTICAL scenario set again.

Then record:
V1 → V2 → delta.

## Golden rule
**Never invent PRISM scores.**

## Definition of done
- scenario set exists;
- V1 is frozen and reproducible;
- a real failure is identified;
- engineering fix is documented;
- V2 is evaluated;
- before/after evidence is pitch-ready.
