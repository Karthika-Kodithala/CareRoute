import re
from typing import Any, Dict, List, Optional, Union
from app.models.schemas import PatientState, SafetyResult, Source


# Diagnostic language patterns that violate non-diagnostic boundary
DIAGNOSTIC_PATTERNS = [
    r"\byou have (a|an|the)?\s*(heart attack|myocardial infarction|stroke|diabetes|hypoglycemia|asthma|gerd|arrhythmia|concussion|cardiac condition|heart problem|pneumonia|kidney failure|infection|tIA)\b",
    r"\byou are suffering from\b",
    r"\bi diagnose you with\b",
    r"\bmy diagnosis is\b",
    r"\bthis is definitely (a|an)?\s*(heart|stroke|cardiac|diabetic|hypoglycemic|asthmatic|serious|fatal|benign|emergency)\b",
    r"\byou do not have (a|an)?\s*(heart attack|heart problem|stroke|serious condition)\b",
    r"\bthis confirms (that )?you have\b",
]

# Unsafe certainty patterns offering false reassurance or discouraging evaluation
UNSAFE_CERTAINTY_PATTERNS = [
    r"\byou are (100%|completely|totally|entirely) (fine|safe|healthy|okay|ok)\b",
    r"\b(there is )?nothing to worry about\b",
    r"\b(there is )?no need to (see a doctor|go to the hospital|seek medical attention|call an ambulance|visit urgent care)\b",
    r"\byou definitely do not need (a doctor|medical care|emergency services|to be evaluated)\b",
    r"\bguaranteed to be (harmless|safe|fine)\b",
    r"\bdon\'?t worry,? it is just\b",
    r"\b100% safe\b",
]

# Unauthorized medication prescribing and dosage instructions
UNSUPPORTED_MEDICATION_PATTERNS = [
    r"\b\d+\s*(mg|g|mcg|ml|tablets?|pills?|capsules?|units?|drops?)\b",
    r"\b(take|start taking|stop taking|discontinue|increase your dose of|decrease your dose of|double your dose of)\s+([a-z0-9\-_]+)?\s*(insulin|metformin|antibiotics?|aspirin|amoxicillin|lisinopril|medication|pills?|prescription)\b",
    r"\bi prescribe\b",
    r"\bi recommend taking\s+\d+\b",
    r"\btake\s+(amoxicillin|ibuprofen|aspirin|tylenol|paracetamol|metformin|insulin|antibiotics)\b",
]

# Unsafe delay patterns when red flags are present
UNSAFE_DELAY_PATTERNS = [
    r"\b(just )?wait a few (days|weeks)\b",
    r"\bwait a week\b",
    r"\bjust sleep it off\b",
    r"\bignore (it|the symptoms?)\b",
    r"\bno rush\b",
    r"\bwait and see before doing anything\b",
]

# Positive escalation indicator keywords
ESCALATION_KEYWORDS = [
    "emergency",
    "urgent",
    "911",
    "emergency department",
    "emergency room",
    "er",
    "ems",
    "immediate medical evaluation",
    "seek immediate",
    "seek medical attention",
    "contact emergency services",
    "urgent care",
    "healthcare provider",
    "doctor",
    "physician",
    "clinical evaluation",
]

RED_FLAG_TERMS = [
    "fainted",
    "fainting",
    "syncope",
    "passed out",
    "loss of consciousness",
    "chest discomfort",
    "chest pain",
    "chest pressure",
    "shortness of breath",
    "difficulty breathing",
    "thunderclap",
    "facial droop",
    "slurred speech",
    "cyanosis",
    "unilateral weakness",
]


def _extract_patient_terms(patient_state: Union[Dict[str, Any], PatientState, None]) -> Dict[str, List[str]]:
    if patient_state is None:
        return {"symptoms": [], "conditions": [], "medications": [], "critical_flags": []}

    if isinstance(patient_state, PatientState):
        state_dict = patient_state.model_dump() if hasattr(patient_state, "model_dump") else patient_state.dict()
    elif isinstance(patient_state, dict):
        state_dict = patient_state
    else:
        state_dict = {}

    return {
        "symptoms": [str(s).lower() for s in state_dict.get("symptoms", [])],
        "conditions": [str(c).lower() for c in state_dict.get("conditions", [])],
        "medications": [str(m).lower() for m in state_dict.get("medications", [])],
        "critical_flags": [str(f).lower() for f in state_dict.get("critical_flags", [])],
    }


def _extract_context_text(retrieved_context: Union[List[Union[Source, Dict[str, Any], str]], None]) -> str:
    """Consolidate retrieved sources into a single normalized text string for grounding checks."""
    if not retrieved_context:
        return ""

    chunks: List[str] = []
    for item in retrieved_context:
        if isinstance(item, Source):
            chunks.append(f"{item.title} {item.section} {item.snippet}")
        elif isinstance(item, dict):
            chunks.append(
                f"{item.get('title', '')} {item.get('section', '')} {item.get('snippet', '')} {item.get('content', '')}"
            )
        elif isinstance(item, str):
            chunks.append(item)
    return " ".join(chunks).lower()


