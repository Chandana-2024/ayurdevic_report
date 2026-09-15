# Agents and Boundaries

## Agent 1 Assessment Agent

Agent 1 performs preliminary AI assessment only. Its outputs are never a final patient-facing recommendation or doctor decision. Its screening heading is **SYMPTOM-BASED DISEASE SCREENING** and always carries **SCREENING / RESEARCH ONLY — NOT A MEDICAL DIAGNOSIS**.

## Agent 2 Personalized Diet Agent

Agent 2 was inspected but not modified because its personalized diet generation is already working correctly. It remains the sole owner of meal selection, portions, food recommendations, nutrition values, nutrition targets, and diet personalization. Report code may validate and adapt its already-produced structured output, but may not replace, duplicate, or alter its diet logic.

## Agent 3 Personalized Lifestyle RAG Agent

Agent 3 creates non-diet lifestyle guidance from patient profile, goal, age/sex when available, activity, sleep, stress, symptoms, Prakriti, Vikriti, Agni, food preferences, allergies, intolerances, conditions, doctor restrictions, relevant Agent 1 data, relevant Agent 2 context, and traceable Lifestyle RAG evidence. Each recommendation records its patient-specific reason, factors used, Ayurvedic basis when retrieved, verified wellness basis when available, safety consideration, `AI-GENERATED — DOCTOR REVIEW REQUIRED`, and doctor-review requirement.

Agent 3 does not diagnose, prescribe medicines, recommend medicine changes, claim cures, promise outcomes, prescribe extreme fasting, severe restriction, detoxification, unsafe cleansing, unsupported supplements, or create a competing diet engine. Traditional Ayurvedic material is presented as educational wellness guidance only.
