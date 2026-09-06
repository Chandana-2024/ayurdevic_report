from typing import Any

from src.scoring import score_agni


def agni_analysis_agent(state: dict[str, Any]) -> dict:
    """
    Agent 1 component:
    Analyze the 11-question Agni assessment and construct the complete
    structured Agent 1 assessment output payload.
    """

    answers = state.get("agni_answers")

    if not answers:
        raise ValueError(
            "agni_answers are required before Agni analysis."
        )

    agni_result = score_agni(answers)

    ayurvedic_assessment = {
        "patient_profile": state.get("patient_profile", {}),
        "prakriti": state.get("prakriti_result", {}),
        "vikriti": state.get("vikriti_result", {}),
        "agni": agni_result,
    }

    return {
        "agni_result": agni_result,
        "ayurvedic_assessment": ayurvedic_assessment,
    }