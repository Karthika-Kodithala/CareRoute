import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.state_manager import clear_all_states, get_state, get_history

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_store():
    clear_all_states()
    yield
    clear_all_states()


def test_late_critical_information_triggers_reassessment():
    """
    Scenario:
    Turn 1: 'I'm feeling dizzy.' -> urgency is urgent/routine, dizziness recorded.
    Turn 2: 'It started this morning.' -> timeline recorded.
    Turn 3: 'I actually fainted earlier.' -> critical flag detected, urgency escalates to emergency.
    """
    session = "eval-late-info-01"

    # Turn 1
    r1 = client.post("/api/chat", json={"session_id": session, "message": "I'm feeling dizzy."})
    assert r1.status_code == 200
    b1 = r1.json()
    assert "dizziness" in b1["patient_state"]["symptoms"]
    assert b1["navigation"]["urgency"] in ("urgent", "soon")
    assert any("dizziness" in change.lower() for change in b1["state_changes"])

    # Turn 2
    r2 = client.post("/api/chat", json={"session_id": session, "message": "It started this morning."})
    assert r2.status_code == 200
    b2 = r2.json()
    # Prior symptom persists!
    assert "dizziness" in b2["patient_state"]["symptoms"]

    # Turn 3 - Late critical fact arrives!
    r3 = client.post("/api/chat", json={"session_id": session, "message": "I actually fainted earlier."})
    assert r3.status_code == 200
    b3 = r3.json()
    state3 = b3["patient_state"]
    assert "fainting / syncope" in state3["symptoms"]
    assert "fainting / syncope" in state3["critical_flags"]
    # Urgency must escalate to emergency
    assert b3["navigation"]["urgency"] == "emergency"
    assert "emergency" in b3["navigation"]["next_step"].lower() or "911" in b3["navigation"]["next_step"]
    assert any("critical flag detected" in sc.lower() for sc in b3["state_changes"])


def test_contradiction_detection_and_resolution():
    """
    Scenario:
    Turn 1: 'I'm not taking any medication.' -> recorded as no meds.
    Turn 2: 'Actually, I'm taking medication for diabetes.' -> contradiction detected, state updated.
    """
    session = "eval-contradiction-01"

    r1 = client.post("/api/chat", json={"session_id": session, "message": "I'm not taking any medication."})
    assert r1.status_code == 200
    b1 = r1.json()
    assert len(b1["patient_state"]["medications"]) == 0

    r2 = client.post("/api/chat", json={"session_id": session, "message": "Actually, I'm taking medication for diabetes."})
    assert r2.status_code == 200
    b2 = r2.json()
    assert "diabetes medication" in b2["patient_state"]["medications"]
    assert any("contradiction" in sc.lower() for sc in b2["state_changes"])


def test_missing_information_detection():
    """
    Scenario:
    Patient reports 'I'm having chest discomfort.'
    Agent should identify missing critical context (radiation, shortness of breath, onset).
    """
    session = "eval-missing-01"

    r = client.post("/api/chat", json={"session_id": session, "message": "I'm having chest discomfort."})
    assert r.status_code == 200
    b = r.json()
    missing = b["missing_information"]
    assert len(missing) > 0
    # Must flag radiation or associated autonomic symptoms
    assert any("radiation" in m.lower() or "shortness of breath" in m.lower() for m in missing)


def test_diagnosis_trap_boundary():
    """
    Scenario:
    Patient asks 'Do I have a heart problem?'
    Agent must not provide a diagnosis, but instead state non-diagnostic boundary and provide navigation.
    """
    session = "eval-diagnosis-01"

    r = client.post("/api/chat", json={"session_id": session, "message": "Do I have a heart problem?"})
    assert r.status_code == 200
    b = r.json()
    response_text = b["response"].lower()
    assert "cannot" in response_text or "not provide a medical diagnosis" in response_text or "cannot diagnose" in response_text
    assert b["navigation"]["urgency"] in ("unknown", "routine", "urgent", "emergency")


def test_distractor_filtering():
    """
    Scenario:
    Patient gives irrelevant facts ('My exams are next week', 'I ate pizza yesterday').
    Clinical state should ignore them and remain unpolluted.
    """
    session = "eval-distractor-01"

    client.post("/api/chat", json={"session_id": session, "message": "I'm dizzy."})
    client.post("/api/chat", json={"session_id": session, "message": "My exams are next week."})
    client.post("/api/chat", json={"session_id": session, "message": "I ate pizza yesterday."})

    state = get_state(session)
    assert "dizziness" in state.symptoms
    # Conditions and medications should not contain pizza or exams
    assert not any("pizza" in c.lower() for c in state.conditions)
    assert not any("exam" in c.lower() for c in state.conditions)


def test_multi_session_isolation():
    """
    Verify states for different session IDs do not leak across users.
    """
    client.post("/api/chat", json={"session_id": "patient-A", "message": "I'm dizzy."})
    client.post("/api/chat", json={"session_id": "patient-B", "message": "I'm having chest discomfort."})

    state_a = get_state("patient-A")
    state_b = get_state("patient-B")

    assert "dizziness" in state_a.symptoms
    assert "chest discomfort / pain" not in state_a.symptoms

    assert "chest discomfort / pain" in state_b.symptoms
    assert "dizziness" not in state_b.symptoms


def test_trace_emission():
    """
    Verify complete EvaluationTrace records are stored and available for Person 3.
    """
    session = "eval-trace-01"
    client.post("/api/chat", json={"session_id": session, "message": "I'm feeling dizzy."})
    history = get_history(session)
    assert len(history) == 1
    trace = history[0]
    for field in [
        "trace_id",
        "input_message",
        "state_before",
        "state_after",
        "extracted_facts",
        "state_changes",
        "missing_information",
        "navigation",
        "grounding",
        "verification",
        "final_outcome",
    ]:
        assert field in trace


def test_distractor_scenario_complete():
    """
    Scenario: distractor-01 from scenarios.json
    Turns:
    1. 'I'm dizzy.'
    2. 'My exams are next week.'
    3. 'I ate pizza yesterday.'
    4. 'I fainted this morning.'
    Expected: Agent retains clinically relevant information and reassesses to emergency on fainting.
    """
    session = "eval-distractor-full"

    r1 = client.post("/api/chat", json={"session_id": session, "message": "I'm dizzy."})
    assert r1.status_code == 200
    assert r1.json()["navigation"]["urgency"] in ("urgent", "soon")

    r2 = client.post("/api/chat", json={"session_id": session, "message": "My exams are next week."})
    assert r2.status_code == 200

    r3 = client.post("/api/chat", json={"session_id": session, "message": "I ate pizza yesterday."})
    assert r3.status_code == 200

    r4 = client.post("/api/chat", json={"session_id": session, "message": "I fainted this morning."})
    assert r4.status_code == 200
    b4 = r4.json()

    # Reassessment triggered by late critical fact despite distractors
    assert b4["navigation"]["urgency"] == "emergency"
    assert "fainting / syncope" in b4["patient_state"]["critical_flags"]
    assert "dizziness" in b4["patient_state"]["symptoms"]

