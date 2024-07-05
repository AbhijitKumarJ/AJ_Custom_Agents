import json
import requests
from pprint import PrettyPrinter
from typing import List, Dict, Any

class Logger:
    def __init__(self):
        self.pp = PrettyPrinter(indent=2)

    def log(self, message: str, data: Any = None):
        print(f"\n{message}")
        if data:
            self.pp.pprint(data)

logger = Logger()

class OllamaAPI:
    def __init__(self, api_url: str):
        self.api_url = api_url

    def call(self, prompt: str) -> str:
        headers = {'Content-Type': 'application/json'}
        data = {
            "model": "llama2",
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(self.api_url, headers=headers, json=data)
        return response.json()['response']

class UserProxyAgent:
    def get_main_task(self) -> str:
        return input("Please enter the main task you want to accomplish: ")

    def get_feedback(self, message: str) -> str:
        return input(message)

class ExecutorAgent:
    def execute_task(self, task: Dict[str, Any]):
        logger.log(f"Executing task: {task['name']}")
        logger.log("Task details:", task)
        # Simulating task execution
        return {"status": "completed", "result": f"Executed {task['name']}"}

class JuniorAgent:
    def __init__(self, ollama_api: OllamaAPI):
        self.ollama_api = ollama_api

    def execute_subtask(self, subtask: Dict[str, Any]) -> Dict[str, Any]:
        logger.log(f"Junior Agent executing subtask: {subtask['name']}")
        # Simulating subtask execution
        result = self.ollama_api.call(f"Provide a detailed result for the subtask: {json.dumps(subtask)}")
        return {"status": "completed", "result": result}

class SeniorAgent:
    def __init__(self, ollama_api: OllamaAPI):
        self.ollama_api = ollama_api

    def plan_task(self, task: str) -> List[Dict[str, Any]]:
        logger.log("Senior Agent planning task:", task)
        prompt = f"Divide the following task into subtasks and return the result as a JSON array of objects. Each object should have 'name', 'description', and 'parameters' keys. If a subtask has further subtasks, include them in a 'subtasks' key: {task}"
        response = self.ollama_api.call(prompt)
        return json.loads(response)

class PrimaryAgent:
    def __init__(self, ollama_api: OllamaAPI, user_proxy: UserProxyAgent, senior_agent: SeniorAgent, junior_agent: JuniorAgent, executor_agent: ExecutorAgent):
        self.ollama_api = ollama_api
        self.user_proxy = user_proxy
        self.senior_agent = senior_agent
        self.junior_agent = junior_agent
        self.executor_agent = executor_agent

    def run(self):
        main_task = self.user_proxy.get_main_task()
        task_plan = self.senior_agent.plan_task(main_task)
        self.execute_task_plan(task_plan)
        logger.log("Main task completed!")

    def execute_task_plan(self, tasks: List[Dict[str, Any]], level: int = 0):
        for task in tasks:
            logger.log(f"{'  ' * level}Current task: {task['name']}")
            logger.log(f"{'  ' * level}Description: {task['description']}")
            logger.log(f"{'  ' * level}Parameters:", task['parameters'])

            if 'subtasks' in task:
                logger.log(f"{'  ' * level}This task has subtasks:")
                for subtask in task['subtasks']:
                    logger.log(f"{'  ' * (level+1)}- {subtask['name']}")

            user_confirmation = self.user_proxy.get_feedback(f"{'  ' * level}Do you agree with this task and its details? (yes/no): ").lower()

            if user_confirmation == 'yes':
                if 'subtasks' in task:
                    self.execute_task_plan(task['subtasks'], level + 1)
                else:
                    result = self.junior_agent.execute_subtask(task)
                    logger.log(f"{'  ' * level}Junior Agent completed subtask:", result)
                execution_result = self.executor_agent.execute_task(task)
                logger.log(f"{'  ' * level}Executor Agent result:", execution_result)
            else:
                user_advice = self.user_proxy.get_feedback(f"{'  ' * level}Please provide your advice on how to proceed: ")
                modified_task = self.modify_task(task, user_advice)
                self.execute_task_plan([modified_task], level)

    def modify_task(self, task: Dict[str, Any], user_advice: str) -> Dict[str, Any]:
        logger.log("Modifying task based on user advice:")
        prompt = f"Based on the user's advice: '{user_advice}', modify the following task: {json.dumps(task)}. Return the modified task as a JSON object with 'name', 'description', 'parameters', and optionally 'subtasks' keys."
        response = self.ollama_api.call(prompt)
        modified_task = json.loads(response)
        logger.log("Modified task:", modified_task)
        return modified_task

def main():
    ollama_api_url = "http://localhost:11434/api/generate"  # Replace with your Ollama API URL
    ollama_api = OllamaAPI(ollama_api_url)
    user_proxy = UserProxyAgent()
    senior_agent = SeniorAgent(ollama_api)
    junior_agent = JuniorAgent(ollama_api)
    executor_agent = ExecutorAgent()
    primary_agent = PrimaryAgent(ollama_api, user_proxy, senior_agent, junior_agent, executor_agent)
    primary_agent.run()

if __name__ == "__main__":
    main()
