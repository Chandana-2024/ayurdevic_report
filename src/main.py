from src.graph import graph
from src.questions import (
    PRAKRITI_QUESTIONS,
    VIKRITI_QUESTIONS,
    AGNI_QUESTIONS,
)


def get_prakriti_answers() -> dict[int, str]:
    """
    Ask the 21 Prakriti questions.

    The user sees only the options.
    The Vata/Pitta/Kapha mapping remains hidden.
    """

    answers = {}

    print("\n" + "=" * 60)
    print("PRAKRITI ASSESSMENT")
    print("=" * 60)

    print(
        "\nChoose the option that describes your usual/natural "
        "pattern best.\n"
    )

    for question in PRAKRITI_QUESTIONS:

        print(f"{question['id']}. {question['text']}")

        for index, option in enumerate(
            question["options"],
            start=1
        ):
            print(
                f"   {index}. {option['text']}"
            )

        while True:

            choice = input(
                "Enter 1, 2, or 3: "
            ).strip()

            if choice in {"1", "2", "3"}:

                selected_option = question[
                    "options"
                ][int(choice) - 1]

                # Store only Dosha mapping.
                answers[
                    question["id"]
                ] = selected_option["dosha"]

                print()
                break

            print(
                "Invalid input. "
                "Please enter 1, 2, or 3.\n"
            )

    return answers


def get_vikriti_answers() -> dict[str, int]:
    """
    Ask the 21 Vikriti questions.

    Scoring:
        1 = Not at all
        3 = Somewhat / Occasionally
        5 = Very often
    """

    answers = {}

    print("\n" + "=" * 60)
    print("VIKRITI ASSESSMENT")
    print("=" * 60)

    print(
        "\nAnswer based on symptoms or changes "
        "you have experienced recently.\n"
    )

    for question in VIKRITI_QUESTIONS:

        print(
            f"{question['id']}. "
            f"{question['text']}"
        )

        for option_number, option in question[
            "options"
        ].items():

            print(
                f"   {option_number}. "
                f"{option['text']}"
            )

        while True:

            choice = input(
                "Enter 1, 2, or 3: "
            ).strip()

            if choice in {"1", "2", "3"}:

                selected_option = question[
                    "options"
                ][choice]

                answers[
                    question["id"]
                ] = selected_option["score"]

                print()
                break

            print(
                "Invalid input. "
                "Please enter 1, 2, or 3.\n"
            )

    return answers


def get_agni_answers() -> dict[str, int]:
    """
    Ask the 11 Agni assessment questions.

    Source:
    Singh et al. (2017)

    Scoring:
        1 = Mandagni
        2 = Vishamagni
        3 = Samagni
        4 = Tikshnagni

    The actual score stored is taken from the
    selected option in AGNI_QUESTIONS.
    """

    answers = {}

    print("\n" + "=" * 60)
    print("AGNI ASSESSMENT")
    print("=" * 60)

    print(
        "\nAnswer according to your usual/current "
        "digestive pattern.\n"
    )

    for question in AGNI_QUESTIONS:

        print(
            f"{question['id']}. "
            f"{question['question']}"
        )

        # Only display options that have actual text.
        # A8 in the published table has no displayed
        # Tikshnagni response.
        display_options = [
            option
            for option in question["options"]
            if option["text"] is not None
        ]

        for index, option in enumerate(
            display_options,
            start=1
        ):
            print(
                f"   {index}. "
                f"{option['text']}"
            )

        while True:

            choice = input(
                f"Enter 1 to {len(display_options)}: "
            ).strip()

            if choice.isdigit():

                choice_number = int(choice)

                if 1 <= choice_number <= len(
                    display_options
                ):

                    selected_option = (
                        display_options[
                            choice_number - 1
                        ]
                    )

                    answers[
                        question["id"]
                    ] = selected_option["score"]

                    print()
                    break

            print(
                f"Invalid input. "
                f"Please enter 1 to "
                f"{len(display_options)}.\n"
            )

    return answers


def get_plan_days() -> int:
    """Ask whether the user wants one day or seven days."""

    print("\nHow many days of diet plan do you want?")
    print("1. One-day plan")
    print("2. Seven-day plan")

    while True:

        choice = input(
            "Enter 1 or 2: "
        ).strip()

        if choice == "1":
            return 1

        if choice == "2":
            return 7

        print(
            "Invalid input. "
            "Please enter 1 or 2."
        )


