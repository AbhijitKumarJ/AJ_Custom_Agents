from aj_mas.skills import BaseSkill, register_skill
from aj_mas.utils import logger
import random

@register_skill
class LocalAttractionSkill(BaseSkill):
    def __init__(self):
        super().__init__("LocalAttractionSkill", "Find and recommend local attractions")

    def execute(self, parameters: dict) -> dict:
        destination = parameters.get('destination')
        interests = parameters.get('interests', [])
        num_recommendations = parameters.get('num_recommendations', 5)

        logger.log(f"Finding attractions in {destination} based on interests: {interests}")
        
        # Simulate attraction search
        attractions = self._search_attractions(destination, interests)
        recommended_attractions = self._recommend_attractions(attractions, num_recommendations)

        result = {
            "all_attractions": attractions,
            "recommended_attractions": recommended_attractions
        }
        self.log_execution(parameters, result)
        return result

    def _search_attractions(self, destination, interests):
        # In a real implementation, this would call a travel API or database
        attraction_types = ["Museum", "Park", "Historical Site", "Theater", "Restaurant", "Market", "Beach", "Mountain"]
        return [
            {
                "name": f"{random.choice(attraction_types)} {i+1}",
                "type": random.choice(attraction_types),
                "rating": round(random.uniform(3, 5), 1),
                "description": f"A wonderful {random.choice(attraction_types).lower()} in {destination}",
                "price": round(random.uniform(0, 50), 2)
            }
            for i in range(20)
        ]

    def _recommend_attractions(self, attractions, num_recommendations):
        # Simple recommendation based on rating
        return sorted(attractions, key=lambda x: x['rating'], reverse=True)[:num_recommendations]