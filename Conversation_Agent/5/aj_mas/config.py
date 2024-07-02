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
