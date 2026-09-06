from typing import Any
from src.services.input_normalizer import normalize_patient_profile


VALID_DOSHAS = {"Vata", "Pitta", "Kapha"}
EXPECTED_QUESTION_IDS = set(range(1, 22))


def validate_patient_profile(profile_data: dict[str, Any]) -> dict[str, Any]:
    """Validate and normalize patient profile dictionary."""
    if not isinstance(profile_data, dict):
        raise ValueError("patient_profile must be a dictionary.")

    return normalize_patient_profile(profile_data)


def intake_profile_agent(state: dict[str, Any]) -> dict:
    """
    Validates questionnaire answers, plan duration, and structured patient profile.
    """
    raw_answers = state.get("questionnaire_answers") or state.get("answers", {})
    plan_days = state.get("plan_days")

    if not isinstance(raw_answers, dict):
        raise ValueError("Questionnaire answers must be a dictionary.")

    normalized_answers: dict[int, str] = {}

    for question_id, answer in raw_answers.items():
        try:
            question_id = int(question_id)
        except (TypeError, ValueError) as error:
            raise ValueError(f"Invalid question ID: {question_id}") from error

        normalized_answers[question_id] = str(answer).strip().title()

    received_question_ids = set(normalized_answers.keys())

    if received_question_ids != EXPECTED_QUESTION_IDS:
        missing = sorted(EXPECTED_QUESTION_IDS - received_question_ids)
        extra = sorted(received_question_ids - EXPECTED_QUESTION_IDS)

        message = "Please provide answers for question IDs 1 through 21."

        if missing:
            message += f" Missing: {missing}."

        if extra:
            message += f" Invalid extra IDs: {extra}."

        raise ValueError(message)

    for question_id, answer in normalized_answers.items():
        if answer not in VALID_DOSHAS:
            raise ValueError(
                f"Invalid answer for question {question_id}. "
                "Expected Vata, Pitta, or Kapha."
            )

    if plan_days not in {1, 7}:
        raise ValueError("Plan duration must be 1 or 7 days.")

    raw_profile = state.get("patient_profile") or state.get("user_input", {})
    patient_profile = validate_patient_profile(raw_profile)

    return {
        "questionnaire_answers": normalized_answers,
        "patient_profile": patient_profile,
        "plan_days": plan_days,
        "errors": [],
    }