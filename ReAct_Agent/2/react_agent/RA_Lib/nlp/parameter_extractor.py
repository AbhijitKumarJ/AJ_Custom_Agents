# Parameter extraction implementation

import re
from ..utils.logger import Logger

class ParameterExtractor:
    @staticmethod
    def extract_parameters(user_input: str, action: str) -> dict:
        Logger.log("Extracting parameters", {"action": action, "input": user_input})
        parameters = {}
        
        if action in ["get_weather", "ask_time"]:
            location_match = re.search(r"in\s+(.+)(?:\?|$)", user_input.lower())
            if location_match:
                parameters["location"] = location_match.group(1).strip()
        
        Logger.log("Extracted parameters", parameters)
        return parameters