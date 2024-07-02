from ..base_tool import BaseTool
from aj_mas.utils import logger
import requests

class APIRequesterTool(BaseTool):
    def __init__(self):
        super().__init__("API Requester", "Make API requests")

    def execute(self, url: str, method: str = 'GET', params: dict = None, headers: dict = None, data: dict = None):
        logger.log(f"Executing API Requester Tool")
        try:
            response = requests.request(method, url, params=params, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return f"Error making API request: {str(e)}"