from ..base_skill import BaseSkill
from ..skill_loader import register_skill
from aj_mas.utils import logger
import random

@register_skill
class ItineraryPlanningSkill(BaseSkill):
    def __init__(self):
        super().__init__("ItineraryPlanningSkill", "Plan travel itineraries")

    def execute(self, parameters: dict) -> dict:
        destination = parameters.get('destination')
        duration = parameters.get('duration')
        preferences = parameters.get('preferences', [])

        logger.log(f"Planning itinerary for {destination} for {duration} days")
        
        # Simulate itinerary planning
        activities = self._generate_activities(destination, duration, preferences)
        itinerary = self._create_itinerary(activities, duration)

        result = {"itinerary": itinerary}
        self.log_execution(parameters, result)
        return result

    def _generate_activities(self, destination, duration, preferences):
        # In a real implementation, this would fetch data from a travel API
        sample_activities = [
            "Visit historical landmarks", "Try local cuisine", "Relax at the beach",
            "Go hiking", "Explore museums", "Attend cultural events",
            "Go shopping", "Take a guided tour", "Visit parks and gardens"
        ]
        return random.sample(sample_activities, min(len(sample_activities), duration * 2))

    def _create_itinerary(self, activities, duration):
        itinerary = {}
        for day in range(1, duration + 1):
            itinerary[f"Day {day}"] = random.sample(activities, min(len(activities), 3))
        return itinerary