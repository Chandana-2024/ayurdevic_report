Antigravity Prompt — Implement the Complete No-Duplicate VedAmrit Patient Question and Two-Report Workflow

# Antigravity Prompt — Implement the Complete No-Duplicate VedAmrit Patient Question and Two-Report Workflow

Act as a senior full-stack developer, AI multi-agent architect, UX designer, Ayurvedic wellness workflow specialist, RAG engineer, data-model architect, and PDF-reporting expert.

Update the existing VedAmrit project so that the patient completes one simple, user-friendly profile and assessment flow. The system must store the answers once and reuse the same information across Agent 1, Agent 2, Agent 3, validation services, reports, and the doctor dashboard.

Use the uploaded VedAmrit PDF as the style reference and the uploaded Lifestyle RAG document as the knowledge source for Agent 3.

---

# MOST IMPORTANT RULES

## 1. Do not change Agent 2

Agent 2 is already working correctly and generates the personalized diet.

Do not:

* Rewrite Agent 2.

* Redesign Agent 2.

* Replace Agent 2.

* Merge Agent 2 with Agent 3.

* Change Agent 2’s personalization logic.

* Change Agent 2’s scoring or nutrition logic.

* Break Agent 2’s current output.

* Create another diet-generation engine inside Agent 3.

Only connect the shared patient state and Agent 1 context to Agent 2 through a safe adapter if necessary.

The final implementation report must clearly confirm:

> Agent 2 was not modified. Its existing personalized diet functionality was preserved.

---

## 2. Agent 3 is the Lifestyle RAG Agent

Agent 3 must be responsible for personalized lifestyle-balance recommendations only.

Agent 3 must use:

* Shared patient profile.

* Health goal.

* Symptoms.

* Prakriti.

* Vikriti.

* Agni.

* Sleep.

* Stress.

* Activity.

* Meal timings.

* Digestion details.

* Dietary preference.

* Allergies.

* Food intolerances.

* Food restrictions.

* Health conditions.

* Medication restrictions.

* Relevant Agent 1 assessment.

* Relevant Agent 2 diet context.

* Lifestyle RAG knowledge base.

Agent 3 must generate personalized recommendations for:

* Daily routine.

* Sleep.

* Stress management.

* Physical activity.

* Meal timing.

* Digestion support.

* Rest and recovery.

* Wellness balance.

* Practical daily habits.

Do not allow Agent 3 to return only generic advice such as:

* Sleep well.

* Exercise regularly.

* Drink water.

* Avoid stress.

* Eat healthy food.

Every major recommendation must include:

1. Recommendation.

2. Patient-specific reason.

3. Patient data or assessment factor used.

4. Ayurvedic basis where supported.

5. Safety consideration.

6. Doctor-review status.

Agent 3 must not:

* Diagnose diseases.

* Prescribe medicines.

* Change medicines.

* Recommend unsupported treatment.

* Promise a cure.

* Make guaranteed medical claims.

* Generate a competing diet plan.

* Ignore allergies or restrictions.

---

# SERVICE SELECTION

At the beginning, the user must select one service:

## Service 1 — Assessment Only

The user receives the preliminary assessment workflow.

For this service:

* Collect the common patient profile.

* Collect the 21 Prakriti questions.

* Collect the 21 Vikriti questions.

* Collect the 11 Agni questions.

* Run Agent 1.

* Generate Report 1.

* Send Report 1 to the doctor dashboard.

* Allow the doctor to approve, reject, or provide feedback.

* Send doctor feedback to the user where appropriate.

* Agent 2 is not required.

* Agent 3 is not required.

* Report 2 is not required.

## Service 2 — Complete Personalized Wellness

For this service:

* Collect the same common patient profile.

* Collect the 21 Prakriti questions.

* Collect the 21 Vikriti questions.

* Collect the 11 Agni questions.

* Run Agent 1.

* Generate Report 1.

* Send Agent 1 output to Agent 2.

* Send Agent 1 output and relevant context to Agent 3.

* Run safety validation.

* Run disease-screening validation.

* Run restriction validation.

* Run nutrition validation.

* Generate Report 2 data.

* Send the complete case to the doctor.

* Require one final doctor decision.

* Generate Report 2 only after explicit doctor approval.

