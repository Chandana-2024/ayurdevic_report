# Two-report implementation report

## Outcome and remaining dependencies

The local Python/LangGraph application now has two report paths, explicit doctor
review, version-bound approval, one shared lifestyle agent and report-side diet
validation. The existing partial implementation was refined; existing unrelated
working-tree edits were preserved.

Agent 2 was inspected but not modified because its personalized diet generation is already working correctly.

The uploaded VedAmrit PDF and Ayurvedic Lifestyle RAG document were not found.
Consequently, exact reference-layout matching and VedAmrit-specific grounding
are not complete. Current retrieval uses the existing classical knowledge base.
No actual patient, doctor, assessment, medicine or nutrition facts were invented.
QA fixtures are explicitly synthetic and are not patient deliverables.

## Code files changed

| File | Result |
| --- | --- |
| `src/graph.py` | Generates assessment PDF after Agent 1 and before diet processing; preserves session metadata. |
| `src/main.py` | Collects lifestyle/safety context, invokes doctor editing, gates final PDF, saves sessions, avoids unapproved final text. |
| `src/agents/lifestyle.py` | Context-aware routine drafts, digestion/sleep/stress/activity adaptation, compound dosha handling and visible missing-evidence flags. |
| `src/agents/ayurveda_rag.py` | Sends full relevant patient context to lifestyle retrieval; food retrieval logic unchanged. |
| `src/agents/lifestyle_agent.py` | Legacy class delegates to the single Agent 3 implementation. |
| `src/agents/final_response.py` | Replaces the extra combined textual report with a doctor-review notice. |
| `src/services/report_workflow.py` | Separate snapshots, explicit approval, canonical content hash, version checks, rejection, invalidation and idempotent export. |
| `src/services/report_validation.py` | Adapts both diet contracts, validates actual selected/edited diet, recalculates totals and records missing data/conflicts. |
| `src/services/doctor_console.py` | JSON editing, medicines, sign-off, atomic local persistence and resumed review command. |
| `src/services/two_report_pdf.py` | Two distinct A4 layouts, required sections/statuses, readable tables, page breaks and approval gate. |
| `src/services/pdf_report.py` | Historical PDF entry points delegate to the same gated final builder. |
| `tests/test_report_security.py` | Approval tampering, regeneration, restrictions, medicines, nutrition, personalization and PDF regression cases. |
| `tests/test_two_report_workflow.py`, `tests/test_report_validation.py`, `tests/test_lifestyle_personalization.py`, `tests/test_full_graph.py` | Align existing tests with assessment-first review and explicit approval. |

`src/services/report_models.py` was inspected and reused for the two report enums,
workflow statuses and metadata; it was already present as an untracked file.
The pre-existing `src/scoring.py` working-tree change was not edited during this
implementation. Agent 2, its diet prompt, filter/ranker/planner/replanner/validator,
portion calculator, diet targets and nutrition calculator have no Git differences.

## Documentation

Updated README and the existing `docs/agents.md`, `architecture.md`,
`doctor-review.md`, `nutrition-validation.md`, `pdf-generation.md`,
`report-schema.md`, `report-workflow.md`, `safety-and-disclaimers.md`,
`validation-rules.md`, `testing.md`, and `changelog.md` alongside implementation.
Added `implementation-contract.md`, `agent-3-personalization.md`, `operations.md`
and this report. Existing useful documentation was retained.

## Data model and agent flow

Only `AI_ASSESSMENT` and `FINAL_PERSONALIZED` are report types. Assessment data,
Agent 2 output, Agent 3 draft, doctor review and approved snapshot remain separate.
The final snapshot selects the reviewed diet/lifestyle once, removes redundant
doctor-edit copies and does not embed Report 1. Metadata includes patient/session
and report identifiers, version, status, creation/update and approval timestamps.

Agent 1 -> Report 1 -> unchanged Agent 2 -> Agent 3 draft -> doctor review ->
explicit approval -> Report 2. Safety PASS is not approval. The doctor reviews
patient data, preliminary assessment, both agent drafts and validation findings.
Patient corrections, assessment confirmations, diet foods/portions, restrictions,
lifestyle edits, medicines, follow-up, monitoring and comments are supported.

Literal boolean review/approval confirmations, nonblank identity/registration and
sign-off are required. Approval records its date, report version and exact content
hash/snapshot. Rejection, changes and content/version tampering block final export.
Unchanged export reuses identity/version; a replacement after edits increments
the version. No patient messaging is performed.

## Validation and safety

The adapter supports `days` and named-meal Agent 2 outputs. It uses doctor edits
when present, checks source food IDs/names and portions against CSV nutrition,
recalculates meals/days/weeks/full plans and compares available targets.
Missing macros remain unknown rather than zero. Discrepancies are recorded;
blocking failures prevent approval, and warnings require explicit doctor review
acknowledgement and remain visible in the PDF.

Allergy, intolerance, avoided-food, source ingredient, dietary preference and
available condition restrictions are checked. Medication/pregnancy/severity and
missing safety context trigger review. Medicine-allergy conflicts block approval.
Condition/restriction checking depends on recorded data and source vocabulary;
it is not a comprehensive drug interaction or clinical contraindication engine.

Screening remains research-only. Agent 3 has no prescribing or competing diet
engine. Retrieved topic matches retain provenance and are explicitly unverified;
unsupported source claims are not promoted to established medical evidence.
Final approved content is distinguished from its AI origin. Non-Latin script
content is rejected for English PDF review rather than silently rendered as boxes.

## Tests and PDF QA

The final full unittest discovery run passed **36 tests**, using cached RAG models
in offline mode and UTF-8 console output. Source syntax compilation passed.
Coverage includes missing/false-string approval, signatures, version tampering,
stored-report tampering, rejection, content edits, unchanged regeneration,
doctor-edited restricted foods, medicine changes/allergies, unknown macros,
negative nutrition, weekly aggregation, Agni-dependent text, retrieval context,
English-script validation and long table exports.

Generated synthetic QA PDFs contain **2 assessment pages and 4 final pages**.
Text extraction and all six rendered pages were inspected. No overlap or clipping
was observed; tables repeat headings and section titles stay with their content.
This verifies sample layouts, not every possible real-world content length.

## Run and use

1. Python 3.11+: `python -m pip install -r requirements.txt`.
2. Run `python -m src.main` and supply real patient data and assessment answers.
3. Report 1 is saved under `reports/AI_Assessment_Report_<session>.pdf` before
   diet generation. Give this preliminary report to the doctor.
4. The doctor uses the console to review/edit JSON, enter medicines and follow-up,
   review warnings, choose approve/reject/changes and sign off.
5. Explicit valid approval enables
   `reports/Final_Personalized_Wellness_Report_<session>.pdf`.
6. Resume saved reviews with
   `python -m src.services.doctor_console reports/session_<session>.json`.

See `operations.md` for detailed editing and test instructions.

## Known limitations

- Missing VedAmrit uploads prevent reference-specific completion.
- Doctor review is a local console workflow with structured JSON editing, not an
  authenticated web portal or independently verified professional identity.
- Sign-off is a recorded name, not a cryptographic digital signature.
- Local session files have no multi-user database locking, role-based access or
  delivery service; deployment hardening remains necessary for clinical use.
- RAG topic matching is not semantic evidence validation. Source-specific rules
  require document verification and doctor review; current personalization is
  conservative and rule-based rather than a clinically validated recommendation model.
- English-script checks cannot determine whether Latin-script prose is English.
