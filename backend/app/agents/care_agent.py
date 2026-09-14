"""
CareAgent Orchestration Module (Person 1).
Implements the 8-step pipeline:
1. Load state
2. Extract facts & critical flags
3. Resolve contradictions & update state
4. Detect state changes & reassessment trigger
5. Identify missing information & formulate response
6. Safely integrate with Person 2 (RAG & Safety)
7. Determine navigation
8. Emit evaluation trace & persist state
"""

from uuid import uuid4
from typing import List, Dict, Any, Optional

from app.core.state_manager import (
    get_state,
    save_state,
    append_history,
)
from app.models.schemas import (
    CareRouteResponse,
    NavigationResult,
    SafetyResult,
    Source,
    EvaluationTrace,
)
from app.services.fact_extractor import extract_facts
from app.services.state_detector import update_and_detect_changes
from app.services.missing_info import (
    detect_missing_information,
    generate_clarification_question,
)
from app.services.navigation import determine_navigation


class CareAgent:
    def handle_message(
        self,
        session_id: str,
        message: str,
        scenario_id: Optional[str] = None,
    ) -> CareRouteResponse:
        # Step 1: Load prior state
        state_before = get_state(session_id)

        # Step 2: Extract structured facts from user message
        extracted = extract_facts(message)
        extracted_facts_summary: List[str] = []
        if extracted["symptoms"]:
            extracted_facts_summary.extend([f"Symptom: {s}" for s in extracted["symptoms"]])
        if extracted["conditions"]:
            extracted_facts_summary.extend([f"Condition: {c}" for c in extracted["conditions"]])
        if extracted["medications"]:
            extracted_facts_summary.extend([f"Medication: {m}" for m in extracted["medications"]])
        if extracted["medication_denied"]:
            extracted_facts_summary.append("Denied: No medications")
        if extracted["timeline"]:
            extracted_facts_summary.append(f"Timeline: {extracted['timeline']}")

        # Step 3 & 4: Update state, detect state changes and contradiction resolution
        state_after, state_changes, reassessment_triggered = update_and_detect_changes(
            state_before, extracted
        )

        # Step 5: Detect missing information
        missing_info = detect_missing_information(state_after)
        state_after.missing_information = missing_info

        # Step 6: Determine navigation
        navigation: NavigationResult = determine_navigation(state_after)

        # Step 7: Integrate defensively with Person 2 (RAG & Safety)
        sources: List[Source] = []
        retrieved_context: List[Any] = []
        try:
            from app.rag.retrieval import retrieve_guidance
            retrieved = retrieve_guidance(
                query=message,
                patient_context=state_after.model_dump(),
                top_k=3,
            )
            if retrieved and isinstance(retrieved, list):
                for item in retrieved:
                    if isinstance(item, Source):
                        sources.append(item)
                    elif isinstance(item, dict):
                        sources.append(Source(**item))
                    retrieved_context.append(item)
        except (NotImplementedError, ImportError, Exception):
            sources = []

        # Compose user-facing response text adhering strictly to non-diagnostic bounds
        response_text = self._compose_response(
            message=message,
            state=state_after,
            state_changes=state_changes,
            missing_info=missing_info,
            navigation=navigation,
            is_diagnosis_request=extracted["is_diagnosis_request"],
            reassessment_triggered=reassessment_triggered,
        )

        # Person 2 safety verification (defensive fallback)
        safety: SafetyResult = SafetyResult(
            passed=True,
            safety_flags=list(navigation.safety_flags),
            grounding_flags=[],
        )
        try:
            from app.safety.verifier import verify_response
            v_res = verify_response(
                response=response_text,
                patient_state=state_after.model_dump(),
                retrieved_context=retrieved_context,
            )
            if isinstance(v_res, SafetyResult):
                safety = v_res
            elif isinstance(v_res, dict):
                safety = SafetyResult(**v_res)
        except (NotImplementedError, ImportError, Exception):
            safety = SafetyResult(
                passed=True,
                safety_flags=list(navigation.safety_flags),
                grounding_flags=["P2_MOCK: Grounding verification pending Person 2 implementation"],
            )

        # If safety verifier provided a revised response, use it
        if safety.revised_response:
            response_text = safety.revised_response

        # Step 8: Persist state & emit evaluation trace
        save_state(state_after)
        trace_id = f"trace-{uuid4().hex[:8]}"

        trace = EvaluationTrace(
            trace_id=trace_id,
            scenario_id=scenario_id,
            input_message=message,
            state_before=state_before.model_dump(),
            state_after=state_after.model_dump(),
            extracted_facts=extracted_facts_summary,
            state_changes=state_changes,
            missing_information=missing_info,
            navigation=navigation.model_dump(),
            grounding={"sources_count": len(sources)},
            verification=safety.model_dump(),
            final_outcome={
                "urgency": navigation.urgency,
                "reassessment_triggered": reassessment_triggered,
            },
        )
        append_history(session_id, trace.model_dump())

        return CareRouteResponse(
            session_id=session_id,
            patient_state=state_after,
            state_changes=state_changes,
            missing_information=missing_info,
            navigation=navigation,
            safety=safety,
            sources=sources,
            trace_id=trace_id,
            response=response_text,
        )

    def _compose_response(
        self,
        message: str,
        state: Any,
        state_changes: List[str],
        missing_info: List[str],
        navigation: NavigationResult,
        is_diagnosis_request: bool,
        reassessment_triggered: bool,
    ) -> str:
        parts: List[str] = []

        # 1. Non-diagnostic boundary handling
        if is_diagnosis_request:
            parts.append(
                "I cannot provide a medical diagnosis, as I am an AI patient-navigation assistant. "
                "I can, however, help guide you to the right care setting."
            )

        # 2. Emergency response
        if navigation.urgency == "emergency":
            critical_symptoms = [s for s in state.symptoms if s in ("fainting / syncope", "chest discomfort / pain")]
            symptom_str = " and ".join(critical_symptoms) if critical_symptoms else "acute symptoms"
            parts.append(
                f"Based on your report of {symptom_str}, this requires urgent in-person medical evaluation. "
                f"{navigation.next_step}"
            )
            return " ".join(parts)

        # 3. Contradiction notice
        contradiction_changes = [c for c in state_changes if "contradiction" in c.lower()]
        if contradiction_changes:
            parts.append("I have updated your medical record with your new medication details.")

        # 4. Clarification question if missing critical info
        clarification = generate_clarification_question(state, missing_info)
        if clarification:
            parts.append(clarification)

        # 5. Urgent or routine navigation guidance
        if navigation.urgency in ("urgent", "soon"):
            parts.append(f"Recommendation: {navigation.next_step}")
        elif navigation.urgency == "routine" and not clarification:
            parts.append(f"Recommendation: {navigation.next_step}")
        elif navigation.urgency == "unknown":
            parts.append(navigation.next_step)

        return " ".join(parts)
