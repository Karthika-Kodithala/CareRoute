"""
State update and change detection service for CareRoute.
Compares previous patient state with newly extracted facts,
resolves contradictions, detects critical state transitions,
and determines if reassessment is required.
"""

from datetime import datetime, timezone
from typing import Dict, List, Tuple, Any
from app.models.schemas import PatientState
from app.models.patient_state import clone_state


def update_and_detect_changes(
    current_state: PatientState,
    extracted_facts: Dict[str, Any],
) -> Tuple[PatientState, List[str], bool]:
    """
    Updates the PatientState with newly extracted facts, computes the diff
    (state_changes), and flags whether clinical reassessment is required.

    Returns:
        (updated_state, state_changes, reassessment_triggered)
    """
    new_state = clone_state(current_state)
    state_changes: List[str] = []
    reassessment_triggered = False

    # 1. Process Symptoms
    for sym in extracted_facts.get("symptoms", []):
        if sym not in new_state.symptoms:
            new_state.symptoms.append(sym)
            state_changes.append(f"Added symptom: {sym}")
            new_state.confidence[sym] = 0.95

    # 2. Process Conditions
    for cond in extracted_facts.get("conditions", []):
        if cond not in new_state.conditions:
            new_state.conditions.append(cond)
            state_changes.append(f"Added medical condition: {cond}")
            new_state.confidence[cond] = 0.90

    # 3. Process Medications & Contradictions
    medication_denied = extracted_facts.get("medication_denied", False)
    new_meds = extracted_facts.get("medications", [])

    if medication_denied:
        if new_state.medications:
            # Patient previously had medications listed, but now denies them
            old_meds_str = ", ".join(new_state.medications)
            state_changes.append(
                f"Contradiction detected: Patient reported no medications, overriding prior medications ({old_meds_str})"
            )
            new_state.medications = []
            reassessment_triggered = True
        else:
            if "no_medications" not in new_state.conditions:
                state_changes.append("Recorded: Patient confirmed taking no medications")
                new_state.confidence["medications_status"] = 0.90
    elif new_meds:
        for med in new_meds:
            if med not in new_state.medications:
                # Check if there was an explicit record or expectation of no medications
                if "no_medications" in new_state.conditions or (
                    new_state.confidence.get("medications_status") == 0.90
                    and not new_state.medications
                ):
                    state_changes.append(
                        f"Contradiction resolved: Patient previously reported no medications, now reports {med}"
                    )
                    reassessment_triggered = True
                else:
                    state_changes.append(f"Added medication: {med}")
                new_state.medications.append(med)
                new_state.confidence[med] = 0.95

    # 4. Process Critical Flags
    new_critical_flags = extracted_facts.get("critical_flags", [])
    for flag in new_critical_flags:
        if flag not in new_state.critical_flags:
            new_state.critical_flags.append(flag)
            state_changes.append(f"Critical flag detected: {flag}")
            # Any new critical flag immediately triggers reassessment!
            reassessment_triggered = True

    # Check if a late-appearing symptom triggers reassessment (e.g. fainting when already dizzy)
    if "fainting / syncope" in new_state.symptoms and "dizziness" in new_state.symptoms:
        # If fainting was just added in this turn
        if any("fainting" in sc.lower() for sc in state_changes):
            reassessment_triggered = True

    new_state.last_updated = datetime.now(timezone.utc).isoformat()

    return new_state, state_changes, reassessment_triggered