Do not ask the patient to complete different forms for Assessment Only and Complete Personalized Wellness. Use one shared profile and conditionally activate the required agents.

---

# ONE COMMON PATIENT FORM

The patient must complete one common profile form only once.

Do not ask the same information again in another agent, report, or doctor form.

Use clear, simple, user-friendly wording.

Avoid unnecessary questions.

Remove the standalone “current season” question. Do not ask the patient for season unless a specific feature genuinely requires it and the information cannot be safely inferred or handled without asking.

The common form must include only the following necessary information.

---

# FINAL PATIENT QUESTION STRUCTURE

## Section A — Personal Details

1. What is your full name?

2. What is your age?

3. What is your gender?

   * Male

   * Female

   * Other

   * Prefer not to say

4. What is your blood group?

   * Optional

   * Prefer not to say

5. What is your height in centimetres?

6. What is your weight in kilograms?

Do not ask for the same personal details again in Agent 1, Agent 2, Agent 3, reports, or the doctor dashboard.

---

## Section B — Health Goal and Food Preferences

7. What is your main health or wellness goal?

Use selectable options plus “Other”:

* General wellness.

* Better digestion.

* Better sleep.

* Stress management.

* Healthy weight management.

* Improved energy.

* Better daily routine.

* Support for an existing health concern.

* Other.

8. What type of diet do you follow?

* Vegetarian.

* Vegan.

* Non-vegetarian.

* Eggetarian.

* Other.

* Not sure.

9. Are there any foods you prefer not to eat?

* Yes — enter food names and reason.

* No.

10. Are there any foods you particularly like or dislike?

* Optional free-text field.

Do not separately ask the same preference information inside Agent 2.

---

## Section C — Allergies, Intolerances, and Restrictions

11. Do you have any food allergies?

* No.

* Yes — enter food names and reactions.

* Not sure.

12. Do you have any food intolerances or foods that cause discomfort?

* No.

* Yes — enter food names and symptoms.

* Not sure.

13. Do you follow any special or significant dietary restrictions?

* No.

* Yes — explain.

* Not sure.

14. Are you allergic to any medicines?

* No.

* Yes — enter medicine names and reactions.

* Not sure.

* Prefer not to say.

15. Are you currently taking medicines or following any medical dietary restrictions?

* No.

* Yes — provide details.

* Not sure.

16. Is pregnancy, breastfeeding, or pregnancy planning relevant to your current health situation?

* No.

* Yes — provide details.

* Not sure.

* Prefer not to say.

Do not ask these questions again in Agent 2, Agent 3, validation, or the doctor workflow.

The doctor may review or edit the stored information, but the doctor should not be asked to re-enter the same patient answers.

---

## Section D — Health Conditions and Symptoms

17. Do you currently have any diagnosed or ongoing health conditions?

* No.

* Yes — enter the condition and relevant details.

* Not sure.

* Prefer not to say.

18. Are you currently experiencing any symptoms, discomfort, or health complaints?

* No.

* Yes.

* Not sure.

If the answer is “Yes,” show the following follow-up fields:

19. What is your main symptom or complaint?

20. How long have you experienced it?

21. How often does it occur?

22. How severe is it?

* Mild.

* Moderate.

* Severe.

* Not sure.

23. What makes it better or worse?

24. Have you received previous treatment for this complaint?

* No.

* Yes — provide details.

* Not sure.

Do not ask the same symptom questions again in the optional screening section if the patient has already provided the information.

Reuse the stored symptom data for disease screening.

---

## Section E — Lifestyle Information

25. How active are you on a typical day?

* Mostly sitting.

* Lightly active.

* Moderately active.

* Very active.

* Not sure.

26. How would you describe your usual sleep?

* Very poor.

* Poor.

* Average.

* Good.

* Very good.

* Irregular.

27. How would you describe your usual stress level?

* Low.

* Moderate.

* High.

* Very high.

* Not sure.

28. What are your usual meal timings?

* Regular.

* Irregular.

* Early meals.

* Late meals.

* Varies daily.

29. How would you describe your usual appetite?

* Low.

* Normal.

* Strong.

* Variable.

* Not sure.

30. How would you describe your digestion?

* Comfortable.

* Slow.

* Irregular.

* Sensitive.

* Heavy after meals.

