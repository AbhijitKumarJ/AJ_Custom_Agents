from .skills.skill_loader import ALL_SKILLS
from .agents.agent_loader import ALL_AGENTS
from .utils.logger import logger
from .config import config
import os


class MultiAgentSystem:
    def __init__(self):
        logger.log("Initializing MultiAgentSystem")
        self.agents = []

        # Create skill instances
        skill_instances = {
            skill_name: skill_class()
            for skill_name, skill_class in ALL_SKILLS.items()
            if config.get("skills", {}).get(skill_name, {}).get("enabled", False)
        }

        # Create agents
        for agent_name, agent_class in ALL_AGENTS.items():
            if config.get("agents", {}).get(agent_name, {}).get("enabled", False):
                if agent_name == "primary":
                    continue  # We'll create the primary agent last
                self.agents.append(
                    agent_class(
                        f"{agent_name.capitalize()} Agent",
                        list(skill_instances.values()),
                    )
                )

        # Create primary agent
        primary_agent_class = ALL_AGENTS.get("primary")
        if primary_agent_class and config.get("agents", {}).get("primary", {}).get(
            "enabled", False
        ):
            self.primary_agent = primary_agent_class("Coordinator", self.agents)
        else:
            raise ValueError("Primary agent is not enabled or not found")

        logger.log(
            "MultiAgentSystem initialized",
            {"agents": [agent.name for agent in self.agents + [self.primary_agent]]},
        )

    def run(self):
        logger.log("Starting MultiAgentSystem")
        print(f"{self.primary_agent.name}: Hello! Welcome to the Multi-Agent System.")

        while True:
            user_id = input("Please enter your user ID (or 'quit' to exit): ")
            if user_id.lower() == "quit":
                break

            self.primary_agent.start_session(user_id)
            print(
                f"{self.primary_agent.name}: Hello, {user_id}! How can I assist you today?"
            )

            while True:
                action = self.primary_agent.get_user_input(
                    "Choose an action (task/add_document/quit): "
                )

                if action.lower() == "quit":
                    break
                elif action.lower() == "add_document":
                    file_path = input("Enter the path to the text file: ")
                    result = self.primary_agent.add_document(file_path)
                    print(f"{self.primary_agent.name}: {result}")
                elif action.lower() == "task":
                    task = self.primary_agent.get_user_input(
                        "Please provide your task: "
                    )
                    try:
                        result = self.primary_agent.perform_task(task)
                        print(
                            f"{self.primary_agent.name}: Task completed. Result: {result}"
                        )
                    except Exception as e:
                        error_msg = f"An error occurred: {str(e)}"
                        logger.log("Error in task execution", {"error": error_msg})
                        print(f"{self.primary_agent.name}: {error_msg}")
                else:
                    print(
                        f"{self.primary_agent.name}: Invalid action. Please choose task, add_document, or quit."
                    )

            self.primary_agent.end_session()
            print(
                f"{self.primary_agent.name}: Goodbye, {user_id}! Your session has ended."
            )

        print(f"{self.primary_agent.name}: Thank you for using our system. Goodbye!")


if __name__ == "__main__":
    system = MultiAgentSystem()
    system.run()
