import copy
import tempfile
import unittest
from pathlib import Path
from test_two_report_workflow import TwoReportWorkflowTests
from src.services.report_workflow import TwoReportWorkflow
from src.services.two_report_pdf import TwoReportPDFGenerator
from src.services.final_report_content import patient_report_content

class ApprovalBoundaryTests(unittest.TestCase):
    def setUp(self):
        fixture = TwoReportWorkflowTests()
        self.state = fixture._state()
        self.approval = fixture._approval()
        self.flow = TwoReportWorkflow(self.state)
        self.flow.create_assessment_report()

    def test_pdf_boundary_all_decisions(self):
        with tempfile.TemporaryDirectory() as folder:
            pdf = TwoReportPDFGenerator(folder)
            for decision in (None, 'PENDING', 'PENDING_DOCTOR_REVIEW', 'REQUEST_CHANGES', 'REJECT', 'unknown'):
                self.state['doctor_review'] = {'decision': decision, 'approved': True}
                with self.assertRaises(PermissionError):
                    pdf.generate_final_report(self.state)
                self.assertEqual(list(Path(folder).glob('*.pdf')), [])
            self.state.pop('doctor_review')
            with self.assertRaises(PermissionError):
                pdf.generate_final_report(self.state)
            self.flow.approve(self.approval)
            self.assertTrue(Path(pdf.generate_final_report(self.state)).exists())

    def test_decisions_retain_data(self):
        original = copy.deepcopy(self.state['meal_plan'])
        self.flow.request_changes({'observations': 'Review timing', 'change_requests': 'Adjust dinner'})
        self.assertEqual(self.state['doctor_review']['change_requests'], 'Adjust dinner')
        self.assertEqual(self.state['meal_plan'], original)
        self.flow.reject({'observations': 'Not suitable'})
        with self.assertRaises(PermissionError):
            self.flow.begin_doctor_review()
        with self.assertRaises(PermissionError):
            self.flow.approve(self.approval)
        self.assertEqual(self.state['meal_plan'], original)
        self.assertIn('assessment_report', self.state)

    def test_seven_days_edits_and_patient_projection(self):
        day = self.state['meal_plan']['days'][0]
        self.state['meal_plan']['days'] = [{**copy.deepcopy(day), 'day': i} for i in range(1,8)]
        original = copy.deepcopy(self.state['meal_plan'])
        edited = copy.deepcopy(original)
        edited['days'][0]['meals'][0]['foods'][0]['food_name'] = 'Doctor edited food'
        review = {**self.approval, 'edited_diet_plan': edited,
                  'edited_lifestyle_recommendations': {'recommendations': [{'category': 'sleep', 'personalized_recommendation': 'Doctor edited sleep', 'debug': 'PRIVATE_DEBUG'}]},
                  'medicines': [{'name': 'Doctor supplied entry', 'source': 'DOCTOR_ENTERED'}]}
        self.flow.approve(review)
        data = patient_report_content(self.state['approved_snapshot'])
        self.assertEqual(self.state['meal_plan'], original)
        self.assertEqual(data['columns'], ['Day','Breakfast'])
        self.assertEqual(len(data['rows']), 7)
        self.assertIn('Doctor edited food', str(data))
        self.assertIn('Doctor edited sleep', str(data))
        self.assertIn('Doctor supplied entry', str(data))
        for private in ('PRIVATE_DEBUG', 'nutrition_total', 'failed_checks', 'seasonal_guidance', 'Mid-Morning'):
            self.assertNotIn(private, str(data))
        self.state['doctor_review']['edited_diet_plan']['days'][0]['day'] = 99
        self.assertFalse(self.flow.approval_is_current())

    def test_medicines_require_doctor_source(self):
        with self.assertRaises(ValueError):
            self.flow.approve({**self.approval, 'medicines': [{'name': 'AI entry'}]})
        self.flow.approve(self.approval)
        self.assertEqual(patient_report_content(self.state['approved_snapshot'])['medicines'], [])
