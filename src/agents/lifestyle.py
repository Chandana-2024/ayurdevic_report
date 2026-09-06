from typing import Any
from src.agents.ayurveda_rag import get_lifestyle_rag_evidence


def lifestyle_agent(state: dict[str, Any]) -> dict[str, Any]:
    """
    Agent 3: Personalized Ayurvedic Lifestyle & Wellness Agent.

    Provides evidence-backed non-diet lifestyle guidance: Dinacharya, sleep routine,
    exercise/activity, meal timing, stress management, and seasonal routine.
    """
    prakriti_result = state.get("prakriti_result", {})
    primary_dosha = prakriti_result.get("primary_dosha") or "Vata"

    patient_profile = state.get("patient_profile", {})
    goal = patient_profile.get("goal", "general wellness")
    health_conditions = patient_profile.get("health_conditions", [])

    # Retrieve classical lifestyle knowledge via RAG
    rag_chunks = get_lifestyle_rag_evidence(
        primary_dosha=primary_dosha,
        goal=goal,
        health_conditions=health_conditions,
    )

    lifestyle_categories = {
        "dinacharya": [],
        "daily_routine": [],
        "sleep": [],
        "activity": [],
        "meal_timing": [],
        "stress_management": [],
        "seasonal_guidance": [],
    }

    sources = []

    for chunk in rag_chunks:
        topic = chunk.get("topic", "").lower()
        recs = chunk.get("recommendations", [])
        src = f"{chunk.get('source_title')} ({chunk.get('source_reference')})"

        if src not in sources:
            sources.append(src)

        if "dinacharya" in topic:
            lifestyle_categories["dinacharya"].extend(recs)
        elif "sleep" in topic:
            lifestyle_categories["sleep"].extend(recs)
        elif "activity" in topic or "exercise" in topic:
            lifestyle_categories["activity"].extend(recs)
        elif "meal" in topic:
            lifestyle_categories["meal_timing"].extend(recs)
        elif "stress" in topic or "mental" in topic:
            lifestyle_categories["stress_management"].extend(recs)
        elif "seasonal" in topic:
            lifestyle_categories["seasonal_guidance"].extend(recs)
        else:
            lifestyle_categories["daily_routine"].extend(recs)

    lifestyle_plan = {
        "primary_dosha": primary_dosha,
        "lifestyle_plan": lifestyle_categories,
        "personalization_factors": [
            "Prakriti",
            "Vikriti",
            "Agni",
            "Goal",
        ],
        "sources": sources,
    }

    return {
        "lifestyle_plan": lifestyle_plan,
    }
