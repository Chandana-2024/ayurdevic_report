from typing import Dict


DOSHAS = ("Vata", "Pitta", "Kapha")


# ============================================================
# PRAKRITI SCORING
# ============================================================

def score_prakriti(answers: Dict[int, str]) -> dict:
    """
    Score Prakriti answers.

    Expected input:

    {
        1: "Vata",
        2: "Pitta",
        3: "Vata"
    }

    Each selected Dosha receives +1.
    """

    expected_ids = set(range(1, 22))
    received_ids = set(answers)
    if received_ids != expected_ids:
        raise ValueError(
            "Please provide answers for all 21 Prakriti questions. "
            f"Missing: {sorted(expected_ids - received_ids)}; "
            f"extra: {sorted(received_ids - expected_ids)}."
        )

    scores = {dosha: 0 for dosha in DOSHAS}

    for question_id, selected_dosha in answers.items():

        selected_dosha = str(selected_dosha).strip().title()

        if selected_dosha not in DOSHAS:
            raise ValueError(
                f"Invalid Prakriti answer for question "
                f"{question_id}: {selected_dosha}"
            )

        scores[selected_dosha] += 1

    total_answers = sum(scores.values())

    if total_answers == 0:
        raise ValueError("No Prakriti answers were provided.")

    ranked_doshas = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    primary_dosha = ranked_doshas[0][0]
    secondary_dosha = ranked_doshas[1][0]

    percentages = {
        dosha: round(
            (score / total_answers) * 100,
            1
        )
        for dosha, score in scores.items()
    }

    return {
        "scores": scores,
        "percentages": percentages,
        "primary_dosha": primary_dosha,
        "secondary_dosha": secondary_dosha,
        "total_answers": total_answers,
    }


# ============================================================
# PRAKRITI CONSTITUTION
# ============================================================

def get_constitution(
    dosha_result: dict,
    mixed_difference: int = 2
) -> str:
    """
    Determine single or mixed Prakriti.

    If the difference between the highest and second-highest
    scores is <= mixed_difference, return a mixed constitution.
    """

    scores = dosha_result["scores"]

    ranked_doshas = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    primary_name, primary_score = ranked_doshas[0]
    secondary_name, secondary_score = ranked_doshas[1]

    if primary_score - secondary_score <= mixed_difference:
        return f"{primary_name}-{secondary_name}"

    return primary_name


# ============================================================
# VIKRITI SCORING
# ============================================================

def score_vikriti(answers: Dict[str, int]) -> dict:
    """
    Score Vikriti answers.

    Each Vikriti question belongs to a specific Dosha.

    Response values:
        1 = Not at all
        3 = Somewhat / Occasionally
        5 = Very often

    Example:

    {
        "V1": 5,
        "V2": 3,
        "V3": 1,
        "P1": 5
    }
    """

    scores = {
        "Vata": 0,
        "Pitta": 0,
        "Kapha": 0
    }

    for question_id, score_data in answers.items():

        if not isinstance(score_data, dict):
            raise ValueError(
                f"Invalid Vikriti answer format for {question_id}"
            )

        dosha = score_data["dosha"]
        score = score_data["score"]

        if dosha not in DOSHAS:
            raise ValueError(
                f"Invalid Dosha for {question_id}: {dosha}"
            )

        if score not in (1, 3, 5):
            raise ValueError(
                f"Invalid Vikriti score for {question_id}: {score}. "
                "Expected 1, 3, or 5."
            )

        scores[dosha] += score

    if not answers:
        raise ValueError("No Vikriti answers were provided.")

    return {
        "scores": scores,
        "questions_answered": len(answers),
        "maximum_score_per_dosha": 35,
        "minimum_score_per_dosha": 7,
    }


# ============================================================
# VIKRITI DOMINANT DOSHA
# ============================================================

def get_vikriti_dominance(vikriti_result: dict) -> dict:

    scores = vikriti_result["scores"]

    ranked = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    primary = ranked[0]
    secondary = ranked[1]

    return {
        "primary": primary[0],
        "primary_score": primary[1],
        "secondary": secondary[0],
        "secondary_score": secondary[1],
        "scores": scores
    }

# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

def score_dosha(answers: Dict[int, str]) -> dict:
    """
    Backward-compatible wrapper.

    Existing parts of the project use score_dosha().
    Internally we now use score_prakriti().
    """
    return score_prakriti(answers)

