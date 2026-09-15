from pathlib import Path

p = Path('src/agents/final_response.py')
s = p.read_text(encoding='utf-8')
p.write_text(s[:s.index('    """')], encoding='utf-8')

p = Path('src/services/two_report_pdf.py')
s = p.read_text(encoding='utf-8')
s = s.replace('PRELIMINARY AI ASSESSMENT - NOT DOCTOR APPROVED', 'PRELIMINARY AI ASSESSMENT — NOT DOCTOR APPROVED')
s = s.replace('SCREENING / RESEARCH ONLY - NOT A MEDICAL DIAGNOSIS', 'SCREENING / RESEARCH ONLY — NOT A MEDICAL DIAGNOSIS')
s = s.replace('AI-GENERATED - DOCTOR REVIEW REQUIRED', 'AI-GENERATED — DOCTOR REVIEW REQUIRED')
s = s.replace('result.get("constitution") or result.get("dominant_dosha")', 'result.get("constitution") or result.get("primary_dosha") or result.get("dominant_dosha")')
s = s.replace('self._p(self._list(validation.get("nutrition_total")))', 'self._p("Full-plan totals: " + self._list(validation.get("nutrition_total")))', 1)
s = s.replace('self._p(self._list(validation.get("nutrition_total")))', 'self._table([[self._p("Day"), self._p("Calculated daily nutrition")], *[[self._p(d.get("day")), self._p(self._list(d.get("daily_total")))] for d in diet.get("days", [])]], [25*mm, 161*mm])')
s = s.replace('self._p("AI-GENERATED — DOCTOR REVIEW REQUIRED"), self._p(item.get("category"))', 'self._p("DOCTOR APPROVED (AI-generated origin)"), self._p(item.get("category"))')
s = s.replace('self._p(doctor.get("follow_up_instructions") or doctor.get("progress_monitoring"))', 'self._p(self._list(doctor.get("follow_up_instructions")) + " | Progress monitoring: " + self._list(doctor.get("progress_monitoring")))')
s = s.replace('validation.get("failed_checks") or validation.get("warnings") or ["PASS"]', '(validation.get("failed_checks", []) + validation.get("warnings", [])) or ["PASS"]')
s = s.replace('self._p(self._list(food.get("nutrition", food)))', 'self._p(self._list({k: food.get("nutrition", food).get(k, "Not provided") for k in ("calories", "protein_g", "carbs_g", "fat_g", "fiber_g")}))')
s = s.replace('        path = self._build(', '''        story.insert(0, self._p(f"Session {state['session_id']} | Approved version {doctor['approved_report_version']} | Approval date {doctor['approval_date']}"))
        story += [Paragraph("Doctor Final Comments", self.section), self._p(doctor.get("final_comments"))]
        path = self._build(''')
p.write_text(s, encoding='utf-8')
