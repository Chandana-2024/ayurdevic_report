from pathlib import Path
from typing import Any

from src.services.food_repository import FoodRepository


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_CSV_PATH = (
    PROJECT_ROOT / "data" / "ayurvedic_food_dishes_dataset_large.csv"
)

NON_VEG_KEYWORDS = {
    "beef", "shrimp", "lobster", "fish", "mutton", "chicken", "pork", "egg",
    "meat", "salmon", "tuna", "prawn", "crab", "squid", "anchovy", "turkey",
    "lamb", "duck", "bacon", "ham"
}

DAIRY_KEYWORDS = {
    "milk", "cheese", "ghee", "butter", "curd", "paneer", "goat cheese",
    "honey", "yogurt", "malai", "dahi", "cream"
}


def normalize_food_name(value: str) -> str:
    return " ".join(str(value).strip().lower().split())


def is_non_vegetarian(food_name: str) -> bool:
    name_norm = normalize_food_name(food_name)
    return any(keyword in name_norm for keyword in NON_VEG_KEYWORDS)


def is_non_vegan(food_name: str) -> bool:
    name_norm = normalize_food_name(food_name)
    if is_non_vegetarian(food_name):
        return True
    return any(keyword in name_norm for keyword in DAIRY_KEYWORDS)


def score_food_candidate(
    candidate: dict[str, Any],
    primary_dosha: str,
    agni_status: str,
    goal: str,
    health_conditions: list[str],
) -> float:
    """
    Transparent rule-based Ayurvedic food ranking score.

    Source/Basis:
    - Primary Dosha Compatibility (Favor: +5, Neutral: +2, Avoid: -5)
    - Agni Adaptation (Mandagni favors Ushna/Tikta; Tikshnagni favors Shita)
    - Goal & Health Condition Matching
    """
    score = 0.0

    # 1. Dosha recommendation score
    recs = candidate.get("dosha_recommendations", {})
    primary_rec = str(recs.get(primary_dosha.lower(), "")).strip().title()

    if primary_rec == "Favor":
        score += 5.0
    elif primary_rec == "Neutral":
        score += 2.0
    elif primary_rec == "Avoid":
        score -= 5.0

    # 2. Agni adaptation
    attrs = candidate.get("ayurvedic_attributes", {})
    virya = str(attrs.get("virya", "")).strip().title()
    rasa = str(attrs.get("rasa", "")).strip().title()

    if agni_status == "Mandagni":
        if "Ushna" in virya:
            score += 2.0
        if "Tikta" in rasa or "Katu" in rasa:
            score += 1.5
    elif agni_status == "Tikshnagni":
        if "Shita" in virya:
            score += 2.0

    # 3. Health Conditions & Goal match
    conds_str = str(candidate.get("health_conditions", "")).lower()
    if goal and goal.lower() in conds_str:
        score += 3.0
    for cond in health_conditions:
        if cond and cond.lower() in conds_str:
            score += 2.0

    return score


def food_retrieval_agent(state: dict[str, Any]) -> dict:
    """
    Retrieves and ranks candidate foods from the CSV dataset.

    Hard Filters:
    - Allergies (hard exclusion)
    - Foods to avoid / Exclusions (hard exclusion)
    - Dietary preference (Vegetarian / Vegan / Non-vegetarian)
    - Unsafe health condition restrictions

    Transparent Ayurvedic Ranking:
    - Dosha compatibility + Agni status + Goal matching
    """
    prakriti_result = state.get("prakriti_result", {})
    constitution = prakriti_result.get(
        "constitution",
        state.get("constitution"),
    )
    primary_dosha = prakriti_result.get("primary_dosha") or "Vata"

    if not constitution:
        raise ValueError(
            "A Prakriti constitution is required before food retrieval."
        )

    patient_profile = state.get("patient_profile", {})
    exclusions = patient_profile.get("food_exclusions", [])
    foods_to_avoid = patient_profile.get("foods_to_avoid", [])
    allergies = patient_profile.get("allergies", [])
    dietary_preference = str(
        patient_profile.get("dietary_preference", "unspecified")
    ).strip().lower()

    health_conditions = patient_profile.get("health_conditions", [])
    goal = patient_profile.get("goal", "")
    agni_status = state.get("agni_result", {}).get("status", "Samagni")

    # Combine all explicit food name exclusions
    all_exclusions = list(dict.fromkeys(exclusions + foods_to_avoid))

    csv_path = Path(state.get("food_dataset_path", DEFAULT_CSV_PATH))
    repository = FoodRepository(csv_path)

    # Fetch larger candidate set from dataset for robust filtering
    raw_candidates = repository.get_compatible_foods(
        constitution=constitution,
        limit=150,
    )

    selected_candidates = []
    excluded_log = []

    for row_index, row in raw_candidates.iterrows():
        candidate = repository.to_candidate_record(row_index, row)
        food_name = candidate["name"]
        norm_name = normalize_food_name(food_name)

        # 1. Hard Exclusion Check
        excluded_by = None
        for excl in all_exclusions:
            if excl and normalize_food_name(excl) in norm_name:
                excluded_by = f"Explicit food exclusion ({excl})"
                break

        if not excluded_by:
            for allergy in allergies:
                if allergy and normalize_food_name(allergy) in norm_name:
                    excluded_by = f"Allergy match ({allergy})"
                    break

        # 2. Hard Dietary Preference Check
        if not excluded_by:
            if dietary_preference in ("vegetarian", "veg"):
                if is_non_vegetarian(food_name):
                    excluded_by = "Dietary preference violation (Non-vegetarian item)"
            elif dietary_preference == "vegan":
                if is_non_vegan(food_name):
                    excluded_by = "Dietary preference violation (Non-vegan item)"

        if excluded_by:
            excluded_log.append({
                "food_name": food_name,
                "reason": excluded_by,
            })
            continue

        # Score remaining candidate
        candidate["ayurvedic_rank_score"] = score_food_candidate(
            candidate=candidate,
            primary_dosha=primary_dosha,
            agni_status=agni_status,
            goal=goal,
            health_conditions=health_conditions,
        )

        selected_candidates.append(candidate)

    # Sort candidate list by transparent Ayurvedic rank score (descending)
    selected_candidates.sort(
        key=lambda item: item["ayurvedic_rank_score"],
        reverse=True,
    )

    if not selected_candidates:
        raise ValueError(
            "No compatible food candidates remain after applying "
            "hard patient constraints."
        )

    return {
        "food_candidates": selected_candidates,
        "food_retrieval_context": {
            "constitution": constitution,
            "primary_dosha": primary_dosha,
            "candidate_count": len(selected_candidates),
            "excluded_foods_log": excluded_log,
            "dietary_preference_applied": dietary_preference,
            "source": "food_dataset",
        },
    }