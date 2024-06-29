# Weather action implementation

import requests
from ..utils.logger import Logger
from ..config import WEATHER_API_KEY

class WeatherAction:
    def execute(self, params: dict) -> str:
        location = params.get('location', 'your area')
        Logger.log("Generating weather response", {"location": location})
        
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API_KEY}&units=metric"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200:
                temp = data['main']['temp']
                description = data['weather'][0]['description']
                return f"The weather in {location} is {description} with a temperature of {temp}°C."
            else:
                return f"I'm sorry, I couldn't fetch the weather information for {location}."
        except Exception as e:
            Logger.log("Error fetching weather data", {"error": str(e)})
            return f"I'm having trouble getting the weather information right now. Please try again later."