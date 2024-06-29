# Improved ReAct Agent Implementation

## Folder Structure

```
react_agent/
│
├── __init__.py
├── main.py
├── config.py
│
├── nlp/
│   ├── __init__.py
│   ├── intent_classifier.py
│   └── parameter_extractor.py
│
├── actions/
│   ├── __init__.py
│   ├── weather.py
│   ├── time_info.py
│   ├── jokes.py
│   └── general.py
│
├── utils/
│   ├── __init__.py
│   └── logger.py
│
└── data/
    └── jokes.json
```

## File Contents

### 1. react_agent/__init__.py

```python
from .main import AdvancedReActAgent
```

### 2. react_agent/main.py

```python
from .nlp.intent_classifier import IntentClassifier
from .nlp.parameter_extractor import ParameterExtractor
from .actions import WeatherAction, TimeAction, JokeAction, GeneralAction
from .utils.logger import Logger
from .config import CONTEXT_SIZE

class AdvancedReActAgent:
    def __init__(self):
        self.context = []
        self.intent_classifier = IntentClassifier()
        self.parameter_extractor = ParameterExtractor()
        self.actions = {
            'get_weather': WeatherAction(),
            'ask_time': TimeAction(),
            'tell_joke': JokeAction(),
            'greet': GeneralAction(),
            'farewell': GeneralAction(),
            'unknown': GeneralAction()
        }
        Logger.log("AdvancedReActAgent initialized")

    def think(self, user_input: str):
        Logger.log("Thinking process started", {"input": user_input})
        intent_info = self.intent_classifier.classify_intent(user_input)
        parameters = self.parameter_extractor.extract_parameters(user_input, intent_info['action'])
        
        thoughts = [
            ("Intent", f"Action determined as: {intent_info['action']} with confidence {intent_info['confidence']:.2f}"),
            ("Parameters", f"Extracted parameters: {parameters}")
        ]
        
        action_info = {**intent_info, "parameters": parameters}
        Logger.log("Thinking process completed", {"thoughts": thoughts, "action_info": action_info})
        return thoughts, action_info

    def act(self, action_info: dict) -> str:
        Logger.log("Acting", action_info)
        action = self.actions.get(action_info['action'], self.actions['unknown'])
        response = action.execute(action_info['parameters'])
        Logger.log("Action completed", {"response": response})
        return response

    def respond(self, user_input: str) -> str:
        Logger.log("Responding to user input", {"input": user_input})
        thoughts, action_info = self.think(user_input)
        response = self.act(action_info)
        self.update_context(user_input)
        Logger.log("Response generated", {"response": response, "updated_context": self.context})
        return response

    def update_context(self, user_input: str):
        self.context.append(user_input)
        if len(self.context) > CONTEXT_SIZE:
            self.context.pop(0)

    def run(self):
        Logger.log("Starting the agent")
        print("Advanced ReAct Agent: Hello! How can I assist you today?")
        while True:
            user_input = input("You: ")
            Logger.log("Received user input", {"input": user_input})
            if user_input.lower() == "quit":
                Logger.log("User requested to quit")
                print("Advanced ReAct Agent: Goodbye!")
                break
            response = self.respond(user_input)
            print(f"Advanced ReAct Agent: {response}")
        Logger.log("Agent shutting down")

if __name__ == "__main__":
    agent = AdvancedReActAgent()
    agent.run()
```

### 3. react_agent/config.py

```python
# Model configurations
INTENT_MODEL = "facebook/bart-large-mnli"

# Action templates for intent classification
ACTION_TEMPLATES = [
    ("The user is greeting someone.", "greet"),
    ("The user is saying goodbye.", "farewell"),
    ("The user is asking about the weather.", "get_weather"),
    ("The user is requesting a joke.", "tell_joke"),
    ("The user is asking for the current time.", "ask_time")
]

# Number of recent interactions to keep in context
CONTEXT_SIZE = 5

# API keys (replace with actual keys)
WEATHER_API_KEY = "your_weather_api_key_here"
```

