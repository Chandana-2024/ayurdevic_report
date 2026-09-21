import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from src.main import get_patient_profile, disease_feature_names, DEFAULT_DISEASE_FEATURES
from src.questions import PRAKRITI_QUESTIONS, VIKRITI_QUESTIONS, AGNI_QUESTIONS
from src.agents.intake import intake_profile_agent
from src.agents.prakriti import prakriti_analysis_agent
from src.agents.vikriti import vikriti_analysis_agent
from src.agents.agni import agni_analysis_agent
from src.agents.lifestyle import lifestyle_agent
from src.agents.lifestyle_agent import LifestyleAgent
from src.services.general_questionnaire import GENERAL_QUESTIONS, validate_general_profile
from src.services.lifestyle_input import project_lifestyle_input
from src.services.diet_presentation import compact_diet_timetable
from src.services.two_report_pdf import TwoReportPDFGenerator


def complete_profile(symptoms=False):
    answers = ["Test Patient", "35", "Female", "165", "65", "2", "1",
               "No", "No", "No", "No", "No", "Yes" if symptoms else "No"]
    if symptoms:
        answers += ["1,2", "1", "A few weeks"]
    answers += ["Low", "Poor", "High", "Sometimes disturbed", "Normal"]
    with patch("builtins.input", side_effect=answers), patch("builtins.print"):
        return get_patient_profile()


def assessment_state(profile):
    return {"patient_profile": profile, "plan_days": 7,
            "questionnaire_answers": {q["id"]: "Vata" for q in PRAKRITI_QUESTIONS},
            "vikriti_answers": {q["id"]: 1 for q in VIKRITI_QUESTIONS},
            "agni_answers": {q["id"]: q["options"][0]["score"] for q in AGNI_QUESTIONS}}