* Bloating or gas.

* Acidity or burning.

* Other.

* Not sure.

31. How are your usual bowel movements?

* Regular and comfortable.

* Constipation.

* Loose stools.

* Irregular.

* Other.

* Prefer not to say.

These answers must be reused by Agent 1, Agent 3, safety validation, and the doctor dashboard.

---

# AYURVEDIC ASSESSMENT QUESTIONS

After the common profile is completed, display the Ayurvedic assessment sections.

## Section F — Prakriti Assessment

Display exactly 21 Prakriti questions.

Use the existing approved Prakriti question content and scoring logic from the project.

Do not rewrite or invent the existing questions unless a confirmed bug exists.

Each question must:

* Have clear answer options.

* Use simple language.

* Explain difficult terms where needed.

* Save the answer immediately in the shared patient state.

* Be shown only once.

* Be linked to a stable question ID.

* Be included in the assessment scoring object.

Use question IDs such as:

* `prakriti_01`

* `prakriti_02`

* through

* `prakriti_21`

## Section G — Vikriti Assessment

Display exactly 21 Vikriti questions.

Use the existing approved Vikriti question content and scoring logic from the project.

Do not rewrite or invent the existing questions unless a confirmed bug exists.

Use stable IDs:

* `vikriti_01`

* `vikriti_02`

* through

* `vikriti_21`

## Section H — Agni Assessment

Display exactly 11 Agni questions.

Use the existing approved Agni question content and scoring logic from the project.

Do not rewrite or invent the existing questions unless a confirmed bug exists.

Use stable IDs:

* `agni_01`

* `agni_02`

* through

* `agni_11`

---

# USER-FRIENDLY FORM EXPERIENCE

Make the form simple and easy to complete.

Requirements:

* Use clear section headings.

* Use one question at a time or a small group of related questions.

* Show progress.

* Show which section the patient is completing.

* Use radio buttons, checkboxes, dropdowns, and text fields appropriately.

* Use plain English.

* Explain why sensitive questions may be relevant.

* Make optional fields clearly optional.

* Do not force the user to answer unnecessary questions.

* Allow the user to go back and edit answers.

* Save progress safely.

* Prevent accidental loss of answers.

* Show a review screen before submission.

* Allow the user to edit answers before final submission.

* Do not ask the same question in multiple screens.

* Do not use different wording for the same underlying field.

* Use one canonical field for each data item.

* Use “Not sure” or “Not provided” where appropriate.

* Never assume that an empty field means “No.”

---

# SHARED PATIENT STATE

Create or use one canonical structured patient state.

The shared state must contain:

* Patient ID.

* Session ID.

* Selected service.

* Personal details.

* Health goal.

* Dietary preference.

* Food preferences.

* Food allergies.

* Food intolerances.

* Foods avoided.

* Dietary restrictions.

* Health conditions.

* Symptoms.

* Symptom details.

* Medicine allergies.

* Current medicines.

* Medication restrictions.

* Pregnancy-related information where applicable.

* Activity level.

* Sleep.

* Stress.

* Meal timings.

* Appetite.

* Digestion.

* Bowel movement information.

* Prakriti answers.

* Vikriti answers.

* Agni answers.

* Agent 1 output.

* Agent 2 output reference.

* Agent 3 output.

* Validation results.

* Doctor review data.

* Report 1 metadata.

* Report 2 metadata where applicable.

* Status.

* Version.

* Audit history.

All agents, validators, reports, and the doctor dashboard must read from this shared state.

Do not create separate duplicate patient forms or duplicate patient objects for each agent.

---

# AGENT FLOW

## For Assessment Only

Use this exact flow:

Patient Form
→ Prakriti/Vikriti/Agni Questions
→ Shared Patient State
→ Agent 1
→ Report 1
→ Doctor Dashboard
→ Doctor Approve / Reject / Feedback
→ Feedback Returned to User

Do not run Agent 2, Agent 3, or Report 2 for Assessment Only.

## For Complete Personalized Wellness

Use this exact flow:

