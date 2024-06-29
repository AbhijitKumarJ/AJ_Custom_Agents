# Configuration settings

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