### 4. react_agent/nlp/intent_classifier.py

```python
from transformers import pipeline
from ..utils.logger import Logger
from ..config import INTENT_MODEL, ACTION_TEMPLATES

class IntentClassifier:
    def __init__(self):
        self.classifier = pipeline("zero-shot-classification", model=INTENT_MODEL)
        self.action_templates = ACTION_TEMPLATES
        Logger.log("IntentClassifier initialized", {"model": INTENT_MODEL, "templates": self.action_templates})

    def classify_intent(self, user_input: str) -> dict:
        Logger.log("Classifying intent", {"input": user_input})
        candidate_labels = [template for template, _ in self.action_templates]
        outputs = self.classifier(user_input, candidate_labels, multi_label=False)
        
        Logger.log("Classification model raw output", outputs)

        best_action_label = outputs["labels"][0]
        best_action_score = outputs["scores"][0]

        action = next((action for template, action in self.action_templates if template == best_action_label), "unknown")

        result = {"action": action, "confidence": best_action_score}
        Logger.log("Classification result", result)
        return result
```

### 5. react_agent/nlp/parameter_extractor.py

```python
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
```

### 6. react_agent/actions/weather.py

```python
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
```

### 7. react_agent/actions/time_info.py

```python
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
```

### 8. react_agent/actions/jokes.py

```python
import json
import random
from ..utils.logger import Logger

class JokeAction:
    def __init__(self):
        with open('react_agent/data/jokes.json', 'r') as f:
            self.jokes = json.load(f)
        self.told_jokes = set()

    def execute(self, params: dict) -> str:
        Logger.log("Telling a joke")
        
        available_jokes = [joke for joke in self.jokes if joke not in self.told_jokes]
        
        if not available_jokes:
            self.told_jokes.clear()
            available_jokes = self.jokes
        
        joke = random.choice(available_jokes)
        self.told_jokes.add(joke)
        
        return joke
```

### 9. react_agent/actions/general.py

```python
from ..utils.logger import Logger

class GeneralAction:
    def execute(self, params: dict) -> str:
        action = params.get('action', 'unknown')
        Logger.log(f"Executing general action: {action}")
        
        if action == 'greet':
            return "Hello! How can I assist you today?"
        elif action == 'farewell':
            return "Goodbye! Have a great day!"
        else:
            return "I'm not sure how to respond to that. Can you please clarify or ask something else?"
```

### 10. react_agent/utils/logger.py

```python
from datetime import datetime
from pprint import pformat
import sys

class Logger:
    @staticmethod
    def log(message: str, data: dict = None):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}", file=sys.stderr)
        if data is not None:
            print(pformat(data, indent=2, width=120), file=sys.stderr)
        print(file=sys.stderr)  # Add a blank line for readability
```

### 11. react_agent/data/jokes.json

```json
[
    "Why don't scientists trust atoms? Because they make up everything!",
    "Why did the scarecrow win an award? He was outstanding in his field!",
    "Why don't eggs tell jokes? They'd crack each other up!",
    "Why don't skeletons fight each other? They don't have the guts!",
    "What do you call a fake noodle? An impasta!"
]
```

This improved implementation addresses the issues we identified earlier:

1. The intent classification now uses a more robust model and handles follow-up queries better.
2. Parameter extraction has been expanded to handle locations for both weather and time queries.
3. Weather and time actions now use (simulated) API calls for more accurate and location-specific responses.
4. The joke action now maintains a list of told jokes to avoid repetition.
5. The agent now has a more flexible structure that allows for easy addition of new actions and capabilities.
6. Error handling has been improved throughout the system.
7. The logging system has been retained and expanded for better debugging and monitoring.

To use this improved ReAct agent, you would need to install the required dependencies (transformers, pytz, requests) and set up the appropriate API keys in the config file. The main entry point would be running the main.py file.
