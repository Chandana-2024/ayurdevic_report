import unittest

from src.scoring import score_agni, score_dosha, score_vikriti
from src.services.report_validation import validate_report_state


class ReportValidationTests(unittest.TestCase):
    def setUp(self):
        self.prakriti_answers = {index: "Vata" for index in range(1, 22)}
        self.vikriti_answers = {
            **{f"V{index}": 1 for index in range(1, 8)},
            **{f"P{index}": 3 for index in range(1, 8)},
            **{f"K{index}": 1 for index in range(1, 8)},
        }
        self.agni_answers = {f"A{index}": 3 for index in range(1, 12)}

    def _state(self):
        nutrition = {"calories": 100, "protein_g": 5, "carbs_g": 15, "fat_g": 2, "fiber_g": 3}
        return {
            "patient_profile": {"name": "Patient", "allergies": [], "foods_to_avoid": []},
            "questionnaire_answers": self.prakriti_answers,
            "vikriti_answers": self.vikriti_answers,
            "agni_answers": self.agni_answers,
            "prakriti_result": {**score_dosha(self.prakriti_answers), "constitution": "Vata"},
            "vikriti_result": score_vikriti(self.vikriti_answers),
            "agni_result": score_agni(self.agni_answers),
            "meal_plan": {"days": [{"day": 1, "meals": [{"meal": "Breakfast", "foods": [{"food_name": "Moong dal", "nutrition": nutrition}], "meal_total": nutrition}], "daily_total": nutrition}]},
        }

    def test_recalculates_plan_total_from_displayed_foods(self):
        snapshot = validate_report_state(self._state())
        self.assertEqual(snapshot["nutrition_total"]["calories"], 100.0)
        self.assertEqual(snapshot["status"], "REVIEW_REQUIRED")
        self.assertTrue(any("portion" in w for w in snapshot["warnings"]))

    def test_rejects_displayed_score_that_does_not_match_answers(self):
        state = self._state()
        state["prakriti_result"]["scores"]["Vata"] = 1
        snapshot = validate_report_state(state)
        self.assertIn("displayed scores do not match", " ".join(snapshot["failed_checks"]))
        self.assertFalse(snapshot["can_finalize"])

    def test_rejects_restricted_ingredient_not_just_food_name(self):
        state = self._state()
        state["patient_profile"]["allergies"] = ["peanut"]
        state["meal_plan"]["days"][0]["meals"][0]["foods"][0]["ingredients"] = "moong dal, peanut"
        snapshot = validate_report_state(state)
        self.assertIn("Restricted food selected", " ".join(snapshot["failed_checks"]))

    def test_prakriti_requires_all_21_source_answers(self):
        with self.assertRaises(ValueError):
            score_dosha({1: "Vata"})

    def test_agni_rejects_unavailable_tikshnagni_response_for_a8(self):
        answers = {f"A{index}": 3 for index in range(1, 12)}
        answers["A8"] = 4
        with self.assertRaises(ValueError):
            score_agni(answers)


if __name__ == "__main__":
    unittest.main()