def score_vikriti(answers: dict[str, int]) -> dict:
    """
    Deterministic Vikriti scoring.

    Each Vikriti question has a score:
        1 = Not at all
        3 = Somewhat / Occasionally
        5 = Very often

    Answers are grouped by:
        V1-V7 -> Vata
        P1-P7 -> Pitta
        K1-K7 -> Kapha
    """

    scores = {
        "Vata": 0,
        "Pitta": 0,
        "Kapha": 0,
    }

    expected_ids = {
        "V1", "V2", "V3", "V4", "V5", "V6", "V7",
        "P1", "P2", "P3", "P4", "P5", "P6", "P7",
        "K1", "K2", "K3", "K4", "K5", "K6", "K7",
    }

    received_ids = set(answers.keys())

    if received_ids != expected_ids:
        missing = sorted(expected_ids - received_ids)
        extra = sorted(received_ids - expected_ids)

        message = "Please provide answers for all 21 Vikriti questions."

        if missing:
            message += f" Missing: {missing}."

        if extra:
            message += f" Invalid extra IDs: {extra}."

        raise ValueError(message)

    for question_id, score in answers.items():

        if score not in {1, 3, 5}:
            raise ValueError(
                f"Invalid score for Vikriti question {question_id}. "
                "Expected 1, 3, or 5."
            )

        if question_id.startswith("V"):
            scores["Vata"] += score

        elif question_id.startswith("P"):
            scores["Pitta"] += score

        elif question_id.startswith("K"):
            scores["Kapha"] += score

    dominant_dosha = max(scores, key=scores.get)

    return {
        "scores": scores,
        "dominant_dosha": dominant_dosha,
        "total_questions": len(answers),
        "assessment_method": "deterministic_21_question_vikriti_scoring",
    }
def score_agni(answers: dict[str, int]) -> dict:
    """
    Score the 11-item Agnibala self-assessment tool.

    Source:
    Singh A, Singh G, Patwardhan K, Gehlot S. (2017)
    Development, Validation, and Verification of a Self-Assessment
    Tool to Estimate Agnibala (Digestive Strength).

    Published scoring:
    1 = Mandagni
    2 = Vishamagni
    3 = Samagni
    4 = Tikshnagni

    The selected response identifies the Agni category.
    Scores are accumulated category-wise and converted to
    percentages using the maximum possible score for each category.

    Maximum scores:
    Mandagni = 11
    Vishamagni = 11
    Samagni = 11
    Tikshnagni = 10
    """

    expected_ids = {
        "A1", "A2", "A3", "A4", "A5",
        "A6", "A7", "A8", "A9", "A10", "A11"
    }

    received_ids = set(answers.keys())

    if received_ids != expected_ids:
        missing = expected_ids - received_ids
        extra = received_ids - expected_ids

        raise ValueError(
            f"Invalid Agni answers. "
            f"Missing: {sorted(missing)} "
            f"Extra: {sorted(extra)}"
        )

    # Each response belongs to one Agni category.
    category_scores = {
        "Mandagni": 0,
        "Vishamagni": 0,
        "Samagni": 0,
        "Tikshnagni": 0,
    }

    response_scores = {}

    tikshnagni_ids = expected_ids - {"A8"}

    for question_id, score in answers.items():

        allowed_scores = {1, 2, 3, 4} if question_id in tikshnagni_ids else {1, 2, 3}
        if score not in allowed_scores:
            raise ValueError(
                f"Invalid score for {question_id}: {score}. "
                f"Allowed scores are {sorted(allowed_scores)}."
            )

        response_scores[question_id] = score

        if score == 1:
            category_scores["Mandagni"] += 1

        elif score == 2:
            category_scores["Vishamagni"] += 1

        elif score == 3:
            category_scores["Samagni"] += 1

        elif score == 4:
            category_scores["Tikshnagni"] += 1

    # Maximum possible scores from the validated tool.
    maximum_scores = {
        "Mandagni": 11,
        "Vishamagni": 11,
        "Samagni": 11,
        "Tikshnagni": 10,
    }

    category_percentages = {
        category: round(
            (category_scores[category] / maximum_scores[category]) * 100,
            2
        )
        for category in category_scores
    }

    maximum_percentage = max(category_percentages.values())

    dominant_agni_states = [
        category
        for category, percentage in category_percentages.items()
        if percentage == maximum_percentage
    ]

    # Do not invent a tie-breaking rule.
    if len(dominant_agni_states) == 1:
        agni_status = dominant_agni_states[0]
    else:
        agni_status = "Tie"

    total_score = sum(answers.values())

    return {
        "response_scores": response_scores,

        "category_scores": category_scores,

        "category_percentages": category_percentages,

        "maximum_scores": maximum_scores,

        "dominant_agni_states": dominant_agni_states,

        "status": agni_status,

        "total_score": total_score,

        "total_questions": len(answers),

        "assessment_method": (
            "Singh et al. 2017 validated "
            "Agnibala self-assessment scoring"
        ),

        "source": (
            "Singh A, Singh G, Patwardhan K, Gehlot S. "
            "Development, Validation, and Verification of a "
            "Self-Assessment Tool to Estimate Agnibala "
            "(Digestive Strength), 2017."
        ),
    }
