import json
from .logger import logger
from .memory_system import memory_system
from .ollama_api import OllamaAPI
from ..config import config
from transformers import AutoModelForCausalLM, AutoTokenizer


class TaskAnalyzer:
    def __init__(self):
        self.config = config
        self.prompt_template = self.config["task_analyzer"]["prompt_template"]
        self.model = self.load_model()
        logger.log("Initialized TaskAnalyzer")

    def load_model(self):
        model_config = self.config["model"]
        if model_config["type"] == "ollama":
            return OllamaAPI(model_config["name"])
        elif model_config["type"] == "transformers":
            tokenizer = AutoTokenizer.from_pretrained(model_config["huggingface_repo"])
            model = AutoModelForCausalLM.from_pretrained(
                model_config["huggingface_repo"]
            )
            return (model, tokenizer)
        else:
            raise ValueError(f"Unsupported model type: {model_config['type']}")

    def analyze_task(self, task, user_id):
        logger.log(f"Analyzing task", {"task": task, "user_id": user_id})

        # Get user history
        user_history = memory_system.get_user_sessions(user_id)
        recent_history = user_history[-5:]  # Get last 5 sessions

        # Prepare context
        context = "\n".join(
            [
                f"Session {i+1}: {session['conversation']}"
                for i, session in enumerate(recent_history)
            ]
        )

        # Prepare prompt
        prompt = self.prompt_template.format(task=task, context=context)

        # Generate response
        if isinstance(self.model, tuple):  # Transformers model
            model, tokenizer = self.model
            inputs = tokenizer(prompt, return_tensors="pt")
            outputs = model.generate(
                **inputs, max_length=self.config["model"]["max_length"]
            )
            response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        else:  # Ollama API
            response = self.model.generate(prompt)

        try:
            parsed_response = json.loads(response)
            logger.log("Extracted parameters and subtasks", parsed_response)
            return parsed_response
        except json.JSONDecodeError:
            logger.error(
                "Error parsing JSON from model response", {"response": response}
            )
            return {"subtasks": [], "parameters": {}}


# task_analyzer = TaskAnalyzer()
