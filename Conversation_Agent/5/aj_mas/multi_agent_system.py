from .agents import create_agent, get_available_agent_types
from .skills import load_skills
from .models import OllamaProvider
from .document_store import FastTextChromaStore
from .utils import logger
from .config import config, load_config
import sys


def initialize_system():
    #config = load_config()
    skills = load_skills()
    model_provider = OllamaProvider(config["model_provider"]["name"])
    document_store = FastTextChromaStore(config["document_store"]["storage_dir"])
    return skills, model_provider, document_store


def run_aj_mas():
    logger.log("Starting AJ_MAS system")
    skills, model_provider, document_store = initialize_system()

    while True:
        print("\nWelcome to AJ_MAS! Please choose an option:")
        print("1. Create an agent")
        print("2. List available agent types")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            agent_type = input("Enter the type of agent you want to create: ")
            agent = create_agent(
                agent_type,
                skills,
                model_provider,
                document_store,
                config["agent_config_path"],
            )
            if agent:
                user_id = input("Enter a user ID for this session: ")
                agent.start_session(user_id)
                while True:
                    task = input(
                        "Enter a task for the agent (or 'quit' to end session): "
                    )
                    if task.lower() == "quit":
                        break
                    response = agent.perform_task(task)
                    print(f"Agent response: {response}")
                agent.end_session()
        elif choice == "2":
            agent_types = get_available_agent_types()
            print(f"Available agent types: {', '.join(agent_types)}")
        elif choice == "3":
            print("Thank you for using AJ_MAS. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    run_aj_mas()
