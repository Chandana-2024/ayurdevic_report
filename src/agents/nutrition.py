from pathlib import Path
from typing import Any

from src.food_retriever import load_food_dataset


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_CSV_PATH = (
    PROJECT_ROOT / "data" / "ayurvedic_food_dishes_dataset_large.csv"
)

NUTRIENT_COLUMNS = {
    "calories": "Calories",
    "protein_g": "Protein_g",
    "carbohydrates_g": "Carbs_g",
    "fat_g": "Fat_g",
    "fiber_g": "Fiber_g",
}


def nutrition_agent(state: dict[str, Any]) -> dict:
    """
    Reads nutrition fields from the CSV schema.

    It does not invent nutrient targets or calculate meal totals because
    the current dataset has no serving-size or quantity information.
    """
    csv_path = Path(state.get("food_dataset_path", DEFAULT_CSV_PATH))
    food_df = load_food_dataset(csv_path)

    available_nutrients = {
        output_name: csv_column
        for output_name, csv_column in NUTRIENT_COLUMNS.items()
        if csv_column in food_df.columns
    }

    missing_nutrients = [
        output_name
        for output_name, csv_column in NUTRIENT_COLUMNS.items()
        if csv_column not in food_df.columns
    ]

    nutrition_notes = [
        "Nutrition values are read only from the food dataset.",
        "Daily nutrition totals are unavailable until serving sizes "
        "or quantities are added to the meal plan.",
    ]

    if missing_nutrients:
        nutrition_notes.append(
            "Unavailable nutrition fields: "
            + ", ".join(missing_nutrients)
            + "."
        )

    nutrition_context = {
        "source": "food_dataset",
        "daily_targets": {
            "calories": None,
            "protein_g": None,
            "carbohydrates_g": None,
            "fat_g": None,
            "fiber_g": None,
        },
        "available_nutrients": available_nutrients,
        "missing_nutrients": missing_nutrients,
        "constraints": [],
        "nutrition_notes": nutrition_notes,
    }

    return {
        "nutrition_context": nutrition_context,
    }