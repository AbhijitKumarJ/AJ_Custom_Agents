# Project Structure

```
5/
  aj_mas.log
  __init__.py
  requirements.txt
  main.py
  aj_mas/
    config.py
    __init__.py
    multi_agent_system.py
    constants.py
    tools/
      base_tool.py
      __init__.py
      tool_registry.py
      example_tool.py
      tool_loader.py
      tool_utils.py
      web_interaction/
        web_scraper_tool.py
        api_requester_tool.py
        __init__.py
        html_parser_tool.py
      file_handling/
        file_reader_tool.py
        __init__.py
        file_writer_tool.py
        CSV_To_JSON_tool.py
      language_processing/
        summarization_tool.py
        __init__.py
        translation_tool.py
        sentiment_analysis_tool.py
    skills/
      __init__.py
      base_skill.py
      skill_loader.py
      skill_registry.py
      example_skill.py
      travel/
        itinerary_planning.py
        flight_booking.py
        hotel_recommendation.py
        __init__.py
      health/
        diet_planner.py
        __init__.py
        symptom_checker.py
    document_store/
      fasttext_chroma_store.py
      __init__.py
      document_store.py
    utils/
      error_handler.py
      logger.py
      __init__.py
    agents/
      agent_factory.py
      __init__.py
      persona_based_agent.py
      base_agent.py
      specialized_agents.py
    config/
      skill_config.json
      agent_config.json
      config.json
      tool_config.json
    models/
      model_provider.py
      ollama_provider.py
      huggingface_provider.py
      __init__.py
    personas/
      persona.py
      __init__.py
      persona_loader.py
```

# File Contents

## aj_mas.log

```
[2024-07-02 23:19:46,751] INFO: Starting AJ_MAS system
[2024-07-02 23:19:46,752] INFO: Registered skill: ItineraryPlanningSkill
[2024-07-02 23:19:46,752] INFO: Registered skill: FlightBookingSkill
[2024-07-02 23:19:46,752] INFO: Registered skill: HotelRecommendationSkill
[2024-07-02 23:19:46,753] ERROR: ERROR: Failed to load skill: itinerary_planning{'error': "No module named 'aj_mas.skills.travel.local_attraction'"}
[2024-07-02 23:21:31,072] INFO: Starting AJ_MAS system
[2024-07-02 23:21:31,074] INFO: Registered skill: ItineraryPlanningSkill
[2024-07-02 23:21:31,074] INFO: Registered skill: FlightBookingSkill
[2024-07-02 23:21:31,074] INFO: Registered skill: HotelRecommendationSkill
[2024-07-02 23:25:55,188] INFO: Starting AJ_MAS system
[2024-07-02 23:25:55,189] INFO: Registered skill: ItineraryPlanningSkill
[2024-07-02 23:25:55,189] INFO: Registered skill: FlightBookingSkill
[2024-07-02 23:25:55,189] INFO: Registered skill: HotelRecommendationSkill
[2024-07-02 23:27:52,704] INFO: Starting AJ_MAS system
[2024-07-02 23:27:52,705] INFO: Registered skill: ItineraryPlanningSkill
[2024-07-02 23:27:52,705] INFO: Registered skill: FlightBookingSkill
[2024-07-02 23:27:52,706] INFO: Registered skill: HotelRecommendationSkill
[2024-07-02 23:28:42,744] INFO: Starting AJ_MAS system
[2024-07-02 23:28:42,745] INFO: Registered skill: ItineraryPlanningSkill
[2024-07-02 23:28:42,745] INFO: Registered skill: FlightBookingSkill
[2024-07-02 23:28:42,745] INFO: Registered skill: HotelRecommendationSkill
[2024-07-03 20:53:55,637] INFO: Starting AJ_MAS system
[2024-07-03 20:53:55,638] INFO: Registered skill: ItineraryPlanningSkill
[2024-07-03 20:53:55,639] INFO: Registered skill: FlightBookingSkill
[2024-07-03 20:53:55,639] INFO: Registered skill: HotelRecommendationSkill

```

## __init__.py

```

```

## requirements.txt

```
torch
transformers
pyyaml
requests
chromadb
fasttext
ollama
matplotlib
seaborn
pandas
pydub
SpeechRecognition
gTTS
numpy
scikit-learn
yake
spacy
statsmodels
beautifulsoup4
feedparser
```

## main.py

```
from aj_mas.multi_agent_system import run_aj_mas

if __name__ == "__main__":
    run_aj_mas()

```

## aj_mas/config.py

```
import json
import os


def load_config(config_path="aj_mas/config/config.json"):
    try:
        with open(config_path, "r") as config_file:
            config = json.load(config_file)
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in configuration file: {config_path}")


def get_config_value(key, default=None):
    config = load_config()
    return config.get(key, default)


def update_config(key, value, config_path="aj_mas/config/config.json"):
    config = load_config(config_path)
    config[key] = value
    with open(config_path, "w") as config_file:
        json.dump(config, config_file, indent=2)


# Default configuration
DEFAULT_CONFIG = {
    "system_name": "AJ_MAS",
    "version": "1.0.0",
    "log_level": "INFO",
    "max_concurrent_agents": 5,
    "model_providers": {
        "ollama": {
            "name": "qwen2:1.5b-instruct-q8_0",
            "api_url": "http://localhost:11434/api/generate",
        }
    },
    "document_store": {
        "type": "fasttext_chroma",
        "storage_dir": "aj_mas/document_storage",
        "fasttext_model": "cc.en.300.bin",
    },
    "agent_config_path": "aj_mas/config/agent_config.json",
    "skill_config_path": "aj_mas/config/skill_config.json",
    "tool_config_path": "aj_mas/config/tool_config.json",
    "api_rate_limit": 100,
    "session_timeout": 3600,
}


def ensure_config_file_exists(config_path="aj_mas/config/config.json"):
    if not os.path.exists(config_path):
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, "w") as config_file:
            json.dump(DEFAULT_CONFIG, config_file, indent=2)
        print(f"Created default configuration file: {config_path}")


# Ensure the config file exists when this module is imported
ensure_config_file_exists()

config = load_config()

```

## aj_mas/__init__.py

