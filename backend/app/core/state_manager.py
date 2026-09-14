import threading
from typing import Dict, List, Any
from app.models.schemas import PatientState
from app.models.patient_state import empty_state, clone_state

_LOCK = threading.Lock()
_STORE: Dict[str, PatientState] = {}
_HISTORY: Dict[str, List[Dict[str, Any]]] = {}


def get_state(session_id: str) -> PatientState:
    with _LOCK:
        if session_id not in _STORE:
            _STORE[session_id] = empty_state(session_id)
        return clone_state(_STORE[session_id])


def save_state(state: PatientState) -> PatientState:
    with _LOCK:
        _STORE[state.session_id] = clone_state(state)
        return clone_state(state)


def reset_state(session_id: str) -> PatientState:
    with _LOCK:
        new_state = empty_state(session_id)
        _STORE[session_id] = new_state
        _HISTORY[session_id] = []
        return clone_state(new_state)


def clear_all_states() -> None:
    with _LOCK:
        _STORE.clear()
        _HISTORY.clear()


def append_history(session_id: str, record: Dict[str, Any]) -> None:
    with _LOCK:
        if session_id not in _HISTORY:
            _HISTORY[session_id] = []
        _HISTORY[session_id].append(record)


def get_history(session_id: str) -> List[Dict[str, Any]]:
    with _LOCK:
        return list(_HISTORY.get(session_id, []))