class ControlledIntegrationTests(unittest.TestCase):
    def test_counts_and_conditional_symptoms(self):
        self.assertEqual([len(GENERAL_QUESTIONS), len(PRAKRITI_QUESTIONS), len(VIKRITI_QUESTIONS), len(AGNI_QUESTIONS)], [20, 21, 21, 11])
        self.assertEqual(len({q[0] for q in GENERAL_QUESTIONS}), 20)
        self.assertEqual(len(disease_feature_names()), 31)
        no = complete_profile()
        self.assertEqual(set(no), {q[0] for q in GENERAL_QUESTIONS})
        self.assertEqual(no["symptoms"], [])
        self.assertIsNone(no["main_complaint"])
        yes = complete_profile(True)
        self.assertEqual(yes["symptoms"], disease_feature_names()[:2])
        self.assertEqual(yes["main_complaint"], yes["symptoms"][0])
        self.assertEqual(yes["symptom_duration"], "A few weeks")
        yes["main_complaint"] = "not selected"
        with self.assertRaisesRegex(ValueError, "selected symptoms"):
            validate_general_profile(yes)

    def test_no_does_not_display_symptom_choices(self):
        from src.main import get_disease_screening_answers
        with patch("builtins.input", return_value="No"), patch("src.main.disease_feature_names") as features:
            self.assertEqual(get_disease_screening_answers(), [])
            features.assert_not_called()

    def test_preserved_instruments_and_scoring(self):
        baseline = json.loads((Path(__file__).parent / "fixtures/controlled_baseline.json").read_text())
        for path, expected in baseline["files"].items():
            # Ignore checkout line-ending conversion, preserve every other byte.
            data = Path(path).read_bytes().replace(b"\r\n", b"\n")
            self.assertEqual(hashlib.sha256(data).hexdigest(), expected, path)
        self.assertEqual(Path("src/services/two_report_pdf.py").read_text(encoding="utf-8").split("    def generate_final_report")[0], baseline["report1_source"])
        self.assertEqual(DEFAULT_DISEASE_FEATURES, baseline["symptoms"])
        self.assertEqual(disease_feature_names(), baseline["model_symptoms"])
        prefix = Path("src/services/two_report_pdf.py").read_text(encoding="utf-8").split("    def generate_final_report(")[0]
        self.assertEqual(hashlib.sha256(prefix.encode()).hexdigest(), baseline["report1_pdf_prefix_sha256"])

    def test_state_and_report1(self):
        profile = complete_profile(True)
        profile.update(current_medicines=["Recorded medicine"], doctor_restrictions=["Recorded restriction"], season="legacy")
        state = assessment_state(profile)
        for agent in (intake_profile_agent, prakriti_analysis_agent, vikriti_analysis_agent, agni_analysis_agent):
            state.update(agent(state))
        for key in ("current_medicines", "doctor_restrictions", "symptoms", "sleep_quality", "digestion", "appetite"):
            self.assertEqual(state["patient_profile"][key], profile[key])
        self.assertNotIn("season", state["patient_profile"])
        with tempfile.TemporaryDirectory() as directory:
            path = TwoReportPDFGenerator(directory).generate_assessment_report(state)
            self.assertTrue(Path(path).read_bytes().startswith(b"%PDF-"))
            data = state["assessment_report"]["assessment_data"]
            self.assertEqual(data["pre_consultation"]["main_complaint"], profile["main_complaint"])
            self.assertEqual(data["patient_profile"]["current_medicines"], profile["current_medicines"])
            self.assertIn("Doctor review", " ".join(data["limitations"]))

    @patch("src.agents.lifestyle.get_lifestyle_rag_evidence", return_value=[{"content": "daily routine sleep meal exercise mind", "metadata": {"source_book": "Test reference", "page": 12}}])
    def test_lifestyle_projection_and_output(self, retrieve):
        state = {"patient_profile": {**complete_profile(True), "season": "Summer", "private_debug": "secret"},
                 "prakriti_result": {"constitution": "Vata"}, "agni_result": {"status": "Vishamagni"}}
        projected = project_lifestyle_input(state)
        self.assertNotIn("name", projected["patient_profile"])
        self.assertNotIn("season", projected["patient_profile"])
        self.assertNotIn("private_debug", projected["patient_profile"])
        result = lifestyle_agent(state)["lifestyle_plan"]
        self.assertEqual({r["category"] for r in result["recommendations"]}, {"daily_routine", "meal_timing", "sleep", "activity", "stress_management"})
        for forbidden in ("seasonal_guidance", "rag_evidence", "rag_query", "factors_used", "personalization_factors", "excerpt", "patient_profile"):
            self.assertNotIn(forbidden, json.dumps(result))
        self.assertIn("Vishamagni", retrieve.call_args.kwargs["patient_context"])
        retrieve.side_effect = RuntimeError("private internal detail")
        fallback = lifestyle_agent(state)["lifestyle_plan"]
        self.assertTrue(fallback["recommendations"])
        self.assertIn("unavailable", " ".join(fallback["safety_flags"]))
        self.assertNotIn("private internal detail", json.dumps(fallback))
        wrapped = LifestyleAgent().generate_lifestyle_plan(state["patient_profile"], {})
        self.assertNotIn("patient_profile", wrapped)
        self.assertNotIn("rag_evidence", wrapped)

    def test_timetable_preserves_actual_meals_without_fabrication(self):
        state = {"meal_plan": {"days": [{"day": day, "notes": ["Same note"], "meals": [
            {"meal": meal, "foods": [{"food_name": "Original food", "portion_g": 100}], "instruction": "Original instruction"}
            for meal in ("Breakfast", "Lunch", "Dinner")]} for day in range(1, 8)]}}
        original = copy.deepcopy(state)
        table = compact_diet_timetable(state)
        self.assertEqual(table["columns"], ["Day", "Breakfast", "Lunch", "Dinner"])
        self.assertEqual([row["day"] for row in table["rows"]], list(range(1, 8)))
        self.assertEqual(table["common"], {"notes": ["Same note"]})
        self.assertTrue(all("notes" not in row["details"] for row in table["rows"]))
        self.assertEqual(state, original)
        self.assertEqual(table["rows"][0]["cells"]["Lunch"][0]["instruction"], "Original instruction")
        single = compact_diet_timetable({"diet_plan": {"breakfast": {"foods": [{"food_name": "Original"}]}}})
        self.assertEqual(single["columns"], ["Day", "breakfast"])
        self.assertEqual(len(single["rows"]), 1)

    @patch("src.agents.lifestyle.get_lifestyle_rag_evidence", return_value=[])
    def test_real_graph_seven_day_output(self, retrieve):
        from src.graph import graph
        state = assessment_state(complete_profile())
        # Use the actual diet/replanning pipeline and all scoring nodes.
        # Only external lifestyle retrieval is isolated in this integration test.
        with tempfile.TemporaryDirectory() as directory:
            generator = TwoReportPDFGenerator(directory)
            with patch("src.services.two_report_pdf.TwoReportPDFGenerator", return_value=generator):
                result = graph.invoke(state)
            categories = [meal["meal"] for meal in result["meal_plan"]["days"][0]["meals"]]
            self.assertEqual(categories, ["Breakfast", "Lunch", "Snack", "Dinner"])
            self.assertEqual(result["diet_timetable"]["columns"], ["Day", *categories])
            self.assertEqual(len(result["diet_timetable"]["rows"]), 7)
            self.assertEqual(result["agent2_output"]["diet_plan"], result["meal_plan"])
            self.assertTrue(Path(result["assessment_pdf_path"]).exists())
            self.assertNotIn("user_input", result)


if __name__ == "__main__":
    unittest.main()
