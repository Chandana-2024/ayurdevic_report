from pathlib import Path
from typing import Any

from src.agents.diet_context import prepare_diet_context
from src.agents.food_filter import FoodFilter
from src.agents.food_ranking import FoodRanker
from src.agents.diet_validation import DietValidator
from src.services.food_repository import FoodRepository
from src.services.nutrition_calculator import calculate_energy_target

# Retry logic for validation loop
MAX_RETRIES = 3


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_CSV_PATH = PROJECT_ROOT / "data" / "ayurvedic_food_dishes_dataset_large.csv"

MEAL_STRUCTURE = ("Breakfast", "Lunch", "Snack", "Dinner")
MEAL_CALORIE_DISTRIBUTION = {
    "Breakfast": 0.25,
    "Lunch": 0.35,
    "Snack": 0.10,
    "Dinner": 0.30,
}


def build_single_day_plan(
    day_number: int,
    ranked_candidates: list[dict[str, Any]],
    target_daily_calories: float,
) -> dict[str, Any]:
    """
    Builds a single day meal plan with 4 meals (Breakfast, Lunch, Snack, Dinner),
    calculating realistic portions and exact nutrition sums.
    """
    if not ranked_candidates:
        raise ValueError("No eligible food candidates available for meal plan generation.")

    # Select foods with candidate rotation per day to provide variety
    foods_per_day = 10
    start_idx = ((day_number - 1) * foods_per_day) % len(ranked_candidates)

    day_pool = [
        ranked_candidates[(start_idx + i) % len(ranked_candidates)]
        for i in range(min(foods_per_day, len(ranked_candidates)))
    ]

    breakfast_pool = day_pool[0:2] or day_pool[0:1]
    lunch_pool = day_pool[2:5] or day_pool[0:2]
    snack_pool = day_pool[5:6] or day_pool[0:1]
    dinner_pool = day_pool[6:9] or day_pool[0:2]

    meal_pools = {
        "Breakfast": breakfast_pool,
        "Lunch": lunch_pool,
        "Snack": snack_pool,
        "Dinner": dinner_pool,
    }

    day_meals = []
    day_cals = 0.0
    day_protein = 0.0
    day_carbs = 0.0
    day_fat = 0.0

    for meal_name in MEAL_STRUCTURE:
        pool = meal_pools[meal_name]
        target_meal_cals = target_daily_calories * MEAL_CALORIE_DISTRIBUTION[meal_name]

        scaled_meal_foods = fit_meal_portions_to_target(
            meal_foods=pool,
            target_meal_calories=target_meal_cals,
        )

        meal_cals = sum(f["nutrition"]["calories"] for f in scaled_meal_foods)
        meal_p = sum(f["nutrition"]["protein_g"] for f in scaled_meal_foods)
        meal_c = sum(f["nutrition"]["carbs_g"] for f in scaled_meal_foods)
        meal_f = sum(f["nutrition"]["fat_g"] for f in scaled_meal_foods)

        day_cals += meal_cals
        day_protein += meal_p
        day_carbs += meal_c
        day_fat += meal_f

        day_meals.append({
            "meal": meal_name,
            "foods": scaled_meal_foods,
            "meal_total": {
                "calories": round(meal_cals, 1),
                "protein_g": round(meal_p, 1),
                "carbs_g": round(meal_c, 1),
                "fat_g": round(meal_f, 1),
            },
        })

    return {
        "day": day_number,
        "meals": day_meals,
        "daily_total": {
            "calories": round(day_cals, 1),
            "protein_g": round(day_protein, 1),
            "carbs_g": round(day_carbs, 1),
            "fat_g": round(day_fat, 1),
        },
    }


