# Testing Requirements

Latest verification: 36 unittest cases passed with cached RAG retrieval and UTF-8
console output; `python -m compileall -q src` passed. On Windows, set
`PYTHONIOENCODING=utf-8` for legacy tests that print source passages. The synthetic
PDF QA set has two assessment pages and four final pages, all visually inspected.
See `implementation-report.md` for tested scope and limitations.

Tests cover Prakriti, Vikriti, and Agni variations; dietary preferences; allergies; intolerances; avoided foods; missing fields; nutrition mismatches; Agent 3 factor personalization and RAG traceability; unapproved, rejected, changes-required, and approved workflows; edited diet; doctor medicines; approval invalidation; report regeneration; duplicate prevention; empty values; English-only output; long tables; and PDF page breaks.
