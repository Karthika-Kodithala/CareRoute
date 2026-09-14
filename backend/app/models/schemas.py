from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    session_id: str
    message: str


class PatientState(BaseModel):
    session_id: str
    symptoms: List[str] = Field(default_factory=list)
    conditions: List[str] = Field(default_factory=list)
    medications: List[str] = Field(default_factory=list)
    critical_flags: List[str] = Field(default_factory=list)
    missing_information: List[str] = Field(default_factory=list)
    confidence: Dict[str, float] = Field(default_factory=dict)
    last_updated: Optional[str] = None


class NavigationResult(BaseModel):
    urgency: str = "unknown"
    next_step: str = ""
    reasoning_summary: str = ""
    safety_flags: List[str] = Field(default_factory=list)


class SafetyResult(BaseModel):
    passed: bool = True
    safety_flags: List[str] = Field(default_factory=list)
    grounding_flags: List[str] = Field(default_factory=list)
    revised_response: Optional[str] = None


class Source(BaseModel):
    title: str
    section: str = ""
    url_or_id: str = ""
    snippet: str = ""


class EvaluationTrace(BaseModel):
    trace_id: str
    scenario_id: Optional[str] = None
    input_message: str
    state_before: Dict[str, Any] = Field(default_factory=dict)
    state_after: Dict[str, Any] = Field(default_factory=dict)
    extracted_facts: List[str] = Field(default_factory=list)
    state_changes: List[str] = Field(default_factory=list)
    missing_information: List[str] = Field(default_factory=list)
    navigation: Dict[str, Any] = Field(default_factory=dict)
    grounding: Dict[str, Any] = Field(default_factory=dict)
    verification: Dict[str, Any] = Field(default_factory=dict)
    final_outcome: Dict[str, Any] = Field(default_factory=dict)


class CareRouteResponse(BaseModel):
    session_id: str
    patient_state: PatientState
    state_changes: List[str] = Field(default_factory=list)
    missing_information: List[str] = Field(default_factory=list)
    navigation: NavigationResult
    safety: SafetyResult
    sources: List[Source] = Field(default_factory=list)
    trace_id: str
    response: str
