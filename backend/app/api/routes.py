from fastapi import APIRouter
from app.models.schemas import ChatRequest, CareRouteResponse
from app.agents.care_agent import CareAgent

router = APIRouter()
agent = CareAgent()


@router.post("/chat", response_model=CareRouteResponse)
def chat(request: ChatRequest):
    return agent.handle_message(
        session_id=request.session_id,
        message=request.message,
    )
