from typing import Any

from src.services.nutrition_calculator import (
    NUTRIENT_FIELDS,
    calculate_nutrition_summary,
)


EXPECTED_MEALS = {"breakfast", "lunch", "dinner"}


def normalize_text(value: str) -> str:
    return " ".join(str(value).strip().lower().split())


def nutrition_values_match(
    expected: dict[str, Any],
    actual: dict[str, Any],
) -> bool:
    """Compare calculated nutrition values safely."""
    for nutrient in NUTRIENT_FIELDS:
        expected_value = expected["values"].get(nutrient)
        actual_value = actual.get("values", {}).get(nutrient)

        if expected_value != actual_value:
            return False

    return True


def safety_fact_checker_agent(state: dict[str, Any]) -> dict:
    """
    Validates data consistency and supported patient constraints.

    Serious data errors result in REVIEW_REQUIRED.
    This agent does not silently repair an invalid plan.
    """
    meal_plan = state.get("meal_plan", {})
    food_candidates = state.get("food_candidates", [])
    patient_profile = state.get("patient_profile", {})
    condition_context = state.get("condition_context", {})

    warnings = []
    failed_checks = []

    checks = {
        "food_data": "PASS",
        "meal_structure": "PASS",
        "nutrition": "PASS",
        "patient_constraints": "PASS",
        "ayurvedic_evidence": "PASS",
    }

    candidate_ids = {
        food.get("food_id")
        for food in food_candidates
        if food.get("food_id")
    }

    candidate_names = {
        normalize_text(food.get("name", ""))
        for food in food_candidates
    }

    if meal_plan.get("duration_days") not in {1, 7}:
        checks["meal_structure"] = "FAIL"
        failed_checks.append("Invalid meal-plan duration.")

    plan_days = meal_plan.get("days", [])

    if len(plan_days) != meal_plan.get("duration_days"):
        checks["meal_structure"] = "FAIL"
        failed_checks.append(
            "Meal-plan day count does not match the requested duration."
        )

    exclusions = {
        normalize_text(item)
        for item in patient_profile.get("food_exclusions", [])
    }

    allergies = {
        normalize_text(item)
        for item in patient_profile.get("allergies", [])
    }

    selected_foods = []

    for day_plan in plan_days:
        meals = day_plan.get("meals", [])

        if len(meals) != 3:
            checks["meal_structure"] = "FAIL"
            failed_checks.append(
                f"Day {day_plan.get('day')} does not contain three meals."
            )
            continue

        meal_types = {meal.get("type") for meal in meals}

        if meal_types != EXPECTED_MEALS:
            checks["meal_structure"] = "FAIL"
            failed_checks.append(
                f"Day {day_plan.get('day')} has invalid meal types."
            )

        day_foods = []

        for meal in meals:
            foods = meal.get("foods", [])

            if not foods:
                checks["meal_structure"] = "FAIL"
                failed_checks.append(
                    f"{meal.get('type')} has no selected foods."
                )

            for food in foods:
                food_id = food.get("food_id")
                food_name = normalize_text(food.get("name", ""))

                if food_id not in candidate_ids:
                    checks["food_data"] = "FAIL"
                    failed_checks.append(
                        f"Food ID '{food_id}' is not an approved candidate."
                    )

                if food_name not in candidate_names:
                    checks["food_data"] = "FAIL"
                    failed_checks.append(
                        f"Food '{food.get('name')}' is not in the dataset candidates."
                    )

                if food.get("source") != "food_dataset":
                    checks["food_data"] = "FAIL"
                    failed_checks.append(
                        f"Food '{food.get('name')}' has an invalid source."
                    )

                if food_name in exclusions:
                    checks["patient_constraints"] = "FAIL"
                    failed_checks.append(
                        f"Excluded food selected: {food.get('name')}."
                    )

                if food_name in allergies:
                    checks["patient_constraints"] = "FAIL"
                    failed_checks.append(
                        f"Allergy-matched food selected: {food.get('name')}."
                    )

                day_foods.append(food)
                selected_foods.append(food)

            expected_meal_nutrition = calculate_nutrition_summary(foods)
            actual_meal_nutrition = meal.get("nutrition", {})

            if not nutrition_values_match(
                expected_meal_nutrition,
                actual_meal_nutrition,
            ):
                checks["nutrition"] = "FAIL"
                failed_checks.append(
                    f"Nutrition values do not match for {meal.get('type')}."
                )

        expected_daily_nutrition = calculate_nutrition_summary(day_foods)
        actual_daily_nutrition = day_plan.get("daily_nutrition", {})

        if not nutrition_values_match(
            expected_daily_nutrition,
            actual_daily_nutrition,
        ):
            checks["nutrition"] = "FAIL"
            failed_checks.append(
                f"Daily nutrition values do not match for day {day_plan.get('day')}."
            )

    if patient_profile.get("allergies"):
        checks["patient_constraints"] = "REVIEW_REQUIRED"
        warnings.append(
            "The dataset has no allergen or ingredient fields; allergy "
            "validation is limited to exact food-name matches."
        )

    if patient_profile.get("dietary_preference", "unspecified") != "unspecified":
        checks["patient_constraints"] = "REVIEW_REQUIRED"
        warnings.append(
            "Dietary preference cannot yet be verified because the CSV "
            "does not include a diet-type field."
        )

    if condition_context.get("conditions_present"):
        checks["patient_constraints"] = "REVIEW_REQUIRED"
        warnings.append(
            "Condition-specific dietary safety rules are not implemented; "
            "practitioner review is required."
        )

    ayurveda_context = state.get("ayurveda_context")

    if not ayurveda_context:
        warnings.append(
            "No Ayurvedic book evidence was used because RAG is not yet configured."
        )
    elif ayurveda_context.get("supported") is False:
        checks["ayurvedic_evidence"] = "REVIEW_REQUIRED"
        warnings.append(
            "Ayurvedic evidence was insufficient for one or more requested claims."
        )

    has_failure = "FAIL" in checks.values()
    needs_review = "REVIEW_REQUIRED" in checks.values()

    status = "PASS"

    if has_failure or needs_review:
        status = "REVIEW_REQUIRED"

    validation_result = {
        "status": status,
        "checks": checks,
        "warnings": warnings,
        "failed_checks": failed_checks,
        "validated_food_count": len(selected_foods),
    }

    return {
        "validation_result": validation_result,
    }