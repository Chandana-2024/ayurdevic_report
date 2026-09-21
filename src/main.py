import pickle
import sys
from datetime import date
from pathlib import Path
from typing import Any

from src.graph import graph
from src.questions import (
    AGNI_QUESTIONS,
    PRAKRITI_QUESTIONS,
    VIKRITI_QUESTIONS,
)
from src.services.pdf_report import VedAmritPDFReport
from src.services.two_report_pdf import TwoReportPDFGenerator
from src.services.report_workflow import TwoReportWorkflow


PROJECT_ROOT = Path(__file__).resolve().parents[1]

FEATURE_PKL_PATH = PROJECT_ROOT / "models" / "disease_features.pkl"


DEFAULT_DISEASE_FEATURES = [
    "acidity",
    "indigestion",
    "headache",
    "blurred_and_distorted_vision",
    "excessive_hunger",
    "muscle_weakness",
    "stiff_neck",
    "swelling_joints",
    "movement_stiffness",
    "depression",
    "irritability",
    "visual_disturbances",
    "painful_walking",
    "abdominal_pain",
    "nausea",
    "vomiting",
    "blood_in_mucus",
    "Fatigue",
    "Fever",
    "Dehydration",
    "loss_of_appetite",
    "cramping",
    "blood_in_stool",
    "gnawing",
    "upper_abdomain_pain",
    "fullness_feeling",
    "hiccups",
    "abdominal_bloating",
    "heartburn",
    "belching",
    "burning_ache",
]


def _safe_print(text: str) -> None:
    """
    Print text safely to the console.

    This avoids Windows cp1252 Unicode encoding errors.
    """
    try:
        print(text)
    except UnicodeEncodeError:
        encoding = sys.stdout.encoding or "utf-8"

        safe_text = text.encode(
            encoding,
            errors="replace",
        ).decode(encoding)

        print(safe_text)

def choose_language() -> str:
    """Return the only supported report language."""
    print("\n" + "=" * 60)
    print("VEDAMRIT - ENGLISH WORKFLOW")
    print("=" * 60)
    return "en"



def get_patient_profile() -> dict[str, Any]:
    from src.services.general_questionnaire import collect_general_profile, validate_general_profile
    profile = collect_general_profile(get_disease_screening_answers)
    validate_general_profile(profile)
    return profile


def get_prakriti_answers(language: str) -> dict[int, str]:
    """
    Ask all 21 Prakriti assessment questions.

    The user sees English and Hindi text together.
    Dosha values remain internal and are not shown to the user.
    """
    answers: dict[int, str] = {}

    print("\n" + "=" * 60)

    if language == "hi":
        print("प्रकृति आकलन (21 प्रश्न)")
        print(
            "जो विकल्प आपके सामान्य और प्राकृतिक स्वभाव "
            "को सबसे अच्छी तरह बताता है, उसे चुनें।\n"
        )
    else:
        print("PRAKRITI ASSESSMENT (21 QUESTIONS)")
        print(
            "Choose the option that describes your "
            "usual/natural constitutional pattern best.\n"
        )

    print("=" * 60)

    for question in PRAKRITI_QUESTIONS:
        print(f"{question['id']}. {question['text']}")

        for index, option in enumerate(
            question["options"],
            start=1,
        ):
            print(f"   {index}. {option['text']}")

        while True:
            choice = input(
                "Enter choice (1, 2, or 3): "
            ).strip()

            if choice in {"1", "2", "3"}:
                selected_option = question["options"][
                    int(choice) - 1
                ]

                answers[question["id"]] = selected_option["dosha"]

                print()
                break

            print(
                "Invalid input. Please enter 1, 2, or 3.\n"
            )

    return answers


def get_vikriti_answers(language: str) -> dict[str, int]:
    """
    Ask all 21 Vikriti assessment questions.

    Scoring:
        1 = Not at all
        3 = Somewhat / Occasionally
        5 = Very often
    """
    answers: dict[str, int] = {}

    print("\n" + "=" * 60)

    if language == "hi":
        print("विकृति आकलन (21 प्रश्न)")
        print(
            "हाल ही में अनुभव किए गए लक्षणों या बदलावों "
            "के आधार पर उत्तर दें।\n"
        )
    else:
        print("VIKRITI ASSESSMENT (21 QUESTIONS)")
        print(
            "Answer based on symptoms or changes "
            "you have experienced recently.\n"
        )

    print("=" * 60)

    for question in VIKRITI_QUESTIONS:
        print(f"{question['id']}. {question['text']}")

        for option_number, option in question["options"].items():
            print(f"   {option_number}. {option['text']}")

        while True:
            choice = input(
                "Enter choice (1, 2, or 3): "
            ).strip()

            if choice in {"1", "2", "3"}:
                selected_option = question["options"][choice]

                answers[question["id"]] = selected_option["score"]

                print()
                break

            print(
                "Invalid input. Please enter 1, 2, or 3.\n"
            )

    return answers