def generate_revised_response(
    original_response: str,
    safety_flags: List[str],
    patient_terms: Dict[str, List[str]],
) -> str:
    """Generate a safe, guideline-compliant revised response when safety checks fail."""
    has_red_flags = bool(
        patient_terms["critical_flags"]
        or any(rf in " ".join(patient_terms["symptoms"]) for rf in RED_FLAG_TERMS)
    )

    if "ESCALATION_RULE_VIOLATION" in safety_flags or has_red_flags:
        return (
            "Based on the symptoms reported (such as fainting or acute discomfort), "
            "this requires immediate clinical attention. Please call emergency services (911) "
            "or proceed to the nearest Emergency Department for immediate medical evaluation."
        )

    if "DIAGNOSTIC_LANGUAGE_DETECTED" in safety_flags:
        return (
            "CareRoute cannot provide a medical diagnosis. Based on your reported symptoms, "
            "we recommend consulting a qualified healthcare provider or visiting urgent care "
            "for a comprehensive clinical evaluation."
        )

    if "UNSUPPORTED_MEDICATION_INSTRUCTION" in safety_flags:
        return (
            "CareRoute cannot prescribe or adjust medication dosages. Please contact your prescribing "
            "doctor or pharmacist regarding your medication regimen, and seek urgent care if you experience "
            "severe symptoms."
        )

    return (
        "Based on your symptoms, please consult a healthcare professional for clinical evaluation. "
        "Seek immediate emergency care if you experience worsening symptoms, chest pain, fainting, or shortness of breath."
    )


def verify_response(
    response: str,
    patient_state: Union[Dict[str, Any], PatientState, None] = None,
    retrieved_context: Optional[List[Any]] = None,
) -> SafetyResult:
    """Verify an agent response against safety constraints, non-diagnostic boundaries, and grounding.

    Args:
        response: The generated textual response to verify.
        patient_state: Current patient state containing symptoms, medications, critical flags.
        retrieved_context: List of retrieved Source objects or guideline dicts.

    Returns:
        SafetyResult with passed status, safety_flags, grounding_flags, and optional revised_response.
    """
    safety_flags: List[str] = []
    grounding_flags: List[str] = []

    text = (response or "").strip()
    text_lower = text.lower()
    patient_terms = _extract_patient_terms(patient_state)
    context_text = _extract_context_text(retrieved_context)

    # 1. Check for Diagnostic Language
    for pattern in DIAGNOSTIC_PATTERNS:
        if re.search(pattern, text_lower, re.IGNORECASE):
            safety_flags.append("DIAGNOSTIC_LANGUAGE_DETECTED")
            break

    # 2. Check for Unsafe Certainty & False Reassurance
    for pattern in UNSAFE_CERTAINTY_PATTERNS:
        if re.search(pattern, text_lower, re.IGNORECASE):
            safety_flags.append("UNSAFE_CERTAINTY_DETECTED")
            break

    # 3. Check for Unsupported Medication / Prescription Instructions
    for pattern in UNSUPPORTED_MEDICATION_PATTERNS:
        if re.search(pattern, text_lower, re.IGNORECASE):
            safety_flags.append("UNSUPPORTED_MEDICATION_INSTRUCTION")
            break

    # 4. Check Escalation Rules for Red Flags
    # Check if patient state contains critical flags or red flag symptoms
    has_critical_flag = bool(patient_terms["critical_flags"])
    has_red_flag_symptom = any(
        any(rf in sym for rf in RED_FLAG_TERMS) for sym in patient_terms["symptoms"]
    )
    is_emergency_scenario = has_critical_flag or has_red_flag_symptom

    if is_emergency_scenario:
        # Must contain escalation guidance
        has_escalation = any(kwd in text_lower for kwd in ESCALATION_KEYWORDS)
        # Must NOT contain unsafe delay advice
        has_unsafe_delay = any(re.search(p, text_lower) for p in UNSAFE_DELAY_PATTERNS)

        if not has_escalation or has_unsafe_delay:
            safety_flags.append("ESCALATION_RULE_VIOLATION")

    # 5. Check Grounding & Unsupported Content
    # If the response mentions specific medication names not present in patient_state or retrieved_context
    med_candidates = ["insulin", "metformin", "amoxicillin", "lisinopril", "atorvastatin", "albuterol"]
    for med in med_candidates:
        if med in text_lower:
            in_patient_meds = any(med in m for m in patient_terms["medications"])
            in_context = med in context_text
            if not in_patient_meds and not in_context:
                grounding_flags.append(f"UNGROUNDED_MEDICATION_REFERENCE: {med}")

    # If response is completely ungrounded or empty
    if not text:
        grounding_flags.append("EMPTY_RESPONSE")

    # Evaluate overall pass / fail
    passed = (len(safety_flags) == 0 and len(grounding_flags) == 0)

    revised_response = None
    if not passed:
        revised_response = generate_revised_response(text, safety_flags, patient_terms)

    return SafetyResult(
        passed=passed,
        safety_flags=safety_flags,
        grounding_flags=grounding_flags,
        revised_response=revised_response,
    )
