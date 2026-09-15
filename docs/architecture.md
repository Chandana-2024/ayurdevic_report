# Two Report Architecture

The system has three distinct agent responsibilities. Agent 1 produces only a preliminary assessment: Prakriti, Vikriti, Agni, symptom screening, scores, limitations, safety warnings, and doctor-review flags. Agent 2 is the existing trusted personalized diet service. Its implementation, prompt, scoring, diet logic, nutrition logic, and output contract are not changed. Agent 3 is the personalized Lifestyle RAG Agent; it produces non-diet wellness guidance with traceable evidence and doctor-review status.

The report workflow is documentation-first and uses separate structured objects: `assessment_data`, `agent2_diet_data`, `agent3_lifestyle_data`, `doctor_review_data`, `final_approved_data`, and `report_metadata`. A report has a patient/session ID, report ID, type, version, status, created/updated timestamps, and (where applicable) approval timestamp. Report types are `AI_ASSESSMENT` and `FINAL_PERSONALIZED`.

Report 1 is generated from assessment data only. The doctor then reviews the assessment plus Agent 2 and Agent 3 drafts outside Report 1. Report 2 references only relevant, reviewed data; it never embeds or duplicates the complete Report 1 object. Changes to approved content invalidate approval and create a clearly versioned replacement rather than silently creating another final report.

The accepted statuses are `DRAFT`, `AI_ASSESSMENT_GENERATED`, `AGENT_3_RECOMMENDATIONS_GENERATED`, `UNDER_DOCTOR_REVIEW`, `CHANGES_REQUIRED`, `DOCTOR_APPROVED`, `FINALIZED`, and `SENT_TO_PATIENT`.
