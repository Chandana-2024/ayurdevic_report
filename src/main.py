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
    """
    Collect accurate patient information.

    No default patient values are used.
    """
    print("\n" + "=" * 60)
    print("PATIENT PROFILE")
    print("=" * 60)

    print("Please provide your accurate information.\n")

    while True:
        name = input("Enter your Full Name: ").strip()

        if name:
            break

        print("Name cannot be empty. Please enter your name.")

    while True:
        age_str = input("Enter your Age: ").strip()

        try:
            age = int(age_str)

            if age <= 0 or age > 120:
                print(
                    "Invalid input. Please enter a realistic age "
                    "between 1 and 120."
                )
                continue

            break

        except ValueError:
            print("Invalid input. Please enter age as a whole number.")

    while True:
        gender = input(
            "Enter your Gender (Male/Female/Other): "
        ).strip()

        if gender:
            break

        print("Gender cannot be empty. Please enter your gender.")

    while True:
        blood_group = input(
            "Enter your Blood Group (e.g. A+, B+, O+, AB+): "
        ).strip()

        if blood_group:
            break

        print("Blood group cannot be empty. Please enter your blood group.")

    while True:
        height_str = input("Enter your Height in cm: ").strip()

        try:
            height_cm = float(height_str)

            if height_cm <= 40 or height_cm > 250:
                print(
                    "Invalid input. Please enter a valid height "
                    "in cm, for example 170."
                )
                continue

            break

        except ValueError:
            print("Invalid input. Please enter height as a number.")

    while True:
        weight_str = input("Enter your Weight in kg: ").strip()

        try:
            weight_kg = float(weight_str)

            if weight_kg <= 20 or weight_kg > 300:
                print(
                    "Invalid input. Please enter a valid weight "
                    "in kg, for example 65."
                )
                continue

            break

        except ValueError:
            print("Invalid input. Please enter weight as a number.")

    while True:
        dietary_preference = input(
            "Enter Dietary Preference "
            "(Vegetarian / Non-vegetarian / Vegan / Other): "
        ).strip()

        if dietary_preference:
            break

        print(
            "Dietary preference cannot be empty. "
            "Please enter your preference."
        )

    while True:
        allergies_input = input(
            "Enter Allergies "
            "(comma separated, or type 'None' if none): "
        ).strip()

        if allergies_input:
            break

        print("Please enter your allergies or type 'None'.")

    while True:
        foods_to_avoid_input = input(
            "Enter Foods to Avoid "
            "(comma separated, or type 'None' if none): "
        ).strip()

        if foods_to_avoid_input:
            break

        print("Please enter foods to avoid or type 'None'.")

    while True:
        health_conditions_input = input(
            "Enter Health Conditions "
            "(comma separated, or type 'None' if none): "
        ).strip()

        if health_conditions_input:
            break

        print("Please enter health conditions or type 'None'.")

    while True:
        goal = input(
            "Enter Primary Health Goal "
            "(e.g. weight management, digestion, general wellness): "
        ).strip()

        if goal:
            break

        print("Goal cannot be empty. Please enter your primary goal.")

    def parse_list(value: str) -> list[str]:
        if not value:
            return []

        if value.lower() in {"none", "nil", "n/a", "no"}:
            return []

        return [
            item.strip()
            for item in value.split(",")
            if item.strip()
        ]

    return {
        "name": name,
        "age": age,
        "gender": gender,
        "blood_group": blood_group,
        "height_cm": height_cm,
        "weight_kg": weight_kg,
        "dietary_preference": dietary_preference,
        "allergies": parse_list(allergies_input),
        "foods_to_avoid": parse_list(foods_to_avoid_input),
        "health_conditions": parse_list(health_conditions_input),
        "goal": goal,
    }


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


