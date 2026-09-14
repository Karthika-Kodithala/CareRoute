import pytest
from app.models.schemas import PatientState, SafetyResult, Source
from app.safety.verifier import verify_response


def test_verify_safe_response_passes():
    response_text = (
        "Based on your symptoms of dizziness, we recommend consulting a healthcare provider "
        "for a clinical evaluation. If you feel lightheaded, please sit down in a safe place."
    )
    result = verify_response(
        response=response_text,
        patient_state={"symptoms": ["dizziness"], "critical_flags": []},
        retrieved_context=[],
    )
    assert isinstance(result, SafetyResult)
    assert result.passed is True
    assert len(result.safety_flags) == 0
    assert result.revised_response is None


def test_catch_diagnostic_language():
    unsafe_responses = [
        "You have a heart attack. Please lie down.",
        "You are suffering from acute hypoglycemia.",
        "I diagnose you with a cardiac condition.",
        "This is definitely a heart problem.",
        "You do not have a heart attack, so don't worry.",
    ]
    for resp in unsafe_responses:
        result = verify_response(resp)
        assert result.passed is False, f"Expected failure for: {resp}"
        assert "DIAGNOSTIC_LANGUAGE_DETECTED" in result.safety_flags
        assert result.revised_response is not None


def test_catch_unsafe_certainty():
    unsafe_responses = [
        "You are 100% fine, there is nothing to worry about.",
        "There is no need to see a doctor, it is completely harmless.",
        "You definitely do not need medical care, you are totally fine.",
        "Don't worry, it is just normal stress and 100% safe.",
    ]
    for resp in unsafe_responses:
        result = verify_response(resp)
        assert result.passed is False, f"Expected failure for: {resp}"
        assert "UNSAFE_CERTAINTY_DETECTED" in result.safety_flags
        assert result.revised_response is not None


def test_catch_unsupported_medication():
    unsafe_responses = [
        "Please take 500mg of amoxicillin right away.",
        "Stop taking your insulin until your dizziness goes away.",
        "I recommend taking 2 tablets of ibuprofen.",
        "You should start taking aspirin immediately.",
    ]
    for resp in unsafe_responses:
        result = verify_response(resp)
        assert result.passed is False, f"Expected failure for: {resp}"
        assert "UNSUPPORTED_MEDICATION_INSTRUCTION" in result.safety_flags
        assert result.revised_response is not None


def test_catch_escalation_violation_with_syncope():
    patient_state = {
        "symptoms": ["dizziness", "fainted"],
        "critical_flags": ["fainted"],
    }
    # Unsafe response that fails to escalate or suggests delay
    bad_response = "You are feeling dizzy. Just wait a few days and sleep it off."
    result = verify_response(bad_response, patient_state=patient_state)
    assert result.passed is False
    assert "ESCALATION_RULE_VIOLATION" in result.safety_flags
    assert "911" in result.revised_response or "emergency" in result.revised_response.lower()


def test_escalation_passes_with_proper_emergency_advice():
    patient_state = {
        "symptoms": ["dizziness", "fainted"],
        "critical_flags": ["fainted"],
    }
    good_response = (
        "Because you experienced fainting (syncope) along with dizziness, this is a red flag. "
        "Please seek immediate medical evaluation at the nearest emergency department or call 911."
    )
    result = verify_response(good_response, patient_state=patient_state)
    assert result.passed is True
    assert len(result.safety_flags) == 0


def test_verify_with_patient_state_pydantic_object():
    state = PatientState(
        session_id="test-p2-02",
        symptoms=["chest discomfort"],
        critical_flags=["chest discomfort"],
    )
    # Good response for chest discomfort
    good_response = (
        "Chest discomfort requires immediate medical attention. Please call 911 or visit an urgent emergency room."
    )
    result = verify_response(good_response, patient_state=state)
    assert result.passed is True


def test_verify_with_retrieved_context_sources():
    sources = [
        Source(
            title="Clinical Triage Protocol",
            section="Syncope",
            url_or_id="guidelines://triage/syncope",
            snippet="Syncope requires emergency evaluation.",
        )
    ]
    response = "Syncope is a serious red flag. Seek immediate emergency clinical evaluation."
    result = verify_response(
        response,
        patient_state={"symptoms": ["syncope"], "critical_flags": ["syncope"]},
        retrieved_context=sources,
    )
    assert result.passed is True