Patient Form
→ Prakriti/Vikriti/Agni Questions
→ Shared Patient State
→ Agent 1
→ Report 1
→ Agent 2 Existing Personalized Diet Agent
→ Agent 3 Personalized Lifestyle RAG Agent
→ Disease Screening
→ Safety Validation
→ Restriction Validation
→ Nutrition Validation
→ Report 2 Draft Data
→ Doctor Dashboard
→ Doctor Review and Editing
→ One Final Doctor Decision
→ Report 2 After Approval
→ Patient Delivery

Report 1 must be generated without waiting for doctor approval.

Report 1 may be viewed by the doctor and passed as context to Agent 2 and Agent 3.

---

# REPORT 1

Create a separate PDF:

**PRELIMINARY AYURVEDIC ASSESSMENT REPORT**

Report 1 must contain:

* Report header.

* Patient profile.

* Selected service.

* Relevant pre-consultation summary.

* Prakriti assessment.

* Vikriti assessment.

* Agni assessment.

* Assessment summary.

* Assessment scores.

* System disease-screening result, if applicable.

* Safety flags.

* Assessment limitations.

* AI assessment status.

* Safety disclaimer.

Display:

**PRELIMINARY AI ASSESSMENT — NOT DOCTOR APPROVED**

Also display:

**This report is preliminary and may be reviewed by a qualified doctor.**

Report 1 must not contain:

* Final personalized diet.

* Final lifestyle plan.

* Agent 2 diet plan.

* Agent 3 final lifestyle recommendations.

* Doctor-approved content.

* Medicines.

* Prescriptions.

* Final follow-up plan.

* Doctor signature.

* Final patient approval.

* Final patient-facing wellness recommendations.

Report 1 is generated immediately after Agent 1 completes.

---

# REPORT 2

For Complete Personalized Wellness, create a separate PDF:

**FINAL PERSONALIZED WELLNESS REPORT**

Report 2 must contain:

* Patient profile.

* Relevant assessment summary.

* Doctor-reviewed assessment.

* Agent 2 personalized diet.

* Food portions.

* Food alternatives.

* Nutrition summary.

* Food preferences.

* Allergies.

* Intolerances.

* Restrictions.

* Foods to prioritize.

* Foods to avoid or limit.

* Agent 3 personalized lifestyle recommendations.

* Doctor-approved lifestyle advice.

* Disease-screening result.

* Safety validation.

* Nutrition validation.

* Doctor feedback.

* Doctor-approved medicines or prescriptions, if entered.

* Dosage, frequency, duration, and instructions, if entered.

* Follow-up instructions.

* Doctor identity.

* Doctor registration number.

* Doctor qualification.

* Doctor sign-off.

* Approval date.

* Approval status.

* Disclaimer.

* References where available.

Report 2 must be generated only after explicit doctor approval.

Do not copy the complete Report 1 into Report 2.

Do not repeat the same assessment explanation.

Use the shared structured data to assemble Report 2.

---

# DOCTOR DASHBOARD

The doctor must log in and select a patient case.

The doctor must see the correct report according to the selected service.

## Assessment Only

The doctor reviews:

* Report 1.

* Patient profile.

* Assessment results.

* Screening.

* Safety flags.

* Limitations.

The doctor can:

* Approve.

* Reject.

* Provide feedback.

* Request clarification.

* Add clinical observations.

* Correct assessment results.

Agent 2, Agent 3, and Report 2 are not required.

## Complete Personalized Wellness

The doctor reviews together:

* Report 1 assessment.

* Agent 2 diet.

* Agent 3 lifestyle recommendations.

* Disease screening.

* Safety validation.

* Restriction validation.

* Nutrition validation.

* Patient restrictions.

* Health conditions.

The doctor can:

* Edit patient information.

* Confirm or edit Prakriti.

* Confirm or edit Vikriti.

* Confirm or edit Agni.

* Edit the diet.

* Edit portions.

* Add or remove foods.

* Edit lifestyle advice.

* Add restrictions.

* Add medicines.

* Add prescriptions.

* Add dosage.

* Add frequency.

* Add duration.

* Add instructions.

* Add clinical observations.

* Add follow-up instructions.

* Add final comments.

* Approve.

* Request changes.

* Reject.

The doctor must provide one clear final decision:

* Approve.

* Request Changes.

* Reject.

---

# APPROVAL RULES

Use clear case statuses:

* Draft.

* AI Assessment Generated.

* Agent 3 Recommendations Generated.

* Under Doctor Review.

