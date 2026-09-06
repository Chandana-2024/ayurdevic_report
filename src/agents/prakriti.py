from typing import Any

from src.scoring import get_constitution, score_dosha


def prakriti_analysis_agent(state: dict[str, Any]) -> dict:
    """
    Deterministic Prakriti assessment agent.

    Takes the user's Prakriti questionnaire answers and calculates:
    - Vata score
    - Pitta score
    - Kapha score
    - percentages
    - primary Dosha
    - secondary Dosha
    - constitution

    No LLM is used for scoring.
    """

    answers = state.get("questionnaire_answers")

    if not answers:
        raise ValueError(
            "questionnaire_answers are required before Prakriti analysis."
        )

    # Deterministic rule-based scoring
    dosha_result = score_dosha(answers)

    # Determine single or mixed constitution
    constitution = get_constitution(dosha_result)

    prakriti_result = {
        "scores": dosha_result["scores"],
        "percentages": dosha_result["percentages"],
        "primary_dosha": dosha_result["primary_dosha"],
        "secondary_dosha": dosha_result["secondary_dosha"],
        "constitution": constitution,
        "total_answers": dosha_result["total_answers"],

        # Updated from the old 20-question description
        "assessment_method": "deterministic_21_question_scoring",
    }

    return {
        "prakriti_result": prakriti_result,

        # Keep these because your existing graph uses them
        "dosha_result": dosha_result,
        "constitution": constitution,
    }