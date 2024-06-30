import logging
from datetime import datetime
from pprint import pformat
import json
from ..config import config


class Logger:
    def __init__(self):
        self.config = config
        logging.basicConfig(
            level=self.config["logging"]["level"],
            filename=self.config["logging"]["file"],
            format="[%(asctime)s] %(levelname)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        self.logger = logging.getLogger()

    def log(self, message, data=None):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        if data:
            log_message += f"\n{pformat(data, indent=2, width=120)}"
        self.logger.info(log_message)
        print(log_message)

    def error(self, message, data=None):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] ERROR: {message}"
        if data:
            log_message += f"\n{pformat(data, indent=2, width=120)}"
        self.logger.error(log_message)
        print(log_message)


logger = Logger()
