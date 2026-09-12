from src.graph import graph
# ============================================================
# 1. PATIENT PROFILE
# ============================================================

patient_profile = {
    "id": "TEST001",
    "name": "Test User",
    "age": 20,
    "gender": "female",
    "blood_group": "O+",
    "height_cm": 154,
    "weight_kg": 55,
    "dietary_preference": "vegetarian",
    "allergies": [],
    "foods_to_avoid": [],
    "health_conditions": [],
    "goal": "general wellness",
}


# ============================================================
# 2. PRAKRITI - 21 QUESTIONS
# ============================================================

# Using the existing 21-question scoring format.
# Values correspond to the answer options already used
# by your AyurGenix Prakriti scoring system.

questionnaire_answers = {
    1: "Vata",
    2: "Vata",
    3: "Pitta",
    4: "Pitta",
    5: "Kapha",
    6: "Vata",
    7: "Pitta",
    8: "Kapha",
    9: "Vata",
    10: "Pitta",
    11: "Kapha",
    12: "Vata",
    13: "Pitta",
    14: "Kapha",
    15: "Vata",
    16: "Pitta",
    17: "Kapha",
    18: "Vata",
    19: "Pitta",
    20: "Kapha",
    21: "Vata",
}


# ============================================================
# 3. VIKRITI - 21 QUESTIONS
# ============================================================

vikriti_answers = {
    "V1": 1,
    "V2": 1,
    "V3": 3,
    "V4": 3,
    "V5": 1,
    "V6": 1,
    "V7": 3,

    "P1": 5,
    "P2": 3,
    "P3": 3,
    "P4": 5,
    "P5": 3,
    "P6": 3,
    "P7": 5,

    "K1": 1,
    "K2": 3,
    "K3": 1,
    "K4": 1,
    "K5": 3,
    "K6": 1,
    "K7": 3,
}


# ============================================================
# 4. AGNI - 11 QUESTIONS
# ============================================================

agni_answers = {
    "A1": 3,
    "A2": 3,
    "A3": 3,
    "A4": 3,
    "A5": 3,
    "A6": 3,
    "A7": 3,
    "A8": 3,
    "A9": 3,
    "A10": 3,
    "A11": 3,
}


# ============================================================
# 5. AYUCARE DISEASE SYMPTOMS - 31 FEATURES
# ============================================================

# 0 = symptom absent
# 1 = symptom present

disease_symptoms = {
    "acidity": 1,
    "indigestion": 1,
    "headache": 0,
    "blurred_and_distorted_vision": 0,
    "excessive_hunger": 0,
    "muscle_weakness": 0,
    "stiff_neck": 0,
    "swelling_joints": 0,
    "movement_stiffness": 0,
    "depression": 0,
    "irritability": 0,
    "visual_disturbances": 0,
    "painful_walking": 0,
    "abdominal_pain": 1,
    "nausea": 1,
    "vomiting": 0,
    "blood_in_mucus": 0,
    "Fatigue": 0,
    "Fever": 0,
    "Dehydration": 0,
    "loss_of_appetite": 0,
    "cramping": 0,
    "blood_in_stool": 0,
    "gnawing": 0,
    "upper_abdomain_pain": 1,
    "fullness_feeling": 1,
    "hiccups": 0,
    "abdominal_bloating": 1,
    "heartburn": 1,
    "belching": 1,
    "burning_ache": 1,
}


# ============================================================
# 6. BUILD LANGGRAPH INPUT STATE
# ============================================================

initial_state = {
    "user_input": patient_profile,
    "patient_profile": patient_profile,

    "questionnaire_answers": questionnaire_answers,
    "answers": questionnaire_answers,

    "vikriti_answers": vikriti_answers,

    "agni_answers": agni_answers,

    "disease_symptoms": disease_symptoms,

    "plan_days": 1,
}


# ============================================================
# 7. RUN COMPLETE LANGGRAPH
# ============================================================

print()
print("============================================================")
print("STARTING AYURGENIX FULL LANGGRAPH TEST")
print("============================================================")
print()

result = graph.invoke(initial_state)

from src.services.pdf_report import AyurGenixPDFReport

pdf_generator = AyurGenixPDFReport()

pdf_path = pdf_generator.generate(
    result,
    filename="AyurGenix_Wellness_Report.pdf"
)

print("\n" + "=" * 60)
print("PDF REPORT GENERATED")
print("=" * 60)
print(f"PDF Path: {pdf_path}")



# ============================================================
# 8. CHECK RESULTS
# ============================================================

print()
print("============================================================")
print("LANGGRAPH EXECUTION COMPLETED")
print("============================================================")


# Disease screening
disease_result = result.get(
    "disease_screening_result"
)

if disease_result:

    screening = disease_result.get(
        "screening_result",
        {}
    )

    print()
    print("DISEASE SCREENING")
    print("----------------------------")
    print(
        "Predicted condition:",
        screening.get("predicted_condition")
    )
    print(
        "Model probability:",
        screening.get("confidence")
    )
    print(
        "Status:",
        screening.get("screening_status")
    )

else:

    print()
    print("WARNING: Disease screening result not found.")


# Prakriti
prakriti = result.get(
    "prakriti_result",
    {}
)

print()
print("PRAKRITI")
print("----------------------------")
print(
    "Constitution:",
    prakriti.get("constitution")
)
print(
    "Primary:",
    prakriti.get("primary_dosha")
)
print(
    "Secondary:",
    prakriti.get("secondary_dosha")
)


# Vikriti
vikriti = result.get(
    "vikriti_result",
    {}
)

print()
print("VIKRITI")
print("----------------------------")
print(
    "Dominant Dosha:",
    vikriti.get("dominant_dosha")
)
print(
    "Scores:",
    vikriti.get("scores")
)


# Agni
agni = result.get(
    "agni_result",
    {}
)

print()
print("AGNI")
print("----------------------------")
print(
    "Status:",
    agni.get("status")
)
print(
    "Category Scores:",
    agni.get("category_scores")
)


# Diet
meal_plan = result.get(
    "meal_plan"
)

print()
print("DIET PLAN")
print("----------------------------")

if meal_plan:
    print("Diet plan generated successfully.")
else:
    print("WARNING: Diet plan not found.")


# Lifestyle
lifestyle = result.get(
    "lifestyle_plan"
)

print()
print("LIFESTYLE")
print("----------------------------")

if lifestyle:
    print("Lifestyle plan generated successfully.")
else:
    print("WARNING: Lifestyle plan not found.")


# Final response
final_response = result.get(
    "final_response"
)

print()
print("FINAL RESPONSE")
print("----------------------------")

if final_response:

    print("Final report generated successfully.")

else:

    print("WARNING: Final response not generated.")


# ============================================================
# 9. PRINT COMPLETE REPORT
# ============================================================

print()
print()
print("============================================================")
print("COMPLETE AYURGENIX REPORT")
print("============================================================")
print()

if final_response:
    import sys
    try:
        print(final_response)
    except UnicodeEncodeError:
        safe = final_response.encode(sys.stdout.encoding or "utf-8", errors="replace").decode(sys.stdout.encoding or "utf-8")
        print(safe)

print()
print("============================================================")
print("TEST FINISHED")
print("============================================================")
