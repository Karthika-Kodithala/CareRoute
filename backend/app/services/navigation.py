"""
Navigation decision service for CareRoute (Person 1).
Determines next-step clinical navigation based on structured patient state.
Strictly non-diagnostic: focuses solely on care settings and triage urgency.
"""

from typing import Optional, Any
from app.models.schemas import PatientState, NavigationResult


def determine_navigation(
    patient_state: PatientState,
    grounded_context: Optional[Any] = None,
) -> NavigationResult:
    """
    Evaluates the patient state and determines the appropriate care navigation level.
    Urgency values must adhere to: 'routine' | 'soon' | 'urgent' | 'emergency' | 'unknown'.
    """
    symptoms = set(patient_state.symptoms)
    critical_flags = set(patient_state.critical_flags)

    # 1. Emergency Tier (Red Flags)
    if "fainting / syncope" in symptoms or "fainting / syncope" in critical_flags:
        return NavigationResult(
            urgency="emergency",
            next_step="Seek emergency medical evaluation immediately. Call 911 or proceed to the nearest emergency department.",
            reasoning_summary=(
                "A reported fainting episode (syncope), particularly when accompanied by dizziness, "
                "represents a critical event requiring immediate medical assessment to rule out "
                "cardiac, neurological, or hemodynamic instability."
            ),
            safety_flags=[
                "CRITICAL_RED_FLAG: Syncope/fainting detected",
                "NON_DIAGNOSTIC: Care setting navigation only",
            ],
        )

    if "chest discomfort / pain" in symptoms or "chest discomfort / pain" in critical_flags:
        return NavigationResult(
            urgency="emergency",
            next_step="Seek emergency medical care immediately. Call 911 or go to the nearest emergency room.",
            reasoning_summary=(
                "Chest discomfort or pain is a red-flag symptom that warrants urgent ruling out "
                "of acute coronary syndromes or life-threatening cardiopulmonary events."
            ),
            safety_flags=[
                "CRITICAL_RED_FLAG: Chest discomfort detected",
                "NON_DIAGNOSTIC: Care setting navigation only",
            ],
        )

    if "shortness of breath" in symptoms or "shortness of breath" in critical_flags:
        return NavigationResult(
            urgency="urgent",
            next_step="Seek urgent medical evaluation at an urgent care clinic or emergency room if breathing worsens.",
            reasoning_summary=(
                "Shortness of breath requires prompt clinical evaluation to examine pulmonary and cardiovascular function."
            ),
            safety_flags=["NON_DIAGNOSTIC: Care setting navigation only"],
        )

    # 2. Urgent Tier
    if "dizziness" in symptoms:
        return NavigationResult(
            urgency="urgent",
            next_step="Visit an urgent care clinic or arrange a same-day medical evaluation.",
            reasoning_summary=(
                "Acute dizziness without fainting warrants timely evaluation to assess blood pressure, "
                "hydration, inner ear function, or medication effects."
            ),
            safety_flags=["NON_DIAGNOSTIC: Care setting navigation only"],
        )

    if "palpitations" in symptoms:
        return NavigationResult(
            urgency="urgent",
            next_step="Contact your healthcare provider today or visit an urgent care center for an ECG evaluation.",
            reasoning_summary=(
                "Unexplained heart palpitations should be evaluated with an electrocardiogram (ECG) "
                "to evaluate heart rhythm."
            ),
            safety_flags=["NON_DIAGNOSTIC: Care setting navigation only"],
        )

    # 3. Soon / Routine Tier
    if symptoms or patient_state.conditions or patient_state.medications:
        return NavigationResult(
            urgency="routine",
            next_step="Schedule an appointment with your primary care provider.",
            reasoning_summary=(
                "Reported medical details do not indicate an acute emergency. Routine follow-up "
                "with a primary physician is recommended."
            ),
            safety_flags=["NON_DIAGNOSTIC: Care setting navigation only"],
        )

    # 4. Unknown Tier
    return NavigationResult(
        urgency="unknown",
        next_step="Please describe your current symptoms or health concerns.",
        reasoning_summary="No clinical symptoms or conditions have been provided yet.",
        safety_flags=["NON_DIAGNOSTIC: Care setting navigation only"],
    )