```
from .multi_agent_system import run_aj_mas
from .config import config, load_config
```

## aj_mas/multi_agent_system.py

```
from .agents import create_agent, get_available_agent_types
from .skills import load_skills
from .models import OllamaProvider
from .document_store import FastTextChromaStore
from .utils import logger
from .config import config, load_config
import sys


def initialize_system():
    #config = load_config()
    skills = load_skills()
    model_provider = OllamaProvider(config["model_provider"]["name"])
    document_store = FastTextChromaStore(config["document_store"]["storage_dir"])
    return skills, model_provider, document_store


def run_aj_mas():
    logger.log("Starting AJ_MAS system")
    skills, model_provider, document_store = initialize_system()

    while True:
        print("\nWelcome to AJ_MAS! Please choose an option:")
        print("1. Create an agent")
        print("2. List available agent types")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            agent_type = input("Enter the type of agent you want to create: ")
            agent = create_agent(
                agent_type,
                skills,
                model_provider,
                document_store,
                config["agent_config_path"],
            )
            if agent:
                user_id = input("Enter a user ID for this session: ")
                agent.start_session(user_id)
                while True:
                    task = input(
                        "Enter a task for the agent (or 'quit' to end session): "
                    )
                    if task.lower() == "quit":
                        break
                    response = agent.perform_task(task)
                    print(f"Agent response: {response}")
                agent.end_session()
        elif choice == "2":
            agent_types = get_available_agent_types()
            print(f"Available agent types: {', '.join(agent_types)}")
        elif choice == "3":
            print("Thank you for using AJ_MAS. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    run_aj_mas()

```

## aj_mas/constants.py

```
# System-wide constants

# Version
VERSION = "1.0.0"

# Skill Areas
SKILL_AREAS = [
    "TRAVEL",
    "FINANCE",
    "HEALTH",
    "TECHNOLOGY",
    "EDUCATION",
    "LEGAL",
    "GENERAL",
]

# Language Proficiency Levels
LANGUAGE_PROFICIENCY = {
    "NATIVE": 5,
    "FLUENT": 4,
    "ADVANCED": 3,
    "INTERMEDIATE": 2,
    "BASIC": 1,
}

# Maximum number of relevant documents to retrieve
MAX_RELEVANT_DOCUMENTS = 5

# Minimum proficiency level for specialized tasks
MIN_SPECIALIZED_PROFICIENCY = 0.7

# Default model parameters
DEFAULT_MAX_TOKENS = 100
DEFAULT_TEMPERATURE = 0.7

# API rate limiting
API_RATE_LIMIT = 100  # requests per minute
API_RATE_LIMIT_PERIOD = 60  # seconds

# Session timeout
SESSION_TIMEOUT = 3600  # 1 hour in seconds

```

## aj_mas/tools/base_tool.py

```
from abc import ABC, abstractmethod
from aj_mas.utils import logger

class BaseTool(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def execute(self, parameters: dict) -> dict:
        pass

    def log_execution(self, parameters: dict, result: dict):
        logger.log(f"Executed {self.name}", {
            "parameters": parameters,
            "result": result
        })

    def __str__(self):
        return f"{self.name}: {self.description}"
```

## aj_mas/tools/__init__.py

```
from .base_tool import BaseTool
from .tool_loader import load_tools, register_tool
from .tool_registry import ToolRegistry
from .tool_utils import chain_tools, parallel_execute, validate_tool_parameters, getToolClassNameFromConfigName
```

## aj_mas/tools/tool_registry.py

```
from typing import Dict, Type
from .base_tool import BaseTool

class ToolRegistry:
    tools: Dict[str, Type[BaseTool]] = {}

    @classmethod
    def register(cls, tool_class: Type[BaseTool]):
        cls.tools[tool_class.__name__] = tool_class

    @classmethod
    def get(cls, tool_name: str) -> Type[BaseTool]:
        return cls.tools.get(tool_name)

    @classmethod
    def list_tools(cls) -> list:
        return list(cls.tools.keys())
```

## aj_mas/tools/example_tool.py

```
from .base_tool import BaseTool
from .tool_loader import register_tool

@register_tool
class ExampleTool(BaseTool):
    def __init__(self):
        super().__init__("ExampleTool", "An example tool implementation")

    def execute(self, parameters: dict) -> dict:
        # Implement the tool's logic here
        result = {"message": f"Executed ExampleTool with parameters: {parameters}"}
        self.log_execution(parameters, result)
        return result
```

## aj_mas/tools/tool_loader.py

```
import importlib
import os
from typing import Dict, Type
from .base_tool import BaseTool
from .tool_registry import ToolRegistry
from .tool_utils import getToolClassNameFromConfigName
from ..utils import logger
from ..config import config, load_config


def load_tools() -> Dict[str, BaseTool]:
    tools = {}
    tool_config = load_config(config["tool_config_path"])
    
    for tool_category, category_tools in tool_config.items():
        for tool_name, tool_info in category_tools.items():
            if tool_info.get('enabled', False):
                try:
                    module = importlib.import_module(f"aj_mas.tools.{tool_category}.{tool_name}")
                    tool_class = getattr(module, f"{getToolClassNameFromConfigName(tool_name)}")
                    tools[tool_name] = tool_class()
                    logger.log(f"Loaded tool: {tool_name}")
                except (ImportError, AttributeError) as e:
                    logger.error(f"Failed to load tool: {tool_name}", {"error": str(e)})
    
    return tools

def register_tool(tool_class: Type[BaseTool]):
    ToolRegistry.register(tool_class)
    logger.log(f"Registered tool: {tool_class.__name__}")

def get_tool(tool_name: str) -> BaseTool:
    return ToolRegistry.get(tool_name)

def list_available_tools() -> list:
    return list(ToolRegistry.tools.keys())
```

## aj_mas/tools/tool_utils.py

