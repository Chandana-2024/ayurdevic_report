# Steps 1–6 implementation

This document describes the checked-in CLI/graph implementation and supersedes
conflicting questionnaire/state descriptions in older planning documents.

## Questionnaire

`src/main.py:get_patient_profile` uses the 20 fields in
`src/services/general_questionnaire.py`. Conditional details belong to their
parent field. Q13 is one Yes/No question with the original 31 model feature
choices; Q14 is restricted to selected symptoms, and Q15 is conditional.
Selecting No skips all three symptom details. The existing scored instruments
in `src/questions.py` remain unchanged: 21 Prakriti, 21 Vikriti, 11 Agni.
Documentation numbering is 21–41, 42–62, 63–73; internal IDs remain unchanged.
The CLI sets seven diet days without asking an extra patient question.

## Common patient state

The established `DietPlanningState` is the common `patient_state`; no parallel
state manager or database was added. Its `patient_profile` is canonical, with
assessment answers/results stored in the same graph state. New CLI requests
do not duplicate it in `user_input`, or repeat Prakriti answers in `answers`.
Legacy input aliases remain supported. Profile normalization preserves supplied
clinical/lifestyle fields and excludes legacy season fields. Agent 1 and the
standalone Agent 2 retain their existing compatibility output contracts; these
are derived outputs, not additional editable patient records.

## Agent 3

`src/services/lifestyle_input.py` projects relevant profile fields, assessment
summaries, doctor restrictions, selected symptoms and actual meal category names.
Agent 3 still uses `src/agents/lifestyle.py` and its existing RAG/recommendation
branches. Season no longer enters this path. Recommendations retain their text,
patient-specific reason, source attribution, safety considerations and review
status. Raw retrieval payloads/excerpts, queries, repeated factor dictionaries,
patient profiles and debug errors are excluded from returned output. The class
wrapper delegates to the same implementation. Missing evidence still produces
the existing conservative recommendations and review-required flag.

## Agent 2 and timetable

The graph's `diet_planning_agent` produces `diet_plan.days[].meals[]` with actual
categories `Breakfast`, `Lunch`, `Snack`, `Dinner`. The separate class entry point
returns a single day keyed `breakfast`, `lunch`, `snack`, `dinner`. Both generation
implementations are unchanged. `compact_diet_timetable` reuses `selected_diet`
to accept both contracts. Columns derive from the supplied meal names in order.
It never adds meals or repeats a single day into an invented week.

The graph exposes `diet_timetable` with `columns`, `rows` and `common`. Each cell
retains original foods, portions and meal details. Common targets and supported
notes are shown once; identical day-level notes are lifted only when present on
every day. No PDF layout is changed and Report 2 is not implemented or extended.

## Report 1 and regression protection

Report 1 still runs immediately after Agni, before diet generation. Its PDF engine,
layout, disclaimers and scoring data are unchanged. Its data adapter preserves
the newly collected fields and no longer exports season. Tests cover completed
general intake through Agent 1 and actual PDF generation, plus a seven-day graph
run with real diet generation (external lifestyle retrieval mocked).

`tests/fixtures/controlled_baseline.json` records pre-change hashes of the complete
instruments, scoring, assessment agents, diet entry points/planner and Report 1
PDF implementation, plus original symptom labels/order. Hashes normalize only
CRLF/LF checkout differences. Existing suite tests remain; the lifestyle test now
checks factors in the retrieval input rather than requiring removed output metadata.

No browser/API/SQLite implementation described in older planning documents exists
in the active `src` tree. Legacy `AYUCARE` applications, Report 2, Kotlin, scoring,
diet logic, the RAG retrieval system and unrelated seasonal knowledge are untouched.
