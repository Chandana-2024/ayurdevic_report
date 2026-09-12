from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


class VedAmritPDFReport:

    def __init__(self, output_dir="reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        styles = getSampleStyleSheet()
        self.font_name = "Helvetica"
        self._register_hindi_font()

        self.title_style = ParagraphStyle(
            "VedAmritTitle",
            parent=styles["Title"],
            alignment=TA_CENTER,
            fontSize=18,
            leading=22,
            spaceAfter=4,
            fontName=self.font_name,
        )

        self.subtitle_style = ParagraphStyle(
            "VedAmritSubtitle",
            parent=styles["Normal"],
            alignment=TA_CENTER,
            fontSize=9,
            textColor=colors.grey,
            spaceAfter=10,
            fontName=self.font_name,
        )

        self.section_style = ParagraphStyle(
            "Section",
            parent=styles["Heading2"],
            fontSize=12,
            leading=14,
            spaceBefore=10,
            spaceAfter=5,
            fontName=self.font_name,
        )

        self.day_header_style = ParagraphStyle(
            "DayHeader",
            parent=styles["Heading3"],
            fontSize=10,
            leading=12,
            spaceBefore=6,
            spaceAfter=4,
            textColor=colors.HexColor("#1A365D"),
            fontName=self.font_name,
        )

        self.body_style = ParagraphStyle(
            "Body",
            parent=styles["Normal"],
            fontSize=8.5,
            leading=11,
            fontName=self.font_name,
        )

        self.small_style = ParagraphStyle(
            "Small",
            parent=styles["Normal"],
            fontSize=7.5,
            leading=9.5,
            fontName=self.font_name,
        )

    def _register_hindi_font(self) -> None:
        font_path = Path(r"C:\Windows\Fonts\Nirmala.ttc")
        if not font_path.exists():
            return

        try:
            pdfmetrics.registerFont(
                TTFont("Nirmala", str(font_path), subfontIndex=0)
            )
            self.font_name = "Nirmala"
        except (OSError, TypeError, ValueError):
            self.font_name = "Helvetica"

    def _text(self, value: Any, fallback: str = "Not provided") -> str:
        if value is None or str(value).strip() in {"", "N/A", "None"}:
            return fallback
        return escape(str(value))

    def _paragraph(self, value: Any, style=None) -> Paragraph:
        return Paragraph(self._text(value), style or self.body_style)

    def _footer(self, canvas, document) -> None:
        canvas.saveState()
        canvas.setFont(self.font_name, 7)
        canvas.setFillColor(colors.grey)
        canvas.drawString(12 * mm, 7 * mm, "VedAmrit | Doctor Verification Required")
        canvas.drawRightString(
            A4[0] - 12 * mm,
            7 * mm,
            f"Page {document.page}",
        )
        canvas.restoreState()

    def generate(self, state: dict[str, Any], filename: str = "VedAmrit_Wellness_Report.pdf") -> str:
        output_path = self.output_dir / filename

        document = SimpleDocTemplate(
            str(output_path),
            pagesize=A4,
            rightMargin=12 * mm,
            leftMargin=12 * mm,
            topMargin=10 * mm,
            bottomMargin=10 * mm,
        )

        story = []

        # ==================================================
        # HEADER
        # ==================================================
        story.append(Paragraph("VedAmrit", self.title_style))
        story.append(
            Paragraph("Personalized Ayurvedic Wellness Report", self.subtitle_style)
        )

        # ==================================================
        # 1. PATIENT PROFILE
        # ==================================================
        story.append(Paragraph("1. PATIENT PROFILE", self.section_style))

        profile = state.get("patient_profile") or state.get("user_input") or {}

        allergies_val = profile.get("allergies", [])
        if isinstance(allergies_val, list):
            allergies_str = ", ".join(map(str, allergies_val)) if allergies_val else "Not provided"
        else:
            allergies_str = str(allergies_val) if allergies_val else "Not provided"

        foods_avoid_val = profile.get("foods_to_avoid", [])
        if isinstance(foods_avoid_val, list):
            foods_avoid_str = ", ".join(map(str, foods_avoid_val)) if foods_avoid_val else "Not provided"
        else:
            foods_avoid_str = str(foods_avoid_val) if foods_avoid_val else "Not provided"

        conditions_val = profile.get("health_conditions", [])
        if isinstance(conditions_val, list):
            conditions_str = ", ".join(map(str, conditions_val)) if conditions_val else "Not provided"
        else:
            conditions_str = str(conditions_val) if conditions_val else "Not provided"

        profile_table_data = [
            [
                Paragraph("<b>Name</b>", self.body_style),
                str(profile.get("name") or "Not provided"),
                Paragraph("<b>Age</b>", self.body_style),
                str(profile.get("age") or "Not provided"),
            ],
            [
                Paragraph("<b>Gender</b>", self.body_style),
                str(profile.get("gender") or "Not provided"),
                Paragraph("<b>Blood Group</b>", self.body_style),
                str(profile.get("blood_group") or "Not provided"),
            ],
            [
                Paragraph("<b>Height</b>", self.body_style),
                f"{profile.get('height_cm') or 'Not provided'} cm",
                Paragraph("<b>Weight</b>", self.body_style),
                f"{profile.get('weight_kg') or 'Not provided'} kg",
            ],
            [
                Paragraph("<b>Dietary Preference</b>", self.body_style),
                str(profile.get("dietary_preference") or "Not provided"),
                Paragraph("<b>Goal</b>", self.body_style),
                str(profile.get("goal") or "Not provided"),
            ],
            [
                Paragraph("<b>Allergies</b>", self.body_style),
                allergies_str,
                Paragraph("<b>Foods to Avoid</b>", self.body_style),
                foods_avoid_str,
            ],
            [
                Paragraph("<b>Health Conditions</b>", self.body_style),
                conditions_str,
                "",
                "",
            ],
            [
                Paragraph("<b>Patient ID</b>", self.body_style),
                str(profile.get("patient_id") or "Not provided"),
                Paragraph("<b>Appointment Date</b>", self.body_style),
                str(profile.get("appointment_date") or "Not provided"),
            ],
            [
                Paragraph("<b>Doctor</b>", self.body_style),
                str(profile.get("doctor_name") or "Not provided"),
                Paragraph("<b>Contact</b>", self.body_style),
                str(profile.get("contact") or "Not provided"),
            ],
        ]

        profile_table = Table(
            profile_table_data,
            colWidths=[35 * mm, 58 * mm, 35 * mm, 58 * mm],
        )
        profile_table.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("FONTSIZE", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 3),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                    ("SPAN", (1, 5), (3, 5)),
                ]
            )
        )
        story.append(profile_table)
        story.append(Paragraph("Reason for Appointment", self.day_header_style))
        story.append(Paragraph("Main complaint, concern, duration, frequency, severity, triggers, and previous treatment: Not provided", self.body_style))
        story.append(Paragraph("Symptoms Summary", self.day_header_style))
        story.append(Paragraph("No structured symptom details were collected in the pre-consultation form.", self.body_style))
        story.append(Paragraph("Allergy and Food Restriction Summary", self.day_header_style))
        story.append(Paragraph(f"Food allergies: {allergies_str} | Medicine allergies: Not provided | Food intolerance: Not provided | Foods avoided: {foods_avoid_str} | Personal preference: {profile.get('dietary_preference') or 'Not provided'}", self.body_style))

        # ==================================================
        # 2. AGENT 1 - AYURVEDIC ASSESSMENT
        # ==================================================
        story.append(Paragraph("2. PRELIMINARY AI-BASED ASSESSMENT", self.section_style))
        story.append(Paragraph("Doctor Verification Required", self.body_style))

        prakriti = state.get("prakriti_result") or {}
        vikriti = state.get("vikriti_result") or {}
        agni = state.get("agni_result") or {}

        p_scores = prakriti.get("scores", {})
        p_scores_str = f"Vata: {p_scores.get('Vata', 0)}, Pitta: {p_scores.get('Pitta', 0)}, Kapha: {p_scores.get('Kapha', 0)}"

        v_scores = vikriti.get("scores", {})
        v_scores_str = f"Vata: {v_scores.get('Vata', 0)}, Pitta: {v_scores.get('Pitta', 0)}, Kapha: {v_scores.get('Kapha', 0)}"

        agni_cat_scores = agni.get("category_scores", {})
        agni_scores_str = ", ".join(f"{k}: {v}" for k, v in agni_cat_scores.items()) if agni_cat_scores else "N/A"

        constitution_str = str(prakriti.get("constitution", state.get("constitution", "N/A")))
        primary_dosha_str = str(prakriti.get("primary_dosha", "N/A"))
        secondary_dosha_str = str(prakriti.get("secondary_dosha", "N/A"))
        prakriti_details = f"Constitution: {constitution_str} | Primary: {primary_dosha_str}"
        if secondary_dosha_str and secondary_dosha_str != "None":
            prakriti_details += f" | Secondary: {secondary_dosha_str}"

        dominant_vikriti = vikriti.get("dominant_dosha") or vikriti.get("dominant") or "N/A"

        assessment_table = Table(
            [
                [Paragraph("<b>Assessment</b>", self.body_style), Paragraph("<b>Result</b>", self.body_style), Paragraph("<b>Scores</b>", self.body_style)],
                [Paragraph("<b>Prakriti</b>", self.body_style), prakriti_details, p_scores_str],
                [Paragraph("<b>Vikriti</b>", self.body_style), f"Dominant {dominant_vikriti}", v_scores_str],
                [Paragraph("<b>Agni</b>", self.body_style), str(agni.get("status", "N/A")), agni_scores_str],
            ],
            colWidths=[28 * mm, 78 * mm, 80 * mm],
        )
        assessment_table.setStyle(
            TableStyle(
                [
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                    ("FONTSIZE", (0, 0), (-1, -1), 8),
                    ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ]
            )
        )
        story.append(assessment_table)

        # ==================================================
        # 3. AGENT 2 - PERSONALIZED DIET PLAN (MAIN SECTION)
        # ==================================================
        story.append(Paragraph("3. PERSONALIZED DIET PLAN — AGENT 2", self.section_style))

        diet = (
            state.get("meal_plan")
            or state.get("diet_plan")
            or (state.get("agent2_output") or {}).get("diet_plan")
            or {}
        )

        duration_days = diet.get("duration_days", state.get("plan_days", 1))
        daily_target = diet.get("daily_target", {})
        target_cals = daily_target.get("calories", "N/A")
        target_p = daily_target.get("protein_g", "N/A")
        target_c = daily_target.get("carbs_g", "N/A")
        target_f = daily_target.get("fat_g", "N/A")
        target_fiber = daily_target.get("fiber_g", "N/A")

        target_summary_text = (
            f"<b>Plan Duration:</b> {duration_days} Day(s) | "
            f"<b>Daily Calorie Target:</b> {target_cals} kcal | "
            f"<b>Target macros:</b> Protein: {target_p}g, Carbs: {target_c}g, "
            f"Fat: {target_f}g, Fibre: {target_fiber}g"
        )
        story.append(Paragraph(target_summary_text, self.body_style))
        story.append(Paragraph("Actual totals below are calculated from the displayed portions.", self.small_style))
        story.append(Spacer(1, 3))

        days = diet.get("days", [])

        if days:
            for day in days:
                day_num = day.get("day", 1)
                story.append(Paragraph(f"<b>DAY {day_num}</b>", self.day_header_style))

                diet_rows = [
                    [
                        Paragraph("<b>Meal</b>", self.small_style),
                        Paragraph("<b>Foods &amp; Portions</b>", self.small_style),
                        Paragraph("<b>Nutrition</b>", self.small_style),
                    ]
                ]

                for meal in day.get("meals", []):
                    meal_name = str(meal.get("meal") or meal.get("type") or "Meal")

                    food_text = []
                    for food in meal.get("foods", []):
                        food_name = food.get("food_name") or food.get("name") or "Food"
                        portion = food.get("portion_g") or food.get("portion") or ""
                        portion_str = f" ({portion}g)" if portion else ""
                        food_text.append(f"{food_name}{portion_str}")

                    meal_total = meal.get("meal_total", {})
                    cals = meal_total.get("calories", meal.get("actual_calories", 0))
                    p = meal_total.get("protein_g", 0)
                    c = meal_total.get("carbs_g", 0)
                    f = meal_total.get("fat_g", 0)

                    fiber = meal_total.get("fiber_g", 0)
                    nutrition_str = f"{cals} kcal | P: {p}g | C: {c}g | F: {f}g | Fibre: {fiber}g"

                    diet_rows.append(
                        [
                            meal_name,
                            ", ".join(food_text) if food_text else "N/A",
                            nutrition_str,
                        ]
                    )

                daily_total = day.get("daily_total", {})
                d_cals = daily_total.get("calories", 0)
                d_p = daily_total.get("protein_g", 0)
                d_c = daily_total.get("carbs_g", 0)
                d_f = daily_total.get("fat_g", 0)
                d_fiber = daily_total.get("fiber_g", 0)

                diet_rows.append(
                    [
                        Paragraph("<b>Daily Total</b>", self.small_style),
                        "",
                        Paragraph(f"<b>{d_cals} kcal | P: {d_p}g | C: {d_c}g | F: {d_f}g | Fibre: {d_fiber}g</b>", self.small_style),
                    ]
                )

                day_table = Table(
                    diet_rows,
                    colWidths=[28 * mm, 98 * mm, 60 * mm],
                )
                day_table.setStyle(
                    TableStyle(
                        [
                            ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                            ("FONTSIZE", (0, 0), (-1, -1), 7.5),
                            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                            ("TOPPADDING", (0, 0), (-1, -1), 2.5),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                            ("LINEABOVE", (0, -1), (-1, -1), 1, colors.black),
                        ]
                    )
                )
                story.append(day_table)
                story.append(Spacer(1, 3))
        else:
            story.append(Paragraph("No detailed meal plan records available.", self.body_style))

        if days:
            summary_cals = sum(float(day.get("daily_total", {}).get("calories", 0) or 0) for day in days)
            summary_protein = sum(float(day.get("daily_total", {}).get("protein_g", 0) or 0) for day in days)
            summary_carbs = sum(float(day.get("daily_total", {}).get("carbs_g", 0) or 0) for day in days)
            summary_fat = sum(float(day.get("daily_total", {}).get("fat_g", 0) or 0) for day in days)
            summary_fiber = sum(float(day.get("daily_total", {}).get("fiber_g", 0) or 0) for day in days)
            story.append(Paragraph("Plan Summary - Actual Displayed Meal Totals", self.day_header_style))
            story.append(Paragraph(
                f"{len(days)} day(s): {summary_cals:.1f} kcal | Protein: {summary_protein:.1f}g | Carbohydrates: {summary_carbs:.1f}g | Fat: {summary_fat:.1f}g | Fibre: {summary_fiber:.1f}g",
                self.body_style,
            ))

        story.append(Paragraph("AI Draft Diet Plan - Doctor Review Required", self.section_style))
        story.append(Paragraph(
            "This meal plan is an AI-generated draft. A doctor must review portions, restrictions, and suitability before approval.",
            self.body_style,
        ))

        # ==================================================
        # 4. AGENT 3 - LIFESTYLE & WELLNESS
        # ==================================================
        story.append(
            Paragraph("4. LIFESTYLE AND WELLNESS ASSISTANT - AI DRAFT", self.section_style)
        )

        lifestyle_data = state.get("lifestyle_plan") or {}
        lifestyle_categories = (
            lifestyle_data.get("lifestyle_plan")
            if isinstance(lifestyle_data.get("lifestyle_plan"), dict)
            else lifestyle_data
        )

        if isinstance(lifestyle_categories, dict) and lifestyle_categories:
            for category, items in lifestyle_categories.items():
                if category in {"primary_dosha", "secondary_dosha", "dominant_vikriti", "agni_status", "personalization_factors", "sources", "rag_evidence_count"}:
                    continue
                if not isinstance(items, list) or not items:
                    continue

                cat_title = category.replace("_", " ").title()
                story.append(Paragraph(f"<b>{cat_title}</b>", self.body_style))

                for item in items:
                    clean_item = str(item).strip()
                    story.append(Paragraph(f"&bull; {clean_item}", self.small_style))
                story.append(Spacer(1, 2))
        else:
            story.append(
                Paragraph("Standard daily routine and wellness guidelines apply.", self.body_style)
            )

        story.append(Paragraph("5. DOCTOR CONSULTATION AND EDITS", self.section_style))
        doctor_rows = [
            [Paragraph("<b>Field</b>", self.body_style), Paragraph("<b>Doctor entry</b>", self.body_style)],
            ["Doctor observations", "Not provided"],
            ["Doctor-confirmed symptoms", "Not provided"],
            ["Doctor-confirmed Prakriti / Vikriti / Agni", "Not provided"],
            ["Doctor assessment and diagnosis", "Not provided"],
            ["Doctor comments", "Not provided"],
        ]
        doctor_table = Table(doctor_rows, colWidths=[65 * mm, 121 * mm])
        doctor_table.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        story.append(doctor_table)

        story.append(Paragraph("6. DOCTOR WELLNESS ADVICE", self.section_style))
        story.append(Paragraph("Doctor-entered or doctor-approved advice: Not provided", self.body_style))

        story.append(Paragraph("7. MEDICINES AND PRESCRIPTIONS", self.section_style))
        medicine_table = Table([
            [Paragraph("<b>Medicine</b>", self.small_style), Paragraph("<b>Dosage</b>", self.small_style), Paragraph("<b>Frequency</b>", self.small_style), Paragraph("<b>Duration</b>", self.small_style), Paragraph("<b>Instructions</b>", self.small_style)],
            ["Not provided", "Not provided", "Not provided", "Not provided", "Doctor entry required"],
        ], colWidths=[38 * mm, 30 * mm, 35 * mm, 30 * mm, 53 * mm])
        medicine_table.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("FONTSIZE", (0, 0), (-1, -1), 7.5),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        story.append(medicine_table)
        story.append(Paragraph("AI must not independently prescribe medicines. Any prescription must be doctor-entered or doctor-approved.", self.small_style))

        story.append(Paragraph("8. FOLLOW-UP AND FINAL APPROVAL", self.section_style))
        approval_rows = [
            ["Report status", "Draft - Under Doctor Review"],
            ["Follow-up date", "Not provided"],
            ["Progress and symptoms to monitor", "Not provided"],
            ["Doctor name / registration number", "Not provided"],
            ["Approval date", "Not provided"],
            ["Doctor signature", "____________________________"],
        ]
        approval_table = Table(approval_rows, colWidths=[65 * mm, 121 * mm])
        approval_table.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        story.append(approval_table)

        # ==================================================
        # 5. DISEASE SCREENING (OPTIONAL)
        # ==================================================
        disease_res = (
            state.get("disease_screening_result")
            or state.get("disease_screening")
        )

        if disease_res:
            screening = (
                disease_res.get("screening_result")
                if isinstance(disease_res, dict) and "screening_result" in disease_res
                else disease_res
            )

            story.append(
                Paragraph("9. SYMPTOM-BASED DISEASE SCREENING", self.section_style)
            )

            predicted = screening.get("predicted_condition", "N/A")
            conf = screening.get("model_probability") or screening.get("confidence")

            if conf is not None:
                try:
                    conf_str = f"{float(conf) * 100:.1f}%"
                except (ValueError, TypeError):
                    conf_str = str(conf)
            else:
                conf_str = "N/A"

            story.append(
                Paragraph(f"<b>Screening Prediction:</b> {predicted}", self.body_style)
            )
            story.append(
                Paragraph(f"<b>Model Probability:</b> {conf_str}", self.body_style)
            )
            story.append(
                Paragraph("<b>Status:</b> Screening / Research Only (Not a medical diagnosis)", self.body_style)
            )
            story.append(
                Paragraph(
                    "<b>Notice:</b> This symptom pattern screening is an exploratory ML model and does not constitute a diagnostic confirmation.",
                    self.small_style,
                )
            )
        else:
            story.append(
                Paragraph("9. SYMPTOM-BASED DISEASE SCREENING", self.section_style)
            )
            story.append(
                Paragraph("Disease screening was not requested for this session.", self.body_style)
            )

        # ==================================================
        # 6. SAFETY & FACT-CHECK
        # ==================================================
        story.append(Paragraph("10. SAFETY & FACT-CHECK REVIEW", self.section_style))

        safety = (
            state.get("validation_result")
            or (state.get("agent2_output") or {}).get("validation")
            or state.get("safety_result")
            or {}
        )

        overall_status = safety.get("overall_status") or safety.get("status") or "PASS"
        story.append(
            Paragraph(f"<b>Overall Safety Status:</b> {overall_status}", self.body_style)
        )

        checks = safety.get("checks", {})
        if checks:
            checks_str = " | ".join(f"{k}: {v}" for k, v in checks.items())
            story.append(Paragraph(f"<b>System Checks:</b> {checks_str}", self.small_style))

        warnings = safety.get("warnings", [])
        if warnings:
            for w in warnings:
                story.append(Paragraph(f"<b>Warning:</b> {w}", self.small_style))

        # ==================================================
        # 7. REFERENCES & SOURCES
        # ==================================================
        story.append(Paragraph("11. REFERENCES & EVIDENCE", self.section_style))

        references = [
            "Prakriti & Vikriti Assessment: Deterministic 21-question clinical scoring model",
            "Agni Assessment: Singh A, Singh G, Patwardhan K, Gehlot S. (2017) Validated Agnibala Tool",
            "Energy & Nutrition Target: Mifflin MD et al. (1990) Predictive REE equation",
            "Ayurvedic Food & Lifestyle: Classical Dravyaguna Reference & Ayurvedic Knowledge Base",
        ]

        if disease_res:
            references.append(
                "Disease Screening: AYUCARE symptom-based Decision Tree model (Research screening only)"
            )

        for ref in references:
            story.append(Paragraph(f"&bull; {ref}", self.small_style))

        # ==================================================
        # FOOTER / NOTICE
        # ==================================================
        story.append(Spacer(1, 6))
        story.append(
            Paragraph(
                "<b>IMPORTANT NOTICE:</b> This is an AI-assisted wellness and diet-planning draft. "
                "It does not replace diagnosis, clinical advice, or treatment by a qualified medical or Ayurvedic healthcare practitioner.",
                self.small_style,
            )
        )

        document.build(
            story,
            onFirstPage=self._footer,
            onLaterPages=self._footer,
        )
        return str(output_path)



AyurGenixPDFReport = VedAmritPDFReport