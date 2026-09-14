# Person 3: implement measurable scoring here.

METRICS = [
    "context_retention",
    "critical_information_detection",
    "question_quality",
    "contradiction_detection",
    "state_update_accuracy",
    "navigation_accuracy",
    "grounding_success",
    "verification_success",
    "task_completion",
]


def compare(v1: dict, v2: dict) -> dict:
    # TODO: calculate actual deltas from recorded results.
    return {"v1": v1, "v2": v2, "delta": {}}
