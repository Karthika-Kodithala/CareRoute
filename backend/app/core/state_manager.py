# Person 1: replace this in-memory starter with the chosen persistence strategy.

from typing import Dict
from app.models.schemas import PatientState
from app.models.patient_state import empty_state

_STORE: Dict[str, PatientState] = {}


def get_state(session_id: str) -> PatientState:
    if session_id not in _STORE:
        _STORE[session_id] = empty_state(session_id)
    return _STORE[session_id]


def save_state(state: PatientState) -> PatientState:
    _STORE[state.session_id] = state
    return state
