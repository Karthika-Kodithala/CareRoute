# Person 1 owns this module.
# Keep the public state shape compatible with app.models.schemas.PatientState.

from datetime import datetime, timezone
from app.models.schemas import PatientState


def empty_state(session_id: str) -> PatientState:
    return PatientState(
        session_id=session_id,
        symptoms=[],
        conditions=[],
        medications=[],
        critical_flags=[],
        missing_information=[],
        confidence={},
        last_updated=datetime.now(timezone.utc).isoformat(),
    )


def clone_state(state: PatientState) -> PatientState:
    return PatientState(
        session_id=state.session_id,
        symptoms=list(state.symptoms),
        conditions=list(state.conditions),
        medications=list(state.medications),
        critical_flags=list(state.critical_flags),
        missing_information=list(state.missing_information),
        confidence=dict(state.confidence),
        last_updated=state.last_updated,
    )
