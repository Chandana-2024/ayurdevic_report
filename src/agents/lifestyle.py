"""Agent 3: personalised, non-diet Lifestyle RAG guidance."""
from __future__ import annotations

from typing import Any
import json

from src.agents.ayurveda_rag import get_lifestyle_rag_evidence


def _value(profile: dict[str, Any], key: str) -> Any:
    value = profile.get(key)
    return value if value not in (None, "", [], {}) else None


def _source(evidence: list[dict[str, Any]], topic: str) -> dict[str, Any] | None:
    for item in evidence:
        content = str(item.get("content", "")).lower()
        if topic in content:
            metadata = item.get("metadata") or {}
            return {"source": metadata.get("source_book") or metadata.get("title") or "Not provided", "page": metadata.get("page_label") or metadata.get("page") or "Not provided", "support": "Retrieved Ayurvedic passage for doctor verification; topic matching alone does not verify a recommendation.", "excerpt": item.get("content"), "verified": False}
    return None


def _recommendation(category: str, recommendation: str, reason: str, factors: dict[str, Any], evidence: dict[str, Any] | None, safety: str) -> dict[str, Any]:
    return {"category": category, "personalized_recommendation": recommendation, "patient_specific_reason": reason, "factors_used": {key: value for key, value in factors.items() if value not in (None, "", [], {})}, "ayurvedic_basis": evidence or {"source": "Not provided", "support": "RAG support unavailable; doctor review required."}, "wellness_basis": "Not provided: no independently verified wellness source supplied.", "safety_consideration": safety, "ai_generated_status": "AI-GENERATED — DOCTOR REVIEW REQUIRED", "doctor_review_status": "REVIEW REQUIRED"}


