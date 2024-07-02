from ..base_tool import BaseTool
from aj_mas.utils import logger
import os

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