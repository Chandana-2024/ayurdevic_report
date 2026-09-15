"""Printable A4 Report 1 and Report 2 builders for the doctor-gated workflow."""
from __future__ import annotations

from pathlib import Path
import unicodedata
from typing import Any
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from src.services.report_workflow import TwoReportWorkflow


class TwoReportPDFGenerator:
    """Builds distinct, English-only documents. Report 2 cannot bypass approval."""
    def __init__(self, output_dir: str = "reports") -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        styles = getSampleStyleSheet()
        self.title = ParagraphStyle("title", parent=styles["Title"], alignment=TA_CENTER, fontName="Helvetica-Bold", fontSize=17, leading=21, textColor=colors.HexColor("#234E52"), spaceAfter=4)
        self.sub = ParagraphStyle("sub", parent=styles["Normal"], alignment=TA_CENTER, fontSize=9, leading=12, textColor=colors.HexColor("#475569"), spaceAfter=7)
        self.section = ParagraphStyle("section", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=10.5, leading=14, textColor=colors.HexColor("#234E52"), backColor=colors.HexColor("#E7F1ED"), borderPadding=4, spaceBefore=8, spaceAfter=5)
        self.body = ParagraphStyle("body", parent=styles["BodyText"], fontSize=8.4, leading=11, spaceAfter=3)
        self.small = ParagraphStyle("small", parent=self.body, fontSize=7.5, leading=9)
        self.section.keepWithNext = True

    def _p(self, value: Any, style: ParagraphStyle | None = None) -> Paragraph:
        text = "Not provided" if value in (None, "", [], {}) else str(value)
        if any(char.isalpha() and 'LATIN' not in unicodedata.name(char, '') for char in text):
            raise ValueError("English-only report required: translate supplied content before export.")
        return Paragraph(escape(text).replace("\n", "<br/>"), style or self.body)

    def _list(self, value: Any) -> str:
        if isinstance(value, dict):
            return ", ".join(f"{str(key).replace('_', ' ').title()}: {self._list(item)}" for key, item in value.items()) or "Not provided"
        if isinstance(value, (list, tuple, set)):
            return "; ".join(self._list(item) for item in value) or "Not provided"
        return str(value) if value not in (None, "") else "Not provided"

    def _table(self, rows: list[list[Any]], widths: list[float], header: bool = True) -> Table:
        table = Table(rows, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT", splitInRow=1)
        commands = [("GRID", (0, 0), (-1, -1), .35, colors.HexColor("#B8C7C9")), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]
        if header:
            commands += [("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DCEDEA")), ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold")]
        table.setStyle(TableStyle(commands))
        return table

    def _footer(self, canvas, doc) -> None:
        canvas.saveState(); canvas.setStrokeColor(colors.HexColor("#CBD5E1")); canvas.line(12*mm, 12*mm, A4[0]-12*mm, 12*mm)
        canvas.setFont("Helvetica", 7); canvas.setFillColor(colors.HexColor("#475569")); canvas.drawString(12*mm, 7*mm, "VedAmrit | English-only AI-assisted wellness workflow")
        canvas.drawString(12*mm, A4[1]-8*mm, doc.title); canvas.drawRightString(A4[0]-12*mm, 7*mm, f"Page {doc.page}"); canvas.restoreState()

    def _build(self, path: Path, title: str, status: str, story: list[Any]) -> str:
        doc = SimpleDocTemplate(str(path), pagesize=A4, leftMargin=12*mm, rightMargin=12*mm, topMargin=13*mm, bottomMargin=18*mm, title=title)
        prefix = [Paragraph("VedAmrit", self.title), Paragraph(title, self.sub), self._table([[self._p("Report status"), self._p(status)]], [45*mm, 141*mm], header=False), Spacer(1, 3)]
        doc.build(prefix + story, onFirstPage=self._footer, onLaterPages=self._footer)
        return str(path)

    def generate_assessment_report(self, state: dict[str, Any], filename: str = "AI_Assessment_Report.pdf") -> str:
        workflow = TwoReportWorkflow(state)
        report = workflow.create_assessment_report(); data = report["assessment_data"]; meta = report["metadata"]; profile = data["patient_profile"]
        story: list[Any] = [Paragraph("PRELIMINARY AI ASSESSMENT — NOT DOCTOR APPROVED", self.section), Paragraph("Doctor review is required before personalized recommendations are finalized.", self.body)]
        story += [Paragraph("2. Patient Profile", self.section), self._table([[self._p("Field"), self._p("Information")], *[[self._p(k.replace("_", " ").title()), self._p(profile.get(k))] for k in ("name", "patient_id", "age", "gender", "height_cm", "weight_kg", "dietary_preference")]], [55*mm, 131*mm])]
        story += [Paragraph("3. Pre-consultation Summary", self.section), self._table([[self._p("Item"), self._p("Patient-provided information")], *[[self._p(k.replace("_", " ").title()), self._p(self._list(v))] for k, v in data["pre_consultation"].items()]], [55*mm, 131*mm])]
        score_rows = [[self._p("Assessment"), self._p("Recorded scores")]]
        for number, name in enumerate(("prakriti", "vikriti", "agni"), start=4):
            result = data[name]
            label = "Agni / Digestion" if name == "agni" else name.title()
            summary = result.get("constitution") or result.get("primary_dosha") or result.get("dominant_dosha") or result.get("status") or "REVIEW REQUIRED"
            story += [Paragraph(f"{number}. {label} Assessment", self.section), self._p(summary)]
            score_rows.append([self._p(label), self._p(self._list(data["assessment_scores"].get(name)))])
        story += [Paragraph("7. SYMPTOM-BASED DISEASE SCREENING", self.section), self._p("SCREENING / RESEARCH ONLY — NOT A MEDICAL DIAGNOSIS"), self._p(self._list(data["disease_screening"]))]
        story += [Paragraph("8. Assessment Scoring Summary", self.section), self._table(score_rows, [55*mm, 131*mm])]
        story += [Paragraph("9. Assessment Limitations", self.section), *[self._p(f"- {item}") for item in data["limitations"]], Paragraph("10. AI Assessment Status", self.section), self._p("AI-GENERATED — DOCTOR REVIEW REQUIRED"), Paragraph("11. Safety Disclaimer", self.section), self._p("This preliminary assessment is educational and supportive only. It is not diagnosis, treatment, a prescription, or a substitute for a qualified doctor.")]
        story.insert(0, self._p(f"Report {meta['report_id']} | Version {meta['report_version']} | Created {meta['created_at']}"))
        return self._build(self.output_dir / filename, "AI ASSESSMENT REPORT", "AI_ASSESSMENT_GENERATED", story)

    def generate_final_report(self, state: dict[str, Any], filename: str = "Final_Personalized_Wellness_Report.pdf") -> str:
        workflow = TwoReportWorkflow(state)
        if not workflow.approval_is_current():
            workflow.invalidate_if_changed()
            raise PermissionError("DOCTOR VERIFICATION REQUIRED")
        from src.services.report_workflow import final_content
        data = final_content(state); profile, assessment, doctor = data["patient_profile"], data["assessment"], data["doctor_review_data"]
        story: list[Any] = [Paragraph("DOCTOR APPROVED", self.section), Paragraph("2. Patient Profile", self.section), self._table([[self._p("Field"), self._p("Information")], *[[self._p(k.replace("_", " ").title()), self._p(self._list(profile.get(k)))] for k in ("name", "age", "gender", "height_cm", "weight_kg")]], [55*mm, 131*mm])]
        story += [Paragraph("3. Relevant Pre-consultation Summary", self.section), self._p(self._list({k: profile.get(k) for k in ("goal", "main_complaint", "health_conditions")}))]
        reviewed_rows = [[self._p("Assessment"), self._p("Doctor-reviewed result")]]
        for key, value in assessment.items():
            if isinstance(value, dict):
                value = value.get("constitution") or value.get("dominant_dosha") or value.get("status") or value.get("primary_dosha") or "Not provided"
            reviewed_rows.append([self._p(key.replace("_", " ").title()), self._p(self._list(value))])
        story += [Paragraph("4. Doctor-reviewed Assessment", self.section), self._table(reviewed_rows, [55*mm, 131*mm])]

        diet_payload = data["agent2_diet_data"]; diet = diet_payload.get("diet_plan", diet_payload) if isinstance(diet_payload, dict) else {}
        validation = data["validation"]
        excluded = diet_payload.get("excluded_foods", []) if isinstance(diet_payload, dict) else []
        story += [Paragraph("5. Personalized Nutrition Analysis", self.section), self._p("NUTRITION REVIEW REQUIRED" if validation["warnings"] or validation["failed_checks"] else "Nutrition values were recalculated from displayed Agent 2 food items."), self._p("Full-plan totals: " + self._list(validation.get("nutrition_total"))), self._p("Weekly totals: " + self._list(validation.get("weekly_totals"))), self._p("Target versus actual: " + self._list(validation.get("target_versus_actual"))), Paragraph("6. Food Preferences, Allergies and Restrictions", self.section), self._p(f"Dietary preference: {profile.get('dietary_preference') or 'Not provided'} | Allergies: {self._list(profile.get('allergies'))} | Intolerances: {self._list(profile.get('food_intolerances'))} | Avoided foods: {self._list(profile.get('foods_to_avoid'))} | Doctor restrictions: {self._list(doctor.get('food_restrictions'))}"), Paragraph("7. Foods to Prioritize", self.section), self._p(self._list((diet_payload.get("priority_foods") if isinstance(diet_payload, dict) else None) or "Not provided")), Paragraph("8. Foods to Avoid or Limit", self.section), self._p(self._list(excluded or profile.get("foods_to_avoid") or "Not provided")), Paragraph("9. Personalized Diet Plan from Agent 2", self.section)]
        for day in diet.get("days", []):
            rows = [[self._p("Meal"), self._p("Food / portion"), self._p("Nutrition")]]
            for meal in day.get("meals", []):
                for food in meal.get("foods", []):
                    rows.append([self._p(meal.get("meal")), self._p(f"{food.get('food_name', food.get('name', 'Not provided'))} ({food.get('portion_g', food.get('portion', 'Not provided'))} g)"), self._p(self._list({k: food.get("nutrition", food).get(k, "Not provided") for k in ("calories", "protein_g", "carbs_g", "fat_g", "fiber_g")}))])
            story.extend([Paragraph(f"Day {day.get('day', 'Not provided')}", self.section), self._table(rows, [32*mm, 72*mm, 82*mm])])
        story += [Paragraph("10. Daily Nutrition Summary", self.section), self._table([[self._p("Day"), self._p("Calculated daily nutrition")], *[[self._p(d.get("day")), self._p(self._list(d.get("daily_total")))] for d in diet.get("days", [])]], [25*mm, 161*mm]), Paragraph("11. Personalized Lifestyle and Wellness Advice from Agent 3", self.section)]
        lifestyle = data["agent3_lifestyle_data"].get("recommendations", data["agent3_lifestyle_data"].get("lifestyle_plan", {}).get("recommendations", [])) if isinstance(data["agent3_lifestyle_data"], dict) else []
        if not lifestyle:
            story.append(self._p("Not provided"))
        for item in lifestyle:
            story.append(self._table([[self._p("DOCTOR APPROVED (AI-generated origin)"), self._p(item.get("category"))], [self._p("Recommendation"), self._p(item.get("personalized_recommendation"))], [self._p("Patient-specific reason"), self._p(item.get("patient_specific_reason"))], [self._p("Factors / Ayurvedic basis"), self._p(self._list(item.get("factors_used")) + " | " + self._list({k: v for k, v in (item.get("ayurvedic_basis") or {}).items() if k != "excerpt"}))], [self._p("Safety / wellness basis"), self._p(self._list(item.get("safety_consideration")) + " | " + self._list(item.get("wellness_basis")))]], [55*mm, 131*mm], header=False))
        medicines = doctor.get("medicines") or []
        story += [Paragraph("12. Doctor-approved Wellness Advice", self.section), self._p(doctor.get("wellness_advice")), Paragraph("13. Medicines and Prescriptions", self.section)]
        medicine_rows = [[self._p("Medicine"), self._p("Dosage"), self._p("Frequency"), self._p("Duration"), self._p("Instructions")]] + [[self._p(m.get("name")), self._p(m.get("dosage")), self._p(m.get("frequency")), self._p(m.get("duration")), self._p(self._list(m.get("instructions")) + " | DOCTOR APPROVED")] for m in medicines]
        if not medicines: medicine_rows.append([self._p("Not provided"), self._p("Not provided"), self._p("Not provided"), self._p("Not provided"), self._p("Doctor entry or approval required")])
        story += [self._table(medicine_rows, [32*mm, 28*mm, 29*mm, 28*mm, 69*mm]), Paragraph("14. Follow-up Plan", self.section), self._table([[self._p("Follow-up date"), self._p(doctor.get("follow_up_date"))], [self._p("Instructions / progress monitoring"), self._p(self._list(doctor.get("follow_up_instructions")) + " | Progress monitoring: " + self._list(doctor.get("progress_monitoring")))]], [55*mm, 131*mm], header=False), Paragraph("15. Safety and Fact-check Review", self.section), self._p(self._list((validation.get("failed_checks", []) + validation.get("warnings", [])) or ["PASS"])), Paragraph("16. References / Evidence", self.section), self._p("Source dataset: " + str(state.get("food_dataset_path") or "data/demo_foods.csv")), self._p("Lifestyle references: " + self._list([{k: v for k, v in (item.get("ayurvedic_basis") or {}).items() if k in ("source", "page")} for item in lifestyle])), Paragraph("17. Educational Disclaimer", self.section), self._p("Traditional Ayurvedic wellness education is not a diagnosis, prescription, disease treatment, cure, prevention promise or guarantee. Follow the reviewing doctor instructions and seek qualified care for severe symptoms."), Paragraph("18. Doctor Approval and Signature", self.section), self._table([[self._p("Doctor"), self._p(doctor.get("doctor_name"))], [self._p("Registration / qualification"), self._p(f"{doctor.get('registration_number') or 'Not provided'} / {doctor.get('qualification') or 'Not provided'}")], [self._p("Approval date / sign-off"), self._p(f"{doctor.get('approval_date') or 'Not provided'} / {doctor.get('signature') or 'Not provided'}")]], [55*mm, 131*mm], header=False)]
        story.insert(0, self._p(f"Report {state['final_report_id']} | Session {state['session_id']} | Approved version {doctor['approved_report_version']} | Approval date {doctor['approval_date']}"))
        story += [Paragraph("Doctor Final Comments", self.section), self._p(doctor.get("final_comments")), self._p("Doctor contact: " + self._list(doctor.get("contact_information")))]
        path = self._build(self.output_dir / filename, "FINAL PERSONALIZED WELLNESS REPORT", "DOCTOR APPROVED", story)
        workflow.create_final_report()
        return path
