import pytest
from app.models.schemas import PatientState, Source
from app.rag.retrieval import retrieve_guidance, retrieve_guidance_raw
from app.rag.knowledge_base import get_knowledge_base


def test_knowledge_base_loading():
    kb = get_knowledge_base()
    docs = kb.get_all_documents()
    assert len(docs) >= 4
    doc_ids = [d["id"] for d in docs]
    assert "GUIDE-SYNCOPE-01" in doc_ids
    assert "GUIDE-CHEST-01" in doc_ids
    assert "GUIDE-DIABETES-01" in doc_ids
    assert "GUIDE-SAFETY-01" in doc_ids


def test_retrieve_guidance_syncope():
    sources = retrieve_guidance("I'm dizzy and I fainted earlier", patient_context=None, top_k=2)
    assert len(sources) <= 2
    assert len(sources) > 0

    first_source = sources[0]
    assert isinstance(first_source, Source)
    assert first_source.title != ""
    assert first_source.section != ""
    assert first_source.url_or_id != ""
    assert first_source.snippet != ""
    assert "syncope" in first_source.url_or_id.lower() or "dizziness" in first_source.title.lower()


def test_retrieve_guidance_chest_discomfort():
    sources = retrieve_guidance("I'm having chest discomfort and pressure", patient_context=None, top_k=2)
    assert len(sources) > 0
    top_source = sources[0]
    assert "chest" in top_source.title.lower() or "chest" in top_source.snippet.lower()
    assert top_source.url_or_id.startswith("guidelines://")


def test_retrieve_guidance_with_patient_context_diabetes():
    patient_context = {
        "symptoms": ["dizziness", "shaking"],
        "conditions": ["type 2 diabetes"],
        "medications": ["insulin", "metformin"],
        "critical_flags": [],
    }
    sources = retrieve_guidance("I feel dizzy", patient_context=patient_context, top_k=3)
    assert len(sources) > 0
    # Diabetes or syncope guidance should be prioritized
    titles = [s.title.lower() for s in sources]
    snippets = [s.snippet.lower() for s in sources]
    has_diabetes_guidance = any("diabetes" in t or "diabetes" in sn for t, sn in zip(titles, snippets))
    assert has_diabetes_guidance


def test_retrieve_guidance_with_patient_state_object():
    state = PatientState(
        session_id="test-p2-01",
        symptoms=["chest pain", "shortness of breath"],
        critical_flags=["chest pain"],
    )
    sources = retrieve_guidance("What should I do?", patient_context=state, top_k=2)
    assert len(sources) > 0
    assert any("chest" in s.title.lower() or "respiratory" in s.title.lower() for s in sources)


def test_retrieve_guidance_top_k():
    sources_1 = retrieve_guidance("dizziness", top_k=1)
    sources_3 = retrieve_guidance("dizziness", top_k=3)
    assert len(sources_1) == 1
    assert len(sources_3) == 3


def test_retrieve_guidance_empty_query():
    sources = retrieve_guidance("", patient_context=None, top_k=2)
    assert len(sources) > 0
    for s in sources:
        assert isinstance(s, Source)
        assert s.title != ""


def test_retrieve_guidance_raw():
    raw_docs = retrieve_guidance_raw("fainted and lightheaded", top_k=2)
    assert len(raw_docs) <= 2
    assert len(raw_docs) > 0
    assert "id" in raw_docs[0]
    assert "content" in raw_docs[0]
    assert "keywords" in raw_docs[0]
