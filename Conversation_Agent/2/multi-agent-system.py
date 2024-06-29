import random
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from pprint import pprint, pformat
from datetime import datetime

class Logger:
    @staticmethod
    def log(message, data=None):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")
        if data:
            print(pformat(data, indent=2, width=120))
        print()  # Add a blank line for readability

class Skill:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        Logger.log(f"Initialized {self.name} Skill", {"description": self.description})

    def execute(self, subtask, **kwargs):
        raise NotImplementedError("This method should be implemented by subclasses")

class MathSkill(Skill):
    def __init__(self):
        super().__init__("Math", "Perform mathematical operations")

    def execute(self, subtask, **kwargs):
        Logger.log(f"Executing Math Skill", {"subtask": subtask, "kwargs": kwargs})
        if subtask == "add":
            result = sum(kwargs.get('numbers', []))
        elif subtask == "multiply":
            result = 1
            for num in kwargs.get('numbers', []):
                result *= num
        else:
            result = f"Unsupported operation: {subtask}"
        Logger.log(f"Math Skill Result", {"result": result})
        return result

class LanguageSkill(Skill):
    def __init__(self):
        super().__init__("Language", "Perform language-related tasks")
        self.tokenizer = AutoTokenizer.from_pretrained("t5-small")
        self.model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)
        Logger.log("Initialized T5 model for translation", {"device": self.device})

    def execute(self, subtask, **kwargs):
        Logger.log(f"Executing Language Skill", {"subtask": subtask, "kwargs": kwargs})
        if subtask == "count_words":
            result = len(kwargs.get('text', '').split())
        elif subtask == "reverse":
            result = kwargs.get('text', '')[::-1]
        elif subtask == "translate":
            if not kwargs.get('target_language'):
                raise ValueError("Target language is required for translation")
            result = self.translate(kwargs.get('text', ''), kwargs.get('target_language'))
        else:
            result = f"Unsupported subtask: {subtask}"
        Logger.log(f"Language Skill Result", {"result": result})
        return result

    def translate(self, text, target_language):
        Logger.log(f"Translating text", {"text": text, "target_language": target_language})
        input_text = f"translate English to {target_language}: {text}"
        input_ids = self.tokenizer.encode(input_text, return_tensors="pt").to(self.device)
        outputs = self.model.generate(input_ids, max_length=100, num_beams=4, early_stopping=True)
        translated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        Logger.log(f"Translation Result", {"translated_text": translated_text})
        return translated_text

class NumberGenerationSkill(Skill):
    def __init__(self):
        super().__init__("NumberGeneration", "Generate number sequences")

    def execute(self, subtask, **kwargs):
        Logger.log(f"Executing NumberGeneration Skill", {"subtask": subtask, "kwargs": kwargs})
        if subtask == "consecutive":
            start = kwargs.get('start', 1)
            end = kwargs.get('end', 10)
            if start < end - 1:
                result = [start, start + 1]
            else:
                result = [end - 1, end]
        else:
            result = f"Unsupported subtask: {subtask}"
        Logger.log(f"NumberGeneration Skill Result", {"result": result})
        return result

class BaseAgent:
    def __init__(self, name, skills):
        self.name = name
        self.skills = {skill.name: skill for skill in skills}
        self.classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        Logger.log(f"Initialized BaseAgent", {"name": name, "skills": list(self.skills.keys())})

    def analyze_task(self, task):
        Logger.log(f"Analyzing task", {"agent": self.name, "task": task})
        skill_names = list(self.skills.keys())
        result = self.classifier(task, skill_names, multi_label=True)
        analysis = list(zip(result['labels'], result['scores']))
        Logger.log(f"Task analysis result", {"analysis": analysis})
        return analysis

    def perform_task(self, task, **kwargs):
        Logger.log(f"Performing task", {"agent": self.name, "task": task, "kwargs": kwargs})
        skill_scores = self.analyze_task(task)
        best_skill = max(skill_scores, key=lambda x: x[1])[0]
        try:
            # Extract subtask from kwargs or use a default value
            subtask = kwargs.pop('subtask', 'default')
            result = self.skills[best_skill].execute(subtask=subtask, **kwargs)
            Logger.log(f"Task result", {"agent": self.name, "result": result})
            return result
        except TypeError as e:
            error_msg = f"Error: {str(e)}. Please provide the necessary arguments for the {best_skill} skill."
            Logger.log(f"Task error", {"agent": self.name, "error": error_msg})
            return error_msg