def get_agni_answers(language: str) -> dict[str, int]:
    """
    Ask all 11 Agni assessment questions.

    The number of options is calculated dynamically because
    some Agni questions contain three options.
    """
    answers: dict[str, int] = {}

    print("\n" + "=" * 60)

    if language == "hi":
        print("अग्नि आकलन (11 प्रश्न)")
        print(
            "अपने सामान्य पाचन पैटर्न के अनुसार उत्तर दें।\n"
        )
    else:
        print("AGNI ASSESSMENT (11 QUESTIONS)")
        print(
            "Answer according to your usual digestive pattern.\n"
        )

    print("=" * 60)

    for question in AGNI_QUESTIONS:
        print(f"{question['id']}. {question['question']}")

        display_options = [
            option
            for option in question["options"]
            if option.get("text") is not None
        ]

        for index, option in enumerate(
            display_options,
            start=1,
        ):
            print(f"   {index}. {option['text']}")

        while True:
            choice = input(
                f"Enter choice (1 to {len(display_options)}): "
            ).strip()

            if choice.isdigit():
                choice_number = int(choice)

                if 1 <= choice_number <= len(display_options):
                    selected_option = display_options[
                        choice_number - 1
                    ]

                    answers[question["id"]] = selected_option["score"]

                    print()
                    break

            print(
                "Invalid input. Please enter a number from "
                f"1 to {len(display_options)}.\n"
            )

    return answers


def get_plan_days() -> int:
    """
    Ask how many days of personalized diet the user wants.

    Allowed range: 1 to 7 days.
    """
    print("\n" + "=" * 60)
    print("DIET PLAN DURATION")
    print("=" * 60)

    while True:
        choice = input(
            "How many days of personalized diet do you want? "
            "(1-7): "
        ).strip()

        if choice.isdigit():
            value = int(choice)

            if 1 <= value <= 7:
                return value

        print(
            "Invalid input. Please enter an integer between 1 and 7."
        )


def disease_feature_names() -> list[str]:
    """Reuse the model feature order and original fallback labels."""
    if FEATURE_PKL_PATH.exists():
        try:
            with open(FEATURE_PKL_PATH, "rb") as file:
                features = pickle.load(file)
            if isinstance(features, list) and len(features) == 31:
                return features
        except Exception:
            pass
    return DEFAULT_DISEASE_FEATURES


def get_disease_screening_answers() -> list[str]:
    """Q13: select existing symptoms once, rather than asking 31 questions."""
    from src.services.general_questionnaire import choose, required_text
    if choose("13. Are you currently experiencing any symptoms or health complaints?", ("No", "Yes")) == "No":
        return []
    features = disease_feature_names()
    for index, feature in enumerate(features, 1):
        print(f"  {index}. {feature}")
    while True:
        answer = required_text("Select all symptoms that apply (comma-separated option numbers)")
        try:
            numbers = list(dict.fromkeys(int(item.strip()) for item in answer.split(",")))
            if not numbers or any(number < 1 or number > len(features) for number in numbers):
                raise ValueError
            return [features[number - 1] for number in numbers]
        except ValueError:
            print("Select one or more of the displayed symptom options.")


def get_doctor_review(state=None) -> dict[str, Any]:
    """Collect only doctor-entered review content; blank entries remain Not provided."""
    print("\nDOCTOR REVIEW (optional; all AI content remains unapproved until confirmed)")
    if input("Is a qualified doctor reviewing this report now? (yes/no): ").strip().lower() not in {"y", "yes"}:
        return {}

    def entry(label: str) -> str | None:
        value = input(f"{label} (leave blank if not provided): ").strip()
        return value or None

    review = {
        "qualified_reviewer": True,
        "doctor_name": entry("Doctor name"),
        "registration_number": entry("Registration number"),
        "qualification": entry("Qualification / specialization"),
        "clinic": entry("Clinic / hospital"),
        "observations": entry("Clinical observations"),
        "confirmed_symptoms": entry("Doctor-confirmed symptoms"),
        "confirmed_prakriti": entry("Doctor-confirmed Prakriti"),
        "confirmed_vikriti": entry("Doctor-confirmed Vikriti"),
        "confirmed_agni": entry("Doctor-confirmed Agni"),
        "assessment": entry("Doctor assessment"),
        "comments": entry("Doctor comments"),
        "wellness_advice": entry("Doctor-approved wellness advice"),
        "food_restrictions": entry("Additional doctor restrictions"),
        "follow_up_date": entry("Follow-up date"),
        "follow_up_instructions": entry("Follow-up instructions / progress monitoring"),
        "final_comments": entry("Final comments"),
    }
    review["edited_diet_plan"] = None
    review["edited_lifestyle_recommendations"] = None
    review["progress_monitoring"] = entry("Progress-monitoring instructions")
    from src.services.doctor_console import review_content
    review = review_content(state if state is not None else {}, review)
    return review


