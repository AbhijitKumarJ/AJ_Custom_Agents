from transformers import pipeline
import random

class BaseAgent:
    def __init__(self, name, expertise):
        self.name = name
        self.expertise = expertise
        self.classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

    def analyze_task(self, task):
        # Simulate task analysis based on expertise
        relevance = self.classifier(task, [self.expertise], multi_label=False)
        return relevance['scores'][0]

    def perform_task(self, task):
        # Simulate task performance
        return f"{self.name} performed task: {task}"

class PrimaryAgent(BaseAgent):
    def __init__(self, name, subordinate_agents):
        super().__init__(name, "coordination")
        self.subordinate_agents = subordinate_agents

    def delegate_task(self, task):
        # Analyze task relevance for each agent
        agent_scores = [(agent, agent.analyze_task(task)) for agent in self.subordinate_agents]
        best_agent = max(agent_scores, key=lambda x: x[1])[0]
        return best_agent.perform_task(task)

    def coordinate_task(self, task):
        print(f"{self.name}: Analyzing task - '{task}'")
        result = self.delegate_task(task)
        print(f"{self.name}: Task completed. Result: {result}")

    def get_user_input(self, prompt):
        return input(f"{self.name}: {prompt}")

class MultiAgentSystem:
    def __init__(self):
        self.agents = [
            BaseAgent("Math Agent", "mathematics"),
            BaseAgent("Language Agent", "language processing"),
            BaseAgent("Data Agent", "data analysis")
        ]
        self.primary_agent = PrimaryAgent("Coordinator", self.agents)

    def run(self):
        print(f"{self.primary_agent.name}: Hello! I'm the coordinator. How can we assist you today?")
        while True:
            task = self.primary_agent.get_user_input("Please provide a task, or type 'quit' to exit: ")
            if task.lower() == 'quit':
                print(f"{self.primary_agent.name}: Thank you for using our system. Goodbye!")
                break
            self.primary_agent.coordinate_task(task)

#if __name__ == "__main__":
system = MultiAgentSystem()
system.run()