# Canonical patient case

The complete supplied specification is preserved in patient-workflow-requirements.md.
Latest naming override: Report 1 is **Ayurvedic Assessment**, downloaded as
`ayurvedic_assessment.pdf`; Report 2 is **final_report**, downloaded as `final_report.pdf`.
Internal report types remain AI_ASSESSMENT and FINAL_PERSONALIZED.

One SQLite case stores a UUID patient/session identity, selected service, answers
keyed by stable question ID, generated outputs, doctor review, version, status
and audit history. Personal answers exist once, in `answers`; agent input profiles
are transient adapters, not separate editable forms. Immutable report/approval
snapshots preserve the exact approved version. SQLite optimistic version checks
prevent silent concurrent overwrites. Each save records an audit event.

The browser shows one question at a time, saves before navigating, supports Back,
Review and edits, and restores the saved case on reload. Unknown/declined and
explicit No remain distinct. Conditional symptom details appear only for Yes.
Blood group and likes/dislikes are optional. Season, duplicate symptom screening,
diet-duration questions, duplicate doctor sign-off and monitoring prompts are removed.
The existing diet default is one day; no diet logic changes are made.

Both services use the same 31-field common schema and unmodified 21/21/11 question
definitions. Stable assessment IDs map to existing scoring keys at the adapter.
Some preserved assessment items concern appetite/sleep/bowels also covered by the
common form. They remain separate scored instrument items as explicitly required;
no automatic answer equivalence or fabricated scoring response is assumed.

Assessment Only invokes Agent 1 and exports Report 1 before doctor review; no
diet/lifestyle/final report is generated. Complete Wellness exports Report 1,
then invokes unchanged diet stages, lifestyle retrieval, screening/safety/restriction/
nutrition validation, and presents draft data to the doctor. Final export and
patient download require a current version-bound approval. Assessment feedback
is visible to the patient in the same app; no external messages are sent.

Doctor accounts are created locally with a password hash and saved doctor profile.
Login grants access to cases. Patient cookies grant access only to their own case.
Requests require CSRF tokens; opaque session cookies are HttpOnly and SameSite.
The server binds localhost by default. Deployments require TLS and operational
access controls. One prefilled doctor review is saved and edited, never re-entered
from scratch. Approval, rejection and changes are distinct decisions.

Screening reuses stored complaints without filling unasked symptoms with zero.
Incomplete feature vectors are marked REVIEW REQUIRED, not classified as disease.
Doctor edits invalidate approval. Agent 2 input adaptation is conservative and
explicitly flags unsupported preferences rather than treating them as confirmed.
