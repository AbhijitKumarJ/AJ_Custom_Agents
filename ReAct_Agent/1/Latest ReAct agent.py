import torch
from typing import List, Tuple, Dict, Any
from transformers import pipeline
from datetime import datetime
from pprint import pprint, pformat
import sys

class Logger:
    @staticmethod
    def log(message: str, data: Any = None):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}", file=sys.stderr)
        if data is not None:
            print(pformat(data, indent=2, width=120), file=sys.stderr)
        print(file=sys.stderr)  # Add a blank line for readability

class IntentClassifier:
    def __init__(self, model_name: str = "facebook/bart-large-mnli"):
        self.classifier = pipeline("zero-shot-classification", model=model_name)
        self.action_templates = [
            ("The user is greeting someone.", "greet"),
            ("The user is saying goodbye.", "farewell"),
            ("The user is asking about the weather.", "get_weather"),
            ("The user is requesting a joke.", "tell_joke"),
            ("The user is asking for the current time.", "ask_time")
        ]
        Logger.log("IntentClassifier initialized", {"model": model_name, "templates": self.action_templates})

    def classify_intent(self, user_input: str) -> Dict:
        Logger.log("IntentClassifier: Classifying intent", {"input": user_input})
        candidate_labels = [template for template, _ in self.action_templates]
        outputs = self.classifier(user_input, candidate_labels, multi_label=False)
        
        Logger.log("IntentClassifier: Classification model raw output", outputs)

        best_action_label = outputs["labels"][0]
        best_action_score = outputs["scores"][0]

        action = next((action for template, action in self.action_templates if template == best_action_label), "unknown")

        result = {"action": action, "confidence": best_action_score}
        Logger.log("IntentClassifier: Classification result", result)
        return result

class ParameterExtractor:
    @staticmethod
    def extract_parameters(user_input: str, action: str) -> Dict:
        Logger.log("ParameterExtractor: Extracting parameters", {"action": action, "input": user_input})
        parameters = {}
        if action == "get_weather":
            words = user_input.lower().split()
            if "in" in words:
                location_index = words.index("in") + 1
                if location_index < len(words):
                    parameters["location"] = " ".join(words[location_index:])
        Logger.log("ParameterExtractor: Extracted parameters", parameters)
        return parameters

class ActionHandler:
    @staticmethod
    def greet(params: Dict) -> str:
        Logger.log("ActionHandler: Generating greeting")
        return "Hello! How can I assist you today?"

    @staticmethod
    def farewell(params: Dict) -> str:
        Logger.log("ActionHandler: Generating farewell")
        return "Goodbye! Have a great day!"

    @staticmethod
    def get_weather(params: Dict) -> str:
        location = params.get('location', 'your area')
        Logger.log("ActionHandler: Generating weather response", {"location": location})
        return f"The weather in {location} is sunny with a high of 75°F (24°C)."

    @staticmethod
    def tell_joke(params: Dict) -> str:
        Logger.log("ActionHandler: Telling a joke")
        return "Why don't scientists trust atoms? Because they make up everything!"

    @staticmethod
    def ask_time(params: Dict) -> str:
        current_time = datetime.now().strftime("%I:%M %p")
        Logger.log("ActionHandler: Providing current time", {"time": current_time})
        return f"The current time is {current_time}."

    @staticmethod
    def unknown_action(params: Dict) -> str:
        Logger.log("ActionHandler: Handling unknown action")
        return "I'm not sure how to respond to that. Can you please clarify or ask something else?"

class AdvancedReActAgent:
    def __init__(self):
        self.context = []
        self.intent_classifier = IntentClassifier()
        self.parameter_extractor = ParameterExtractor()
        self.action_handler = ActionHandler()
        Logger.log("AdvancedReActAgent initialized")

    def think(self, user_input: str) -> Tuple[List[Tuple[str, str]], Dict]:
        Logger.log("AdvancedReActAgent: Thinking process started", {"input": user_input})
        intent_info = self.intent_classifier.classify_intent(user_input)
        parameters = self.parameter_extractor.extract_parameters(user_input, intent_info['action'])
        
        thoughts = [
            ("Intent", f"Model determined the action as: {intent_info['action']} with confidence {intent_info['confidence']:.2f}"),
            ("Parameters", f"Extracted parameters: {parameters}")
        ]
        
        action_info = {**intent_info, "parameters": parameters}
        Logger.log("AdvancedReActAgent: Thinking process completed", {"thoughts": thoughts, "action_info": action_info})
        return thoughts, action_info

    def act(self, action_info: Dict) -> str:
        Logger.log("AdvancedReActAgent: Acting", action_info)
        action_method = getattr(self.action_handler, action_info['action'], self.action_handler.unknown_action)
        response = action_method(action_info['parameters'])
        Logger.log("AdvancedReActAgent: Action completed", {"response": response})
        return response

    def respond(self, user_input: str) -> str:
        Logger.log("AdvancedReActAgent: Responding to user input", {"input": user_input})
        thoughts, action_info = self.think(user_input)
        response = self.act(action_info)
        self.context.append(user_input)
        if len(self.context) > 5:  # Keep only the last 5 interactions for context
            self.context.pop(0)
        Logger.log("AdvancedReActAgent: Response generated", {"response": response, "updated_context": self.context})
        return response

    def run(self):
        Logger.log("AdvancedReActAgent: Starting the agent")
        print("Advanced ReAct Agent: Hello! I'm an advanced ReAct agent using a Hugging Face model. How can I assist you?")
        while True:
            user_input = input("You: ")
            Logger.log("AdvancedReActAgent: Received user input", {"input": user_input})
            if user_input.lower() == "quit":
                Logger.log("AdvancedReActAgent: User requested to quit")
                print("Advanced ReAct Agent: Goodbye!")
                break
            response = self.respond(user_input)
            print(f"Advanced ReAct Agent: {response}")
        Logger.log("AdvancedReActAgent: Agent shutting down")

#if __name__ == "__main__":
Logger.log("Main: Initializing AdvancedReActAgent")
agent = AdvancedReActAgent()
Logger.log("Main: Starting agent run")
agent.run()