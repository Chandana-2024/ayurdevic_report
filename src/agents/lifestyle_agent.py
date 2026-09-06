from typing import Any
from src.rag.rag_service import AyurvedaRAGService

class LifestyleAgent:

    def __init__(self):
        self.rag_service = AyurvedaRAGService()

    def generate_lifestyle_plan(
        self,
        patient_profile: dict[str, Any],
        ayurvedic_assessment: dict[str, Any],
    ) -> dict[str, Any]:

        prakriti = ayurvedic_assessment.get("prakriti", {})
        vikriti = ayurvedic_assessment.get("vikriti", {})
        agni = ayurvedic_assessment.get("agni", {})

        primary_dosha = prakriti.get("primary_dosha")
        secondary_dosha = prakriti.get("secondary_dosha")
        dominant_vikriti = vikriti.get("dominant_dosha")
        agni_status = agni.get("status")

        rag_query = (
            f"Ayurvedic lifestyle recommendations for "
            f"{primary_dosha} Prakriti, "
            f"{dominant_vikriti} Vikriti, "
            f"{agni_status} Agni. "
            f"Include Dinacharya, sleep, exercise, meal timing, "
            f"stress management and seasonal routine."
        )

        rag_evidence = self.rag_service.retrieve(
            query=rag_query,
            k=5,
        )

        plan = {
            "daily_routine": self._daily_routine(
                primary_dosha,
                dominant_vikriti,
            ),

            "sleep": self._sleep_routine(
                primary_dosha,
                dominant_vikriti,
            ),

            "meal_timing": self._meal_timing(
                agni_status,
            ),

            "physical_activity": self._physical_activity(
                primary_dosha,
                dominant_vikriti,
            ),

            "stress_management": self._stress_management(
                primary_dosha,
                dominant_vikriti,
            ),

            "seasonal_routine": self._seasonal_routine(
                primary_dosha,
                dominant_vikriti,
            ),
        }

        return {
            "agent": "Lifestyle / Wellness Agent",

            "patient_profile": patient_profile,

            "ayurvedic_assessment": {
                "prakriti": prakriti,
                "vikriti": vikriti,
                "agni": agni,
            },

            "lifestyle_plan": plan,

            "rag_evidence": rag_evidence,

            "status": "generated",
        }

    # ---------------------------------------------------------
    # DAILY ROUTINE
    # ---------------------------------------------------------

    @staticmethod
    def _daily_routine(
        primary_dosha,
        dominant_vikriti,
    ):

        recommendations = [
            "Maintain a consistent daily routine.",
            "Keep regular timings for waking, meals and sleep.",
            "Avoid frequently changing the daily schedule.",
        ]

        if dominant_vikriti == "vata":
            recommendations.extend([
                "Prefer a calm and stable daily routine.",
                "Avoid excessive irregularity and overexertion.",
            ])

        elif dominant_vikriti == "pitta":
            recommendations.extend([
                "Include adequate relaxation and breaks.",
                "Avoid excessive heat and overexertion.",
            ])

        elif dominant_vikriti == "kapha":
            recommendations.extend([
                "Maintain an active daily routine.",
                "Avoid excessive daytime inactivity.",
            ])

        return recommendations

    # ---------------------------------------------------------
    # SLEEP
    # ---------------------------------------------------------

    @staticmethod
    def _sleep_routine(
        primary_dosha,
        dominant_vikriti,
    ):

        recommendations = [
            "Maintain a consistent sleep and wake schedule.",
            "Keep the sleeping environment comfortable and calm.",
            "Reduce stimulating activities before bedtime.",
        ]

        if dominant_vikriti == "vata":
            recommendations.append(
                "Give particular importance to regular sleep timing."
            )

        elif dominant_vikriti == "pitta":
            recommendations.append(
                "Allow sufficient time for relaxation before sleep."
            )

        elif dominant_vikriti == "kapha":
            recommendations.append(
                "Avoid excessive daytime sleeping and inactivity."
            )

        return recommendations

    # ---------------------------------------------------------
    # MEAL TIMING
    # ---------------------------------------------------------

    @staticmethod
    def _meal_timing(agni_status):

        recommendations = [
            "Maintain regular meal timings.",
            "Avoid unnecessarily skipping meals.",
            "Allow adequate time between meals.",
        ]

        if agni_status == "Vishamagni":
            recommendations.extend([
                "Prefer consistent meal timing.",
                "Avoid highly irregular eating patterns.",
            ])

        elif agni_status == "Mandagni":
            recommendations.extend([
                "Avoid repeatedly eating when previous meals have not been digested.",
                "Prefer appropriate meal spacing.",
            ])

        elif agni_status == "Tikshnagni":
            recommendations.extend([
                "Avoid unnecessarily prolonged gaps between meals.",
            ])

        elif agni_status == "Samagni":
            recommendations.append(
                "Continue maintaining regular meal timing."
            )

        return recommendations

    # ---------------------------------------------------------
    # PHYSICAL ACTIVITY
    # ---------------------------------------------------------

    @staticmethod
    def _physical_activity(
        primary_dosha,
        dominant_vikriti,
    ):

        recommendations = [
            "Include regular physical activity appropriate to individual capacity.",
            "Avoid sudden excessive increases in exercise intensity.",
        ]

        if dominant_vikriti == "vata":
            recommendations.extend([
                "Prefer gentle to moderate and consistent activity.",
                "Avoid excessive physical exhaustion.",
            ])

        elif dominant_vikriti == "pitta":
            recommendations.extend([
                "Avoid excessive exercise in very hot conditions.",
                "Include adequate recovery after activity.",
            ])

        elif dominant_vikriti == "kapha":
            recommendations.extend([
                "Regular moderate activity can help maintain an active routine.",
                "Avoid prolonged inactivity.",
            ])

        return recommendations

    # ---------------------------------------------------------
    # STRESS MANAGEMENT
    # ---------------------------------------------------------

    @staticmethod
    def _stress_management(
        primary_dosha,
        dominant_vikriti,
    ):

        recommendations = [
            "Include relaxation time in the daily routine.",
            "Use calming activities such as breathing practices or meditation.",
            "Maintain a balanced work, study and rest schedule.",
        ]

        if dominant_vikriti == "vata":
            recommendations.append(
                "Prefer grounding and calming activities."
            )

        elif dominant_vikriti == "pitta":
            recommendations.append(
                "Include activities that support relaxation and cooling."
            )

        elif dominant_vikriti == "kapha":
            recommendations.append(
                "Include stimulating and engaging activities to avoid excessive inactivity."
            )

        return recommendations

    # ---------------------------------------------------------
    # SEASONAL ROUTINE
    # ---------------------------------------------------------

    @staticmethod
    def _seasonal_routine(
        primary_dosha,
        dominant_vikriti,
    ):

        return [
            "Adjust daily activity and routine according to season and environmental conditions.",
            "Pay attention to changes in temperature, weather and activity requirements.",
            "Use the Ayurvedic knowledge base to provide season-specific recommendations.",
        ]