```
from typing import List
from .base_tool import BaseTool


def chain_tools(tools: List[BaseTool], initial_input: dict) -> dict:
    result = initial_input
    for tool in tools:
        result = tool.execute(result)
    return result


def parallel_execute(tools: List[BaseTool], input_data: dict) -> List[dict]:
    return [tool.execute(input_data) for tool in tools]


def validate_tool_parameters(tool: BaseTool, parameters: dict) -> bool:
    # Implement parameter validation logic here
    # This is a placeholder implementation
    return True


def getToolClassNameFromConfigName(tool_config_name: str) -> str:
    return "".join(
        [name_part.capitalize() for name_part in tool_config_name.split("_")]
    )

```

## aj_mas/tools/web_interaction/web_scraper_tool.py

```
from ..base_tool import BaseTool
from aj_mas.utils import logger
import requests
from bs4 import BeautifulSoup

class WebScraperTool(BaseTool):
    def __init__(self):
        super().__init__("Web Scraper", "Scrape content from web pages")

    def execute(self, url: str, selector: str):
        logger.log(f"Executing Web Scraper Tool")
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            elements = soup.select(selector)
            return [element.get_text().strip() for element in elements]
        except Exception as e:
            return f"Error scraping web page: {str(e)}"
```

## aj_mas/tools/web_interaction/api_requester_tool.py

```
from ..base_tool import BaseTool
from aj_mas.utils import logger
import requests

class APIRequesterTool(BaseTool):
    def __init__(self):
        super().__init__("API Requester", "Make API requests")

    def execute(self, url: str, method: str = 'GET', params: dict = None, headers: dict = None, data: dict = None):
        logger.log(f"Executing API Requester Tool")
        try:
            response = requests.request(method, url, params=params, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return f"Error making API request: {str(e)}"
```

## aj_mas/tools/web_interaction/__init__.py

```
# Placeholder

```

## aj_mas/tools/web_interaction/html_parser_tool.py

```
from ..base_tool import BaseTool
from aj_mas.utils import logger
from bs4 import BeautifulSoup

class HTMLParserTool(BaseTool):
    def __init__(self):
        super().__init__("HTML Parser", "Parse and extract information from HTML content")

    def execute(self, html_content: str, parser: str = 'html.parser'):
        logger.log(f"Executing HTML Parser Tool")
        try:
            soup = BeautifulSoup(html_content, parser)
            
            # Extract basic information
            title = soup.title.string if soup.title else "No title found"
            headings = [h.text for h in soup.find_all(['h1', 'h2', 'h3'])]
            paragraphs = [p.text for p in soup.find_all('p')]
            links = [{'text': a.text, 'href': a.get('href')} for a in soup.find_all('a')]
            
            return {
                'title': title,
                'headings': headings,
                'paragraphs': paragraphs,
                'links': links
            }
        except Exception as e:
            return f"Error parsing HTML: {str(e)}"
```

## aj_mas/tools/file_handling/file_reader_tool.py

```
from ..base_tool import BaseTool
from aj_mas.utils import logger
import os

class FileReaderTool(BaseTool):
    def __init__(self):
        super().__init__("File Reader", "Read contents of a file")

    def execute(self, file_path: str):
        logger.log(f"Executing File Reader Tool")
        if not os.path.exists(file_path):
            return f"Error: File not found at {file_path}"
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return content
        except Exception as e:
            return f"Error reading file: {str(e)}"
```

## aj_mas/tools/file_handling/__init__.py

```
# Placeholder

```

## aj_mas/tools/file_handling/file_writer_tool.py

```
from ..base_tool import BaseTool
from aj_mas.utils import logger
import os

class FileWriterTool(BaseTool):
    def __init__(self):
        super().__init__("File Writer", "Write content to a file")

    def execute(self, file_path: str, content: str):
        logger.log(f"Executing File Writer Tool")
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            return f"Content successfully written to {file_path}"
        except Exception as e:
            return f"Error writing to file: {str(e)}"
```

## aj_mas/tools/file_handling/CSV_To_JSON_tool.py

```
from ..base_tool import BaseTool
from aj_mas.utils import logger
import pandas as pd

class CSVToJSONTool(BaseTool):
    def __init__(self):
        super().__init__("CSV to JSON Converter", "Convert CSV file to JSON format")

    def execute(self, csv_file_path: str, json_file_path: str):
        logger.log(f"Executing CSV to JSON Conversion Tool")
        try:
            df = pd.read_csv(csv_file_path)
            df.to_json(json_file_path, orient='records')
            return f"CSV file successfully converted to JSON and saved at {json_file_path}"
        except Exception as e:
            return f"Error converting CSV to JSON: {str(e)}"
```

## aj_mas/tools/language_processing/summarization_tool.py

```
from ..base_tool import BaseTool
from aj_mas.utils import logger

class SummarizationTool(BaseTool):
    def __init__(self, model_provider):
        super().__init__("Summarization", "Summarize a given text")
        self.model_provider = model_provider

    def execute(self, text: str, max_length: int = 100):
        logger.log(f"Executing Summarization Tool")
        prompt = f"Summarize the following text in {max_length} words: {text}"
        summary = self.model_provider.generate(prompt)
        return summary
```

## aj_mas/tools/language_processing/__init__.py

```
# Placeholder

```

## aj_mas/tools/language_processing/translation_tool.py

```
from ..base_tool import BaseTool
from aj_mas.utils import logger

class TranslationTool(BaseTool):
    def __init__(self, model_provider):
        super().__init__("Translation", "Translate text from one language to another")
        self.model_provider = model_provider

    def execute(self, text: str, source_language: str, target_language: str):
        logger.log(f"Executing Translation Tool")
        prompt = f"Translate the following {source_language} text to {target_language}: {text}"
        translated_text = self.model_provider.generate(prompt)
        return translated_text
```

## aj_mas/tools/language_processing/sentiment_analysis_tool.py

```
from ..base_tool import BaseTool
from aj_mas.utils import logger

class SentimentAnalysisTool(BaseTool):
    def __init__(self, model_provider):
        super().__init__("Sentiment Analysis", "Analyze the sentiment of a given text")
        self.model_provider = model_provider

    def execute(self, text: str):
        logger.log(f"Executing Sentiment Analysis Tool")
        prompt = f"Analyze the sentiment of the following text and respond with either 'positive', 'negative', or 'neutral': {text}"
        sentiment = self.model_provider.generate(prompt)
        return sentiment.strip().lower()
```

## aj_mas/skills/__init__.py

