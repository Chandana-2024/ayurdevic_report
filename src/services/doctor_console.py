"""Local doctor review interface; it does not authenticate a clinical identity."""
from copy import deepcopy
import json
from pathlib import Path

from src.services.report_validation import validate_report_state
from src.services.report_workflow import final_content


def review_content(state, review):
    """Provide editable structured content and show the exact result before sign-off."""
    def edit(label, current):
        print(f"\n{label}:\n{json.dumps(current, indent=2, ensure_ascii=True)}")
        while True:
            value = input(f"Replacement {label} JSON (blank keeps current): ").strip()
            if not value:
                return deepcopy(current)
            try:
                parsed = json.loads(value)
                if not isinstance(parsed, dict):
                    raise ValueError("Expected a JSON object")
                return parsed
            except (ValueError, TypeError) as error:
                print(f"Invalid edit: {error}")

    state["patient_profile"] = edit("patient profile", state.get("patient_profile") or {})
    for key in ("prakriti_result", "vikriti_result", "agni_result"):
        state[key] = edit(key, state.get(key) or {})
    review["edited_diet_plan"] = edit("diet plan (add/remove foods or change portions)", state.get("agent2_output") or {"diet_plan": state.get("meal_plan") or {}})
    review["edited_lifestyle_recommendations"] = edit("lifestyle recommendations", state.get("lifestyle_plan") or {})
    review["medicines"] = []
    while input("Add a doctor-entered medicine/prescription? (yes/no): ").strip().lower() == "yes":
        medicine = {key: input(f"Medicine {key}: ").strip() or None for key in ("name", "dosage", "frequency", "duration", "instructions")}
        medicine["doctor_approval_status"] = "DOCTOR APPROVED"
        medicine["source"] = "DOCTOR_ENTERED"
        review["medicines"].append(medicine)
    state["doctor_review"] = review
    print("\nAI-GENERATED — DOCTOR REVIEW REQUIRED\n")
    print(json.dumps(final_content(state), indent=2, ensure_ascii=True))
    warnings = validate_report_state(state)["warnings"]
    review["validation_reviewed"] = not warnings or input("Have you reviewed every displayed validation warning? (yes/no): ").strip().lower() == "yes"
    decision = input("Decision (approve / reject / changes): ").strip().lower()
    review["decision"] = {"approve": "APPROVED", "reject": "REJECTED"}.get(decision, "CHANGES_REQUIRED")
    review["approved"] = decision == "approve"
    review["signature"] = input("Doctor sign-off name for this exact content: ").strip() or None
    return review


def save_session(state, directory="reports"):
    """Persist locally using a session-specific, atomically replaced JSON record."""
    root = Path(directory)
    root.mkdir(parents=True, exist_ok=True)
    path = root / f"session_{state['session_id']}.json"
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(state, indent=2, ensure_ascii=True, allow_nan=False), encoding="utf-8")
    temporary.replace(path)
    return path


def main():
    """Resume a saved local session for a later doctor review."""
    import argparse
    from src.main import get_doctor_review
    from src.services.report_workflow import TwoReportWorkflow
    from src.services.two_report_pdf import TwoReportPDFGenerator
    parser = argparse.ArgumentParser(description="Resume a local doctor review")
    parser.add_argument("session_file", type=Path)
    args = parser.parse_args()
    state = json.loads(args.session_file.read_text(encoding="utf-8"))
    for key in ("answers", "questionnaire_answers"):
        if key in state:
            state[key] = {int(k): v for k, v in state[key].items()}
    flow = TwoReportWorkflow(state)
    flow.begin_doctor_review()
    review = get_doctor_review(state)
    if review.get("approved") is True:
        try:
            flow.approve(review)
            path = TwoReportPDFGenerator(str(args.session_file.parent)).generate_final_report(state, f"Final_Personalized_Wellness_Report_{flow.session_id}.pdf")
            print(f"DOCTOR APPROVED: {path}")
        except (ValueError, PermissionError) as error:
            flow.request_changes()
            print(f"DOCTOR VERIFICATION REQUIRED: {error}")
    else:
        flow.request_changes()
        print("DOCTOR VERIFICATION REQUIRED")
    save_session(state, str(args.session_file.parent))


if __name__ == "__main__":
    main()
