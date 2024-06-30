from .base_agent import BaseAgent
from ..utils.logger import logger
import os


class PrimaryAgent(BaseAgent):
    def __init__(self, name, subordinate_agents):
        super().__init__(name, [])
        self.subordinate_agents = subordinate_agents
        self.current_user_id = None
        logger.log(
            f"Initialized PrimaryAgent",
            {
                "name": name,
                "subordinate_agents": [agent.name for agent in subordinate_agents],
            },
        )

    def perform_task(self, task, **kwargs):
        self.add_to_memory({"role": "user", "content": task})

        # Retrieve relevant documents
        relevant_docs = self.retrieve_relevant_documents(task)
        context = f"Relevant information:\n" + "\n".join(
            [f"{doc[0]}: {doc[1]}" for doc in relevant_docs]
        )

        # Add context to the task
        task_with_context = f"{context}\n\nUser task: {task}"

        result = self.coordinate_task(task_with_context)
        self.add_to_memory({"role": "system", "content": str(result)})
        return result

    def delegate_task(self, task, **kwargs):
        logger.log(
            f"Delegating task", {"agent": self.name, "task": task, "kwargs": kwargs}
        )
        agent_scores = [
            (agent, max(agent.analyze_task(task), key=lambda x: x[1])[1])
            for agent in self.subordinate_agents
        ]
        best_agent = max(agent_scores, key=lambda x: x[1])[0]
        logger.log(f"Selected agent for task", {"selected_agent": best_agent.name})
        return best_agent.perform_task(task, **kwargs)

    def coordinate_task(self, task):
        logger.log(f"Coordinating complex task", {"agent": self.name, "task": task})

        task_info = self.task_analyzer.analyze_task(task, self.current_user_id)
        subtasks = task_info["subtasks"]
        parameters = task_info["parameters"]

        if subtasks:
            results = []
            for subtask in subtasks:
                result = self.delegate_task(subtask, **parameters)
                results.append(result)
            result = results
        else:
            result = self.delegate_task(task, **parameters)

        logger.log(f"Task coordination completed", {"result": result})
        return result

    def get_user_input(self, prompt):
        user_input = input(f"{self.name}: {prompt}")
        logger.log("Received user input", {"input": user_input})
        return user_input

    def start_session(self, user_id):
        self.current_user_id = user_id
        self.memory.end_current_session(
            self.current_user_id
        )  # End any existing session
        logger.log(f"Started new session for user", {"user_id": user_id})

    def end_session(self):
        if self.current_user_id:
            self.memory.end_current_session(self.current_user_id)
            logger.log(f"Ended session for user", {"user_id": self.current_user_id})
            self.current_user_id = None

    def add_document(self, file_path):
        if not os.path.exists(file_path):
            return f"File not found: {file_path}"

        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        filename = os.path.basename(file_path)
        self.document_store.add_document(filename, content)
        return f"Document added: {filename}"
