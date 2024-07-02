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
