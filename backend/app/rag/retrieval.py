import re
from typing import Any, Dict, List, Optional, Union
from app.models.schemas import PatientState, Source
from app.rag.knowledge_base import get_knowledge_base


def _tokenize(text: str) -> List[str]:
    """Simple tokenization: lowercase alphanumeric words."""
    if not text:
        return []
    return re.findall(r"\b[a-z0-9]+\b", text.lower())


def _extract_context_terms(patient_context: Union[Dict[str, Any], PatientState, None]) -> Dict[str, List[str]]:
    """Extract structured lists from patient context regardless of input type."""
    if patient_context is None:
        return {"symptoms": [], "conditions": [], "medications": [], "critical_flags": []}

    if isinstance(patient_context, PatientState):
        ctx = patient_context.model_dump() if hasattr(patient_context, "model_dump") else patient_context.dict()
    elif isinstance(patient_context, dict):
        ctx = patient_context
    else:
        ctx = {}

    return {
        "symptoms": [str(s).lower() for s in ctx.get("symptoms", [])],
        "conditions": [str(c).lower() for c in ctx.get("conditions", [])],
        "medications": [str(m).lower() for m in ctx.get("medications", [])],
        "critical_flags": [str(f).lower() for f in ctx.get("critical_flags", [])],
    }


def calculate_relevance_score(
    doc: Dict[str, Any],
    query_text: str,
    query_tokens: List[str],
    context_terms: Dict[str, List[str]],
) -> float:
    """Calculate clinical relevance score for a document against query and patient context."""
    score = 0.0
    doc_id = doc.get("id", "")
    title = doc.get("title", "").lower()
    snippet = doc.get("snippet", "").lower()
    content = doc.get("content", "").lower()
    keywords = [k.lower() for k in doc.get("keywords", [])]
    red_flags = [rf.lower() for rf in doc.get("red_flags", [])]

    # Baseline safety/general relevance
    if doc_id == "GUIDE-SAFETY-01":
        score += 0.5
    elif doc_id == "GUIDE-GENERAL-TRIAGE-01":
        score += 0.2

    # 1. Exact phrase matching on query
    if query_text:
        q_clean = query_text.strip().lower()
        for kw in keywords:
            if kw in q_clean:
                score += 4.0
            elif q_clean in kw:
                score += 2.0

        for rf in red_flags:
            if rf in q_clean:
                score += 6.0

    # 2. Token overlap with keywords, title, snippet, content
    doc_searchable_tokens = set()
    for kw in keywords:
        doc_searchable_tokens.update(_tokenize(kw))
    doc_searchable_tokens.update(_tokenize(title))

    for token in query_tokens:
        if token in doc_searchable_tokens:
            score += 2.0
        elif token in snippet or token in content:
            score += 1.0

    # 3. Patient context matching
    # Symptoms
    for symptom in context_terms["symptoms"]:
        s_tokens = _tokenize(symptom)
        for kw in keywords:
            if symptom in kw or any(st in kw for st in s_tokens):
                score += 3.5
        for rf in red_flags:
            if symptom in rf or any(st in rf for st in s_tokens):
                score += 5.0

    # Conditions
    for cond in context_terms["conditions"]:
        c_tokens = _tokenize(cond)
        for kw in keywords:
            if cond in kw or any(ct in kw for ct in c_tokens):
                score += 4.0

    # Medications
    for med in context_terms["medications"]:
        m_tokens = _tokenize(med)
        for kw in keywords:
            if med in kw or any(mt in kw for mt in m_tokens):
                score += 3.5

    # Critical flags (highest priority)
    for flag in context_terms["critical_flags"]:
        f_tokens = _tokenize(flag)
        for rf in red_flags:
            if flag in rf or any(ft in rf for ft in f_tokens):
                score += 7.0
        for kw in keywords:
            if flag in kw or any(ft in kw for ft in f_tokens):
                score += 4.0

    return score


def retrieve_guidance(
    query: str,
    patient_context: Union[Dict[str, Any], PatientState, None] = None,
    top_k: int = 3,
) -> List[Source]:
    """Retrieve top_k grounded clinical guidance sources based on query and patient context.

    Args:
        query: Patient query message or triage search query string.
        patient_context: Structured patient state (dict or PatientState) containing
                         symptoms, conditions, medications, critical_flags.
        top_k: Maximum number of sources to return.

    Returns:
        List of Source objects containing title, section, url_or_id, and snippet.
    """
    kb = get_knowledge_base()
    documents = kb.get_all_documents()

    query_text = (query or "").lower()
    query_tokens = _tokenize(query_text)
    context_terms = _extract_context_terms(patient_context)

    scored_docs = []
    for doc in documents:
        score = calculate_relevance_score(doc, query_text, query_tokens, context_terms)
        scored_docs.append((score, doc))

    # Sort descending by score
    scored_docs.sort(key=lambda x: x[0], reverse=True)

    # Convert top_k to Source schemas
    results: List[Source] = []
    for score, doc in scored_docs[:top_k]:
        results.append(
            Source(
                title=doc.get("title", "Clinical Protocol"),
                section=doc.get("section", "Clinical Navigation Guidance"),
                url_or_id=doc.get("url_or_id", doc.get("id", "")),
                snippet=doc.get("snippet", doc.get("content", "")[:200]),
            )
        )

    return results


def retrieve_guidance_raw(
    query: str,
    patient_context: Union[Dict[str, Any], PatientState, None] = None,
    top_k: int = 3,
) -> List[Dict[str, Any]]:
    """Retrieve top_k raw guideline documents including full content and metadata."""
    kb = get_knowledge_base()
    documents = kb.get_all_documents()

    query_text = (query or "").lower()
    query_tokens = _tokenize(query_text)
    context_terms = _extract_context_terms(patient_context)

    scored_docs = []
    for doc in documents:
        score = calculate_relevance_score(doc, query_text, query_tokens, context_terms)
        scored_docs.append((score, doc))

    scored_docs.sort(key=lambda x: x[0], reverse=True)
    return [doc for score, doc in scored_docs[:top_k]]
