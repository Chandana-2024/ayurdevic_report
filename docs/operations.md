# Running and reviewing reports

1. Use Python 3.11+ and install `requirements.txt`. Keep `data/demo_foods.csv`
   and the existing RAG index available. Start `python -m src.main`.
2. Enter actual patient information and assessment answers. Optional lifestyle
   and safety inputs can be left unknown; explicitly record none/not applicable
   only when confirmed. Never copy reference or test patient details.
3. The graph writes `reports/AI_Assessment_Report_<session>.pdf` immediately
   after assessment, before diet generation. Provide this preliminary document
   to the reviewing doctor. It includes no doctor or final recommendation content.
4. The local doctor console collects identity and review fields. It displays
   patient, assessment, Agent 2 diet and Agent 3 lifestyle JSON. Paste replacement
   JSON objects to edit patient fields, assessment, foods, portions or lifestyle;
   blank retains the current object. A diet uses `diet_plan.days[].meals[].foods[]`
   or the existing named-meal contract. Delete/add array entries to remove/add foods.
5. Add doctor-entered medicines and their dosage, frequency, duration and
   instructions. Review the exact combined content and all validation findings.
   Choose approve, reject or changes and enter sign-off. Validation failures block
   approval. Warnings require explicit review acknowledgement and remain printed.
6. Only successful explicit approval allows
   `reports/Final_Personalized_Wellness_Report_<session>.pdf`. A local
   `reports/session_<session>.json` preserves state, exact approved content and
   approval metadata. Files are patient data: use appropriate deployment access controls.

For programmatic use, `TwoReportWorkflow(state)` supports assessment generation,
draft registration, beginning review, requesting changes, rejection, explicit
approval, approval freshness checks and final generation. The PDF facade uses
the same gate. An unchanged re-export preserves identifier/version; changed
approved content requires fresh approval and a versioned replacement.

There is no authenticated web doctor portal, digital signature verification,
patient messaging integration or cross-process database locking. Local sign-off
records a doctor's supplied identity; it does not independently verify credentials.
SENT_TO_PATIENT is reserved for an authorized delivery integration, not automatic
email or messaging. Resume a saved review using
`python -m src.services.doctor_console reports/session_<session>.json`.

## Verification commands

`python -m unittest discover -s tests -p 'test_*.py'` runs the existing suite;
some legacy test modules execute integration work on import and require the RAG
model/cache. Target report tests with `test_report*.py` and
`test_two_report_workflow.py`; personalization tests use mocked retrieval.
`python -m compileall -q src` checks syntax.

PDF QA uses synthetic, explicitly labeled fixtures in `tmp/pdfs`, text extraction
with pypdf and page rendering. These files are never actual patient reports or
evidence of clinical approval. The missing uploaded reference PDF prevents a
claim of exact visual matching.
