"""
Test Suite for AyurGenix Agent 2 (Personalized Diet Agent)

Tests the current class-based architecture:
- FoodFilter: Hard dietary constraints
- FoodRanker: Ayurvedic food ranking
- PortionCalculator: Portion sizing
- DietValidator: Meal plan validation
- diet_planning_agent: Orchestrator
"""

import unittest
from src.services.input_normalizer import (
    normalize_dietary_preference,
    normalize_goal,
    normalize_patient_profile,
    normalize_vikriti_result,
)
from src.agents.food_filter import FoodFilter
from src.agents.food_ranking import FoodRanker
from src.agents.diet_validation import DietValidator
from src.agents.diet_planning import diet_planning_agent


class TestAyurGenixInputNormalization(unittest.TestCase):
    """Test input normalization utilities"""

    def test_normalize_dietary_preference(self):
        """Test dietary preference spelling correction"""
        self.assertEqual(normalize_dietary_preference("vegetrain"), "Vegetarian")
        self.assertEqual(normalize_dietary_preference("veg"), "Vegetarian")
        self.assertEqual(normalize_dietary_preference("vegan"), "Vegan")
        self.assertEqual(normalize_dietary_preference("nonveg"), "Non-vegetarian")

    def test_normalize_goal(self):
        """Test goal normalization"""
        self.assertEqual(normalize_goal("weight mangement"), "weight_management")
        self.assertEqual(normalize_goal("weight loss"), "weight_loss")

    def test_normalize_vikriti_result(self):
        """Test vikriti tie resolution"""
        vik_data = {"scores": {"Vata": 7, "Pitta": 21, "Kapha": 21}}
        norm_vik = normalize_vikriti_result(vik_data)
        self.assertTrue(norm_vik["tie"])
        self.assertIn("Pitta", norm_vik["dominant"])
        self.assertIn("Kapha", norm_vik["dominant"])


class TestFoodFilterClass(unittest.TestCase):
    """Test FoodFilter class-based API"""

    def setUp(self):
        self.filter_engine = FoodFilter()
        self.vegetarian_profile = {
            "dietary_preference": "Vegetarian",
            "allergies": [],
            "foods_to_avoid": [],
        }

    def test_filter_vegetarian_diet(self):
        """Test filtering non-vegetarian foods"""
        candidates = [
            {
                "food_id": 1,
                "food_name": "Rice",
                "diet_type": "Vegan",
                "ingredients": "rice",
                "allergens": [],
            },
            {
                "food_id": 2,
                "food_name": "Shrimp Curry",
                "diet_type": "Non-vegetarian",
                "ingredients": "shrimp,coconut",
                "allergens": [],
            },
            {
                "food_id": 3,
                "food_name": "Moong Dal",
                "diet_type": "Vegetarian",
                "ingredients": "moong dal",
                "allergens": [],
            },
        ]

        eligible, excluded = self.filter_engine.filter_foods(
            foods=candidates,
            patient_profile=self.vegetarian_profile,
        )

        eligible_names = [f["food_name"] for f in eligible]
        excluded_names = [f["food_name"] for f in excluded]

        # Vegetarian diet should include Rice and Moong Dal, exclude Shrimp
        self.assertIn("Rice", eligible_names)
        self.assertIn("Moong Dal", eligible_names)
        self.assertIn("Shrimp Curry", excluded_names)
        self.assertEqual(len(eligible), 2)
        self.assertEqual(len(excluded), 1)

    def test_filter_with_allergies(self):
        """Test filtering foods by allergy"""
        candidates = [
            {
                "food_id": 1,
                "food_name": "Peanut Chutney",
                "diet_type": "Vegetarian",
                "ingredients": "peanut,oil",
                "allergens": ["peanut"],
            },
            {
                "food_id": 2,
                "food_name": "Steamed Rice",
                "diet_type": "Vegan",
                "ingredients": "rice,water",
                "allergens": [],
            },
        ]

        profile_with_allergy = {
            "dietary_preference": "Vegetarian",
            "allergies": ["peanut"],
            "foods_to_avoid": [],
        }

        eligible, excluded = self.filter_engine.filter_foods(
            foods=candidates,
            patient_profile=profile_with_allergy,
        )

        eligible_names = [f["food_name"] for f in eligible]
        self.assertIn("Steamed Rice", eligible_names)
        self.assertNotIn("Peanut Chutney", eligible_names)
        self.assertEqual(len(eligible), 1)

    def test_filter_with_avoid_list(self):
        """Test filtering foods from avoid list"""
        candidates = [
            {
                "food_id": 1,
                "food_name": "Brinjal Curry",
                "diet_type": "Vegetarian",
                "ingredients": "brinjal,oil",
                "allergens": [],
            },
            {
                "food_id": 2,
                "food_name": "Steamed Rice",
                "diet_type": "Vegan",
                "ingredients": "rice",
                "allergens": [],
            },
        ]

        profile_with_avoids = {
            "dietary_preference": "Vegetarian",
            "allergies": [],
            "foods_to_avoid": ["brinjal"],
        }

        eligible, excluded = self.filter_engine.filter_foods(
            foods=candidates,
            patient_profile=profile_with_avoids,
        )

        eligible_names = [f["food_name"] for f in eligible]
        self.assertIn("Steamed Rice", eligible_names)
        self.assertNotIn("Brinjal Curry", eligible_names)


