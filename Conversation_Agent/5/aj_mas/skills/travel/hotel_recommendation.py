from ..base_skill import BaseSkill
from ..skill_loader import register_skill
from aj_mas.utils import logger
import random

@register_skill
class HotelRecommendationSkill(BaseSkill):
    def __init__(self):
        super().__init__("HotelRecommendationSkill", "Recommend hotels based on preferences")

    def execute(self, parameters: dict) -> dict:
        destination = parameters.get('destination')
        check_in = parameters.get('check_in')
        check_out = parameters.get('check_out')
        guests = parameters.get('guests', 1)
        preferences = parameters.get('preferences', [])

        logger.log(f"Searching hotels in {destination} from {check_in} to {check_out} for {guests} guests")
        
        # Simulate hotel search
        hotels = self._search_hotels(destination, check_in, check_out, guests)
        recommended_hotel = self._recommend_hotel(hotels, preferences)

        result = {
            "available_hotels": hotels,
            "recommended_hotel": recommended_hotel
        }
        self.log_execution(parameters, result)
        return result

    def _search_hotels(self, destination, check_in, check_out, guests):
        # In a real implementation, this would call a hotel booking API
        hotel_names = ["Grand Plaza", "Sunset Resort", "City View Inn", "Riverside Hotel", "Mountain Lodge"]
        return [
            {
                "name": random.choice(hotel_names),
                "rating": round(random.uniform(3, 5), 1),
                "price_per_night": round(random.uniform(50, 300), 2),
                "amenities": random.sample(["WiFi", "Pool", "Gym", "Restaurant", "Bar", "Spa"], random.randint(2, 5))
            }
            for _ in range(5)
        ]

    def _recommend_hotel(self, hotels, preferences):
        # Simple recommendation based on rating and matching preferences
        return max(hotels, key=lambda x: (x['rating'] + len(set(x['amenities']) & set(preferences))))