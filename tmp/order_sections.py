from pathlib import Path
p = Path('src/services/two_report_pdf.py')
s = p.read_text(encoding='utf-8')
start = s.index('        story.append(Paragraph("3. Prakriti,')
end = s.index('        story += [Paragraph("9. Assessment Limitations"', start)
s = s[:start] + '''        score_rows = [[self._p("Assessment"), self._p("Recorded scores")]]
        for number, name in enumerate(("prakriti", "vikriti", "agni"), start=4):
            result = data[name]
            label = "Agni / Digestion" if name == "agni" else name.title()
            summary = result.get("constitution") or result.get("primary_dosha") or result.get("dominant_dosha") or result.get("status") or "REVIEW REQUIRED"
            story += [Paragraph(f"{number}. {label} Assessment", self.section), self._p(summary)]
            score_rows.append([self._p(label), self._p(self._list(data["assessment_scores"].get(name)))])
        story += [Paragraph("7. SYMPTOM-BASED DISEASE SCREENING", self.section), self._p("SCREENING / RESEARCH ONLY — NOT A MEDICAL DIAGNOSIS"), self._p(self._list(data["disease_screening"]))]
        story += [Paragraph("8. Assessment Scoring Summary", self.section), self._table(score_rows, [55*mm, 131*mm])]
''' + s[end:]
s = s.replace('"1. Patient Profile"', '"2. Patient Profile"').replace('"2. Pre-consultation Summary"', '"3. Pre-consultation Summary"')
# Reorder complete section objects, not just their labels.
start = s.index('        story += [Paragraph("4. Food Preferences')
end = s.index('\n        for day in diet.get', start)
block = s[start:end]
prefix = '        story += ['
content = block[len(prefix):-1]
split = content.index('Paragraph("3. Personalized Nutrition Analysis"')
next_section = content.index('Paragraph("5. Foods to Prioritize"')
restriction = content[:split]
nutrition = content[split:next_section]
remaining = content[next_section:]
s = s[:start] + prefix + nutrition + restriction + remaining + ']' + s[end:]
s = s.replace('        for item in lifestyle:\n', '        if not lifestyle:\n            story.append(self._p("Not provided"))\n        for item in lifestyle:\n')
s = s.replace('self._p(m.get("instructions"))] for m in medicines]', 'self._p(self._list(m.get("instructions")) + " | DOCTOR APPROVED")] for m in medicines]')
s = s.replace('self._p("Full-plan totals: " + self._list(validation.get("nutrition_total")))', 'self._p("Full-plan totals: " + self._list(validation.get("nutrition_total"))), self._p("Weekly totals: " + self._list(validation.get("weekly_totals"))), self._p("Target versus actual: " + self._list(validation.get("target_versus_actual")))')
p.write_text(s, encoding='utf-8')
