# Person 1 owns the orchestration logic.
# This is deliberately a mock so the frontend can be integrated immediately.

from uuid import uuid4

from app.core.state_manager import get_state
from app.models.schemas import (
    CareRouteResponse,
    NavigationResult,
    SafetyResult,
)


class CareAgent:
    def handle_message(self, session_id: str, message: str) -> CareRouteResponse:
        state = get_state(session_id)

        # TODO Person 1:
        # 1. Extract facts from message.
        # 2. Compare with previous state.
        # 3. Update persistent state.
        # 4. Detect important state changes.
        # 5. Decide whether clarification/reassessment is needed.
        # 6. Call RAG/safety modules.
        # 7. Produce final navigation.
        # 8. Emit a complete evaluation trace.

        trace_id = f"trace-{uuid4().hex[:8]}"

        navigation = NavigationResult(
            urgency="needs-review",
            next_step="Replace this mock response with CareRoute navigation.",
            reasoning_summary="Starter response only.",
        )

        safety = SafetyResult(
            passed=True,
            safety_flags=[],
            grounding_flags=["MOCK: grounding not implemented"],
        )

        return CareRouteResponse(
            session_id=session_id,
            patient_state=state,
            state_changes=[],
            missing_information=[],
            navigation=navigation,
            safety=safety,
            sources=[],
            trace_id=trace_id,
            response="CareRoute starter response. Implement the agent workflow.",
        )
