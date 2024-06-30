from .base_skill import BaseSkill
from ..utils.logger import logger


class MathSkill(BaseSkill):
    def __init__(self):
        super().__init__("Math", "Perform mathematical operations")

    def execute(self, subtask, **kwargs):
        logger.log(f"Executing Math Skill", {"subtask": subtask, "kwargs": kwargs})
        if subtask == "add":
            result = sum(kwargs.get("numbers", []))
        elif subtask == "multiply":
            result = 1
            for num in kwargs.get("numbers", []):
                result *= num
        else:
            result = f"Unsupported operation: {subtask}"
        logger.log(f"Math Skill Result", {"result": result})
        return result
