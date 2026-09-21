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
from src.agents.lifestyle import lifestyle_agent
from src.agents.disease_screening_agent import disease_screening_agent


# ============================================================
# LANGGRAPH STATE
# ============================================================

class DietPlanningState(TypedDict, total=False):
    """Common patient_state: one profile, stable assessment answers and results.

    user_input and answers remain legacy input aliases; new callers use
    patient_profile and questionnaire_answers. Agent/report snapshots remain
    compatibility outputs, not independently editable patient records.
    """
    agent2_output: dict[str, Any]
    diet_timetable: dict[str, Any]
    doctor_review: dict[str, Any]
    review_validation: dict[str, Any]
    approved_snapshot: dict[str, Any]
    final_report: dict[str, Any]
    final_report_version: int
    final_report_id: str
    session_id: str
    patient_id: str
    assessment_report: dict[str, Any]
    assessment_pdf_path: str
    workflow_status: str
    # --------------------------------------------------------
    # User input
    # --------------------------------------------------------
    user_input: dict[str, Any]

    # --------------------------------------------------------
    # Ayurvedic Prakriti questionnaire
    # --------------------------------------------------------
    answers: dict[int, str]
    questionnaire_answers: dict[int, str]

    # --------------------------------------------------------
    # Ayurvedic Vikriti questionnaire
    # --------------------------------------------------------
    vikriti_answers: dict[str, int]

    # --------------------------------------------------------
    # Agni questionnaire
    # --------------------------------------------------------
    agni_answers: dict[str, Any]

    # --------------------------------------------------------
    # Disease screening
    # --------------------------------------------------------
    # 31 AYUCARE symptom features.
    #
    # Example:
    # {
    #     "acidity": 1,
    #     "indigestion": 0,
    #     "headache": 1,
    #     ...
    # }
    #
    # 0 = symptom absent
    # 1 = symptom present
    # --------------------------------------------------------
    disease_symptoms: dict[str, int]

    disease_screening_result: dict[str, Any]

    # --------------------------------------------------------
    # Diet plan settings
    # --------------------------------------------------------
    plan_days: int
    food_dataset_path: str

    # --------------------------------------------------------
    # Patient profile
    # --------------------------------------------------------
    patient_profile: dict[str, Any]

    # --------------------------------------------------------
    # Ayurvedic assessment results
    # --------------------------------------------------------
    prakriti_result: dict[str, Any]
    vikriti_result: dict[str, Any]
    agni_result: dict[str, Any]

    ayurvedic_assessment: dict[str, Any]
    dosha_result: dict[str, Any]
    constitution: str

    # --------------------------------------------------------
    # Nutrition and condition context
    # --------------------------------------------------------
    nutrition_context: dict[str, Any]
    condition_context: dict[str, Any]

    # --------------------------------------------------------
    # Food pipeline
    # --------------------------------------------------------
    food_candidates: list[dict[str, Any]]
    food_retrieval_context: dict[str, Any]

    # --------------------------------------------------------
    # Diet / lifestyle
    # --------------------------------------------------------
    meal_plan: dict[str, Any]
    lifestyle_plan: dict[str, Any]
    validation_result: dict[str, Any]

    # --------------------------------------------------------
    # Final response
    # --------------------------------------------------------
    final_response: str

    # --------------------------------------------------------
    # Errors
    # --------------------------------------------------------
    errors: list[str]


# ============================================================
# REVIEW RESPONSE
# ============================================================

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
        response_lines.extend(
            f"- {warning}"
            for warning in warnings
        )

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


# ============================================================
# DISEASE SCREENING ROUTER
# ============================================================

def route_after_intake(
    state: DietPlanningState,
) -> Literal["disease_screening_agent", "prakriti_analysis_agent"]:
    """
    Decide whether AYUCARE disease screening should run.

    Disease screening is OPTIONAL.

    If the user provides the 31 disease symptoms,
    the Disease Screening Agent runs.

    If symptoms are not provided, the existing AyurGenix
    workflow continues directly to Prakriti assessment.
    """

    disease_symptoms = state.get("disease_symptoms")

    if disease_symptoms:
        return "disease_screening_agent"

    return "prakriti_analysis_agent"


# ============================================================
# SAFETY ROUTER
# ============================================================

def route_after_safety(
    state: DietPlanningState,
) -> Literal["lifestyle_agent", "review_response"]:
    """
    Route safely based on the fact-checker result.
    """

    validation_result = state.get("validation_result", {})

    if validation_result.get("status") in {
        "PASS",
        "REVIEW_REQUIRED",
    }:
        return "lifestyle_agent"

    return "review_response"


