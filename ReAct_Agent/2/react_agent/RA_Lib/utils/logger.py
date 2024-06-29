# Logger implementation

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