* Changes Required.

* Doctor Approved.

* Finalized.

* Sent to Patient.

* Rejected.

For Assessment Only:

* Report 1 can be generated before approval.

* Doctor feedback is saved.

* The feedback can be returned to the user.

* Report 2 is not required.

For Complete Personalized Wellness:

* Report 2 must not be finalized before doctor approval.

* Report 2 must not be sent to the patient before doctor approval.

* Empty doctor fields must never count as approval.

* AI-generated content must never automatically become doctor-approved.

* If the doctor requests changes, return the case for correction.

* Do not ask the patient or doctor to repeat information already stored.

* If approved content changes, invalidate the previous approval and require fresh approval.

Display:

**DOCTOR VERIFICATION REQUIRED**

before approval.

Display:

**DOCTOR APPROVED**

only after explicit approval.

---

# DISEASE SCREENING SAFETY

Use the heading:

**SYMPTOM-BASED DISEASE SCREENING**

Always display:

**SCREENING / RESEARCH ONLY — NOT A MEDICAL DIAGNOSIS**

Reuse symptoms already collected in the common form.

Do not ask the patient to repeat the same symptom questions.

The system must not:

* Diagnose diseases.

* Present screening as confirmation.

* Prescribe medicines.

* Generate disease treatment.

* Replace a qualified doctor.

---

# MEDICINE SAFETY

AI must never independently prescribe medicines.

Medicines and prescriptions must be:

* Entered by the doctor, or

* Explicitly approved by the doctor.

If no medicine is entered, display:

**Not provided**

Never generate medicine names from AI suggestions.

---

# NUTRITION VALIDATION

Do not modify Agent 2’s working diet logic.

Validate Agent 2’s output before placing it in Report 2.

Check:

* Food name.

* Portion.

* Calories.

* Protein.

* Carbohydrates.

* Fat.

* Fibre.

* Meal totals.

* Daily totals.

* Weekly totals.

* Target versus actual nutrition.

* Diet-plan values versus PDF values.

If values conflict, display:

**NUTRITION REVIEW REQUIRED**

Do not hide missing or conflicting nutrition data.

---

# DUPLICATE-PREVENTION REQUIREMENTS

Prevent duplicate questions and duplicate report sections at the data-model level.

Use:

* One canonical field per patient answer.

* One stable question ID per question.

* One shared patient state.

* One report object per report type.

* One patient/session ID.

* One report version.

* One audit history.

* One doctor-review object.

Do not duplicate:

* Patient profile.

* Health goal.

* Allergies.

* Restrictions.

* Symptoms.

* Assessment results.

* Diet information.

* Lifestyle information.

* Doctor details.

* Disclaimers.

* Approval information.

Report types must be:

* `AI_ASSESSMENT`

* `FINAL_PERSONALIZED`

Do not silently create multiple final reports.

If regenerating a report:

* Update the existing version, or

* Create a clearly versioned replacement.

---

# PDF DESIGN

Use the VedAmrit PDF as a visual reference only.

Both PDFs must be:

* English-only.

* A4.

* Printable.

* Professional.

* Doctor-friendly.

* Clearly paginated.

* Easy to read.

* Free from overlapping text.

* Free from clipped tables.

* Free from duplicate sections.

Use:

* Light pastel section headers.

* Clear section hierarchy.

* Professional tables.

* Status labels.

* Warning boxes.

* Consistent typography.

* Clean margins.

* Page numbers.

* Headers and footers.

* Correct table page breaks.

* Repeated table headings on new pages.

Do not copy patient information from the reference PDF.

---

# REQUIRED DOCUMENTATION

Add all requirements in this prompt to the project documentation.

Update or create suitable documentation files such as:

* `docs/architecture.md`

* `docs/patient-questionnaire.md`

* `docs/shared-patient-state.md`

* `docs/agents.md`

* `docs/agent-2-protection.md`

* `docs/agent-3-lifestyle-rag.md`

* `docs/report-workflow.md`

* `docs/doctor-review.md`

* `docs/approval-workflow.md`

* `docs/validation-rules.md`

* `docs/nutrition-validation.md`

* `docs/duplicate-prevention.md`

* `docs/pdf-generation.md`

* `docs/safety-rules.md`

* `docs/testing.md`

