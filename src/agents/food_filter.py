from typing import Any


class FoodFilter:
    """
    Applies hard dietary constraints before food ranking.

    Hard constraints:
    1. Dietary preference
    2. Allergies
    3. Foods explicitly avoided
    """

    def filter_foods(
        self,
        foods: list[dict[str, Any]],
        patient_profile: dict[str, Any],
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:

        dietary_preference = (
            patient_profile.get("dietary_preference", "")
            .strip()
            .lower()
        )

        allergies = self._normalize_list(
            patient_profile.get("allergies", [])
        )

        foods_to_avoid = self._normalize_list(
            patient_profile.get("foods_to_avoid", [])
        )

        allowed_foods = []
        excluded_foods = []

        for food in foods:

            reason = self._check_food(
                food=food,
                dietary_preference=dietary_preference,
                allergies=allergies,
                foods_to_avoid=foods_to_avoid,
            )

            if reason:
                excluded_foods.append({
                    "food_id": food["food_id"],
                    "food_name": food["food_name"],
                    "reason": reason,
                })
            else:
                allowed_foods.append(food)

        return allowed_foods, excluded_foods

    def _check_food(
        self,
        food: dict[str, Any],
        dietary_preference: str,
        allergies: list[str],
        foods_to_avoid: list[str],
    ) -> str | None:

        food_name = food["food_name"].lower()

        ingredients = [
            item.lower()
            for item in food.get("ingredients", [])
        ]

        allergens = [
            item.lower()
            for item in food.get("allergens", [])
        ]

        # --------------------------------------------------
        # 1. DIETARY PREFERENCE
        # --------------------------------------------------

        food_diet = food.get("diet_type", "").lower()

        if dietary_preference == "vegan":
            if food_diet != "vegan":
                return "Not suitable for vegan diet"

        elif dietary_preference == "vegetarian":
            if food_diet not in ["vegan", "vegetarian"]:
                return "Not suitable for vegetarian diet"

        # --------------------------------------------------
        # 2. ALLERGIES
        # --------------------------------------------------

        for allergy in allergies:

            if allergy in allergens:
                return f"Contains allergen: {allergy}"

            if allergy in ingredients:
                return f"Contains allergenic ingredient: {allergy}"

            if allergy in food_name:
                return f"Food name contains allergen: {allergy}"

        # --------------------------------------------------
        # 3. FOODS TO AVOID
        # --------------------------------------------------

        for avoided in foods_to_avoid:

            if avoided in food_name:
                return f"Food is explicitly avoided: {avoided}"

            if avoided in ingredients:
                return f"Contains avoided ingredient: {avoided}"

        return None

    @staticmethod
    def _normalize_list(value: Any) -> list[str]:

        if value is None:
            return []

        if isinstance(value, str):
            return [
                item.strip().lower()
                for item in value.split(",")
                if item.strip()
            ]

        if isinstance(value, list):
            return [
                str(item).strip().lower()
                for item in value
                if str(item).strip()
            ]

        return []