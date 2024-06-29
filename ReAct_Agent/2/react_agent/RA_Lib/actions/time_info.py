# Time action implementation

from datetime import datetime
import pytz
from ..utils.logger import Logger

class TimeAction:
    def execute(self, params: dict) -> str:
        location = params.get('location', 'UTC')
        Logger.log("Providing current time", {"location": location})
        
        try:
            tz = pytz.timezone(location)
            current_time = datetime.now(tz).strftime("%I:%M %p")
            return f"The current time in {location} is {current_time}."
        except pytz.exceptions.UnknownTimeZoneError:
            return f"I'm sorry, I don't have timezone information for {location}. The current UTC time is {datetime.utcnow().strftime('%I:%M %p')}."
        except Exception as e:
            Logger.log("Error fetching time data", {"error": str(e)})
            return "I'm having trouble getting the time information right now. Please try again later."