Document:

* The final question list.

* Removed duplicate questions.

* Removed unnecessary season question.

* Shared patient-state design.

* Service-selection logic.

* Agent 1 flow.

* Agent 2 protection.

* Agent 3 personalization.

* RAG usage.

* Report 1.

* Report 2.

* Doctor review.

* Approval rules.

* Validation rules.

* Duplicate prevention.

* Error handling.

* Testing.

---

# REQUIRED IMPLEMENTATION PROCESS

## Step 1 — Inspect

Inspect the existing project before editing:

* Patient forms.

* Question definitions.

* Question IDs.

* Scoring logic.

* Agent 1.

* Agent 2.

* Agent 3.

* RAG retrieval.

* Shared state.

* Report generation.

* PDF generation.

* Doctor dashboard.

* Approval workflow.

* Database models.

* Duplicate-question causes.

* Duplicate-report causes.

* Documentation.

## Step 2 — Explain

Before making changes, explain:

* Which questions are duplicated.

* Which questions are unnecessary.

* Where the common form should be implemented.

* How the shared patient state will work.

* How Assessment Only differs from Complete Personalized Wellness.

* How Agent 2 will remain untouched.

* How Agent 3 will be personalized.

* How Report 1 and Report 2 will be separated.

* Which files require changes.

* Which documentation files require updates.

## Step 3 — Implement

Implement the cleaned questionnaire and workflow without unrelated changes.

## Step 4 — Verify

Verify:

* Each patient question appears only once.

* Prakriti has exactly 21 questions.

* Vikriti has exactly 21 questions.

* Agni has exactly 11 questions.

* Season is not asked as a standalone unnecessary question.

* Agent 2 remains unchanged.

* Agent 3 uses the shared patient state and Lifestyle RAG.

* Report 1 is generated without approval.

* Assessment Only does not run unnecessary agents.

* Complete Wellness runs Agent 1, Agent 2, Agent 3, and validations.

* Report 2 requires explicit doctor approval.

* Doctor feedback is saved.

* Patient answers are not requested again.

* Doctor answers are not requested again.

* Duplicate report sections are prevented.

* Nutrition totals are validated.

* PDFs are printable and English-only.

## Step 5 — Final response

After implementation, provide:

* Files changed.

* Documentation files changed.

* Confirmation that Agent 2 was not modified.

* Final question structure.

* Removed questions.

* Removed duplicate fields.

* Shared-state changes.

* Agent 3 changes.

* RAG changes.

* Report 1 changes.

* Report 2 changes.

* Doctor dashboard changes.

* Approval workflow changes.

* Validation changes.

* Duplicate-prevention changes.

* Testing results.

* Known limitations.

* Instructions to run the project.

* Instructions to test Assessment Only.

* Instructions to test Complete Personalized Wellness.

* Instructions to generate Report 1.

* Instructions to complete doctor review.

* Instructions to generate Report 2.

---

# FINAL SUCCESS CRITERIA

The implementation is complete only when:

1. The patient completes one common profile form.

2. The patient answers each required question only once.

3. Duplicate questions are removed.

4. The unnecessary standalone season question is removed.

5. Prakriti contains exactly 21 questions.

6. Vikriti contains exactly 21 questions.

7. Agni contains exactly 11 questions.

8. All answers are stored in one shared patient state.

9. Agent 1 generates Report 1 immediately after assessment.

10. Report 1 does not require approval before generation.

11. Assessment Only does not run Agent 2, Agent 3, or Report 2.

12. Agent 2 remains unchanged.

13. Agent 2’s existing personalized diet is used.

14. Agent 3 generates personalized lifestyle-balance recommendations through RAG.

15. Agent 3 does not produce generic advice only.

16. Agent 3 does not prescribe medicines or diagnose diseases.

17. Safety, restriction, disease-screening, and nutrition validation are applied.

18. Report 1 and Report 2 are separate PDFs.

19. Report 2 is generated only after explicit doctor approval.

20. Doctor feedback and edits are saved.

21. The same patient and doctor questions are not repeatedly asked.

22. Duplicate report sections are prevented.

23. The final PDF exactly matches doctor-approved data.

24. All logic is documented in project documentation files.

25. The system is user-friendly, English-only, professional, and printable.
