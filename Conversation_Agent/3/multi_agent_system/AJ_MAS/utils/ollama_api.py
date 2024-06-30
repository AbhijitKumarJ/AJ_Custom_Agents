import requests
import json
from .logger import logger


class OllamaAPI:
    def __init__(self, model_name="qwen:1.5b"):
        self.model_name = model_name
        self.api_url = "http://localhost:11434/api/generate"
        logger.log(f"Initialized OllamaAPI", {"model": self.model_name})

    def generate(self, prompt, max_length=100, temperature=0.7):
        data = {
            "model": self.model_name,
            "prompt": prompt,
            "max_tokens": max_length,
            "temperature": temperature,
            "stream": False,
        }

        try:
            response = requests.post(self.api_url, json=data)
            response.raise_for_status()  # Raise an exception for bad status codes
            result = response.json()
            logger.log(
                "Ollama API response received",
                {
                    "prompt": prompt[:50] + "...",
                    "response_length": len(result.get("response", "")),
                },
            )
            return result.get("response", "")
        except requests.RequestException as e:
            logger.error(f"Error in Ollama API request", {"error": str(e)})
            return f"Error: {str(e)}"
        except json.JSONDecodeError:
            logger.error("Error decoding JSON from Ollama API response")
            return "Error: Invalid response from Ollama API"

    def get_model_info(self):
        info_url = "http://localhost:11434/api/show"
        data = {"name": self.model_name}

        try:
            response = requests.post(info_url, json=data)
            response.raise_for_status()
            result = response.json()
            logger.log(
                "Retrieved model info from Ollama API", {"model": self.model_name}
            )
            return result
        except requests.RequestException as e:
            logger.error(
                f"Error retrieving model info from Ollama API", {"error": str(e)}
            )
            return None


# You can add more methods here as needed, such as for fine-tuning or other Ollama API functionalities
# Initialize OllamaAPI with default model
# ollama_api = OllamaAPI()
