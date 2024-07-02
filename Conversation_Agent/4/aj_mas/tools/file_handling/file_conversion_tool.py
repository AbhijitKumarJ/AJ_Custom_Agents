from ..base_tool import BaseTool
from aj_mas.utils import logger
import pandas as pd

class CSVToJSONTool(BaseTool):
    def __init__(self):
        super().__init__("CSV to JSON Converter", "Convert CSV file to JSON format")

    def execute(self, csv_file_path: str, json_file_path: str):
        logger.log(f"Executing CSV to JSON Conversion Tool")
        try:
            df = pd.read_csv(csv_file_path)
            df.to_json(json_file_path, orient='records')
            return f"CSV file successfully converted to JSON and saved at {json_file_path}"
        except Exception as e:
            return f"Error converting CSV to JSON: {str(e)}"