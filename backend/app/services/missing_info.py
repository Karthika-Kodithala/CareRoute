"""
Missing information detection service for CareRoute.
Identifies clinically critical gaps in the patient's reported symptoms
to guide navigation and generate targeted clarification questions.
"""

from typing import List, Optional
from app.models.schemas import PatientState


def detect_missing_information(state: PatientState) -> List[str]:
    """
    Evaluates current symptoms and flags to detect missing clinical context.
    """
    missing: List[str] = []
    symptoms = set(state.symptoms)

    if "chest discomfort / pain" in symptoms:
        missing.append("Pain radiation (does the discomfort radiate to arm, neck, jaw, or back?)")
        missing.append("Associated autonomic symptoms (shortness of breath, sweating, nausea)")
        missing.append("Onset and context (sudden or gradual; at rest or during exertion)")

    if "dizziness" in symptoms:
        if "fainting / syncope" not in symptoms:
            missing.append("Episode severity (any loss of consciousness, blacking out, or fainting?)")
        missing.append("Onset and duration (how long have you felt dizzy?)")
        missing.append("Positional trigger (does dizziness worsen upon standing up?)")

    if "fainting / syncope" in symptoms:
        missing.append("Duration of unconsciousness and recovery time")
        missing.append("Fall-related physical trauma or head injury")
        missing.append("Warning symptoms prior to collapse (palpitations, aura, chest pain)")

    if "shortness of breath" in symptoms:
        missing.append("Severity and progression (at rest or only with exertion)")
        missing.append("Associated chest pain, fever, or leg swelling")

    return missing


def generate_clarification_question(state: PatientState, missing_info: List[str]) -> Optional[str]:
    """
    Generates a targeted, empathetic question to elicit the most critical missing fact.
    """
    if not missing_info:
        return None

    symptoms = set(state.symptoms)

    if "chest discomfort / pain" in symptoms:
        return (
            "To ensure your safety, could you share if the chest discomfort is spreading "
            "to your arm, neck, or back, and whether you are also experiencing shortness of breath or sweating?"
        )

    if "dizziness" in symptoms and "fainting / syncope" not in symptoms:
        return (
            "I hear that you are experiencing dizziness. Did you at any point lose consciousness, "
            "faint, or black out, and how long has this sensation lasted?"
        )

    if "fainting / syncope" in symptoms:
        return (
            "Because you mentioned fainting, did you hit your head or injure yourself, "
            "and did you experience chest pain or a racing heart before passing out?"
        )

    return f"Could you provide more details regarding: {missing_info[0]}?"