def lifestyle_agent(state: dict[str, Any]) -> dict[str, Any]:
    """Generate structured recommendations without food, medicine, or diagnosis advice."""
    profile = {**(state.get("user_input") or {}), **(state.get("patient_profile") or {})}
    prakriti, vikriti, agni = state.get("prakriti_result") or {}, state.get("vikriti_result") or {}, state.get("agni_result") or {}
    doctor = state.get("doctor_review") or {}
    primary = doctor.get("confirmed_prakriti") or prakriti.get("constitution") or prakriti.get("primary_dosha")
    current = doctor.get("confirmed_vikriti") or vikriti.get("dominant_dosha")
    agni_status = doctor.get("confirmed_agni") or agni.get("status")
    symptoms = _value(profile, "symptoms") or state.get("disease_symptoms")
    restrictions_known = all(_value(profile, key) is not None for key in ("allergies", "medicine_allergies", "food_intolerances", "foods_to_avoid", "health_conditions", "medication_restrictions", "pregnancy_information"))
    factors = {"prakriti": primary, "vikriti": current, "agni": agni_status, "goal": _value(profile, "goal"), "age": _value(profile, "age"), "sex": _value(profile, "gender"), "activity_level": _value(profile, "activity_level"), "sleep": _value(profile, "sleep_information") or _value(profile, "sleep_quality"), "stress": _value(profile, "stress_level"), "symptoms": symptoms, "dietary_preference": _value(profile, "dietary_preference"), "restrictions": restrictions_known, "doctor_restrictions": (state.get("doctor_review") or {}).get("food_restrictions")}
    for key in ("allergies", "medicine_allergies", "food_intolerances", "foods_to_avoid", "health_conditions", "medication_restrictions", "pregnancy_information", "season"):
        factors[key] = _value(profile, key)
    diet = (state.get("agent2_output") or {}).get("diet_plan") or state.get("meal_plan") or {}
    factors["agent2_meal_schedule"] = [meal.get("meal") for day in diet.get("days", []) for meal in day.get("meals", [])] or list(diet.keys())
    query = json.dumps({k: v for k, v in factors.items() if v not in (None, "", [], {})}, sort_keys=True)
    retrieval_error = None
    try:
        evidence = get_lifestyle_rag_evidence(primary or "constitution", str(factors["goal"] or "wellness"), profile.get("health_conditions") or [], patient_context=query)
    except Exception as error:
        evidence = []
        retrieval_error = type(error).__name__
    doshas = str(current or primary or "").lower()
    vata, pitta, kapha = "vata" in doshas, "pitta" in doshas, "kapha" in doshas
    recommendations = [
        _recommendation("daily_routine", "Use a stable wake, meal, and wind-down schedule that fits your current daily commitments.", f"This is tailored to {current or primary or 'an unconfirmed constitution'} and the recorded goal of {factors['goal'] or 'wellness'}.", factors, _source(evidence, "routine"), "Adjust for work, caregiving, symptoms, and doctor instructions; do not use this as treatment."),
        _recommendation("meal_timing", "Keep meal timing regular and choose meal size based on comfort and digestive tolerance rather than forcing fasting or restriction.", f"Agni is recorded as {agni_status or 'not provided'}, so timing guidance requires clinical review if symptoms persist.", factors, _source(evidence, "meal"), "This is not a diet plan and does not override Agent 2, allergies, conditions, or doctor restrictions."),
    ]
    if factors["sleep"] or vata or pitta:
        recommendations.append(_recommendation("sleep", "Set a consistent, low-stimulation pre-sleep routine and record whether sleep quality changes over the next review period.", f"Sleep information is {factors['sleep'] or 'not provided'}; {'Vata/Pitta-related assessment factors also make regular wind-down especially relevant.' if (vata or pitta) else 'the plan therefore remains conservative.'}", factors, _source(evidence, "sleep"), "Seek clinical assessment for severe, persistent, or safety-critical sleep problems."))
    if factors["activity_level"] or kapha:
        activity_text = "Use regular, moderate activity that is comfortable and sustainable, with gradual changes only." if kapha else "Choose gradual, comfortable activity with rest and hydration appropriate to your capacity."
        recommendations.append(_recommendation("activity", activity_text, f"Activity level is {factors['activity_level'] or 'not provided'} and the current assessment includes {current or primary or 'unconfirmed'} factors.", factors, _source(evidence, "exercise"), "Stop and seek clinician guidance for pain, dizziness, severe breathlessness, pregnancy-related restrictions, or condition-specific limitations."))
    if factors["stress"] or vata or pitta:
        recommendations.append(_recommendation("stress_management", "Schedule a brief, non-strenuous calming practice you already tolerate, such as quiet breathing or reflection, and note its effect on routine and sleep.", f"Stress is {factors['stress'] or 'not provided'}; this is adapted to the current {current or primary or 'unconfirmed'} assessment rather than offered as a cure.", factors, _source(evidence, "mind"), "Do not use this in place of mental-health, emergency, or medical care."))
    if _value(profile, "season"):
        recommendations.append(_recommendation("seasonal_guidance", "Discuss only small routine adjustments for the recorded season with the reviewing doctor; avoid extreme seasonal cleanses.", f"Season is recorded as {profile.get('season')} and current Vikriti/Agni may affect tolerance.", factors, _source(evidence, "season"), "No detoxification, unsafe cleansing, or fasting is recommended."))
    safety_flags = []
    if not evidence:
        safety_flags.append("REVIEW REQUIRED: Lifestyle RAG evidence unavailable" + (f" ({retrieval_error})" if retrieval_error else "") + ". No source-specific Ayurvedic rule has been verified.")
    # Recommendations change with supplied routine constraints; no new diet is created.
    for item in recommendations:
        category = item["category"]
        if category == "meal_timing":
            if "visham" in str(agni_status).lower():
                item["personalized_recommendation"] = "Use the existing Agent 2 meal schedule as an anchor and record skipped meals and digestive discomfort for doctor review; avoid compensatory fasting."
            elif "manda" in str(agni_status).lower():
                item["personalized_recommendation"] = "Record fullness around the existing Agent 2 meals and ask the doctor to review timing if discomfort persists; keep prescribed portions unchanged until reviewed."
            elif "tiksh" in str(agni_status).lower():
                item["personalized_recommendation"] = "Record hunger and discomfort between the existing Agent 2 meals and review long gaps with the doctor; do not introduce fasting."
        elif category == "activity" and str(factors["activity_level"]).lower() in {"low", "sedentary"}:
            item["personalized_recommendation"] = "Discuss a comfortable movement break during your longest seated period with the doctor; start only within your recorded restrictions and current tolerance."
        elif category == "sleep" and factors["sleep"]:
            item["personalized_recommendation"] = f"For your reported sleep pattern ({factors['sleep']}), record bedtime, waking and interruptions, and choose one tolerable wind-down step to review with the doctor."
        elif category == "stress_management" and factors["stress"]:
            item["personalized_recommendation"] = f"For the reported stress level ({factors['stress']}), place a brief quiet pause before the daily activity you find most demanding and record whether it is tolerable."
        if factors.get("doctor_restrictions") or factors.get("health_conditions") or factors.get("pregnancy_information"):
            item["safety_consideration"] += " Reviewing doctor must reconcile this suggestion with: " + json.dumps({k: factors[k] for k in ("doctor_restrictions", "health_conditions", "pregnancy_information", "medication_restrictions") if factors.get(k)})
    if not restrictions_known:
        safety_flags.append("REVIEW REQUIRED: allergy, intolerance, avoided-food, or condition information is incomplete.")
    if symptoms:
        safety_flags.append("Condition-related symptoms require doctor review; this output is not a diagnosis.")
    return {"lifestyle_plan": {"recommendations": recommendations, "personalization_factors": [key for key, value in factors.items() if value not in (None, "", [], {})], "rag_evidence": evidence, "rag_query": query, "safety_flags": safety_flags, "draft_status": "AI-GENERATED — DOCTOR REVIEW REQUIRED"}}
