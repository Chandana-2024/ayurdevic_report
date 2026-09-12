from typing import Any

from src.agents.ayurveda_rag import get_lifestyle_rag_evidence


def _categorize_evidence(content: str) -> str:
    """
    Determine which lifestyle category a retrieved RAG passage
    is most relevant to.
    """

    text = content.lower()

    if any(word in text for word in [
        "dinacharya",
        "daily routine",
        "morning routine",
        "waking",
        "bathing",
    ]):
        return "dinacharya"

    if any(word in text for word in [
        "sleep",
        "bedtime",
        "sleeping",
        "night",
        "rest",
    ]):
        return "sleep"

    if any(word in text for word in [
        "exercise",
        "vyayama",
        "physical activity",
        "activity",
        "walking",
    ]):
        return "activity"

    if any(word in text for word in [
        "meal timing",
        "meals",
        "food timing",
        "eating",
        "diet",
    ]):
        return "meal_timing"

    if any(word in text for word in [
        "stress",
        "mental",
        "mind",
        "meditation",
        "breathing",
        "anxiety",
    ]):
        return "stress_management"

    if any(word in text for word in [
        "season",
        "seasonal",
        "ritu",
        "summer",
        "winter",
        "monsoon",
    ]):
        return "seasonal_guidance"

    return "daily_routine"


def lifestyle_agent(state: dict[str, Any]) -> dict[str, Any]:
    """
    Agent 3: Personalized Ayurvedic Lifestyle & Wellness Agent.

    Provides non-diet lifestyle guidance using:
    - Prakriti
    - Vikriti
    - Agni
    - Patient goal
    - Ayurvedic RAG evidence

    This agent does not diagnose disease or prescribe medication.
    """

    prakriti_result = state.get("prakriti_result", {})
    vikriti_result = state.get("vikriti_result", {})
    agni_result = state.get("agni_result", {})

    primary_dosha = prakriti_result.get("primary_dosha") or "Vata"
    secondary_dosha = prakriti_result.get("secondary_dosha")
    dominant_vikriti = vikriti_result.get("dominant_dosha")
    agni_status = agni_result.get("status")

    patient_profile = state.get("patient_profile", {})

    goal = patient_profile.get(
        "goal",
        "general wellness",
    )

    health_conditions = patient_profile.get(
        "health_conditions",
        [],
    )

    # ---------------------------------------------------------
    # RAG RETRIEVAL
    # ---------------------------------------------------------

    rag_chunks = get_lifestyle_rag_evidence(
        primary_dosha=primary_dosha,
        goal=goal,
        health_conditions=health_conditions,
    )

    # ---------------------------------------------------------
    # LIFESTYLE CATEGORIES
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # PROCESS RAG EVIDENCE
    # ---------------------------------------------------------

    for chunk in rag_chunks:

        content = chunk.get("content", "").strip()

        metadata = chunk.get("metadata", {})

        if not content:
            continue

        category = _categorize_evidence(content)

        source_book = (
            metadata.get("source_book")
            or metadata.get("title")
            or metadata.get("source")
            or "Ayurvedic knowledge base"
        )

        page = metadata.get("page_label")

        if page:
            source = f"{source_book}, page {page}"
        else:
            source = str(source_book)

        if source not in sources:
            sources.append(source)

    # ---------------------------------------------------------
    # FALLBACK RULE-BASED GUIDANCE
    # ---------------------------------------------------------

    # RAG provides evidence. These simple rules ensure that the
    # user still receives practical lifestyle guidance when a
    # retrieved passage does not directly cover every category.

    if not lifestyle_categories["daily_routine"]:
        lifestyle_categories["daily_routine"] = [
            "Maintain a consistent daily routine.",
        ]

    if not lifestyle_categories["sleep"]:
        lifestyle_categories["sleep"] = [
            "Maintain a consistent sleep and wake schedule.",
        ]

    if not lifestyle_categories["activity"]:
        lifestyle_categories["activity"] = [
            "Include physical activity only when medically suitable.",
        ]

    if not lifestyle_categories["meal_timing"]:
        lifestyle_categories["meal_timing"] = [
            "Maintain regular meal timings.",
        ]

    if not lifestyle_categories["stress_management"]:
        lifestyle_categories["stress_management"] = [
            "Include a short, regular relaxation period in the day.",
        ]

    if not lifestyle_categories["seasonal_guidance"]:
        lifestyle_categories["seasonal_guidance"] = [
            "Review seasonal changes with the doctor before making major adjustments.",
        ]

    if not lifestyle_categories["dinacharya"]:
        lifestyle_categories["dinacharya"] = [
            "Maintain a regular daily routine.",
        ]

    # ---------------------------------------------------------
    # REMOVE DUPLICATES
    # ---------------------------------------------------------

    for category, recommendations in lifestyle_categories.items():
        lifestyle_categories[category] = list(
            dict.fromkeys(recommendations)
        )

    # ---------------------------------------------------------
    # FINAL LIFESTYLE PLAN
    # ---------------------------------------------------------

    lifestyle_plan = {
        "primary_dosha": primary_dosha,
        "secondary_dosha": secondary_dosha,
        "dominant_vikriti": dominant_vikriti,
        "agni_status": agni_status,

        "lifestyle_plan": lifestyle_categories,

        "lifestyle_summary": {
            "sleep_duration": "Not provided",
            "sleep_quality": "Not provided",
            "meal_timing": "Not provided",
            "physical_activity": "Not provided",
            "water_intake": "Not provided",
            "stress_level": "Not provided",
            "screen_time": "Not provided",
            "daily_routine": "Not provided",
            "bowel_routine": "Not provided",
        },

        "lifestyle_concerns": [],

        "draft_status": "AI-generated draft - Doctor review required",

        "personalization_factors": [
            "Prakriti",
            "Vikriti",
            "Agni",
            "Goal",
        ],

        "sources": sources,

        "rag_evidence_count": len(rag_chunks),
    }

    return {
        "lifestyle_plan": lifestyle_plan,
    }