def get_patient_profile():
    print("\n" + "=" * 60)
    print("PATIENT PROFILE")
    print("=" * 60)

    name = input("Name: ").strip()

    while True:
        try:
            age = int(input("Age: ").strip())

            if age <= 0:
                print("Please enter a valid age.")
                continue

            break
        except ValueError:
            print("Please enter age as a number.")

    gender = input("Gender: ").strip()

    blood_group = input("Blood Group: ").strip()

    while True:
        try:
            height_cm = float(input("Height (cm): ").strip())

            if height_cm <= 0:
                print("Please enter a valid height.")
                continue

            break
        except ValueError:
            print("Please enter height as a number.")

    while True:
        try:
            weight_kg = float(input("Weight (kg): ").strip())

            if weight_kg <= 0:
                print("Please enter a valid weight.")
                continue

            break
        except ValueError:
            print("Please enter weight as a number.")

    dietary_preference = input(
        "Dietary preference (Vegetarian/Non-vegetarian/Vegan/Other): "
    ).strip()

    allergies_input = input(
        "Allergies (comma separated, or type None): "
    ).strip()

    foods_to_avoid_input = input(
        "Foods to avoid (comma separated, or type None): "
    ).strip()

    health_conditions_input = input(
        "Health conditions (comma separated, or type None): "
    ).strip()

    goal = input(
        "Goal (e.g. weight management, general wellness, digestion): "
    ).strip()

    def convert_to_list(value):
        if not value or value.lower() == "none":
            return []

        return [
            item.strip()
            for item in value.split(",")
            if item.strip()
        ]

    patient_profile = {
        "name": name,
        "age": age,
        "gender": gender,
        "blood_group": blood_group,
        "height_cm": height_cm,
        "weight_kg": weight_kg,
        "dietary_preference": dietary_preference,
        "allergies": convert_to_list(allergies_input),
        "foods_to_avoid": convert_to_list(foods_to_avoid_input),
        "health_conditions": convert_to_list(health_conditions_input),
        "goal": goal,
    }

    return patient_profile


def main():

    try:

        patient_profile = get_patient_profile()

        # ------------------------------------------------
        # STEP 1: Prakriti assessment
        # ------------------------------------------------

        prakriti_answers = (
            get_prakriti_answers()
        )

        # ------------------------------------------------
        # STEP 2: Vikriti assessment
        # ------------------------------------------------

        vikriti_answers = (
            get_vikriti_answers()
        )

        # ------------------------------------------------
        # STEP 3: Agni assessment
        # ------------------------------------------------

        agni_answers = (
            get_agni_answers()
        )

        # ------------------------------------------------
        # STEP 4: Meal-plan duration
        # ------------------------------------------------

        plan_days = get_plan_days()

        # ------------------------------------------------
        # STEP 5: Send everything to LangGraph
        # ------------------------------------------------

        result = graph.invoke(
            {
                "answers": prakriti_answers,

                # Existing Prakriti key
                "questionnaire_answers": (
                    prakriti_answers
                ),

                # Vikriti
                "vikriti_answers": (
                    vikriti_answers
                ),

                # NEW: Agni
                "agni_answers": (
                    agni_answers
                ),

                # Patient profile
                "patient_profile": patient_profile,

                # Plan duration
                "plan_days": plan_days,
            }
        )

        # ------------------------------------------------
        # STEP 6: Display final result
        # ------------------------------------------------

        print("\n" + "=" * 60)
        print("FINAL AYURVEDIC ASSESSMENT / DIET RESULT")
        print("=" * 60)

        print(
            result.get(
                "final_response",
                "No final response generated."
            )
        )

        print("=" * 60)

    except FileNotFoundError as error:

        print(
            f"\nDataset error: {error}"
        )

        print(
            "Check that the dataset is available "
            "in the expected folder."
        )

    except ValueError as error:

        print(
            f"\nInput or data error: {error}"
        )

    except Exception as error:

        print(
            f"\nUnexpected error: {error}"
        )


if __name__ == "__main__":
    main()