```
from .base_skill import BaseSkill
from .skill_loader import load_skills, register_skill, get_skill, list_available_skills
from .skill_registry import SkillRegistry
```

## aj_mas/skills/base_skill.py

```
from abc import ABC, abstractmethod
from ..utils import logger

class BaseSkill(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def execute(self, parameters: dict) -> dict:
        pass

    def log_execution(self, parameters: dict, result: dict):
        logger.log(f"Executed {self.name}", {
            "parameters": parameters,
            "result": result
        })

    def __str__(self):
        return f"{self.name}: {self.description}"
```

## aj_mas/skills/skill_loader.py

```
import importlib
import os
from typing import Dict, Type
from .base_skill import BaseSkill
from .skill_registry import SkillRegistry
from ..utils import logger
from ..config import config, load_config

def load_skills() -> Dict[str, BaseSkill]:
    skills = {}
    skill_config = load_config(config["skill_config_path"])
    print(skill_config)

    for skill_category, category_skills in skill_config.items():
        for skill_name, skill_info in category_skills.items():
            if skill_info.get('enabled', False):
                try:
                    module = importlib.import_module(f"aj_mas.skills.{skill_category}.{skill_name}")
                    skill_class_name=getSkillClassNameFromConfigName(skill_name)
                    print(dir(module))
                    print("***" + skill_class_name)
                    skill_class = getattr(module, skill_class_name)
                    skills[skill_name] = skill_class()
                    logger.log(f"Loaded skill: {skill_name}")
                except (ImportError, AttributeError) as e:
                    logger.error(f"Failed to load skill: {skill_name}", {"error": str(e)})
    
    return skills

def register_skill(skill_class: Type[BaseSkill]):
    SkillRegistry.register(skill_class)
    logger.log(f"Registered skill: {skill_class.__name__}")

def get_skill(skill_name: str) -> BaseSkill:
    return SkillRegistry.get(skill_name)

def list_available_skills() -> list:
    return list(SkillRegistry.skills.keys())

def getSkillClassNameFromConfigName(skill_config_name: str) -> str:
    return "".join(
        [name_part.capitalize() for name_part in skill_config_name.split("_")]
    ) + "Skill"
```

## aj_mas/skills/skill_registry.py

```
from typing import Dict, Type
from .base_skill import BaseSkill

class SkillRegistry:
    skills: Dict[str, Type[BaseSkill]] = {}

    @classmethod
    def register(cls, skill_class: Type[BaseSkill]):
        cls.skills[skill_class.__name__] = skill_class

    @classmethod
    def get(cls, skill_name: str) -> Type[BaseSkill]:
        return cls.skills.get(skill_name)

    @classmethod
    def list_skills(cls) -> list:
        return list(cls.skills.keys())
```

## aj_mas/skills/example_skill.py

```
from .base_skill import BaseSkill
from .skill_loader import register_skill

@register_skill
class ExampleSkill(BaseSkill):
    def __init__(self):
        super().__init__("ExampleSkill", "An example skill implementation")

    def execute(self, parameters: dict) -> dict:
        # Implement the skill's logic here
        result = {"message": f"Executed ExampleSkill with parameters: {parameters}"}
        self.log_execution(parameters, result)
        return result
```

## aj_mas/skills/travel/itinerary_planning.py

```
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
```

## aj_mas/skills/travel/flight_booking.py

```
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
```

## aj_mas/skills/travel/hotel_recommendation.py

```
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
```

## aj_mas/skills/travel/__init__.py

```
from .itinerary_planning import ItineraryPlanningSkill
from .flight_booking import FlightBookingSkill
from .hotel_recommendation import HotelRecommendationSkill
```

## aj_mas/skills/health/diet_planner.py

```
from ..base_skill import BaseSkill
from ..skill_loader import register_skill
from aj_mas.utils import logger
import random

@register_skill
class DietPlannerSkill(BaseSkill):
    def __init__(self):
        super().__init__("DietPlannerSkill", "Create personalized diet plans")

    def execute(self, parameters: dict) -> dict:
        height = parameters.get('height')
        weight = parameters.get('weight')
        age = parameters.get('age')
        gender = parameters.get('gender')
        goal = parameters.get('goal')
        dietary_restrictions = parameters.get('dietary_restrictions', [])

        logger.log(f"Creating diet plan for {age}-year-old {gender}, height: {height}, weight: {weight}, goal: {goal}")
        
        diet_plan = self._create_diet_plan(height, weight, age, gender, goal, dietary_restrictions)

        result = {"diet_plan": diet_plan}
        self.log_execution(parameters, result)
        return result

    def _create_diet_plan(self, height, weight, age, gender, goal, dietary_restrictions):
        # In a real implementation, this would use nutritional databases and personalized calculations
        bmi = weight / ((height / 100) ** 2)
        
        if bmi < 18.5:
            calorie_adjustment = 500  # Increase calories for underweight
        elif bmi > 25:
            calorie_adjustment = -500  # Decrease calories for overweight
        else:
            calorie_adjustment = 0

        base_calories = 2000 if gender == "female" else 2500
        recommended_calories = base_calories + calorie_adjustment

        meal_plan = {
            "breakfast": ["Oatmeal with fruits", "Greek yogurt with nuts", "Whole grain toast with avocado"],
            "lunch": ["Grilled chicken salad", "Quinoa bowl with vegetables", "Lentil soup with whole grain bread"],
            "dinner": ["Baked salmon with roasted vegetables", "Stir-fry tofu with brown rice", "Lean beef with sweet potato"],
            "snacks": ["Apple with almond butter", "Carrot sticks with hummus", "Mixed nuts"]
        }

        return {
            "recommended_calories": recommended_calories,
            "meal_plan": {meal: random.sample(options, k=3) for meal, options in meal_plan.items()},
            "dietary_advice": f"Focus on {goal}. Ensure to stay hydrated and include a variety of fruits and vegetables.",
            "restrictions_considered": dietary_restrictions
        }
```

## aj_mas/skills/health/__init__.py

```
from .symptom_checker import SymptomCheckerSkill
from .diet_planner import DietPlannerSkill
```

## aj_mas/skills/health/symptom_checker.py