class PrimaryAgent(BaseAgent):
    def __init__(self, name, subordinate_agents):
        super().__init__(name, [])
        self.subordinate_agents = subordinate_agents
        Logger.log(f"Initialized PrimaryAgent", {"name": name, "subordinate_agents": [agent.name for agent in subordinate_agents]})

    def delegate_task(self, task, **kwargs):
        Logger.log(f"Delegating task", {"agent": self.name, "task": task, "kwargs": kwargs})
        agent_scores = [(agent, max(agent.analyze_task(task), key=lambda x: x[1])[1]) 
                        for agent in self.subordinate_agents]
        best_agent = max(agent_scores, key=lambda x: x[1])[0]
        Logger.log(f"Selected agent for task", {"selected_agent": best_agent.name})
        return best_agent.perform_task(task, **kwargs)

    def coordinate_task(self, task):
        Logger.log(f"Coordinating complex task", {"agent": self.name, "task": task})
        
        if "numbers" in task.lower() and "french" in task.lower():
            Logger.log("Breaking down complex task")
            number_agent = next(agent for agent in self.subordinate_agents if isinstance(agent.skills.get("NumberGeneration"), NumberGenerationSkill))
            numbers = number_agent.perform_task(task="generate numbers", subtask="consecutive", start=1, end=10)
            
            number_string = f"{numbers[0]} and {numbers[1]}"
            Logger.log("Generated number string", {"number_string": number_string})
            
            language_agent = next(agent for agent in self.subordinate_agents if isinstance(agent.skills.get("Language"), LanguageSkill))
            result = language_agent.perform_task(task="translate to French", subtask="translate", text=number_string, target_language="French")
        else:
            result = self.delegate_task(task, subtask="default")
        
        Logger.log(f"Task coordination completed", {"result": result})
        return result

    def get_user_input(self, prompt):
        user_input = input(f"{self.name}: {prompt}")
        Logger.log("Received user input", {"input": user_input})
        return user_input


class MultiAgentSystem:
    def __init__(self):
        Logger.log("Initializing MultiAgentSystem")
        self.agents = [
            BaseAgent("Math Agent", [MathSkill()]),
            BaseAgent("Language Agent", [LanguageSkill()]),
            BaseAgent("Number Agent", [NumberGenerationSkill()]),
            BaseAgent("Multi-skilled Agent", [MathSkill(), LanguageSkill(), NumberGenerationSkill()])
        ]
        self.primary_agent = PrimaryAgent("Coordinator", self.agents)
        Logger.log("MultiAgentSystem initialized", {"agents": [agent.name for agent in self.agents]})

    def run(self):
        Logger.log("Starting MultiAgentSystem")
        print(f"{self.primary_agent.name}: Hello! I'm the coordinator. How can we assist you today?")
        while True:
            task = self.primary_agent.get_user_input("Please provide a task, or type 'quit' to exit: ")
            if task.lower() == 'quit':
                Logger.log("User requested to quit")
                print(f"{self.primary_agent.name}: Thank you for using our system. Goodbye!")
                break
            
            try:
                result = self.primary_agent.coordinate_task(task)
                print(f"{self.primary_agent.name}: Task completed. Result: {result}")
            except Exception as e:
                error_msg = f"An error occurred: {str(e)}"
                Logger.log("Error in task execution", {"error": error_msg})
                print(f"{self.primary_agent.name}: {error_msg}")

if __name__ == "__main__":
    system = MultiAgentSystem()
    system.run()