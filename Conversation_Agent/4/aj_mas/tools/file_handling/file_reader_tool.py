from ..base_tool import BaseTool
from utils.logger import logger
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