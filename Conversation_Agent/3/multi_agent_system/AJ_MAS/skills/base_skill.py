from abc import ABC, abstractmethod
from ..utils.logger import logger


class BaseSkill(ABC):
    def __init__(self, name, description):
        self.name = name
        self.description = description
        logger.log(f"Initialized {self.name} Skill", {"description": self.description})

    @abstractmethod
    def execute(self, subtask, **kwargs):
        pass