```
from ..base_skill import BaseSkill
from ..skill_loader import register_skill
from aj_mas.utils import logger
import random

@register_skill
class SymptomCheckerSkill(BaseSkill):
    def __init__(self):
        super().__init__("SymptomCheckerSkill", "Check symptoms and provide health advice")

    def execute(self, parameters: dict) -> dict:
        symptoms = parameters.get('symptoms', [])
        age = parameters.get('age')
        gender = parameters.get('gender')

        logger.log(f"Checking symptoms for {age}-year-old {gender}: {', '.join(symptoms)}")
        
        diagnosis = self._analyze_symptoms(symptoms, age, gender)

        result = {"diagnosis": diagnosis}
        self.log_execution(parameters, result)
        return result

    def _analyze_symptoms(self, symptoms, age, gender):
        # In a real implementation, this would use a medical knowledge base and more sophisticated analysis
        possible_conditions = ["Common Cold", "Flu", "Allergies", "Stress", "Dehydration"]
        severity = random.choice(["Mild", "Moderate", "Severe"])
        
        recommendations = [
            "Rest and stay hydrated",
            "Take over-the-counter pain relievers if needed",
            "Monitor your symptoms"
        ]
        
        if severity == "Severe" or len(symptoms) > 3:
            recommendations.append("Consult a healthcare professional")

        return {
            "possible_conditions": random.sample(possible_conditions, k=min(len(possible_conditions), len(symptoms))),
            "severity": severity,
            "recommendations": recommendations,
            "disclaimer": "This is not a professional medical diagnosis. Please consult a doctor for accurate medical advice."
        }
```

## aj_mas/document_store/fasttext_chroma_store.py

```
import os
import hashlib
import fasttext
import chromadb
from chromadb.config import Settings
from typing import List, Tuple
from .document_store import DocumentStore
from ..utils import logger

class FastTextChromaStore(DocumentStore):
    def __init__(self, storage_dir: str = "aj_mas/document_storage", model_path: str = "cc.en.300.bin"):
        self.storage_dir = storage_dir
        if not os.path.exists(storage_dir):
            os.makedirs(storage_dir)

        self.model = fasttext.load_model(model_path)
        
        self.chroma_client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=os.path.join(storage_dir, "chroma_db")
        ))
        self.collection = self.chroma_client.get_or_create_collection("documents")
        
        self.load_documents()
        logger.log(f"Initialized FastTextChromaStore with {len(self.collection.get()['ids'])} documents")

    def load_documents(self):
        for filename in os.listdir(self.storage_dir):
            if filename.endswith(".txt"):
                file_path = os.path.join(self.storage_dir, filename)
                self._process_and_store_document(file_path)

    def _process_and_store_document(self, file_path: str):
        filename = os.path.basename(file_path)
        file_hash = self._get_file_hash(file_path)
        
        existing_docs = self.collection.get(ids=[file_hash])
        if existing_docs["ids"]:
            logger.log(f"Document {filename} already processed and stored.")
            return

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        embedding = self._get_document_embedding(content)

        self.collection.add(
            ids=[file_hash],
            embeddings=[embedding],
            metadatas=[{"filename": filename}],
            documents=[content]
        )
        logger.log(f"Processed and stored document: {filename}")

    def _get_file_hash(self, file_path: str) -> str:
        with open(file_path, "rb") as file:
            return hashlib.md5(file.read()).hexdigest()

    def _get_document_embedding(self, content: str) -> List[float]:
        words = content.split()
        word_vectors = [self.model.get_word_vector(word) for word in words]
        return list(sum(word_vectors) / len(word_vectors))

    def add_document(self, filename: str, content: str):
        file_path = os.path.join(self.storage_dir, filename)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        self._process_and_store_document(file_path)

    def retrieve_relevant_content(self, query: str, top_k: int = 3) -> List[Tuple[str, str]]:
        query_embedding = self._get_document_embedding(query)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        relevant_content = []
        for i in range(len(results["ids"][0])):
            filename = results["metadatas"][0][i]["filename"]
            content = results["documents"][0][i][:500]  # First 500 characters
            relevant_content.append((filename, content))

        logger.log(f"Retrieved {len(relevant_content)} relevant documents for query")
        return relevant_content
```

## aj_mas/document_store/__init__.py

```
# Import main classes and functions for easy access
from .document_store import DocumentStore
from .fasttext_chroma_store import FastTextChromaStore
```

## aj_mas/document_store/document_store.py

```
from abc import ABC, abstractmethod
from typing import List, Tuple

class DocumentStore(ABC):
    @abstractmethod
    def add_document(self, filename: str, content: str):
        pass

    @abstractmethod
    def retrieve_relevant_content(self, query: str, top_k: int = 3) -> List[Tuple[str, str]]:
        pass
```

## aj_mas/utils/error_handler.py

```
import traceback
from .logger import logger


class AJMASError(Exception):
    """Base class for AJ_MAS exceptions."""

    pass


def handle_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AJMASError as e:
            logger.error(f"AJ_MAS Error in {func.__name__}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {str(e)}")
            logger.debug(f"Traceback: {traceback.format_exc()}")
            raise AJMASError(f"An unexpected error occurred: {str(e)}")

    return wrapper


def safe_execute(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"Error executing {func.__name__}: {str(e)}")
        logger.debug(f"Traceback: {traceback.format_exc()}")
        return None

```

## aj_mas/utils/logger.py

```
import logging
from datetime import datetime
from pprint import pformat
import json


class Logger:
    def __init__(self, log_file="aj_mas.log", log_level=logging.INFO):
        self.logger = logging.getLogger("AJ_MAS")
        self.logger.setLevel(log_level)

        formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")

        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def log(self, message, data=None):
        log_entry = f"{message}"
        if data:
            log_entry += f"{pformat(data, indent=2, width=120)}"
        self.logger.info(log_entry)

    def error(self, message, data=None):
        log_entry = f"ERROR: {message}"
        if data:
            log_entry += f"{pformat(data, indent=2, width=120)}"
        self.logger.error(log_entry)

    def warning(self, message, data=None):
        log_entry = f"WARNING: {message}"
        if data:
            log_entry += f"{pformat(data, indent=2, width=120)}"
        self.logger.warning(log_entry)

    def debug(self, message, data=None):
        log_entry = f"DEBUG: {message}"
        if data:
            log_entry += f"{pformat(data, indent=2, width=120)}"
        self.logger.debug(log_entry)


logger = Logger()

```

