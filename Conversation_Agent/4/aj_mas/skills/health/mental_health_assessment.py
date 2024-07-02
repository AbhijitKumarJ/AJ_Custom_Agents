from ..base_skill import BaseSkill
from ..skill_loader import register_skill
from aj_mas.utils import logger
import random

@register_skill
class MentalHealthAssessmentSkill(BaseSkill):
    def __init__(self):
        super().__init__("MentalHealthAssessmentSkill", "Assess mental health and provide resources")

    def execute(self, parameters: dict) -> dict:
        mood = parameters.get('mood')
        stress_level = parameters.get('stress_level')
        sleep_quality = parameters.get('sleep_quality')
        recent_life_events = parameters.get('recent_life_events', [])

        logger.log(f"Assessing mental health: mood - {mood}, stress level - {stress_level}, sleep quality - {sleep_quality}")
        
        assessment = self._assess_mental_health(mood, stress_level, sleep_quality, recent_life_events)

        result = {"mental_health_assessment": assessment}
        self.log_execution(parameters, result)
        return result

    def _assess_mental_health(self, mood, stress_level, sleep_quality, recent_life_events):
        # In a real implementation, this would use validated psychological assessments and more comprehensive analysis
        mood_score = {"excellent": 5, "good": 4, "neutral": 3, "poor": 2, "very poor": 1}.get(mood.lower(), 3)
        stress_score = {"low": 1, "medium": 2, "high": 3}.get(stress_level.lower(), 2)
        sleep_score = {"good": 3, "fair": 2, "poor": 1}.get(sleep_quality.lower(), 2)

        overall_score = mood_score + (3 - stress_score) + sleep_score

        if overall_score <= 5:
            status = "Concerning"
            recommendations = [
                "Consider speaking with a mental health professional",
                "Practice stress-reduction techniques like meditation",
                "Prioritize sleep and establish a consistent sleep schedule"
            ]
        elif overall_score <= 8:
            status = "Fair"
            recommendations = [
                "Incorporate regular exercise into your routine",
                "Practice mindfulness or relaxation techniques",
                "Reach out to friends or family for support"
            ]
        else:
            status = "Good"
            recommendations = [
                "Maintain your current positive habits",
                "Consider starting a gratitude journal",
                "Explore new hobbies or activities"
            ]

        return {
            "overall_status": status,
            "mood_assessment": f"Your mood is {mood}",
            "stress_assessment": f"Your stress level is {stress_level}",
            "sleep_assessment": f"Your sleep quality is {sleep_quality}",
            "life_events_impact": "Recent life events may be affecting your mental health" if recent_life_events else "No significant recent life events noted",
            "recommendations": recommendations,
            "resources": [
                "National Mental Health Hotline: 1-800-XXX-XXXX",
                "www.mentalhealth.gov",
                "Local community mental health center"
            ],
            "disclaimer": "This assessment is not a substitute for professional medical advice, diagnosis, or treatment."
        }