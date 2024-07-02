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