## aj_mas/utils/__init__.py

```
from .logger import logger
from .error_handler import handle_error, AJMASError, safe_execute
```

## aj_mas/agents/agent_factory.py

```
from ..utils import logger
from ..personas import load_personas
from .specialized_agents import TravelAgent, FinancialAdvisor, MedicalDoctor, LegalAdvisor, SoftwareEngineer

def create_agent(agent_type, skills, model_provider, document_store, config_path):
    personas = load_personas(config_path)
    persona = personas.get(agent_type)
    
    if not persona:
        logger.error(f"No persona found for agent type: {agent_type}")
        return None
    
    agent_classes = {
        "travel_agent": TravelAgent,
        "financial_advisor": FinancialAdvisor,
        "medical_doctor": MedicalDoctor,
        "legal_advisor": LegalAdvisor,
        "software_engineer": SoftwareEngineer
    }
    
    agent_class = agent_classes.get(agent_type)
    if not agent_class:
        logger.error(f"No agent class found for agent type: {agent_type}")
        return None
    
    return agent_class(persona.name, skills, model_provider, document_store, persona)

def get_available_agent_types():
    return ["travel_agent", "financial_advisor", "medical_doctor", "legal_advisor", "software_engineer"]
```

## aj_mas/agents/__init__.py

```
from .base_agent import BaseAgent
from .persona_based_agent import PersonaBasedAgent
from .specialized_agents import TravelAgent, FinancialAdvisor, MedicalDoctor, LegalAdvisor, SoftwareEngineer
from .agent_factory import create_agent, get_available_agent_types
```

## aj_mas/agents/persona_based_agent.py

```
from .base_agent import BaseAgent
from ..utils import logger, handle_error
from ..personas import SkillArea
import os

class PersonaBasedAgent(BaseAgent):
    def __init__(self, name, skills, model_provider, document_store, persona):
        super().__init__(name, skills, model_provider, document_store)
        self.persona = persona
        self.current_user_id = None

    @handle_error
    def perform_task(self, task):
        logger.log(f"Agent {self.name} performing task: {task}")
        task_analysis = self.model_provider.analyze_task(task, self.current_user_id)
        skill_area = self._determine_skill_area(task_analysis)
        
        proficiency = self.persona.skill_proficiencies.get(skill_area, 0)
        if proficiency < 0.3:
            return self._generate_low_proficiency_response(skill_area, task)
        
        relevant_docs = self.document_store.retrieve_relevant_content(task)
        context = self._prepare_context(relevant_docs)
        
        skill_result = self._execute_skill(skill_area, task, task_analysis, context)
        adjusted_response = self._adjust_response_for_persona(skill_result, proficiency)
        
        return adjusted_response

    def start_session(self, user_id):
        self.current_user_id = user_id
        logger.log(f"Agent {self.name} started session for user: {user_id}")

    def end_session(self):
        logger.log(f"Agent {self.name} ended session for user: {self.current_user_id}")
        self.current_user_id = None

    def add_document(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            filename = os.path.basename(file_path)
            self.document_store.add_document(filename, content)
            return f"Document added: {filename}"
        except Exception as e:
            logger.error(f"Error adding document: {str(e)}")
            return f"Error adding document: {str(e)}"

    def _determine_skill_area(self, task_analysis):
        # Implement logic to determine the most relevant skill area based on task analysis
        # This is a placeholder implementation
        return SkillArea.GENERAL

    def _generate_low_proficiency_response(self, skill_area, task):
        prompt = f"Generate a response for an agent with low proficiency in {skill_area.value} when asked about the task: {task}. The agent should politely express limited knowledge and suggest seeking information from a more qualified source."
        return self.model_provider.generate(prompt)

    def _prepare_context(self, relevant_docs):
        return "\n".join([f"{doc[0]}: {doc[1]}" for doc in relevant_docs])

    def _execute_skill(self, skill_area, task, task_analysis, context):
        # Implement logic to select and execute the most appropriate skill
        # This is a placeholder implementation
        return f"Executed skill for {skill_area.value} with task: {task}"

    def _adjust_response_for_persona(self, skill_result, proficiency):
        prompt = f"""
        Adjust the following skill execution result:
        '{skill_result}'
        
        Consider these persona characteristics:
        - Name: {self.persona.name}
        - Gender: {self.persona.gender}
        - Ethnicity: {self.persona.ethnicity}
        - Religious inclination: {self.persona.religious_inclination}
        - Personality traits: {', '.join(self.persona.personality_traits)}
        - Communication style: {self.persona.communication_style}
        - Proficiency level: {proficiency}

        Rewrite the response to reflect these characteristics and the proficiency level.
        """
        return self.model_provider.generate(prompt)
```

## aj_mas/agents/base_agent.py

```
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, name, skills, model_provider, document_store):
        self.name = name
        self.skills = skills
        self.model_provider = model_provider
        self.document_store = document_store

    @abstractmethod
    def perform_task(self, task):
        pass

    @abstractmethod
    def start_session(self, user_id):
        pass

    @abstractmethod
    def end_session(self):
        pass

    @abstractmethod
    def add_document(self, file_path):
        pass
```

## aj_mas/agents/specialized_agents.py

