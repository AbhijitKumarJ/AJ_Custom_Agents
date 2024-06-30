import os
import importlib
from .base_agent import BaseAgent


def load_agents():
    agents = {}
    agents_dir = os.path.dirname(__file__)
    for filename in os.listdir(agents_dir):
        if filename.endswith("_agent.py") and filename != "base_agent.py":
            module_name = filename[:-3]  # Remove .py extension
            module = importlib.import_module(f"AJ_MAS.agents.{module_name}")
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (
                    isinstance(attr, type)
                    and issubclass(attr, BaseAgent)
                    and attr != BaseAgent
                ):
                    agent_name = attr_name.replace("Agent", "").lower()
                    agents[agent_name] = attr
    return agents


ALL_AGENTS = load_agents()
