import os

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def write_file(path, content):
    with open(path, 'w') as f:
        f.write(content)
    print(f"Created file: {path}")

def create_models_files():
    models_dir = "aj_mas/models"
    create_directory(models_dir)

    # __init__.py
    init_content = """
from .model_provider import ModelProvider
from .ollama_provider import OllamaProvider
from .huggingface_provider import HuggingFaceProvider
"""
    write_file(os.path.join(models_dir, "__init__.py"), init_content.strip())

    # model_provider.py
    model_provider_content = """
from abc import ABC, abstractmethod

class ModelProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, max_length: int = 100, temperature: float = 0.7) -> str:
        pass

    @abstractmethod
    def analyze_task(self, task: str, user_id: str) -> dict:
        pass
"""
    write_file(os.path.join(models_dir, "model_provider.py"), model_provider_content.strip())

    # ollama_provider.py
    ollama_provider_content = """
import requests
import json
from .model_provider import ModelProvider
from utils.logger import logger
from config import config

class OllamaProvider(ModelProvider):
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.api_url = config['model_providers']['ollama']['api_url']

    def generate(self, prompt: str, max_length: int = 100, temperature: float = 0.7) -> str:
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
                       {"prompt": prompt[:50] + "...", "response_length": len(result.get("response", ""))})
            return result.get("response", "")
        except requests.RequestException as e:
            logger.error(f"Error in Ollama API request", {"error": str(e)})
            return f"Error: {str(e)}"
        except json.JSONDecodeError:
            logger.error("Error decoding JSON from Ollama API response")
            return "Error: Invalid response from Ollama API"

    def analyze_task(self, task: str, user_id: str) -> dict:
        prompt = f"Analyze the following task for user {user_id}:\\n{task}\\n\\nProvide a JSON response with 'subtasks' and 'parameters'."
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
"""
    write_file(os.path.join(models_dir, "ollama_provider.py"), ollama_provider_content.strip())

    # huggingface_provider.py
    huggingface_provider_content = """
import json
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from .model_provider import ModelProvider
from utils.logger import logger
from config import config

class HuggingFaceProvider(ModelProvider):
    def __init__(self, model_name: str):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
        logger.log(f"Initialized HuggingFace model", {"model": model_name, "device": self.device})

    def generate(self, prompt: str, max_length: int = 100, temperature: float = 0.7) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                temperature=temperature,
                num_return_sequences=1
            )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        logger.log("HuggingFace model response generated", 
                   {"prompt": prompt[:50] + "...", "response_length": len(response)})
        return response

    def analyze_task(self, task: str, user_id: str) -> dict:
        prompt = f"Analyze the following task for user {user_id}:\\n{task}\\n\\nProvide a JSON response with 'subtasks' and 'parameters'."
        response = self.generate(prompt)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            logger.error("Error parsing JSON from task analysis")
            return {"subtasks": [], "parameters": {}}
"""
    write_file(os.path.join(models_dir, "huggingface_provider.py"), huggingface_provider_content.strip())

if __name__ == "__main__":
    create_models_files()
    print("AJ_MAS models files created successfully!")