```
from .persona_based_agent import PersonaBasedAgent
from ..personas import SkillArea

class TravelAgent(PersonaBasedAgent):
    def __init__(self, name, skills, model_provider, document_store, persona):
        super().__init__(name, skills, model_provider, document_store, persona)
    
    def _determine_skill_area(self, task_analysis):
        # Implement travel-specific skill area determination
        return SkillArea.TRAVEL

class FinancialAdvisor(PersonaBasedAgent):
    def __init__(self, name, skills, model_provider, document_store, persona):
        super().__init__(name, skills, model_provider, document_store, persona)
    
    def _determine_skill_area(self, task_analysis):
        # Implement finance-specific skill area determination
        return SkillArea.FINANCE

class MedicalDoctor(PersonaBasedAgent):
    def __init__(self, name, skills, model_provider, document_store, persona):
        super().__init__(name, skills, model_provider, document_store, persona)
    
    def _determine_skill_area(self, task_analysis):
        # Implement medical-specific skill area determination
        return SkillArea.HEALTH

class LegalAdvisor(PersonaBasedAgent):
    def __init__(self, name, skills, model_provider, document_store, persona):
        super().__init__(name, skills, model_provider, document_store, persona)
    
    def _determine_skill_area(self, task_analysis):
        # Implement legal-specific skill area determination
        return SkillArea.LAW

class SoftwareEngineer(PersonaBasedAgent):
    def __init__(self, name, skills, model_provider, document_store, persona):
        super().__init__(name, skills, model_provider, document_store, persona)
    
    def _determine_skill_area(self, task_analysis):
        # Implement software engineering-specific skill area determination
        return SkillArea.TECHNOLOGY
```

## aj_mas/config/skill_config.json

```
{
  "travel": {
    "itinerary_planning": {
      "enabled": true,
      "max_days": 30,
      "default_budget": 1000
    },
    "hotel_recommendation": {
      "enabled": true,
      "max_price": 500,
      "min_rating": 3.5
    },
    "flight_booking": {
      "enabled": true,
      "preferred_airlines": [
        "Airline1",
        "Airline2"
      ]
    }
  },
  "health": {
    "diet_planner": {
      "enabled": true
    },
    "symptom_checker": {
      "enabled": true
    }
  }
}
```

## aj_mas/config/agent_config.json

```
{
  "travel_agent": {
    "name": "Alex Johnson",
    "gender": "Non-binary",
    "ethnicity": "Mixed Asian-European",
    "religious_inclination": "Agnostic",
    "skill_proficiencies": {
      "TRAVEL": 0.95,
      "ENTERTAINMENT": 0.7,
      "CULTURE": 0.8
    },
    "tool_proficiencies": {
      "FlightBookingTool": 0.95,
      "HotelRecommendationTool": 0.9,
      "ItineraryPlanningTool": 0.95
    },
    "language_proficiencies": {
      "English": "NATIVE",
      "Spanish": "ADVANCED",
      "French": "INTERMEDIATE"
    },
    "personality_traits": [
      "Enthusiastic",
      "Detail-oriented"
    ],
    "communication_style": "Friendly and professional"
  },
  "financial_advisor": {
    "name": "Morgan Lee",
    "gender": "Female",
    "ethnicity": "African American",
    "religious_inclination": "Christian",
    "skill_proficiencies": {
      "FINANCE": 0.95,
      "BUSINESS": 0.85,
      "MATHEMATICS": 0.8
    },
    "tool_proficiencies": {
      "InvestmentAnalysisTool": 0.95,
      "TaxPlanningTool": 0.9,
      "RetirementPlanningTool": 0.95
    },
    "language_proficiencies": {
      "English": "NATIVE"
    },
    "personality_traits": [
      "Analytical",
      "Patient"
    ],
    "communication_style": "Clear and reassuring"
  }
}
```

## aj_mas/config/config.json

```
{
  "default_model_provider": "ollama",
  "system_name": "AJ_MAS",
  "version": "1.0.0",
  "log_level": "INFO",
  "max_concurrent_agents": 5,
  "model_providers": {
    "ollama": {
      "name": "qwen2:1.5b",
      "api_url": "http://localhost:11434/api/generate"
    }
  },
  "document_store": {
    "type": "fasttext_chroma",
    "storage_dir": "aj_mas/document_storage",
    "fasttext_model": "cc.en.300.bin"
  },
  "agent_config_path": "aj_mas/config/agent_config.json",
  "skill_config_path": "aj_mas/config/skill_config.json",
  "tool_config_path": "aj_mas/config/tool_config.json",
  "api_rate_limit": 100,
  "session_timeout": 3600
}

```

## aj_mas/config/tool_config.json

```
{
  "web_interaction": {
    "api_requester_tool": {
      "enabled": true,
      "max_retries": 3,
      "timeout": 30
    },
    "web_scraper_tool": {
      "enabled": true,
      "user_agent": "AJ_MAS Bot 1.0"
    },
    "html_parser_tool": {
      "enabled": true,
      "user_agent": "AJ_MAS Bot 1.0"
    }
  },
  "file_handling": {
    "file_writer_tool": {
      "enabled": true
    },
    "file_reader_tool": {
      "enabled": true
    },
    "CSV_To_JSON_tool":{
      "enabled": true
    }
  },
  "language_processing": {
    "summarization_tool": {
      "enabled": true,
      "max_summary_length": 200
    },
    "translation_tool": {
      "enabled": true,
      "max_summary_length": 200
    },
    "sentiment_analysis_tool": {
      "enabled": true,
      "sentiment_levels": [
        "Very Negative",
        "Negative",
        "Neutral",
        "Positive",
        "Very Positive"
      ]
    }
  }
}
```

## aj_mas/models/model_provider.py

```
from abc import ABC, abstractmethod

class ModelProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, max_length: int = 100, temperature: float = 0.7) -> str:
        pass

    @abstractmethod
    def analyze_task(self, task: str, user_id: str) -> dict:
        pass
```

## aj_mas/models/ollama_provider.py