def main() -> None:
    try:
            # STEP 1: Use the English-only workflow
        language = choose_language()

        # STEP 2: Collect real patient profile
        patient_profile = get_patient_profile()
        # STEP 3: Collect 21 Prakriti answers
        prakriti_answers = get_prakriti_answers(language)

        # STEP 4: Collect 21 Vikriti answers
        vikriti_answers = get_vikriti_answers(language)

        # STEP 5: Collect 11 Agni answers
        agni_answers = get_agni_answers(language)

        # Diet duration is a workflow setting, not an additional patient question.
        # DietPlanningState is the common patient state; profiles are collected once.
        initial_state = {
            "questionnaire_answers": prakriti_answers,
            "vikriti_answers": vikriti_answers,
            "agni_answers": agni_answers,
            "patient_profile": patient_profile,
            "plan_days": 7,
        }
        if patient_profile["symptoms"]:
            initial_state["disease_symptoms"] = {
                feature: int(feature in patient_profile["symptoms"])
                for feature in disease_feature_names()
            }

        print("\n" + "=" * 60)

        if language == "hi":
            print("VEDAMRIT WORKFLOW PROCESSING...")
        else:
            print("PROCESSING VEDAMRIT WORKFLOW...")

        print("=" * 60)

        # STEP 9: Invoke LangGraph workflow
        result = graph.invoke(initial_state)
        result["generated_date"] = str(date.today())
        result["last_updated_date"] = str(date.today())
        # Report 1 intentionally contains only Agent 1's preliminary assessment.
        report_workflow = TwoReportWorkflow(result)
        report_generator = TwoReportPDFGenerator()
        report1_path = report_generator.generate_assessment_report(
            result,
            filename=f"AI_Assessment_Report_{report_workflow.session_id}.pdf",
        )
        print(f"\nAI Assessment Report generated for doctor review:\n{Path(report1_path).resolve()}")

        report_workflow.register_agent3_draft()
        report_workflow.begin_doctor_review()
        doctor_review = get_doctor_review(result)
        try:
            if doctor_review:
                report_workflow.record_decision(doctor_review)
            if doctor_review.get("decision") == "APPROVE":
                report2_path = report_generator.generate_final_report(
                    result,
                    filename=f"Final_Personalized_Wellness_Report_{report_workflow.session_id}.pdf",
                )
                print(f"\nDoctor-approved final report generated:\n{Path(report2_path).resolve()}")
            else:
                print("\nReport 2 was not generated. Review status: " + result["workflow_status"])
        except (ValueError, PermissionError) as error:
            report_workflow.request_changes(doctor_review)
            print(f"\nDOCTOR VERIFICATION REQUIRED: {error}")

        # STEP 10: Display final response
        print("\n" + "=" * 60)

        if language == "hi":
            print("अंतिम आयुर्वेदिक आकलन / डाइट परिणाम")
        else:
            print("FINAL AYURVEDIC ASSESSMENT / DIET RESULT")

        print("=" * 60)

        final_response_text = result.get(
            "final_response",
            "No final response generated.",
        )

        if report_workflow.approval_is_current():
            print("DOCTOR APPROVED - use the final reviewed PDF above.")
        else:
            print("DOCTOR VERIFICATION REQUIRED")
        from src.services.doctor_console import save_session
        print(f"Session saved: {save_session(result).resolve()}")

        print("=" * 60)

        # STEP 11: Display two-report workflow result.
        print("\n" + "=" * 50)
        print("VedAmrit completed successfully")
        print("=" * 50)

        print("\nReport 1 is always generated first. Report 2 requires explicit doctor approval.")
        print()

    except FileNotFoundError as error:
        print(f"\nDataset error: {error}")
        print(
            "Check that the dataset is available "
            "in the expected folder."
        )

    except ValueError as error:
        print(f"\nInput or data error: {error}")

    except Exception as error:
        print(f"\nUnexpected error: {error}")


if __name__ == "__main__":
    main()
