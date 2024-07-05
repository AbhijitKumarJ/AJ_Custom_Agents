import json
import requests

class AdvancedFeedbackDrivenAgent:
    def __init__(self, ollama_api_url):
        self.ollama_api_url = ollama_api_url
        self.task = None
        self.subtasks = []
        self.current_subtask = 0

    def run(self):
        self.task = input("Please enter the task you want to accomplish: ")
        self.get_subtasks()
        
        while self.current_subtask < len(self.subtasks):
            subtask = self.subtasks[self.current_subtask]
            self.get_subtask_details(subtask)
            
            print(f"\nCurrent subtask: {subtask['name']}")
            print(f"Details: {json.dumps(subtask['details'], indent=2)}")
            print(f"Remaining subtasks: {[st['name'] for st in self.subtasks[self.current_subtask+1:]]}")
            
            user_confirmation = input("Do you agree with this subtask and the future plan? (yes/no): ").lower()
            
            if user_confirmation == 'yes':
                self.execute_subtask(subtask)
                self.current_subtask += 1
            else:
                user_advice = input("Please provide your advice on how to proceed: ")
                self.modify_plan(user_advice)
        
        print("\nTask completed!")

    def get_subtasks(self):
        prompt = f"Divide the following task into subtasks and return the result as a JSON array of subtask names: {self.task}"
        response = self.call_ollama_api(prompt)
        self.subtasks = [{"name": name} for name in json.loads(response)]

    def get_subtask_details(self, subtask):
        prompt = f"Provide details for the subtask '{subtask['name']}' including any parameters or further subtasks. Return the result as a JSON object."
        response = self.call_ollama_api(prompt)
        subtask['details'] = json.loads(response)

    def execute_subtask(self, subtask):
        print(f"Executing subtask: {subtask['name']}")
        # Here you would implement the actual execution of the subtask
        # This could involve further API calls, user interactions, or other actions

    def modify_plan(self, user_advice):
        prompt = f"Based on the user's advice: '{user_advice}', suggest a new set of subtasks to accomplish the original task: {self.task}. Return the result as a JSON array of subtask names."
        response = self.call_ollama_api(prompt)
        new_subtasks = json.loads(response)
        
        print("Suggested new subtasks based on your advice:")
        for i, subtask in enumerate(new_subtasks):
            print(f"{i+1}. {subtask}")
        
        user_confirmation = input("Do you want to proceed with these new subtasks? (yes/no): ").lower()
        if user_confirmation == 'yes':
            self.subtasks = [{"name": name} for name in new_subtasks]
            self.current_subtask = 0
        else:
            print("Continuing with the current plan.")

    def call_ollama_api(self, prompt):
        headers = {'Content-Type': 'application/json'}
        data = {
            "model": "llama2",
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(self.ollama_api_url, headers=headers, json=data)
        return response.json()['response']

# Example usage
ollama_api_url = "http://localhost:11434/api/generate"  # Replace with your Ollama API URL
agent = AdvancedFeedbackDrivenAgent(ollama_api_url)
agent.run()
