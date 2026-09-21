"""The 20 general fields; scored instruments remain in src.questions unchanged."""

GENERAL_QUESTIONS = (
    ("name", "What is your name?", None),
    ("age", "What is your age?", None),
    ("gender", "What is your gender?", None),
    ("height_cm", "What is your height? (cm)", None),
    ("weight_kg", "What is your weight? (kg)", None),
    ("goal", "What is your main wellness goal?", ("Weight management", "Better digestion", "Better sleep", "Stress management", "Improve energy/fitness", "General wellness", "Other")),
    ("dietary_preference", "What is your diet type?", ("Vegetarian", "Non-vegetarian", "Vegan", "Other")),
    ("allergies", "Do you have any food allergies or intolerances?", ("No", "Yes")),
    ("foods_to_avoid", "Are there any foods you avoid or any dietary restrictions you follow?", ("No", "Yes")),
    ("health_conditions", "Do you have any diagnosed or ongoing health conditions?", ("No", "Yes")),
    ("current_medicines", "Are you currently taking any medicines?", ("No", "Yes")),
    ("doctor_restrictions", "Has a doctor given you any medical or dietary restrictions?", ("No", "Yes")),
    ("symptoms", "Are you currently experiencing any symptoms or health complaints?", ("No", "Yes")),
    ("main_complaint", "Which symptom bothers you the most?", None),
    ("symptom_duration", "How long have you been experiencing it?", ("A few days", "A few weeks", "A few months", "Long-term")),
    ("activity_level", "What is your usual physical activity level?", ("Low", "Moderate", "High")),
    ("sleep_quality", "How would you rate your sleep quality?", ("Poor", "Average", "Good")),
    ("stress_level", "How would you rate your stress level?", ("Low", "Moderate", "High")),
    ("digestion", "How would you describe your digestion?", ("Poor", "Sometimes disturbed", "Good")),
    ("appetite", "How would you describe your appetite?", ("Low", "Normal", "High")),
)


def required_text(prompt):
    while True:
        value = input(prompt + ": ").strip()
        if value:
            return value
        print("Please provide an answer.")


def choose(prompt, options):
    print(prompt)
    for index, option in enumerate(options, 1):
        print(f"  {index}. {option}")
    while True:
        answer = required_text("Select one option")
        if answer.isdigit() and 1 <= int(answer) <= len(options):
            return options[int(answer) - 1]
        for option in options:
            if answer.casefold() == option.casefold():
                return option
        print("Select one of the displayed options.")


def collect_general_profile(symptom_selector):
    profile = {}
    for number, (key, wording, options) in enumerate(GENERAL_QUESTIONS, 1):
        prompt = f"{number}. {wording}"
        if key == "symptoms":
            profile[key] = symptom_selector()
        elif key in {"main_complaint", "symptom_duration"}:
            profile[key] = (choose(prompt, profile["symptoms"] if key == "main_complaint" else options)
                            if profile["symptoms"] else None)
        elif key in {"allergies", "foods_to_avoid", "health_conditions", "current_medicines", "doctor_restrictions"}:
            if choose(prompt, options) == "No":
                profile[key] = []
            elif key == "allergies":
                # Keep food names usable by the existing hard filter; retain reactions separately.
                foods = required_text("Specify foods (comma separated)")
                profile[key] = [food.strip() for food in foods.split(",") if food.strip()]
                profile["allergy_reactions"] = required_text("Specify the reaction/problem for these foods")
            else:
                details = required_text("Please specify (comma separated)")
                profile[key] = [item.strip() for item in details.split(",") if item.strip()]
        elif key in {"age", "height_cm", "weight_kg"}:
            while True:
                try:
                    value = (int if key == "age" else float)(required_text(prompt))
                    low, high = {"age": (0, 120), "height_cm": (40, 250), "weight_kg": (20, 300)}[key]
                    if not low < value <= high:
                        raise ValueError
                    profile[key] = value
                    break
                except ValueError:
                    print("Please enter a valid number within the supported profile range.")
        else:
            profile[key] = choose(prompt, options) if options else required_text(prompt)
            if profile[key] == "Other" and key in {"goal", "dietary_preference"}:
                profile[key + "_details"] = required_text("Please specify")
    return profile


def validate_general_profile(profile):
    """Validate the new form without imposing new requirements on legacy API callers."""
    for key, _, options in GENERAL_QUESTIONS:
        if key not in profile:
            raise ValueError(f"Missing general questionnaire field: {key}.")
        value = profile[key]
        if key in {"main_complaint", "symptom_duration"} and not profile["symptoms"]:
            if value is not None:
                raise ValueError("Main symptom and duration require selected symptoms.")
        elif key == "main_complaint":
            if value not in profile["symptoms"]:
                raise ValueError("Main symptom must be one of the selected symptoms.")
        elif options and "Yes" not in options and value not in options:
            raise ValueError(f"Invalid option for {key}.")
        elif value is None or value == "":
            raise ValueError(f"Missing general questionnaire field: {key}.")
