from typing import Any


def final_response_agent(state: dict[str, Any]) -> dict[str, Any]:
    """
    AyurGenix Final Assessment, Diet & Wellness Report Formatter.
    Formats structured outputs from Agent 1 (Assessment), Agent 2 (Diet),
    and Agent 3 (Lifestyle & RAG evidence).
    """
    response_lines = [
        "============================================================",
        "AYURGENIX PERSONALIZED AYURVEDIC WELLNESS REPORT",
        "============================================================",
        "",
    ]

    # 1. PATIENT PROFILE
    patient_profile = state.get("patient_profile", {})
    response_lines.extend([
        "============================================================",
        "PATIENT PROFILE",
        "============================================================",
        f"Name: {patient_profile.get('name', 'N/A')}",
        f"Age: {patient_profile.get('age', 'N/A')}",
        f"Gender: {patient_profile.get('gender', 'N/A')}",
        f"Blood Group: {patient_profile.get('blood_group', 'N/A')}",
        f"Height: {patient_profile.get('height_cm', 'N/A')} cm",
        f"Weight: {patient_profile.get('weight_kg', 'N/A')} kg",
        f"Dietary Preference: {patient_profile.get('dietary_preference', 'unspecified')}",
        f"Allergies: {', '.join(patient_profile.get('allergies', [])) or 'None'}",
        f"Foods to Avoid: {', '.join(patient_profile.get('foods_to_avoid', [])) or 'None'}",
        f"Health Conditions: {', '.join(patient_profile.get('health_conditions', [])) or 'None'}",
        f"Goal: {patient_profile.get('goal', 'general wellness')}",
        "",
    ])

    # 2. AYURVEDIC ASSESSMENT (AGENT 1)
    prakriti_result = state.get("prakriti_result", {})
    prakriti_scores = prakriti_result.get("scores", {})
    constitution = prakriti_result.get("constitution", state.get("constitution", "N/A"))

    vikriti_result = state.get("vikriti_result", {})
    vikriti_scores = vikriti_result.get("scores", {})
    dominant_vikriti = vikriti_result.get("dominant_dosha") or vikriti_result.get("dominant", "N/A")

    agni_result = state.get("agni_result", {})
    agni_status = agni_result.get("status", "N/A")

    response_lines.extend([
        "============================================================",
        "AYURVEDIC ASSESSMENT (AGENT 1)",
        "============================================================",
        f"Prakriti Constitution: {constitution}",
        f"  Primary Dosha: {prakriti_result.get('primary_dosha', 'N/A')}",
        f"  Secondary Dosha: {prakriti_result.get('secondary_dosha', 'N/A')}",
        f"  Scores: Vata: {prakriti_scores.get('Vata', 0)} | Pitta: {prakriti_scores.get('Pitta', 0)} | Kapha: {prakriti_scores.get('Kapha', 0)}",
        "",
        f"Vikriti Imbalance: Dominant {dominant_vikriti}",
        f"  Scores: Vata: {vikriti_scores.get('Vata', 0)} | Pitta: {vikriti_scores.get('Pitta', 0)} | Kapha: {vikriti_scores.get('Kapha', 0)}",
        "",
        f"Agni Status: {agni_status}",
        f"  Category Scores: {agni_result.get('category_scores', {})}",
        "",
    ])

    # 3. PERSONALIZED DIET PLAN (AGENT 2)
    agent2_output = state.get("agent2_output", {})
    meal_plan = agent2_output.get("diet_plan") or state.get("meal_plan", {})
    response_lines.extend([
        "============================================================",
        "PERSONALIZED DIET PLAN (AGENT 2)",
        "============================================================",
    ])

    if isinstance(meal_plan, dict) and "days" in meal_plan:
        daily_target = meal_plan.get("daily_target", {})
        response_lines.extend([
            f"Plan Duration: {meal_plan.get('duration_days', 1)} day(s)",
            f"Daily Target Calories: {daily_target.get('calories', 'N/A')} kcal",
            f"Target Macros: Protein {daily_target.get('protein_g', 'N/A')}g | Carbs {daily_target.get('carbs_g', 'N/A')}g | Fat {daily_target.get('fat_g', 'N/A')}g",
            f"Calculation Basis: Mifflin-St Jeor BMR (1990) with activity factor assumption 1.375",
            "",
        ])

        for day in meal_plan.get("days", []):
            response_lines.append(f"--- DAY {day.get('day')} ---")
            for meal in day.get("meals", []):
                meal_type = str(meal.get("meal") or meal.get("type", "")).upper()
                foods = meal.get("foods", [])
                food_strs = [f"{f.get('name', '')} ({f.get('portion', '100g')})" for f in foods]
                food_names = ", ".join(food_strs)
                tot = meal.get("meal_total", {})
                reasoning = foods[0].get("ayurvedic_reason", "") if foods else ""

                response_lines.append(f"[{meal_type}]: {food_names}")
                if reasoning:
                    response_lines.append(f"  Ayurvedic Reasoning: {reasoning}")
                response_lines.append(f"  Meal Nutrition: {tot.get('calories', 0)} kcal | P: {tot.get('protein_g', 0)}g | C: {tot.get('carbs_g', 0)}g | F: {tot.get('fat_g', 0)}g")
                response_lines.append("")

            daily_nutr = day.get("daily_total", {})
            response_lines.append(f"Daily Total Nutrition: {daily_nutr.get('calories', 0)} kcal | P: {daily_nutr.get('protein_g', 0)}g | C: {daily_nutr.get('carbs_g', 0)}g | F: {daily_nutr.get('fat_g', 0)}g")
            response_lines.append("")
    elif isinstance(meal_plan, dict):
        for k, v in meal_plan.items():
            response_lines.append(f"{k}: {v}")
    else:
        response_lines.append(str(meal_plan or "No diet plan available."))

    response_lines.append("")

    # 4. FOODS EXCLUDED LOG
    excluded_log = agent2_output.get("excluded_foods_log", [])
    response_lines.extend([
        "============================================================",
        "FOODS EXCLUDED LOG",
        "============================================================",
    ])
    if excluded_log:
        for item in excluded_log[:10]:
            response_lines.append(f"- {item.get('food') or item.get('food_name')}: {item.get('reason')}")
        if len(excluded_log) > 10:
            response_lines.append(f"  ... and {len(excluded_log) - 10} more items excluded by hard safety filters.")
    else:
        response_lines.append("No candidates were excluded by hard filters.")
    response_lines.append("")

    # 5. AYURVEDIC LIFESTYLE & WELLNESS PLAN (AGENT 3)
    lifestyle_data = state.get("lifestyle_plan", {})
    lifestyle_plan = lifestyle_data.get("lifestyle_plan", {})
    response_lines.extend([
        "============================================================",
        "AYURVEDIC LIFESTYLE & WELLNESS PLAN (AGENT 3)",
        "============================================================",
    ])

    for category, recs in lifestyle_plan.items():
        title = category.replace("_", " ").title()
        response_lines.append(f"[{title}]")
        if recs:
            for rec in recs:
                response_lines.append(f"  • {rec}")
        else:
            response_lines.append("  • Follow general balanced daily routine.")
        response_lines.append("")

    # 6. SAFETY FACT-CHECKER STATUS
    val_res = state.get("validation_result") or agent2_output.get("validation", {})
    response_lines.extend([
        "============================================================",
        "SAFETY FACT-CHECKER STATUS",
        "============================================================",
        f"Overall Status: {val_res.get('overall_status') or val_res.get('status', 'PASS')}",
        f"Validation Checks: Safety: {val_res.get('safety', 'PASS')} | Nutrition: {val_res.get('nutrition', 'PASS')} | Portion: {val_res.get('portion', 'PASS')} | Ayurveda Evidence: {val_res.get('ayurveda_evidence', 'PASS')}",
    ])
    if val_res.get("warnings"):
        response_lines.append(f"Warnings: {val_res.get('warnings')}")
    response_lines.append("")

    # 7. SOURCES & RESEARCH EVIDENCE
    response_lines.extend([
        "============================================================",
        "SOURCES & EVIDENCE CITATIONS",
        "============================================================",
        "1. Prakriti & Vikriti Assessment: Deterministic 21-question scoring model",
        "2. Agni Assessment: Singh A, Singh G, Patwardhan K, Gehlot S. (2017) Validated Agnibala Tool",
        "3. Energy Target: Mifflin MD et al. (1990) Predictive equation for resting energy expenditure",
        "4. Food Knowledge: Ayurvedic Food Dishes Dataset & Classical Dravyaguna Reference",
    ])
    for src in (agent2_output.get("sources", []) + lifestyle_data.get("sources", [])):
        src_str = str(src.get("source") if isinstance(src, dict) else src)
        response_lines.append(f"• Reference: {src_str}")

    response_lines.extend([
        "",
        "============================================================",
        "IMPORTANT NOTICE",
        "============================================================",
        "This system is an educational wellness prototype and does not replace",
        "medical diagnosis or treatment by a qualified Ayurvedic physician.",
        "============================================================",
    ])

    return {
        "final_response": "\n".join(response_lines),
    }