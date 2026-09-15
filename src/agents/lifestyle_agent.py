"""Compatibility entry point for the single personalized Lifestyle RAG agent."""
from src.agents.lifestyle import lifestyle_agent


class LifestyleAgent:
    def generate_lifestyle_plan(self, patient_profile, ayurvedic_assessment):
        state = {"patient_profile": patient_profile,
                 "prakriti_result": ayurvedic_assessment.get("prakriti", {}),
                 "vikriti_result": ayurvedic_assessment.get("vikriti", {}),
                 "agni_result": ayurvedic_assessment.get("agni", {})}
        plan = lifestyle_agent(state)["lifestyle_plan"]
        evidence = [{"content": item.get("content", ""),
                     "source_book": item.get("metadata", {}).get("source_book", "Not provided"),
                     "page": item.get("metadata", {}).get("page", "Not provided"),
                     "author": item.get("metadata", {}).get("author", "Not provided")}
                    for item in plan.get("rag_evidence", [])]
        return {"agent": "Personalized Lifestyle RAG Agent", "patient_profile": patient_profile,
                "ayurvedic_assessment": ayurvedic_assessment, "lifestyle_plan": plan,
                "rag_evidence": evidence, "status": "AI-GENERATED - DOCTOR REVIEW REQUIRED"}
