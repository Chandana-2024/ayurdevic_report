from typing import Any

from src.scoring import score_vikriti


def vikriti_analysis_agent(state: dict[str, Any]) -> dict:
    """
    Deterministic Vikriti assessment agent.

    This agent does not use an LLM.
    """

    answers = state.get("vikriti_answers")

    if not answers:
        raise ValueError(
            "vikriti_answers are required before Vikriti analysis."
        )

    vikriti_result = score_vikriti(answers)

    return {
        "vikriti_result": vikriti_result,
    }