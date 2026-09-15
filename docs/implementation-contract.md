# Implementation contract and acceptance checklist

This supplements the existing architecture, agents, schema, workflow, doctor review,
nutrition, safety, PDF and testing documents. Those requirements remain mandatory.

## Boundaries and known integration defects

Agent 2 was inspected but not modified because its personalized diet generation is already working correctly.
Its prompts, ranking, portions, nutrition targets, meal planning and output contract
are protected. Adaptation and discrepancy recording belong in report services.
The two supported contracts are a `days` plan and a dictionary of named meals.
Missing macros in the latter are unknown, never zero. Doctor edits must be the
same source used for validation, approval and PDF rendering.

The previous report implementation had a separate legacy combined-report path,
validated stale meal data, and generated fresh identifiers without replacement
version semantics. Report builders must share the workflow gate and snapshot.

## Approval invariants

Require literal boolean qualified-reviewer and approval confirmations, nonblank
identity, registration and sign-off. Bind canonical JSON content, version and
approval time. Rejection and requested changes revoke approval. Repeated export
of unchanged approved content reuses its identifier/version; changed content
requires a new version and fresh approval. Keep the exact approved snapshot.
No patient delivery integration may bypass these checks. Local doctor identity
entry is not authentication or professional-registration verification.

## Doctor editing

Before signing, show assessment, diet, lifestyle and validation to the reviewer.
Allow structured JSON edits of patient fields, assessment, foods, portions,
added/removed foods and lifestyle. Allow doctor-entered medicines with name,
dosage, frequency, duration, instructions and approval status. Collect observations,
confirmed symptoms/Prakriti/Vikriti/Agni, assessment, comments, restrictions,
wellness advice, follow-up date/instructions, monitoring, final comments and signature.
Support approve, reject and request changes. Never manufacture missing entries.

## Lifestyle grounding

Prakriti is baseline; Vikriti is current imbalance. Preserve both, including Vata,
Pitta, Kapha, Vata-Pitta, Pitta-Kapha, Vata-Kapha and Vata-Pitta-Kapha.
Use current Vikriti, Agni, symptoms, season and doctor restrictions to resolve
competing principles conservatively. Do not infer unsupported rules.
Agni may inform timing/regularity and discussion of digestive tolerance; Agent 2
retains food preparation, portions, heaviness and nutrition decisions.
Retrieval must receive actual patient context, not only a generic dosha query.
Each major recommendation needs recommendation, reason, factors, supported
Ayurvedic basis, verified wellness basis if available, safety, AI origin and
doctor-review status. Missing evidence is explicitly unavailable, not a citation.
No medicines, supplements, cleansing, detox, fasting, severe restriction, diagnoses,
medicine changes, cures, prevention promises or guaranteed outcomes.

## Output and error behavior

Exactly two report types: AI_ASSESSMENT and FINAL_PERSONALIZED. Report 1 never
includes doctor data, final advice, diet, lifestyle, medicines, follow-up or signature.
Report 2 uses relevant reviewed assessment rather than embedding Report 1.
Each patient, assessment, nutrition, diet, lifestyle, doctor, disclaimer, approval,
header and footer appears once per semantic section (running headers may repeat).
English-only A4, pastel headings, warning boxes, readable tables, repeated table
headers and pagination. Missing values: Not provided or REVIEW REQUIRED.
Validation failures must remain visible. All required sections are specified in
report-schema.md. No reference patient data may be copied.

The uploaded VedAmrit reference PDF and lifestyle document are not present in
the inspected workspace. Visual matching and source-specific grounding remain
unverified until supplied. Existing classical retrieval is a fallback only.

## Verification

Test missing/invalid approval, rejection, requested changes, version tampering,
post-approval edits, unchanged regeneration, doctor diet and medicine edits,
missing/negative/nonfinite nutrition, daily/weekly/plan totals, restriction conflicts,
different constitutions/digestion/preferences, missing patient fields, English-only
rendering and long-table pagination. Test fixtures are synthetic, never patient facts.
