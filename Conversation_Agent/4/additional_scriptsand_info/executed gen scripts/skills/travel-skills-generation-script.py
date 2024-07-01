import os

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def write_file(path, content):
    with open(path, 'w') as f:
        f.write(content)
    print(f"Created file: {path}")

def create_travel_skills():
    travel_dir = "aj_mas/skills/travel"
    create_directory(travel_dir)

    # __init__.py
    init_content = """
from .itinerary_planning import ItineraryPlanningSkill
from .flight_booking import FlightBookingSkill
from .hotel_recommendation import HotelRecommendationSkill
from .local_attraction import LocalAttractionSkill
"""
    write_file(os.path.join(travel_dir, "__init__.py"), init_content.strip())

    # itinerary_planning.py
    itinerary_planning_content = """
from aj_mas.skills import BaseSkill, register_skill
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
"""
    write_file(os.path.join(travel_dir, "itinerary_planning.py"), itinerary_planning_content.strip())

    # flight_booking.py
    flight_booking_content = """
from aj_mas.skills import BaseSkill, register_skill
from aj_mas.utils import logger
import random

@register_skill
class FlightBookingSkill(BaseSkill):
    def __init__(self):
        super().__init__("FlightBookingSkill", "Search and book flights")

    def execute(self, parameters: dict) -> dict:
        origin = parameters.get('origin')
        destination = parameters.get('destination')
        date = parameters.get('date')
        passengers = parameters.get('passengers', 1)

        logger.log(f"Searching flights from {origin} to {destination} on {date} for {passengers} passengers")
        
        # Simulate flight search
        flights = self._search_flights(origin, destination, date, passengers)
        recommended_flight = self._recommend_flight(flights)

        result = {
            "available_flights": flights,
            "recommended_flight": recommended_flight
        }
        self.log_execution(parameters, result)
        return result

    def _search_flights(self, origin, destination, date, passengers):
        # In a real implementation, this would call a flight booking API
        airlines = ["AirMax", "SkyHigh", "EagleWings", "OceanAir"]
        return [
            {
                "airline": random.choice(airlines),
                "flight_number": f"FL{random.randint(100, 999)}",
                "departure_time": f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}",
                "arrival_time": f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}",
                "price": round(random.uniform(200, 1000), 2)
            }
            for _ in range(5)
        ]

    def _recommend_flight(self, flights):
        # Simple recommendation based on price
        return min(flights, key=lambda x: x['price'])
"""
    write_file(os.path.join(travel_dir, "flight_booking.py"), flight_booking_content.strip())

    # hotel_recommendation.py
    hotel_recommendation_content = """
from aj_mas.skills import BaseSkill, register_skill
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
"""
    write_file(os.path.join(travel_dir, "hotel_recommendation.py"), hotel_recommendation_content.strip())

    # local_attraction.py
    local_attraction_content = """
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
"""
    write_file(os.path.join(travel_dir, "local_attraction.py"), local_attraction_content.strip())

if __name__ == "__main__":
    create_travel_skills()
    print("AJ_MAS travel skills created successfully!")