def get_disease_screening_answers() -> dict[str, int] | None:
    """
    Ask whether the user wants symptom-based disease screening.

    If the user selects yes, collect all 31 symptom features.
    If the user selects no, return None.
    """
    print("\n" + "=" * 60)
    print("OPTIONAL DISEASE SCREENING")
    print("=" * 60)

    while True:
        choice = input(
            "Do you want to include symptom-based disease screening? "
            "(yes/no): "
        ).strip().lower()

        if choice in {"yes", "y"}:
            do_screening = True
            break

        if choice in {"no", "n"}:
            do_screening = False
            break

        print(
            "Invalid input. Please enter 'yes' or 'no'."
        )

    if not do_screening:
        print(
            "Skipping disease screening as requested.\n"
        )
        return None

    feature_names = DEFAULT_DISEASE_FEATURES

    if FEATURE_PKL_PATH.exists():
        try:
            with open(FEATURE_PKL_PATH, "rb") as file:
                loaded_features = pickle.load(file)

                if (
                    isinstance(loaded_features, list)
                    and len(loaded_features) == 31
                ):
                    feature_names = loaded_features

        except Exception:
            feature_names = DEFAULT_DISEASE_FEATURES

    print(
        "\nPlease answer the following 31 symptom screening questions."
    )
    print(
        "Enter 1 for YES (symptom present) "
        "or 0 for NO (symptom absent).\n"
    )

    symptoms: dict[str, int] = {}

    for index, feature in enumerate(
        feature_names,
        start=1,
    ):
        display_name = feature.replace(
            "_",
            " ",
        ).title()

        while True:
            answer = input(
                f"{index}. Do you experience {display_name}? "
                "(1 = Yes, 0 = No): "
            ).strip()

            if answer in {"1", "0"}:
                symptoms[feature] = int(answer)
                break

            if answer.lower() in {"y", "yes"}:
                symptoms[feature] = 1
                break

            if answer.lower() in {"n", "no"}:
                symptoms[feature] = 0
                break

            print(
                "Invalid input. Please enter 1 (Yes) or 0 (No)."
            )

    print()

    return symptoms


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
        "qualification": entry("Qualification"),
        "contact_information": entry("Contact information"),
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
        "signature": entry("Doctor signature / sign-off name"),
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
        for field in ("activity_level", "sleep_information", "stress_level", "food_intolerances", "medicine_allergies", "medication_restrictions", "pregnancy_information", "significant_dietary_restrictions", "season"):
            value = input(f"{field.replace('_', ' ').title()} (blank means unknown; use none/not applicable only if confirmed): ").strip()
            patient_profile[field] = value or None

        # STEP 3: Collect 21 Prakriti answers
        prakriti_answers = get_prakriti_answers(language)

        # STEP 4: Collect 21 Vikriti answers
        vikriti_answers = get_vikriti_answers(language)

        # STEP 5: Collect 11 Agni answers
        agni_answers = get_agni_answers(language)

        # STEP 6: Ask diet plan duration
        plan_days = get_plan_days()

        # STEP 7: Optional disease screening
        disease_symptoms = get_disease_screening_answers()

        # STEP 8: Prepare LangGraph state
        initial_state = {
            "answers": prakriti_answers,
            "questionnaire_answers": prakriti_answers,
            "vikriti_answers": vikriti_answers,
            "agni_answers": agni_answers,
            "patient_profile": patient_profile,
            "user_input": patient_profile,
            "plan_days": plan_days,
        }

        if disease_symptoms is not None:
            initial_state["disease_symptoms"] = disease_symptoms

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
        result["doctor_review"] = doctor_review
        if doctor_review.get("approved"):
            try:
                report_workflow.approve(doctor_review)
                report2_path = report_generator.generate_final_report(
                    result,
                    filename=f"Final_Personalized_Wellness_Report_{report_workflow.session_id}.pdf",
                )
                print(f"\nDoctor-approved final report generated:\n{Path(report2_path).resolve()}")
            except (ValueError, PermissionError) as error:
                report_workflow.request_changes()
                print(f"\nDOCTOR VERIFICATION REQUIRED: {error}")
        else:
            report_workflow.request_changes()
            print("\nDOCTOR VERIFICATION REQUIRED - Report 2 was not generated.")

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
