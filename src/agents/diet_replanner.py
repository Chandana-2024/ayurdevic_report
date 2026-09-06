from typing import Any

from src.agents.diet_meal_planner import DietMealPlanner
from src.services.portion_calculator import PortionCalculator
from src.agents.diet_validation import DietValidator


class DietReplanner:

    def __init__(self):
        self.meal_planner = DietMealPlanner()
        self.portion_calculator = PortionCalculator()
        self.validator = DietValidator()

    def replan(
        self,
        ranked_foods: list[dict[str, Any]],
        daily_target: dict[str, Any],
        patient_profile: dict[str, Any],
    ) -> dict[str, Any]:

        best_plan = None
        best_validation = None
        best_error = float("inf")

        # Try several starting positions in the ranked list
        for start_index in range(0, 10):

            alternative_foods = ranked_foods[start_index:]

            meal_plan = self.meal_planner.build_day(
                alternative_foods,
                daily_target
            )

            portion_plan = self.portion_calculator.calculate_portions(
                meal_plan
            )

            validation = self.validator.validate(
                portion_plan,
                patient_profile
            )

            # Calculate total calorie error
            total_error = 0

            for meal in portion_plan.values():

                target = meal.get("target_calories")

                actual = meal.get("actual_calories", 0)

                if target is not None:
                    total_error += abs(actual - target)

            # Keep the best plan found
            if total_error < best_error:

                best_error = total_error
                best_plan = portion_plan
                best_validation = validation

            # Stop immediately if a valid plan is found
            if validation["valid"]:

                return {
                    "plan": portion_plan,
                    "validation": validation,
                    "replanned": start_index > 0,
                }

        # Return the closest plan if no completely valid plan exists
        return {
            "plan": best_plan,
            "validation": best_validation,
            "replanned": True,
        }