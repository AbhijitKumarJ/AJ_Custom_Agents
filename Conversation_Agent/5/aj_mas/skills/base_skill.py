from abc import ABC, abstractmethod
from ..utils import logger

class BaseSkill(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def execute(self, parameters: dict) -> dict:
        pass

    def log_execution(self, parameters: dict, result: dict):
        logger.log(f"Executed {self.name}", {
            "parameters": parameters,
            "result": result
        })

    def __str__(self):
        return f"{self.name}: {self.description}"