from typing import Any


def final_response_agent(state: dict[str, Any]) -> dict[str, Any]:
    """
    VedAmrit final report formatter.

    Includes:
    - Patient profile
    - AYUCARE symptom-based disease screening
    - Prakriti
    - Vikriti
    - Agni
    - Personalized diet
    - Excluded foods
    - Lifestyle and wellness
    - Safety validation
    - Sources

    Disease screening is for research/demo screening only.
    It is NOT a medical diagnosis.
    """

    response_lines = []

    # ============================================================
    # HEADER
    # ============================================================

    response_lines.extend([
        "============================================================",
        "VEDAMRIT PERSONALIZED AYURVEDIC WELLNESS REPORT",
        "============================================================",
        "",
    ])

    # ============================================================
    # 1. PATIENT PROFILE
    # ============================================================

    patient_profile = state.get("patient_profile", {})

    allergies = patient_profile.get("allergies", [])
    foods_to_avoid = patient_profile.get("foods_to_avoid", [])
    health_conditions = patient_profile.get("health_conditions", [])

    if not isinstance(allergies, list):
        allergies = [str(allergies)]

    if not isinstance(foods_to_avoid, list):
        foods_to_avoid = [str(foods_to_avoid)]

    if not isinstance(health_conditions, list):
        health_conditions = [str(health_conditions)]

    response_lines.extend([
        "============================================================",
        "PATIENT PROFILE",
        "============================================================",
        f"Name: {patient_profile.get('name', 'N/A')}",
        f"Age: {patient_profile.get('age', 'N/A')}",
        f"Gender: {patient_profile.get('gender', 'N/A')}",
        f"Blood Group: {patient_profile.get('blood_group', 'N/A')}",
        f"Height: {patient_profile.get('height_cm', 'N/A')} cm",
        f"Weight: {patient_profile.get('weight_kg', 'N/A')} kg",
        f"Dietary Preference: "
        f"{patient_profile.get('dietary_preference', 'unspecified')}",
        f"Allergies: "
        f"{', '.join(map(str, allergies)) if allergies else 'None'}",
        f"Foods to Avoid: "
        f"{', '.join(map(str, foods_to_avoid)) if foods_to_avoid else 'None'}",
        f"Health Conditions: "
        f"{', '.join(map(str, health_conditions)) if health_conditions else 'None'}",
        f"Goal: {patient_profile.get('goal', 'general wellness')}",
        "",
    ])

    # ============================================================
    # 2. AYUCARE DISEASE SCREENING
    # ============================================================

    disease_screening = state.get("disease_screening_result")

    response_lines.extend([
        "============================================================",
        "SYMPTOM-BASED DISEASE SCREENING",
        "============================================================",
    ])

    if disease_screening:

        screening_result = disease_screening.get(
            "screening_result",
            {}
        )

        predicted_condition = screening_result.get(
            "predicted_condition",
            "N/A"
        )

        model_probability = screening_result.get(
            "confidence"
        )

        probabilities = screening_result.get(
            "probabilities",
            {}
        )

        screening_status = screening_result.get(
            "screening_status",
            "screening_only"
        )

        response_lines.append(
            f"Screening Result: {predicted_condition}"
        )

        if model_probability is not None:
            try:
                percentage = float(model_probability) * 100

                response_lines.append(
                    f"Model Probability: {percentage:.2f}%"
                )

            except (TypeError, ValueError):
                response_lines.append(
                    f"Model Probability: {model_probability}"
                )

        response_lines.append(
            f"Screening Status: {screening_status}"
        )

        response_lines.append(
            "Medical Diagnosis: NO"
        )

        if probabilities:

            response_lines.append("")
            response_lines.append(
                "Model Class Probabilities:"
            )

            for condition, probability in probabilities.items():

                try:
                    percentage = float(probability) * 100

                    response_lines.append(
                        f"  - {condition}: {percentage:.2f}%"
                    )

                except (TypeError, ValueError):

                    response_lines.append(
                        f"  - {condition}: {probability}"
                    )

        response_lines.append("")

        response_lines.append(
            "Safety Notice: This symptom-based result is generated "
            "for screening/research purposes only. It is not a "
            "medical diagnosis."
        )

    else:

        response_lines.append(
            "Disease screening was not requested."
        )

        response_lines.append(
            "The VedAmrit wellness workflow continues without "
            "symptom-based disease screening."
        )

    response_lines.append("")

    # ============================================================
    # 3. AYURVEDIC ASSESSMENT - AGENT 1
    # ============================================================

    prakriti_result = state.get(
        "prakriti_result",
        {}
    )

    prakriti_scores = prakriti_result.get(
        "scores",
        {}
    )

    constitution = prakriti_result.get(
        "constitution",
        state.get("constitution", "N/A")
    )

    vikriti_result = state.get(
        "vikriti_result",
        {}
    )

    vikriti_scores = vikriti_result.get(
        "scores",
        {}
    )

    dominant_vikriti = (
        vikriti_result.get("dominant_dosha")
        or vikriti_result.get("dominant")
        or "N/A"
    )

    agni_result = state.get(
        "agni_result",
        {}
    )

    agni_status = agni_result.get(
        "status",
        "N/A"
    )

    response_lines.extend([
        "============================================================",
        "AYURVEDIC ASSESSMENT (AGENT 1)",
        "============================================================",
        f"Prakriti Constitution: {constitution}",
        f"  Primary Dosha: "
        f"{prakriti_result.get('primary_dosha', 'N/A')}",
        f"  Secondary Dosha: "
        f"{prakriti_result.get('secondary_dosha', 'N/A')}",
        f"  Scores: "
        f"Vata: {prakriti_scores.get('Vata', 0)} | "
        f"Pitta: {prakriti_scores.get('Pitta', 0)} | "
        f"Kapha: {prakriti_scores.get('Kapha', 0)}",
        "",
        f"Vikriti Imbalance: Dominant {dominant_vikriti}",
        f"  Scores: "
        f"Vata: {vikriti_scores.get('Vata', 0)} | "
        f"Pitta: {vikriti_scores.get('Pitta', 0)} | "
        f"Kapha: {vikriti_scores.get('Kapha', 0)}",
        "",
        f"Agni Status: {agni_status}",
        f"  Category Scores: "
        f"{agni_result.get('category_scores', {})}",
        "",
    ])

    # ============================================================
    # 4. PERSONALIZED DIET PLAN - AGENT 2
    # ============================================================

    agent2_output = state.get(
        "agent2_output",
        {}
    )

    meal_plan = (
        agent2_output.get("diet_plan")
        or state.get("meal_plan", {})
    )

    response_lines.extend([
        "============================================================",
        "PERSONALIZED DIET PLAN (AGENT 2)",
        "============================================================",
    ])

    if isinstance(meal_plan, dict) and "days" in meal_plan:

        daily_target = meal_plan.get(
            "daily_target",
            {}
        )

        response_lines.extend([
            f"Plan Duration: "
            f"{meal_plan.get('duration_days', 1)} day(s)",

            f"Daily Target Calories: "
            f"{daily_target.get('calories', 'N/A')} kcal",

            f"Target Macros: "
            f"Protein {daily_target.get('protein_g', 'N/A')}g | "
            f"Carbs {daily_target.get('carbs_g', 'N/A')}g | "
            f"Fat {daily_target.get('fat_g', 'N/A')}g",

            "Calculation Basis: Mifflin-St Jeor BMR (1990) "
            "with activity factor assumption 1.375",

            "",
        ])

        for day in meal_plan.get("days", []):

            response_lines.append(
                f"--- DAY {day.get('day', 'N/A')} ---"
            )

            for meal in day.get("meals", []):

                meal_type = str(
                    meal.get("meal")
                    or meal.get("type")
                    or "Meal"
                ).upper()

                foods = meal.get(
                    "foods",
                    []
                )

                food_strings = []

                for food in foods:

                    food_name = (
                        food.get("name")
                        or food.get("food_name")
                        or "Unknown food"
                    )

                    portion = (
                        food.get("portion")
                        or food.get("portion_g")
                        or "100g"
                    )

                    food_strings.append(
                        f"{food_name} ({portion})"
                    )

                food_names = ", ".join(
                    food_strings
                )

                meal_total = meal.get(
                    "meal_total",
                    {}
                )

                reasoning = ""

                if foods:

                    reasoning = foods[0].get(
                        "ayurvedic_reason",
                        ""
                    )

                response_lines.append(
                    f"[{meal_type}]: {food_names}"
                )

                if reasoning:

                    response_lines.append(
                        f"  Ayurvedic Reasoning: {reasoning}"
                    )

                response_lines.append(
                    f"  Meal Nutrition: "
                    f"{meal_total.get('calories', 0)} kcal | "
                    f"P: {meal_total.get('protein_g', 0)}g | "
                    f"C: {meal_total.get('carbs_g', 0)}g | "
                    f"F: {meal_total.get('fat_g', 0)}g"
                )

                response_lines.append("")

            daily_total = day.get(
                "daily_total",
                {}
            )

            response_lines.append(
                f"Daily Total Nutrition: "
                f"{daily_total.get('calories', 0)} kcal | "
                f"P: {daily_total.get('protein_g', 0)}g | "
                f"C: {daily_total.get('carbs_g', 0)}g | "
                f"F: {daily_total.get('fat_g', 0)}g"
            )

            response_lines.append("")

    elif isinstance(meal_plan, dict):

        for key, value in meal_plan.items():

            response_lines.append(
                f"{key}: {value}"
            )

    else:

        response_lines.append(
            "No diet plan available."
        )

    response_lines.append("")

    # ============================================================
    # 5. FOODS EXCLUDED LOG
    # ============================================================

    excluded_log = agent2_output.get(
        "excluded_foods_log",
        []
    )

    response_lines.extend([
        "============================================================",
        "FOODS EXCLUDED LOG",
        "============================================================",
    ])

    if excluded_log:

        for item in excluded_log[:10]:

            food_name = (
                item.get("food")
                or item.get("food_name")
                or "Unknown food"
            )

            reason = item.get(
                "reason",
                "Not suitable"
            )

            response_lines.append(
                f"- {food_name}: {reason}"
            )

        if len(excluded_log) > 10:

            response_lines.append(
                f"  ... and {len(excluded_log) - 10} "
                f"more items excluded by hard safety filters."
            )

    else:

        response_lines.append(
            "No candidates were excluded by hard filters."
        )

    response_lines.append("")

    # ============================================================
    # 6. LIFESTYLE & WELLNESS - AGENT 3
    # ============================================================

    lifestyle_data = state.get(
        "lifestyle_plan",
        {}
    )

    lifestyle_plan = lifestyle_data.get(
        "lifestyle_plan",
        {}
    )

    response_lines.extend([
        "============================================================",
        "LIFESTYLE AND WELLNESS ASSISTANT - AI DRAFT",
        "============================================================",
    ])

    if lifestyle_plan:

        for category, recommendations in lifestyle_plan.items():

            title = category.replace(
                "_",
                " "
            ).title()

            response_lines.append(
                f"[{title}]"
            )

            if isinstance(recommendations, list):

                for recommendation in recommendations:

                    response_lines.append(
                        f"  • {recommendation}"
                    )

            else:

                response_lines.append(
                    f"  • {recommendations}"
                )

            response_lines.append("")

    else:

        response_lines.append(
            "No lifestyle recommendations available."
        )

        response_lines.append("")

    # ============================================================
    # 7. SAFETY FACT-CHECKER
    # ============================================================

    val_res = (
        state.get("validation_result")
        or agent2_output.get("validation")
        or {}
    )

    overall_status = (
        val_res.get("overall_status")
        or val_res.get("status")
        or "PASS"
    )

    safety_status = val_res.get(
        "safety",
        "PASS"
    )

    nutrition_status = val_res.get(
        "nutrition",
        "PASS"
    )

    portion_status = val_res.get(
        "portion",
        "PASS"
    )

    ayurveda_evidence_status = val_res.get(
        "ayurveda_evidence",
        "PASS"
    )

    response_lines.extend([
        "============================================================",
        "SAFETY FACT-CHECKER STATUS",
        "============================================================",
        f"Overall Status: {overall_status}",
        f"Validation Checks: "
        f"Safety: {safety_status} | "
        f"Nutrition: {nutrition_status} | "
        f"Portion: {portion_status} | "
        f"Ayurveda Evidence: {ayurveda_evidence_status}",
    ])

    warnings = val_res.get(
        "warnings",
        []
    )

    if warnings:

        response_lines.append(
            f"Warnings: {warnings}"
        )

    response_lines.append("")

    # ============================================================
    # 8. SOURCES
    # ============================================================

    response_lines.extend([
        "============================================================",
        "SOURCES & RESEARCH EVIDENCE",
        "============================================================",
        "1. Prakriti & Vikriti Assessment: "
        "Deterministic 21-question scoring model",

        "2. Agni Assessment: "
        "Singh A, Singh G, Patwardhan K, Gehlot S. (2017) "
        "Validated Agnibala Tool",

        "3. Energy Target: "
        "Mifflin MD et al. (1990) "
        "Predictive equation for resting energy expenditure",

        "4. Food Knowledge: "
        "Ayurvedic Food Dishes Dataset & "
        "Classical Dravyaguna Reference",

        "5. Disease Screening: "
        "AYUCARE symptom-based Decision Tree model "
        "(research/demo screening only)",
    ])

    diet_sources = agent2_output.get(
        "sources",
        []
    )

    lifestyle_sources = lifestyle_data.get(
        "sources",
        []
    )

    all_sources = (
        diet_sources
        + lifestyle_sources
    )

    for source in all_sources:

        if isinstance(source, dict):

            source_name = source.get(
                "source",
                str(source)
            )

        else:

            source_name = str(source)

        response_lines.append(
            f"• Reference: {source_name}"
        )

    response_lines.append("")

    # ============================================================
    # 9. IMPORTANT NOTICE
    # ============================================================

    response_lines.extend([
        "============================================================",
        "IMPORTANT NOTICE",
        "============================================================",
        "This system is an educational wellness prototype.",
        "",
        "The symptom-based disease screening result is NOT a "
        "medical diagnosis.",
        "",
        "The disease screening model is provided for "
        "research/demo screening purposes only.",
        "",
        "VedAmrit does not replace diagnosis or treatment by a "
        "qualified medical or Ayurvedic professional.",
        "",
        "============================================================",
    ])

    return {
        "final_response": "\n".join(response_lines)
    }