```
import requests
import json
from .model_provider import ModelProvider
from ..utils import logger
from ..config import config

class OllamaProvider(ModelProvider):
    def __init__(self, model_name: str):
        self.config=config
        self.model_name = model_name
        self.api_url = self.config['model_providers']['ollama']['api_url']

    def generate(self, prompt: str, max_length: int = 100, temperature: float = 0.7) -> str:
        data = {
            "model": self.model_name,
            "prompt": prompt,
            "max_tokens": max_length,
            "temperature": temperature,
            "stream": False,
        }

        try:
            response = requests.post(self.api_url, json=data)
            response.raise_for_status()
            result = response.json()
            logger.log("Ollama API response received", 
                       {"prompt": prompt[:50] + "...", "response_length": len(result.get("response", ""))})
            return result.get("response", "")
        except requests.RequestException as e:
            logger.error(f"Error in Ollama API request", {"error": str(e)})
            return f"Error: {str(e)}"
        except json.JSONDecodeError:
            logger.error("Error decoding JSON from Ollama API response")
            return "Error: Invalid response from Ollama API"

    def analyze_task(self, task: str, user_id: str) -> dict:
        prompt = f"Analyze the following task for user {user_id}:\n{task}\n\nProvide a JSON response with 'subtasks' and 'parameters'."
        response = self.generate(prompt)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            logger.error("Error parsing JSON from task analysis")
            return {"subtasks": [], "parameters": {}}

    def get_model_info(self):
        info_url = f"{self.api_url}/show"
        data = {"name": self.model_name}

        try:
            response = requests.post(info_url, json=data)
            response.raise_for_status()
            result = response.json()
            logger.log("Retrieved model info from Ollama API", {"model": self.model_name})
            return result
        except requests.RequestException as e:
            logger.error(f"Error retrieving model info from Ollama API", {"error": str(e)})
            return None
```

## aj_mas/models/huggingface_provider.py

```
import json
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from .model_provider import ModelProvider
from ..utils.logger import logger

class HuggingFaceProvider(ModelProvider):
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
        logger.log(f"Initialized HuggingFace model", {"model": model_name, "device": self.device})

    def generate(self, prompt: str, max_length: int = 100, temperature: float = 0.7) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                temperature=temperature,
                num_return_sequences=1
            )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        logger.log("HuggingFace model response generated", 
                   {"prompt": prompt[:50] + "...", "response_length": len(response)})
        return response

    def analyze_task(self, task: str, user_id: str) -> dict:
        prompt = f"Analyze the following task for user {user_id}:\n{task}\n\nProvide a JSON response with 'subtasks' and 'parameters'."
        response = self.generate(prompt)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            logger.error("Error parsing JSON from task analysis")
            return {"subtasks": [], "parameters": {}}
```

## aj_mas/models/__init__.py

```
from .model_provider import ModelProvider
from .ollama_provider import OllamaProvider
from .huggingface_provider import HuggingFaceProvider
```

## aj_mas/personas/persona.py

```
from enum import Enum
from typing import Dict, List

class SkillArea(Enum):
    TRAVEL = "Travel"
    HEALTH = "Health"

class LanguageProficiency(Enum):
    NATIVE = 5
    FLUENT = 4
    ADVANCED = 3
    INTERMEDIATE = 2
    BASIC = 1

class AgentPersona:
    def __init__(self, name: str, gender: str, ethnicity: str, religious_inclination: str):
        self.name = name
        self.gender = gender
        self.ethnicity = ethnicity
        self.religious_inclination = religious_inclination
        self.skill_proficiencies: Dict[SkillArea, float] = {}
        self.tool_proficiencies: Dict[str, float] = {}
        self.language_proficiencies: Dict[str, LanguageProficiency] = {}
        self.personality_traits: List[str] = []
        self.communication_style: str = ""

    def set_skill_proficiency(self, skill_area: SkillArea, proficiency: float):
        if 0 <= proficiency <= 1:
            self.skill_proficiencies[skill_area] = proficiency
        else:
            raise ValueError("Proficiency must be between 0 and 1")

    def set_tool_proficiency(self, tool_name: str, proficiency: float):
        if 0 <= proficiency <= 1:
            self.tool_proficiencies[tool_name] = proficiency
        else:
            raise ValueError("Proficiency must be between 0 and 1")

    def set_language_proficiency(self, language: str, proficiency: LanguageProficiency):
        self.language_proficiencies[language] = proficiency

    def add_personality_trait(self, trait: str):
        self.personality_traits.append(trait)

    def set_communication_style(self, style: str):
        self.communication_style = style

    def __str__(self):
        return f"AgentPersona: {self.name} ({self.gender}, {self.ethnicity})"

    def to_dict(self):
        return {
            "name": self.name,
            "gender": self.gender,
            "ethnicity": self.ethnicity,
            "religious_inclination": self.religious_inclination,
            "skill_proficiencies": {k.value: v for k, v in self.skill_proficiencies.items()},
            "tool_proficiencies": self.tool_proficiencies,
            "language_proficiencies": {k: v.value for k, v in self.language_proficiencies.items()},
            "personality_traits": self.personality_traits,
            "communication_style": self.communication_style
        }

    @classmethod
    def from_dict(cls, data):
        persona = cls(
            data["name"],
            data["gender"],
            data["ethnicity"],
            data["religious_inclination"]
        )
        for skill, prof in data["skill_proficiencies"].items():
            persona.set_skill_proficiency(SkillArea(skill), prof)
        for tool, prof in data["tool_proficiencies"].items():
            persona.set_tool_proficiency(tool, prof)
        for lang, prof in data["language_proficiencies"].items():
            persona.set_language_proficiency(lang, LanguageProficiency(prof))
        for trait in data["personality_traits"]:
            persona.add_personality_trait(trait)
        persona.set_communication_style(data["communication_style"])
        return persona

```

## aj_mas/personas/__init__.py

```
from .persona import AgentPersona, SkillArea, LanguageProficiency
from .persona_loader import load_personas, save_personas
```

## aj_mas/personas/persona_loader.py

```
import json
from typing import Dict
from .persona import AgentPersona

def load_personas(config_path: str) -> Dict[str, AgentPersona]:
    with open(config_path, 'r') as f:
        config_data = json.load(f)
    
    personas = {}
    for agent_type, persona_data in config_data.items():
        personas[agent_type] = AgentPersona.from_dict(persona_data)
    
    return personas

def save_personas(personas: Dict[str, AgentPersona], config_path: str):
    config_data = {agent_type: persona.to_dict() for agent_type, persona in personas.items()}
    with open(config_path, 'w') as f:
        json.dump(config_data, f, indent=2)

# Example usage:
# personas = load_personas("path/to/agent_config.json")
# travel_agent_persona = personas["travel_agent"]
# 
# # Modify persona if needed
# travel_agent_persona.add_personality_trait("Adventurous")
# 
# # Save updated personas
# save_personas(personas, "path/to/agent_config.json")
```
