from typing import Any


class DietValidator:

    def validate(
        self,
        diet_plan: dict[str, Any],
        patient_profile: dict[str, Any],
    ) -> dict[str, Any]:

        validated_meals = {}
        all_valid = True

        for meal_name, meal in diet_plan.items():

            target = meal.get("target_calories")
            actual = meal.get("actual_calories", 0)

            if target is None:
                calorie_valid = True
                difference = 0
            else:
                difference = actual - target

                # Allow 10% calorie deviation
                tolerance = target * 0.10

                calorie_valid = abs(difference) <= tolerance

            meal_issues = []

            if not calorie_valid:
                meal_issues.append(
                    f"Calorie target exceeded by {round(abs(difference), 1)} kcal"
                    if difference > 0
                    else
                    f"Calorie target short by {round(abs(difference), 1)} kcal"
                )

            # Check portions
            for food in meal.get("foods", []):

                portion = food.get("portion_g", 0)
                min_g = food.get("min_serving_g", 0)
                max_g = food.get("max_serving_g", 0)

                if portion < min_g:
                    meal_issues.append(
                        f"{food['food_name']} is below minimum serving"
                    )

                if portion > max_g:
                    meal_issues.append(
                        f"{food['food_name']} exceeds maximum serving"
                    )

            meal_valid = len(meal_issues) == 0

            if not meal_valid:
                all_valid = False

            validated_meals[meal_name] = {
                **meal,
                "validation": {
                    "valid": meal_valid,
                    "calorie_valid": calorie_valid,
                    "issues": meal_issues,
                },
            }

        return {
            "valid": all_valid,
            "meals": validated_meals,
        }