def diet_planning_agent(state: dict[str, Any]) -> dict[str, Any]:
    """
    Agent 2: Personalized Ayurvedic Diet Agent.
    Orchestrates Context Preparation, Target Calculation, Hard Filtering,
    Ayurvedic Ranking, Portion Scaling, Validation, and Re-planning retry loop.
    """
    # 1. Prepare standardized context
    context_res = prepare_diet_context(state)
    patient_profile = context_res["patient_profile"]
    ayurvedic_assessment = context_res["ayurvedic_assessment"]

    plan_days = int(state.get("plan_days") or 7)
    if plan_days not in (1, 7):
        plan_days = 7

    # 2. Nutrition Energy Targets (Mifflin-St Jeor)
    energy_target = calculate_energy_target(patient_profile)
    target_cals = float(energy_target.get("target_calories") or 2000.0)

    # 3. Load dataset
    csv_path = Path(state.get("food_dataset_path", DEFAULT_CSV_PATH))
    repository = FoodRepository(csv_path)

    prakriti_const = ayurvedic_assessment["prakriti"]["constitution"]
    raw_df = repository.get_compatible_foods(constitution=prakriti_const, limit=150)
    raw_candidates = [repository.to_candidate_record(idx, row) for idx, row in raw_df.iterrows()]

    # 4. Hard Safety Filters
    # Convert to format expected by FoodFilter
    filter_engine = FoodFilter()
    eligible_candidates, excluded_foods = filter_engine.filter_foods(
        foods=raw_candidates,
        patient_profile=patient_profile,
    )

    # Extract exclusion logs for output
    excluded_log = [
        {"food_name": f["food_name"], "reason": f.get("reason", "Safety filter")}
        for f in excluded_foods
    ]
    quality_warnings = []

    if not eligible_candidates:
        raise ValueError("No food candidates remain after applying hard safety filters.")

    # 5. Transparent Ayurvedic Ranking
    ranker = FoodRanker()
    ranked_candidates = ranker.rank_foods(
        foods=eligible_candidates,
        ayurvedic_assessment=ayurvedic_assessment,
        patient_profile=patient_profile,
    )

    # 6. Re-planning Retry Loop
    attempt = 0
    final_plan_days = []
    val_res = {}

    while attempt < MAX_RETRIES:
        attempt += 1
        current_days = []
        for d in range(1, plan_days + 1):
            day_plan = build_single_day_plan(
                day_number=d,
                ranked_candidates=ranked_candidates,
                target_daily_calories=target_cals,
            )
            current_days.append(day_plan)

        candidate_diet_plan = {
            "duration_days": plan_days,
            "daily_target": {
                "calories": target_cals,
                "protein_g": energy_target.get("target_protein_g", 0),
                "carbs_g": energy_target.get("target_carbs_g", 0),
                "fat_g": energy_target.get("target_fat_g", 0),
            },
            "days": current_days,
        }

        # Convert plan to meal-level format for validation
        meal_level_plan = {}
        for day in current_days:
            for meal_name, meal_data in day.items():
                if meal_name not in meal_level_plan:
                    meal_level_plan[meal_name] = {
                        "target_calories": meal_data.get("target_calories"),
                        "actual_calories": meal_data.get("actual_calories", 0),
                        "foods": meal_data.get("foods", []),
                    }

        validator = DietValidator()
        val_res = validator.validate(
            diet_plan=meal_level_plan,
            patient_profile=patient_profile,
        )

        # Transform validator output to expected format
        if val_res.get("valid"):
            val_res["overall_status"] = "PASS"
            val_res["safety"] = "PASS"
        else:
            val_res["overall_status"] = "REVIEW_REQUIRED"
            val_res["safety"] = "FAIL"

        final_plan_days = current_days

        if val_res["overall_status"] == "PASS":
            break

    if val_res.get("overall_status") != "PASS":
        val_res["overall_status"] = "REVIEW_REQUIRED"

    # Collect unique sources
    unique_sources = []
    for candidate in ranked_candidates[:15]:
        for src in candidate.get("sources", []):
            if src not in unique_sources:
                unique_sources.append(src)

    formatted_output = {
        "diet_plan": {
            "duration_days": plan_days,
            "daily_target": {
                "calories": target_cals,
                "protein_g": energy_target.get("target_protein_g", 0),
                "carbs_g": energy_target.get("target_carbs_g", 0),
                "fat_g": energy_target.get("target_fat_g", 0),
            },
            "days": final_plan_days,
        },
        "validation": val_res,
        "sources": unique_sources,
        "warnings": quality_warnings,
        "excluded_foods_log": excluded_log,
    }

    return {
        "meal_plan": formatted_output["diet_plan"],
        "agent2_output": formatted_output,
        "validation_result": val_res,
    }