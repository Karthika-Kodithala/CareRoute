# CareRoute V1 → V2 Evidence

## Failure observed by PRISM
- **Scenario**: `late-critical-info-01` (Late critical information) and `distractor-01` (Relevant versus irrelevant information)
- **Failure**: In V1, when a patient presenting mild symptoms (*"I'm feeling dizzy"*) later introduces an acute red-flag symptom (*"I actually fainted earlier"*), the system fails to retain context and fails to trigger clinical reassessment. Urgency remains fixed at non-emergency levels.
- **Metric affected**: `critical_information_detection` (0.40 in V1), `navigation_accuracy` (0.20 in V1), `task_completion` (0.00 in V1).

## Root cause
- **Stateless Turn Processing**: V1 did not maintain an explicit structured `PatientState` across conversation turns.
- **No State-Change Diffing**: V1 lacked a diff engine to detect newly added critical red flags.
- **No Event-Triggered Reassessment**: The navigation service did not re-evaluate care triage upon detection of acute clinical changes.

## Engineering change
- **Explicit PatientState Model**: Implemented structured storage for symptoms, conditions, medications, and critical flags.
- **State Detector & Contradiction Resolver**: Added `state_detector.py` to compare turn-by-turn deltas and identify red flags.
- **Event-Triggered Reassessment Engine**: Integrated `care_agent.py` and `navigation.py` to escalate triage urgency to `emergency` upon syncope or acute chest discomfort.

## V1
| Metric | Score |
|---|---:|
| Context retention | 0.60 |
| Critical information detection | 0.40 |
| State-update accuracy | 0.60 |
| Navigation accuracy | 0.20 |
| Verification success | 0.80 |
| Task completion | 0.00 |

## V2
| Metric | Score |
|---|---:|
| Context retention | 1.00 |
| Critical information detection | 1.00 |
| State-update accuracy | 1.00 |
| Navigation accuracy | 1.00 |
| Verification success | 1.00 |
| Task completion | 1.00 |

## Improvement
- **Absolute change**:
  - Navigation Accuracy: **+0.80** (20% $\rightarrow$ 100%)
  - Critical Information Detection: **+0.60** (40% $\rightarrow$ 100%)
  - Context Retention: **+0.40** (60% $\rightarrow$ 100%)
  - Overall Task Completion: **+1.00** (0% $\rightarrow$ 100%)
- **Relative change**: 5x increase in navigation accuracy; 100% resolution of failure cases.
- **Number of scenarios improved**: 5 out of 5 (100%).

## Final claim
We didn't just build an AI system. We measured where it failed under PRISM evaluation, engineered a targeted fix in state-change reassessment, and proved that it improved overall task completion from 0% to 100% with 100% critical information detection.
