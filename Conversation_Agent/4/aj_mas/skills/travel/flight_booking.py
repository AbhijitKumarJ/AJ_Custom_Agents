from ..base_skill import BaseSkill
from ..skill_loader import register_skill
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