class TestFoodRankerClass(unittest.TestCase):
    """Test FoodRanker class-based API"""

    def setUp(self):
        self.ranker = FoodRanker()
        self.base_foods = [
            {
                "food_id": 1,
                "food_name": "Ghee",
                "diet_type": "Vegetarian",
                "ingredients": "butter",
                "allergens": [],
                "vata_effect": -1,
                "pitta_effect": 1,
                "kapha_effect": 1,
            },
            {
                "food_id": 2,
                "food_name": "Cooling Rice",
                "diet_type": "Vegan",
                "ingredients": "rice",
                "allergens": [],
                "vata_effect": 0,
                "pitta_effect": -1,
                "kapha_effect": 0,
            },
        ]

    def test_rank_foods_returns_ranked_list(self):
        """Test that ranking returns a list of foods"""
        ayurvedic_assessment = {
            "prakriti": {
                "primary_dosha": "Pitta",
                "secondary_dosha": "Vata",
                "constitution": "Pitta-Vata",
            },
            "vikriti": {
                "dominant_dosha": "Pitta",
                "secondary_dosha": "Vata",
            },
            "agni": {"status": "Tikshnagni"},
        }
        patient_profile = {
            "goal": "weight_loss",
            "age": 30,
            "dietary_preference": "Vegetarian",
        }

        ranked = self.ranker.rank_foods(
            foods=self.base_foods,
            ayurvedic_assessment=ayurvedic_assessment,
            patient_profile=patient_profile,
        )

        self.assertIsInstance(ranked, list)
        self.assertEqual(len(ranked), len(self.base_foods))

    def test_ranked_foods_have_ranking_score(self):
        """Test that each ranked food has a ranking field"""
        ayurvedic_assessment = {
            "prakriti": {"primary_dosha": "Pitta", "secondary_dosha": "Vata"},
            "vikriti": {"dominant_dosha": "Pitta"},
            "agni": {"status": "Tikshnagni"},
        }
        patient_profile = {"goal": "weight_loss", "dietary_preference": "Vegetarian"}

        ranked = self.ranker.rank_foods(
            foods=self.base_foods,
            ayurvedic_assessment=ayurvedic_assessment,
            patient_profile=patient_profile,
        )

        for food in ranked:
            self.assertIn("ranking", food)
            self.assertIsInstance(food["ranking"], dict)
            self.assertIn("score", food["ranking"])
            self.assertIn("reasons", food["ranking"])


class TestDietValidatorClass(unittest.TestCase):
    """Test DietValidator class-based API"""

    def setUp(self):
        self.validator = DietValidator()

    def test_validate_single_meal(self):
        """Test validation of a single meal plan"""
        meal_plan = {
            "Breakfast": {
                "target_calories": 500.0,
                "actual_calories": 480.0,
                "foods": [
                    {
                        "food_id": 1,
                        "food_name": "Oatmeal",
                        "portion_g": 150.0,
                        "min_serving_g": 100.0,
                        "max_serving_g": 200.0,
                    }
                ],
            }
        }
        patient_profile = {"dietary_preference": "Vegan"}

        result = self.validator.validate(
            diet_plan=meal_plan,
            patient_profile=patient_profile,
        )

        self.assertIsInstance(result, dict)
        # Result should have 'valid' key (bool) and 'meals' key (dict)
        self.assertIn("valid", result)
        self.assertIn("meals", result)

    def test_validate_multiple_meals(self):
        """Test validation of a multi-meal plan"""
        meal_plan = {
            "Breakfast": {
                "target_calories": 400.0,
                "actual_calories": 420.0,
                "foods": [
                    {
                        "food_id": 1,
                        "food_name": "Oatmeal",
                        "portion_g": 150.0,
                        "min_serving_g": 100.0,
                        "max_serving_g": 200.0,
                    }
                ],
            },
            "Lunch": {
                "target_calories": 600.0,
                "actual_calories": 590.0,
                "foods": [
                    {
                        "food_id": 2,
                        "food_name": "Rice",
                        "portion_g": 200.0,
                        "min_serving_g": 150.0,
                        "max_serving_g": 250.0,
                    }
                ],
            },
        }
        patient_profile = {"dietary_preference": "Vegetarian"}

        result = self.validator.validate(
            diet_plan=meal_plan,
            patient_profile=patient_profile,
        )

        self.assertIn("valid", result)
        self.assertIn("meals", result)
        # Check that both meals are validated
        self.assertIn("Breakfast", result["meals"])
        self.assertIn("Lunch", result["meals"])


class TestAgent2Components(unittest.TestCase):
    """Test Agent 2 (Diet Planning Agent) component imports and API"""

    def test_diet_planning_agent_imports_successfully(self):
        """Sanity check: verify diet_planning_agent can be imported without error"""
        # This validates that diet_planning.py uses correct class-based API
        # instead of missing functional API
        self.assertIsNotNone(diet_planning_agent)
        self.assertTrue(callable(diet_planning_agent))


if __name__ == "__main__":
    unittest.main()
