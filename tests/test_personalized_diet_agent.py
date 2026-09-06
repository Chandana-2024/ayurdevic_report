from src.agents.personalized_diet_agent import (
    PersonalizedDietAgent
)


patient_profile = {
    "name": "Demo User",
    "age": 20,
    "gender": "female",
    "height_cm": 160,
    "weight_kg": 55,

    "dietary_preference": "vegan",

    "allergies": [
        "onion"
    ],

    "foods_to_avoid": [
        "capsicum"
    ],

    "health_conditions": [],

    "goal": "general wellness",
}


# This represents Agent 1 output
ayurvedic_assessment = {

    "prakriti": {
        "primary_dosha": "Pitta",
        "secondary_dosha": "Vata",
        "constitution": "Pitta-Vata",
    },

    "vikriti": {
        "dominant_dosha": "Pitta",
    },

    "agni": {
        "status": "Mandagni",
    },
}


# Create Agent 2
agent = PersonalizedDietAgent()


# Generate personalized diet
result = agent.generate_diet(
    patient_profile,
    ayurvedic_assessment
)


print("\n==============================")
print("AYURGENIX — AGENT 2")
print("PERSONALIZED DIET PLAN")
print("==============================")


print(
    f"\nStatus: {result['status']}"
)


print("\nNUTRITION TARGET")

print(
    f"Calories: "
    f"{result['nutrition_target']['calories']}"
)

print(
    f"Protein: "
    f"{result['nutrition_target']['protein_g']} g"
)

print(
    f"Carbs: "
    f"{result['nutrition_target']['carbs_g']} g"
)

print(
    f"Fat: "
    f"{result['nutrition_target']['fat_g']} g"
)

print(
    f"Fiber: "
    f"{result['nutrition_target']['fiber_g']} g"
)


print("\nMEAL PLAN")


for meal_name, meal in result["diet_plan"].items():

    print(f"\n{meal_name.upper()}")

    print(
        f"Target: "
        f"{meal['target_calories']} kcal"
    )

    print(
        f"Actual: "
        f"{meal['actual_calories']} kcal"
    )

    print(
        f"Difference: "
        f"{meal['calorie_difference']} kcal"
    )

    for food in meal["foods"]:

        print(
            f" - {food['food_name']} "
            f"| {food['portion_g']} g "
            f"| {food['calories']} kcal "
            f"| Score: {food['ranking_score']}"
        )


print("\nVALIDATION")

print(
    f"Overall valid: "
    f"{result['validation']['valid']}"
)


print("\nEXCLUDED FOODS")

print(
    f"Total excluded: "
    f"{len(result['excluded_foods'])}"
)