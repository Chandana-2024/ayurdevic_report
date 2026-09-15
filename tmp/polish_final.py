from pathlib import Path
p = Path('src/services/two_report_pdf.py')
s = p.read_text(encoding='utf-8')
start = s.index('        story: list[Any] = [Paragraph("DOCTOR APPROVED"')
end = s.index('\n        diet_payload =', start)
s = s[:start] + '''        story: list[Any] = [Paragraph("DOCTOR APPROVED", self.section), Paragraph("2. Patient Profile", self.section), self._table([[self._p("Field"), self._p("Information")], *[[self._p(k.replace("_", " ").title()), self._p(self._list(profile.get(k)))] for k in ("name", "age", "gender", "height_cm", "weight_kg")]], [55*mm, 131*mm])]
        story += [Paragraph("3. Relevant Pre-consultation Summary", self.section), self._p(self._list({k: profile.get(k) for k in ("goal", "main_complaint", "health_conditions")}))]
        reviewed_rows = [[self._p("Assessment"), self._p("Doctor-reviewed result")]]
        for key, value in assessment.items():
            if isinstance(value, dict):
                value = value.get("constitution") or value.get("dominant_dosha") or value.get("status") or value.get("primary_dosha") or "Not provided"
            reviewed_rows.append([self._p(key.replace("_", " ").title()), self._p(self._list(value))])
        story += [Paragraph("4. Doctor-reviewed Assessment", self.section), self._table(reviewed_rows, [55*mm, 131*mm])]
''' + s[end:]
# Existing section numbers follow the complete 18-section specification (header is 1).
for old, new in [(16,18),(15,17),(14,16),(13,15),(12,14),(11,13),(10,12),(9,11),(8,10),(7,9),(6,8),(5,7)]:
    # Only final-builder suffix, preserving assessment headings.
    marker = s.index('    def generate_final_report')
    s = s[:marker] + s[marker:].replace(f'Paragraph("{old}. ', f'Paragraph("{new}. ')
# These two now precede the shifted sections.
s = s.replace('Paragraph("3. Personalized Nutrition Analysis"', 'Paragraph("5. Personalized Nutrition Analysis"')
s = s.replace('Paragraph("4. Food Preferences, Allergies and Restrictions"', 'Paragraph("6. Food Preferences, Allergies and Restrictions"')
s = s.replace('self._list(item.get("ayurvedic_basis"))', 'self._list({k: v for k, v in (item.get("ayurvedic_basis") or {}).items() if k != "excerpt"})')
s = s.replace('self._p("Agent 2 nutrition data, recorded questionnaire scoring, and traceable Agent 3 Lifestyle RAG references are educational support. This report does not replace medical care.")', 'self._p("Source dataset: " + str(state.get("food_dataset_path") or "data/demo_foods.csv")), self._p("Lifestyle references: " + self._list([{k: v for k, v in (item.get("ayurvedic_basis") or {}).items() if k in ("source", "page")} for item in lifestyle]))')
p.write_text(s, encoding='utf-8')

p = Path('src/agents/lifestyle.py')
s = p.read_text(encoding='utf-8').replace('"Conservative routine guidance; it is not medical treatment."', '"Not provided: no independently verified wellness source supplied."')
s = s.replace('AI-GENERATED - DOCTOR REVIEW REQUIRED', 'AI-GENERATED — DOCTOR REVIEW REQUIRED')
p.write_text(s, encoding='utf-8')
p = Path('tests/test_lifestyle_personalization.py')
s = p.read_text(encoding='utf-8').replace('AI-GENERATED - DOCTOR REVIEW REQUIRED', 'AI-GENERATED — DOCTOR REVIEW REQUIRED')
p.write_text(s, encoding='utf-8')
for p in Path('docs').glob('*.md'):
    s = p.read_text(encoding='utf-8')
    for old, new in [('AI-GENERATED - DOCTOR REVIEW REQUIRED', 'AI-GENERATED — DOCTOR REVIEW REQUIRED'), ('PRELIMINARY AI ASSESSMENT - NOT DOCTOR APPROVED', 'PRELIMINARY AI ASSESSMENT — NOT DOCTOR APPROVED'), ('SCREENING / RESEARCH ONLY - NOT A MEDICAL DIAGNOSIS', 'SCREENING / RESEARCH ONLY — NOT A MEDICAL DIAGNOSIS')]:
        s = s.replace(old, new)
    p.write_text(s, encoding='utf-8')
