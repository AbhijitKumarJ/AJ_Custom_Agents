import json
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from .model_provider import ModelProvider
from ..utils.logger import logger

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
        prompt = f"Analyze the following task for user {user_id}:\n{task}\n\nProvide a JSON response with 'subtasks' and 'parameters'."
        response = self.generate(prompt)
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            logger.error("Error parsing JSON from task analysis")
            return {"subtasks": [], "parameters": {}}