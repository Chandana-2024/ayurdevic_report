from typing import Any

from src.ml.disease_predictor import DiseasePredictor


class DiseaseScreeningAgent:
    """
    Symptom-based disease screening agent.

    IMPORTANT:
    This is a screening/research feature only.
    It does not provide a medical diagnosis or treatment.
    """

    def __init__(self):
        self.predictor = DiseasePredictor()

    def run(self, symptoms: dict[str, int]) -> dict[str, Any]:
        prediction = self.predictor.predict(symptoms)

        return {
            "agent": "Disease Screening Agent",
            "screening_result": prediction,
            "safety_message": (
                "This result is generated from symptom patterns "
                "for screening/research purposes only. "
                "It is not a medical diagnosis."
            ),
        }


def disease_screening_agent(state: dict[str, Any]) -> dict[str, Any]:
    """
    LangGraph-compatible node.

    Expects:
        state["disease_symptoms"]

    Example:
        {
            "acidity": 1,
            "indigestion": 1,
            ...
        }
    """

    symptoms = state.get("disease_symptoms")

    if not symptoms:
        raise ValueError(
            "disease_symptoms are required for disease screening."
        )

    agent = DiseaseScreeningAgent()

    result = agent.run(symptoms)

    return {
        "disease_screening_result": result
    }