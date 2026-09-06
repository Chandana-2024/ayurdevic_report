from typing import Any, Literal, TypedDict

from langgraph.graph import END, START, StateGraph

from src.agents.conditions import condition_agent
from src.agents.diet_planning import diet_planning_agent
from src.agents.final_response import final_response_agent
from src.agents.food_retrieval import food_retrieval_agent
from src.agents.intake import intake_profile_agent
from src.agents.nutrition import nutrition_agent
from src.agents.prakriti import prakriti_analysis_agent
from src.agents.safety import safety_fact_checker_agent
from src.agents.vikriti import vikriti_analysis_agent
from src.agents.agni import agni_analysis_agent


class DietPlanningState(TypedDict, total=False):
    user_input: dict[str, Any]

    answers: dict[int, str]
    questionnaire_answers: dict[int, str]

    vikriti_answers: dict[str, int]

    plan_days: int
    food_dataset_path: str

    patient_profile: dict[str, Any]

    prakriti_result: dict[str, Any]
    vikriti_result: dict[str, Any]
    agni_answers: dict[str, Any]
    agni_result: dict[str, Any]
    ayurvedic_assessment: dict[str, Any]
    dosha_result: dict[str, Any]
    constitution: str

    nutrition_context: dict[str, Any]
    condition_context: dict[str, Any]

    food_candidates: list[dict[str, Any]]
    food_retrieval_context: dict[str, Any]

    meal_plan: dict[str, Any]
    lifestyle_plan: dict[str, Any]
    validation_result: dict[str, Any]

    final_response: str
    errors: list[str]


def review_response_agent(state: DietPlanningState) -> dict:
    """
    Safe response when validation needs review.
    The meal plan is intentionally not displayed.
    """
    validation_result = state.get("validation_result", {})

    response_lines = [
        "PLAN REVIEW REQUIRED",
        "",
        "A final diet plan was not shown because one or more "
        "validation checks require review.",
        "",
        "Validation checks:",
    ]

    for check_name, status in validation_result.get("checks", {}).items():
        response_lines.append(f"- {check_name}: {status}")

    warnings = validation_result.get("warnings", [])
    failed_checks = validation_result.get("failed_checks", [])

    if warnings:
        response_lines.extend(["", "Warnings:"])
        response_lines.extend(f"- {warning}" for warning in warnings)

    if failed_checks:
        response_lines.extend(["", "Failed checks:"])
        response_lines.extend(
            f"- {failed_check}"
            for failed_check in failed_checks
        )

    response_lines.extend([
        "",
        "Please review the missing safety information or modify the "
        "profile before generating a plan.",
    ])

    return {
        "final_response": "\n".join(response_lines),
    }


from src.agents.lifestyle import lifestyle_agent


def route_after_safety(
    state: DietPlanningState,
) -> Literal["lifestyle_agent", "review_response"]:
    """Route safely based on the fact-checker result."""
    validation_result = state.get("validation_result", {})

    if validation_result.get("status") in {"PASS", "REVIEW_REQUIRED"}:
        return "lifestyle_agent"

    return "review_response"


# Build the multi-agent LangGraph workflow.
builder = StateGraph(DietPlanningState)

builder.add_node("intake_profile_agent", intake_profile_agent)
builder.add_node("prakriti_analysis_agent", prakriti_analysis_agent)
builder.add_node("vikriti_analysis_agent", vikriti_analysis_agent)
builder.add_node("agni_agent", agni_analysis_agent)
builder.add_node("nutrition_agent", nutrition_agent)
builder.add_node("condition_agent", condition_agent)
builder.add_node("food_retrieval_agent", food_retrieval_agent)
builder.add_node("diet_planning_agent", diet_planning_agent)
builder.add_node("safety_fact_checker_agent", safety_fact_checker_agent)
builder.add_node("lifestyle_agent", lifestyle_agent)
builder.add_node("final_response", final_response_agent)
builder.add_node("review_response", review_response_agent)


builder.add_edge(START, "intake_profile_agent")
builder.add_edge("intake_profile_agent", "prakriti_analysis_agent")
builder.add_edge("prakriti_analysis_agent", "vikriti_analysis_agent")
builder.add_edge("vikriti_analysis_agent", "agni_agent")
builder.add_edge("agni_agent", "nutrition_agent")
builder.add_edge("nutrition_agent", "condition_agent")
builder.add_edge("condition_agent", "food_retrieval_agent")
builder.add_edge("food_retrieval_agent", "diet_planning_agent")
builder.add_edge("diet_planning_agent", "safety_fact_checker_agent")

builder.add_conditional_edges(
    "safety_fact_checker_agent",
    route_after_safety,
    {
        "lifestyle_agent": "lifestyle_agent",
        "review_response": "review_response",
    },
)

builder.add_edge("lifestyle_agent", "final_response")
builder.add_edge("final_response", END)
builder.add_edge("review_response", END)

graph = builder.compile()