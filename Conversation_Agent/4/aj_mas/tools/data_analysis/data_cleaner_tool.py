from ..base_tool import BaseTool
from utils.logger import logger
import pandas as pd

class DataCleanerTool(BaseTool):
    def __init__(self):
        super().__init__("Data Cleaner", "Clean and preprocess data")

    def execute(self, data: pd.DataFrame, operations: list):
        logger.log(f"Executing Data Cleaner Tool")
        try:
            for operation in operations:
                if operation == 'remove_duplicates':
                    data = data.drop_duplicates()
                elif operation == 'fill_na':
                    data = data.fillna(data.mean())
                elif operation == 'normalize':
                    data = (data - data.min()) / (data.max() - data.min())
                else:
                    logger.log(f"Unsupported operation: {operation}")
            return data
        except Exception as e:
            return f"Error cleaning data: {str(e)}"