# ============================================================
# BUILD LANGGRAPH
# ============================================================

builder = StateGraph(DietPlanningState)


def assessment_report_node(state):
    from src.services.report_workflow import TwoReportWorkflow
    from src.services.two_report_pdf import TwoReportPDFGenerator
    working = dict(state)
    flow = TwoReportWorkflow(working)
    path = TwoReportPDFGenerator().generate_assessment_report(working, f"AI_Assessment_Report_{flow.session_id}.pdf")
    return {"session_id": flow.session_id, "patient_id": working["patient_id"], "assessment_report": working["assessment_report"],
            "assessment_pdf_path": path, "workflow_status": working["workflow_status"]}


builder.add_node("assessment_report", assessment_report_node)
from src.services.diet_presentation import diet_presentation_agent
builder.add_node("diet_presentation", diet_presentation_agent)


def pending_doctor_review_node(state):
    from src.services.report_workflow import TwoReportWorkflow
    working = dict(state)
    TwoReportWorkflow(working).begin_doctor_review()
    return {"review_validation": working["review_validation"],
            "workflow_status": working["workflow_status"]}


builder.add_node("pending_doctor_review", pending_doctor_review_node)


# ------------------------------------------------------------
# Add nodes
# ------------------------------------------------------------

builder.add_node(
    "intake_profile_agent",
    intake_profile_agent,
)

builder.add_node(
    "disease_screening_agent",
    disease_screening_agent,
)

builder.add_node(
    "prakriti_analysis_agent",
    prakriti_analysis_agent,
)

builder.add_node(
    "vikriti_analysis_agent",
    vikriti_analysis_agent,
)

builder.add_node(
    "agni_agent",
    agni_analysis_agent,
)

builder.add_node(
    "nutrition_agent",
    nutrition_agent,
)

builder.add_node(
    "condition_agent",
    condition_agent,
)

builder.add_node(
    "food_retrieval_agent",
    food_retrieval_agent,
)

builder.add_node(
    "diet_planning_agent",
    diet_planning_agent,
)

builder.add_node(
    "safety_fact_checker_agent",
    safety_fact_checker_agent,
)

builder.add_node(
    "lifestyle_agent",
    lifestyle_agent,
)

builder.add_node(
    "final_response",
    final_response_agent,
)

builder.add_node(
    "review_response",
    review_response_agent,
)


# ============================================================
# GRAPH EDGES
# ============================================================

# ------------------------------------------------------------
# START → Intake
# ------------------------------------------------------------

builder.add_edge(
    START,
    "intake_profile_agent",
)


# ------------------------------------------------------------
# Intake → Disease Screening OR Prakriti
# ------------------------------------------------------------

builder.add_conditional_edges(
    "intake_profile_agent",
    route_after_intake,
    {
        "disease_screening_agent": "disease_screening_agent",
        "prakriti_analysis_agent": "prakriti_analysis_agent",
    },
)


# ------------------------------------------------------------
# Disease Screening → Prakriti
# ------------------------------------------------------------

builder.add_edge(
    "disease_screening_agent",
    "prakriti_analysis_agent",
)


# ------------------------------------------------------------
# Ayurvedic Assessment Pipeline
# ------------------------------------------------------------

builder.add_edge(
    "prakriti_analysis_agent",
    "vikriti_analysis_agent",
)

builder.add_edge(
    "vikriti_analysis_agent",
    "agni_agent",
)

builder.add_edge(
    "agni_agent",
    "assessment_report",
)
builder.add_edge("assessment_report", "nutrition_agent")

builder.add_edge(
    "nutrition_agent",
    "condition_agent",
)

builder.add_edge(
    "condition_agent",
    "food_retrieval_agent",
)

builder.add_edge(
    "food_retrieval_agent",
    "diet_planning_agent",
)

builder.add_edge(
    "diet_planning_agent",
    "diet_presentation",
)
builder.add_edge("diet_presentation", "safety_fact_checker_agent")


# ============================================================
# SAFETY → LIFESTYLE OR REVIEW
# ============================================================

builder.add_conditional_edges(
    "safety_fact_checker_agent",
    route_after_safety,
    {
        "lifestyle_agent": "lifestyle_agent",
        "review_response": "review_response",
    },
)


# ============================================================
# FINAL RESPONSE
# ============================================================

builder.add_edge(
    "lifestyle_agent",
    "final_response",
)

builder.add_edge(
    "final_response",
    "pending_doctor_review",
)

builder.add_edge(
    "review_response",
    "pending_doctor_review",
)
builder.add_edge("pending_doctor_review", END)


# ============================================================
# COMPILE GRAPH
# ============================================================

graph = builder.compile()
