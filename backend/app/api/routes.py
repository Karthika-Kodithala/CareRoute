from fastapi import APIRouter
from app.models.schemas import ChatRequest, CareRouteResponse, PatientState
from app.agents.care_agent import CareAgent
from app.core.state_manager import get_state, reset_state, get_history

router = APIRouter()
agent = CareAgent()


@router.post("/chat", response_model=CareRouteResponse)
def chat(request: ChatRequest):
    return agent.handle_message(
        session_id=request.session_id,
        message=request.message,
    )


@router.get("/state/{session_id}", response_model=PatientState)
def read_state(session_id: str):
    return get_state(session_id)


@router.post("/reset/{session_id}", response_model=PatientState)
def reset_session(session_id: str):
    return reset_state(session_id)


@router.get("/history/{session_id}")
def read_history(session_id: str):
    return get_history(session_id)

