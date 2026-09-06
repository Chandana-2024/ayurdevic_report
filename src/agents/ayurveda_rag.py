from typing import Any
from src.rag.retriever import AyurvedaRetriever

_retriever = AyurvedaRetriever()


def get_food_ayurvedic_rag_evidence(
    food_name: str,
    rasa: str | None = None,
    virya: str | None = None,
    vipaka: str | None = None,
) -> dict[str, Any]:
    """Retrieve Ayurvedic food property evidence without LLM hallucination."""
    return _retriever.retrieve_food_ayurvedic_evidence(
        food_name=food_name,
        rasa=rasa,
        virya=virya,
        vipaka=vipaka,
    )


def get_lifestyle_rag_evidence(
    primary_dosha: str,
    goal: str = "",
    health_conditions: list[str] | None = None,
) -> list[dict[str, Any]]:
    """Retrieve evidence-backed lifestyle & wellness guidance for Agent 3."""
    return _retriever.retrieve_lifestyle_knowledge(
        primary_dosha=primary_dosha,
        goal=goal,
        health_conditions=health_conditions,
    )
