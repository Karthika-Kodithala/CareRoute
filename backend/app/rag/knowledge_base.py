import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from app.models.schemas import Source


CORPUS_PATH = Path(__file__).parent / "corpus.json"


class KnowledgeBase:
    """Curated clinical knowledge base for CareRoute RAG retrieval."""

    def __init__(self, corpus_path: Optional[Path] = None):
        self.corpus_path = corpus_path or CORPUS_PATH
        self.documents: List[Dict[str, Any]] = self._load_corpus()

    def _load_corpus(self) -> List[Dict[str, Any]]:
        if self.corpus_path.exists():
            try:
                with open(self.corpus_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return self._default_corpus()

    def get_all_documents(self) -> List[Dict[str, Any]]:
        return self.documents

    def get_document_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        for doc in self.documents:
            if doc.get("id") == doc_id:
                return doc
        return None

    def _default_corpus(self) -> List[Dict[str, Any]]:
        return [
            {
                "id": "GUIDE-SYNCOPE-01",
                "title": "Clinical Triage Protocol: Dizziness, Lightheadedness, and Syncope",
                "section": "Emergency Red Flags & Triage Escalation",
                "url_or_id": "guidelines://triage/syncope-dizziness-v1",
                "snippet": "Dizziness accompanied by fainting (syncope) or transient loss of consciousness is a red flag requiring immediate emergency or urgent clinical assessment to rule out cardiac arrhythmias, neurological events, or severe hemodynamic instability.",
                "content": "Patients presenting with dizziness, lightheadedness, or vertigo must be screened for syncope (fainting) or loss of consciousness. Any report of actual fainting or passing out is an immediate escalation event requiring emergency medical services (EMS / 911) or prompt emergency department evaluation.",
                "keywords": ["dizzy", "dizziness", "lightheaded", "faint", "fainted", "fainting", "syncope", "passed out", "loss of consciousness"],
                "urgency": "emergency",
                "red_flags": ["fainted", "fainting", "syncope", "passed out", "loss of consciousness"],
            },
            {
                "id": "GUIDE-CHEST-01",
                "title": "Emergency Navigation: Acute Chest Discomfort and Cardiac Symptoms",
                "section": "Red Flag Identification & Immediate Escalation",
                "url_or_id": "guidelines://triage/chest-discomfort-v1",
                "snippet": "Any unexplained chest discomfort, pressure, or tightness is a critical red flag requiring urgent emergency medical evaluation. CareRoute must not diagnose or rule out myocardial infarction, but must guide the patient to immediate emergency services.",
                "content": "Unexplained chest discomfort, pressure, heaviness, tightness, or pain in the chest area must be treated as a high-urgency clinical situation. Immediate emergency medical evaluation (calling 911 or visiting the nearest Emergency Department) is required.",
                "keywords": ["chest discomfort", "chest pain", "chest pressure", "tightness", "heart problem", "cardiac", "angina", "myocardial", "shortness of breath"],
                "urgency": "emergency",
                "red_flags": ["chest discomfort", "chest pain", "chest pressure", "radiating pain"],
            },
            {
                "id": "GUIDE-DIABETES-01",
                "title": "Clinical Navigation: Diabetes, Glycemic Symptoms, and Medication Safety",
                "section": "Hypoglycemia Risk, Medication Reconciliation & Safe Care Routing",
                "url_or_id": "guidelines://triage/diabetes-medication-v1",
                "snippet": "Patients with diabetes taking hypoglycemic medications or insulin who experience dizziness or weakness are at acute risk for hypoglycemia. CareRoute must never adjust, prescribe, or discontinue medication dosages.",
                "content": "When a patient reports a diagnosis of diabetes or use of diabetic medications, non-specific symptoms like dizziness indicate possible hypoglycemia. CareRoute is strictly prohibited from advising medication changes.",
                "keywords": ["diabetes", "diabetic", "insulin", "metformin", "blood sugar", "glucose", "hypoglycemia", "medication"],
                "urgency": "urgent-care",
                "red_flags": ["hypoglycemia", "severe shakiness"],
            },
            {
                "id": "GUIDE-SAFETY-01",
                "title": "CareRoute AI Safety Protocol: Clinical Boundaries & Non-Diagnostic Scope",
                "section": "Communication Constraints & Safe Navigation Standards",
                "url_or_id": "guidelines://safety/clinical-boundaries-v1",
                "snippet": "CareRoute is a clinical navigation and triage assistant. Responses must never issue definitive medical diagnoses, offer false certainty or reassurance, or provide ungrounded prescription instructions.",
                "content": "Avoid definitive diagnostic statements. Avoid dangerous reassurance. Never suggest specific medication dosages. Prioritize timely clinical evaluation.",
                "keywords": ["safety", "boundaries", "diagnosis", "prescribe", "medication", "certainty", "disclaimer", "triage"],
                "urgency": "advisory",
                "red_flags": [],
            },
        ]


# Singleton instance
_knowledge_base_instance: Optional[KnowledgeBase] = None


def get_knowledge_base() -> KnowledgeBase:
    global _knowledge_base_instance
    if _knowledge_base_instance is None:
        _knowledge_base_instance = KnowledgeBase()
    return _knowledge_base_instance
