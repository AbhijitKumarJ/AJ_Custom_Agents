# Re-export utility classes and functions for easier imports

from .logger import logger
from .task_analyzer import task_analyzer
from .memory_system import memory_system
from .document_store import document_store
from .ollama_api import OllamaAPI

# You can add any additional small, general-purpose utility functions here


def is_valid_file_path(path):
    """Check if a given path is a valid file path."""
    import os

    return os.path.isfile(path)


def safe_json_loads(json_string, default=None):
    """Safely load a JSON string, returning a default value if it fails."""
    import json

    try:
        return json.loads(json_string)
    except json.JSONDecodeError:
        return default


# Add more utility functions as needed


# You can also define any constants that might be used across the project

MAX_DOCUMENT_SIZE = 1024 * 1024  # 1 MB
SUPPORTED_DOCUMENT_TYPES = [".txt", ".md", ".json"]
