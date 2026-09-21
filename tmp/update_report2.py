from pathlib import Path
import hashlib
import json

p = Path('src/services/two_report_pdf.py')
s = p.read_text(encoding='utf-8')
start = s.index('    def generate_final_report(')
prefix = s[:start]
# The original whole-file guard included Report 2. Preserve the entire unchanged
# Report 1/shared-helper prefix instead now that Report 2 is explicitly in scope.
baseline_path = Path('tests/fixtures/controlled_baseline.json')
baseline = json.loads(baseline_path.read_text())
baseline['files'].pop('src/services/two_report_pdf.py', None)
baseline['report1_pdf_prefix_sha256'] = hashlib.sha256(prefix.encode()).hexdigest()
baseline_path.write_text(json.dumps(baseline, indent=2) + '\n')
p.write_text(prefix + '''    def generate_final_report(self, state: dict[str, Any], filename: str = "Final_Personalized_Wellness_Report.pdf") -> str:
        """Render only the current, explicitly approved patient-facing snapshot."""
        workflow = TwoReportWorkflow(state)
        if not workflow.approval_is_current():
            workflow.invalidate_if_changed()
            raise PermissionError("Stored doctor decision must be APPROVE for this exact content.")
        from src.services.final_report_content import patient_report_content
        from copy import deepcopy
        data = patient_report_content(deepcopy(state["approved_snapshot"]))
        story: list[Any] = []

        def pairs(title, values):
            if values:
                story.append(Paragraph(title, self.section))
                story.append(self._table([[self._p(label), self._p(value)] for label, value in values], [47*mm, 139*mm], header=False))

        pairs("Patient information", data["patient"])
        pairs("Short assessment summary", data["assessment"])
        story.append(Paragraph("Personalized diet timetable", self.section))
        if data["rows"] and len(data["columns"]) > 1:
            # Split unusually wide plans into column groups, retaining every actual
            # meal category and day. Four meal columns fit the existing A4 style.
            for offset in range(1, len(data["columns"]), 4):
                columns = data["columns"][offset:offset + 4]
                rows = [[self._p("Day", self.small), *[self._p(column, self.small) for column in columns]]]
                rows += [[self._p(row[0], self.small), *[self._p(value or "Not supplied", self.small) for value in row[offset:offset + 4]]] for row in data["rows"]]
                story.append(self._table(rows, [15*mm] + [171*mm / len(columns)] * len(columns)))
        else:
            story.append(self._p("No diet timetable was supplied for this review."))
        pairs("Food guidance", data["food_guidance"])
        if data["lifestyle"]:
            story.append(Paragraph("Lifestyle recommendations", self.section))
            for item in data["lifestyle"]:
                story.append(KeepTogether([self._p(item["label"], self.section), self._p(item["recommendation"])]))
                if item["safety"]:
                    story.append(self._p(item["safety"], self.small))
        pairs("Doctor review and approval", data["doctor"])
        if data["medicines"]:
            story.append(Paragraph("Medicines / prescriptions entered by your doctor", self.section))
            rows = [[self._p(label, self.small) for label in ("Medicine", "Dosage", "Frequency", "Duration", "Instructions")]]
            rows += [[self._p(value, self.small) for value in row] for row in data["medicines"]]
            story.append(self._table(rows, [36*mm, 28*mm, 28*mm, 26*mm, 68*mm]))
        story.append(KeepTogether([
            self._p("Approved by Doctor: " + data["doctor_name"]),
            self._p("Typed doctor name: " + data["typed_name"]),
            self._p("Doctor signature: ______________________________"),
        ]))
        story += [Paragraph("Safety note", self.section), self._p("This wellness plan supports your care. Follow the reviewing doctor's instructions and seek qualified care for severe or persistent symptoms.", self.small)]
        # Recheck before writing as well as at entry; there is no ungated export path.
        if not workflow.approval_is_current():
            raise PermissionError("Doctor approval no longer matches the report content.")
        path = self._build(self.output_dir / filename, "FINAL PERSONALIZED WELLNESS REPORT", "Approved by Doctor", story)
        workflow.create_final_report()
        return path
''', encoding='utf-8')
