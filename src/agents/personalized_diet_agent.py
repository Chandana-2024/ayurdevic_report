from typing import Any

from src.services.food_repository import FoodRepository
from src.agents.food_filter import FoodFilter
from src.agents.food_ranking import FoodRanker
from src.services.diet_target import calculate_diet_target
from src.agents.diet_meal_planner import DietMealPlanner
from src.services.portion_calculator import PortionCalculator
from src.agents.diet_validation import DietValidator
from src.agents.diet_replanner import DietReplanner


class PersonalizedDietAgent:

    def __init__(self):

        self.food_repository = FoodRepository()
        self.food_filter = FoodFilter()
        self.food_ranker = FoodRanker()
        self.meal_planner = DietMealPlanner()
        self.portion_calculator = PortionCalculator()
        self.validator = DietValidator()
        self.replanner = DietReplanner()

    def generate_diet(
        self,
        patient_profile: dict[str, Any],
        ayurvedic_assessment: dict[str, Any],
    ) -> dict[str, Any]:

        # --------------------------------
        # 1. Load food dataset
        # --------------------------------

        foods = self.food_repository.get_all_foods()


        # --------------------------------
        # 2. Hard filtering
        # --------------------------------

        allowed_foods, excluded_foods = (
            self.food_filter.filter_foods(
                foods,
                patient_profile
            )
        )


        if not allowed_foods:

            raise ValueError(
                "No suitable foods available "
                "after applying dietary restrictions."
            )


        # --------------------------------
        # 3. Ayurvedic food ranking
        # --------------------------------

        ranked_foods = self.food_ranker.rank_foods(
            allowed_foods,
            ayurvedic_assessment,
            patient_profile
        )


        # --------------------------------
        # 4. Nutrition target
        # --------------------------------

        daily_target = calculate_diet_target(
            patient_profile
        )


        # --------------------------------
        # 5. Build meals
        # --------------------------------

        meal_plan = self.meal_planner.build_day(
            ranked_foods,
            daily_target
        )


        # --------------------------------
        # 6. Calculate portions
        # --------------------------------

        portion_plan = (
            self.portion_calculator.calculate_portions(
                meal_plan
            )
        )


        # --------------------------------
        # 7. Validate
        # --------------------------------

        validation = self.validator.validate(
            portion_plan,
            patient_profile
        )


        # --------------------------------
        # 8. Re-plan if necessary
        # --------------------------------

        if not validation["valid"]:

            replanned = self.replanner.replan(
                ranked_foods,
                daily_target,
                patient_profile
            )

            final_plan = replanned["plan"]
            final_validation = replanned["validation"]

        else:

            final_plan = portion_plan
            final_validation = validation


        # --------------------------------
        # 9. Return Agent 2 result
        # --------------------------------

        return {
            "agent": "Personalized Diet Agent",

            "patient_profile": patient_profile,

            "ayurvedic_assessment": ayurvedic_assessment,

            "nutrition_target": daily_target,

            "excluded_foods": excluded_foods,

            "diet_plan": final_plan,

            "validation": final_validation,

            "status": (
                "valid"
                if final_validation["valid"]
                else "needs_review"
            ),
        }