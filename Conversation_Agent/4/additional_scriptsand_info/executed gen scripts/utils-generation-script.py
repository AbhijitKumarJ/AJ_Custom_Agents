import os

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def write_file(path, content):
    with open(path, 'w') as f:
        f.write(content)
    print(f"Created file: {path}")

def create_utils_files():
    utils_dir = "aj_mas/utils"
    create_directory(utils_dir)

    # __init__.py
    init_content = """
from .logger import logger
from .config_loader import load_config
from .error_handler import handle_error, AJMASError
"""
    write_file(os.path.join(utils_dir, "__init__.py"), init_content.strip())

    # logger.py
    logger_content = """
import logging
from datetime import datetime
from pprint import pformat
import json

class Logger:
    def __init__(self, log_file='aj_mas.log', log_level=logging.INFO):
        self.logger = logging.getLogger('AJ_MAS')
        self.logger.setLevel(log_level)

        formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')

        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def log(self, message, data=None):
        log_entry = f"{message}"
        if data:
            log_entry += f"\n{pformat(data, indent=2, width=120)}"
        self.logger.info(log_entry)

    def error(self, message, data=None):
        log_entry = f"ERROR: {message}"
        if data:
            log_entry += f"\n{pformat(data, indent=2, width=120)}"
        self.logger.error(log_entry)

    def warning(self, message, data=None):
        log_entry = f"WARNING: {message}"
        if data:
            log_entry += f"\n{pformat(data, indent=2, width=120)}"
        self.logger.warning(log_entry)

    def debug(self, message, data=None):
        log_entry = f"DEBUG: {message}"
        if data:
            log_entry += f"\n{pformat(data, indent=2, width=120)}"
        self.logger.debug(log_entry)

logger = Logger()
"""
    write_file(os.path.join(utils_dir, "logger.py"), logger_content.strip())

    # config_loader.py
    config_loader_content = """
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
"""
    write_file(os.path.join(utils_dir, "config_loader.py"), config_loader_content.strip())

    # error_handler.py
    error_handler_content = """
import traceback
from .logger import logger

class AJMASError(Exception):
    """"""Base class for AJ_MAS exceptions.""""""
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
"""
    write_file(os.path.join(utils_dir, "error_handler.py"), error_handler_content.strip())

if __name__ == "__main__":
    create_utils_files()
    print("AJ_MAS utils files created successfully!")
