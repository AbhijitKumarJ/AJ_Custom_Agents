import requests
import json
from .model_provider import ModelProvider
from ..utils import logger
from ..config import config

class OllamaProvider(ModelProvider):
    def __init__(self, model_name: str):
        self.config=config
        self.model_name = model_name
        self.api_url = self.config['model_providers']['ollama']['api_url']

    def generate(self, prompt: str, max_length: int = 500, temperature: float = 0.7) -> str:
        data = {
            "model": self.model_name,
            "prompt": prompt,
            "max_tokens": max_length,
            "temperature": temperature,
            "stream": False,
        }

        try:
            response = requests.post(self.api_url, json=data)
            response.raise_for_status()
            result = response.json()
            logger.log("Ollama API response received", 
                       {"prompt": prompt + "...", "response_length": len(result.get("response", ""))})
            logger.log(result)
            return result.get("response", "")
        except requests.RequestException as e:
            logger.error(f"Error in Ollama API request", {"error": str(e)})
            return f"Error: {str(e)}"
        except json.JSONDecodeError:
            logger.error("Error decoding JSON from Ollama API response")
            return "Error: Invalid response from Ollama API"

    def analyze_task(self, task: str, user_id: str) -> dict:
        prompt = f"Analyze the following task for user {user_id}:\n{task}\n\nProvide a JSON response with 'subtasks' and 'parameters'."
        response = self.generate(prompt)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            logger.error("Error parsing JSON from task analysis")
            return {"subtasks": [], "parameters": {}}

    def get_model_info(self):
        info_url = f"{self.api_url}/show"
        data = {"name": self.model_name}

        try:
            response = requests.post(info_url, json=data)
            response.raise_for_status()
            result = response.json()
            logger.log("Retrieved model info from Ollama API", {"model": self.model_name})
            return result
        except requests.RequestException as e:
            logger.error(f"Error retrieving model info from Ollama API", {"error": str(e)})
            return None