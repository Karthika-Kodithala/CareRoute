"""
Fact extraction service for CareRoute.
Extracts symptoms, conditions, medications, critical red-flag symptoms,
negations, and clinical intent without diagnosing.
"""

import re
from typing import Dict, List, Set, Any, Optional

# Pre-defined clinical entity dictionaries and patterns
SYMPTOM_PATTERNS: Dict[str, List[str]] = {
    "dizziness": [
        r"\bdizz(?:y|iness)\b",
        r"\blightheaded(?:ness)?\b",
        r"\bfeeling faint\b",
        r"\bvertigo\b",
        r"\bunsteady\b",
    ],
    "fainting / syncope": [
        r"\bfaint(?:ed|ing)?\b",
        r"\bpass(?:ed)? out\b",
        r"\bblack(?:ed)? out\b",
        r"\bloss of consciousness\b",
        r"\bsyncope\b",
    ],
    "chest discomfort / pain": [
        r"\bchest (?:pain|discomfort|pressure|tightness|heaviness|aching)\b",
        r"\bpain in (?:my )?chest\b",
        r"\btightness in (?:my )?chest\b",
        r"\bangina\b",
    ],
    "shortness of breath": [
        r"\bshort(?:ness)? of breath\b",
        r"\btrouble breathing\b",
        r"\bdifficulty breathing\b",
        r"\bbreathless(?:ness)?\b",
        r"\bhard to breathe\b",
        r"\bdyspnea\b",
    ],
    "palpitations": [
        r"\bpalpitation(?:s)?\b",
        r"\bracing heart\b",
        r"\bheart racing\b",
        r"\bpounding heart\b",
        r"\birregular heart(?:beat)?\b",
        r"\bfluttering in chest\b",
    ],
    "headache": [
        r"\bheadache(?:s)?\b",
        r"\bmigraine(?:s)?\b",
        r"\bhead pain\b",
    ],
    "nausea": [
        r"\bnausea\b",
        r"\bnauseous\b",
        r"\bvomit(?:ing|ed)?\b",
        r"\bthrowing up\b",
    ],
    "fatigue": [
        r"\bfatigue(?:d)?\b",
        r"\bexhaust(?:ed|ion)\b",
        r"\btired(?:ness)?\b",
    ],
}

CONDITION_PATTERNS: Dict[str, List[str]] = {
    "diabetes": [
        r"\bdiabet(?:es|ic)\b",
        r"\btype [12] diabetes\b",
    ],
    "hypertension": [
        r"\bhypertension\b",
        r"\bhigh blood pressure\b",
    ],
    "asthma": [
        r"\basthma\b",
        r"\basthmatic\b",
    ],
    "heart disease": [
        r"\bheart disease\b",
        r"\bcoronary (?:artery )?disease\b",
        r"\bheart condition\b",
        r"\bheart attack history\b",
    ],
}

MEDICATION_PATTERNS: Dict[str, List[str]] = {
    "diabetes medication": [
        r"\bmedication for diabetes\b",
        r"\bdiabetes (?:meds|medication|medicine)\b",
        r"\binsulin\b",
        r"\bmetformin\b",
        r"\bglipizide\b",
    ],
    "blood pressure medication": [
        r"\bblood pressure (?:meds|medication|medicine)\b",
        r"\bmedication for (?:high )?blood pressure\b",
        r"\blisinopril\b",
        r"\bamlodipine\b",
        r"\bmetoprolol\b",
    ],
    "aspirin": [
        r"\baspirin\b",
    ],
    "inhaler": [
        r"\binhaler\b",
        r"\balbuterol\b",
    ],
}

CRITICAL_FLAG_SYMPTOMS: Set[str] = {
    "fainting / syncope",
    "chest discomfort / pain",
    "shortness of breath",
}

# Negation patterns for medication
MEDICATION_NEGATION_PATTERNS = [
    r"\bnot taking any (?:meds|medication|medicine)\b",
    r"\bno medication(?:s)?\b",
    r"\bno meds\b",
    r"\bdon't take any (?:meds|medication|medicine)\b",
    r"\bnever take(?:n)? (?:meds|medication|medicine)\b",
]

# Diagnosis request patterns (patient asking the system to diagnose)
DIAGNOSIS_REQUEST_PATTERNS = [
    r"\bdo i have\b",
    r"\bcould this be\b",
    r"\bis this\b",
    r"\bis it a\b",
    r"\bam i having\b",
    r"\bwhat disease\b",
    r"\bdiagnos(?:e|is)\b",
]


def extract_facts(message: str) -> Dict[str, Any]:
    """
    Parses an incoming patient message to extract structured medical facts,
    negations, timeline mentions, and critical flags.
    """
    cleaned_msg = message.lower().strip()
    
    extracted_symptoms: List[str] = []
    extracted_conditions: List[str] = []
    extracted_medications: List[str] = []
    critical_flags: List[str] = []
    
    # Check for diagnosis request
    is_diagnosis_request = any(re.search(p, cleaned_msg) for p in DIAGNOSIS_REQUEST_PATTERNS)
    
    # Check medication negations
    medication_denied = any(re.search(p, cleaned_msg) for p in MEDICATION_NEGATION_PATTERNS)
    
    # Check symptoms
    for symptom, patterns in SYMPTOM_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, cleaned_msg):
                # Verify it's not negated like "no chest pain"
                negated_pattern = rf"\b(?:no|not having|don't have|never had)\s+{pattern}"
                if not re.search(negated_pattern, cleaned_msg):
                    if symptom not in extracted_symptoms:
                        extracted_symptoms.append(symptom)
                    if symptom in CRITICAL_FLAG_SYMPTOMS and symptom not in critical_flags:
                        critical_flags.append(symptom)
                break

    # Check conditions
    for condition, patterns in CONDITION_PATTERNS.items():
        for pattern in patterns:
            # Distinguish from questions like "Do I have a heart problem?" vs "I have diabetes"
            if re.search(pattern, cleaned_msg):
                if not is_diagnosis_request:
                    if condition not in extracted_conditions:
                        extracted_conditions.append(condition)
                break

    # Check medications
    if not medication_denied:
        for med, patterns in MEDICATION_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, cleaned_msg):
                    if med not in extracted_medications:
                        extracted_medications.append(med)
                    break

    # Extract timeline/onset if present
    timeline: Optional[str] = None
    onset_matches = re.findall(
        r"\b(?:started|began|since|for)\s+([a-zA-Z0-9\s]+?)(?:[.,;]|$)",
        cleaned_msg,
    )
    if onset_matches:
        timeline = onset_matches[0].strip()
    elif "this morning" in cleaned_msg:
        timeline = "this morning"
    elif "earlier" in cleaned_msg:
        timeline = "earlier today"
    elif "yesterday" in cleaned_msg:
        timeline = "yesterday"

    return {
        "symptoms": extracted_symptoms,
        "conditions": extracted_conditions,
        "medications": extracted_medications,
        "medication_denied": medication_denied,
        "critical_flags": critical_flags,
        "is_diagnosis_request": is_diagnosis_request,
        "timeline": timeline,
    }
