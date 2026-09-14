# Person 1 owns this module.
# Keep the public state shape compatible with app.models.schemas.PatientState.

from datetime import datetime, timezone
from app.models.schemas import PatientState


def empty_state(session_id: str) -> PatientState:
    return PatientState(
        session_id=session_id,
        last_updated=datetime.now(timezone.utc).isoformat(),
    )
