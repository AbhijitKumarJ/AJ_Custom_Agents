from ..base_tool import BaseTool
from utils.logger import logger
import requests

class BlockchainExplorerTool(BaseTool):
    def __init__(self, api_url, api_key):
        super().__init__("Blockchain Explorer", "Retrieve information from blockchain explorers")
        self.api_url = api_url
        self.api_key = api_key

    def execute(self, action: str, params: dict):
        logger.log(f"Executing Blockchain Explorer Tool")
        try:
            headers = {'Content-Type': 'application/json', 'X-API-Key': self.api_key}
            response = requests.get(f"{self.api_url}/{action}", params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return f"Error in blockchain explorer query: {str(e)}"