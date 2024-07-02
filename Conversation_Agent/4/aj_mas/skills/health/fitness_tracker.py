from ..base_skill import BaseSkill
from ..skill_loader import register_skill
from aj_mas.utils import logger
import random

@register_skill
class FitnessTrackerSkill(BaseSkill):
    def __init__(self):
        super().__init__("FitnessTrackerSkill", "Track and analyze fitness activities")

    def execute(self, parameters: dict) -> dict:
        activity_type = parameters.get('activity_type')
        duration = parameters.get('duration')
        intensity = parameters.get('intensity')
        user_stats = parameters.get('user_stats', {})

        logger.log(f"Tracking fitness activity: {activity_type} for {duration} minutes at {intensity} intensity")
        
        fitness_analysis = self._analyze_fitness_activity(activity_type, duration, intensity, user_stats)

        result = {"fitness_analysis": fitness_analysis}
        self.log_execution(parameters, result)
        return result

    def _analyze_fitness_activity(self, activity_type, duration, intensity, user_stats):
        # In a real implementation, this would use more accurate fitness formulas and personalized data
        calories_burned_per_minute = {
            "running": 11.4,
            "cycling": 7.5,
            "swimming": 8.3,
            "weightlifting": 6.0
        }.get(activity_type.lower(), 5.0)  # Default to 5.0 for unknown activities

        intensity_multiplier = {"low": 0.8, "medium": 1.0, "high": 1.2}.get(intensity.lower(), 1.0)
        total_calories_burned = calories_burned_per_minute * duration * intensity_multiplier

        return {
            "activity_summary": {
                "type": activity_type,
                "duration": duration,
                "intensity": intensity
            },
            "calories_burned": round(total_calories_burned, 2),
            "health_impact": {
                "cardiovascular": random.choice(["Improved", "Maintained", "Slightly improved"]),
                "muscular": random.choice(["Strengthened", "Toned", "Maintained"]),
                "flexibility": random.choice(["Increased", "Maintained", "Slightly improved"])
            },
            "recommendation": f"Great job on your {activity_type}! Consider increasing duration or intensity for more benefits.",
            "next_goal_suggestion": f"Try to reach {round(duration * 1.1)} minutes in your next {activity_type} session."
        }