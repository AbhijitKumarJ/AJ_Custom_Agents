import os

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def write_file(path, content):
    with open(path, 'w') as f:
        f.write(content)
    print(f"Created file: {path}")

def create_aj_mas_main_files():
    aj_mas_dir = "aj_mas"
    create_directory(aj_mas_dir)

    # __init__.py
    init_content = """
from .main import run_aj_mas
from .config import load_config
"""
    write_file(os.path.join(aj_mas_dir, "__init__.py"), init_content.strip())

    # main.py
    main_content = """
from aj_mas.agents import create_agent, get_available_agent_types
from aj_mas.skills import load_skills
from aj_mas.models import OllamaProvider
from aj_mas.document_store import FastTextChromaStore
from aj_mas.utils import logger, load_config
import sys

def initialize_system():
    config = load_config()
    skills = load_skills()
    model_provider = OllamaProvider(config['model_provider']['name'])
    document_store = FastTextChromaStore(config['document_store']['storage_dir'])
    return config, skills, model_provider, document_store

def run_aj_mas():
    logger.log("Starting AJ_MAS system")
    config, skills, model_provider, document_store = initialize_system()

    while True:
        print("\\nWelcome to AJ_MAS! Please choose an option:")
        print("1. Create an agent")
        print("2. List available agent types")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            agent_type = input("Enter the type of agent you want to create: ")
            agent = create_agent(agent_type, skills, model_provider, document_store, config['agent_config_path'])
            if agent:
                user_id = input("Enter a user ID for this session: ")
                agent.start_session(user_id)
                while True:
                    task = input("Enter a task for the agent (or 'quit' to end session): ")
                    if task.lower() == 'quit':
                        break
                    response = agent.perform_task(task)
                    print(f"Agent response: {response}")
                agent.end_session()
        elif choice == '2':
            agent_types = get_available_agent_types()
            print(f"Available agent types: {', '.join(agent_types)}")
        elif choice == '3':
            print("Thank you for using AJ_MAS. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    run_aj_mas()
"""
    write_file(os.path.join(aj_mas_dir, "main.py"), main_content.strip())

    # config.py
    config_content = """
import json
import os

def load_config(config_path='config/config.json'):
    try:
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON in configuration file: {config_path}")

def get_config_value(key, default=None):
    config = load_config()
    return config.get(key, default)

def update_config(key, value, config_path='config/config.json'):
    config = load_config(config_path)
    config[key] = value
    with open(config_path, 'w') as config_file:
        json.dump(config, config_file, indent=2)

# Default configuration
DEFAULT_CONFIG = {
    "system_name": "AJ_MAS",
    "version": "1.0.0",
    "log_level": "INFO",
    "max_concurrent_agents": 5,
    "model_provider": {
        "name": "qwen2:1.5b-instruct-q8_0",
        "api_url": "http://localhost:11434/api/generate"
    },
    "document_store": {
        "type": "fasttext_chroma",
        "storage_dir": "aj_mas/document_storage",
        "fasttext_model": "cc.en.300.bin"
    },
    "agent_config_path": "config/agent_config.json",
    "skill_config_path": "config/skill_config.json",
    "api_rate_limit": 100,
    "session_timeout": 3600
}

def ensure_config_file_exists(config_path='config/config.json'):
    if not os.path.exists(config_path):
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w') as config_file:
            json.dump(DEFAULT_CONFIG, config_file, indent=2)
        print(f"Created default configuration file: {config_path}")

# Ensure the config file exists when this module is imported
ensure_config_file_exists()
"""
    write_file(os.path.join(aj_mas_dir, "config.py"), config_content.strip())

    # constants.py
    constants_content = """
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
    "GENERAL"
]

# Language Proficiency Levels
LANGUAGE_PROFICIENCY = {
    "NATIVE": 5,
    "FLUENT": 4,
    "ADVANCED": 3,
    "INTERMEDIATE": 2,
    "BASIC": 1
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
"""
    write_file(os.path.join(aj_mas_dir, "constants.py"), constants_content.strip())

if __name__ == "__main__":
    create_aj_mas_main_files()
    print("AJ_MAS main files created successfully!")
