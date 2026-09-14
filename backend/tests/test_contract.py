from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_chat_contract():
    response = client.post(
        "/api/chat",
        json={"session_id": "test-001", "message": "I'm dizzy."},
    )
    assert response.status_code == 200
    body = response.json()

    for key in [
        "session_id",
        "patient_state",
        "state_changes",
        "missing_information",
        "navigation",
        "safety",
        "sources",
        "trace_id",
        "response",
    ]:
        assert key in body
