from .base_skill import BaseSkill
from ..utils.logger import logger


class NumberGenerationSkill(BaseSkill):
    def __init__(self):
        super().__init__("NumberGeneration", "Generate number sequences")

    def execute(self, subtask, **kwargs):
        logger.log(
            f"Executing NumberGeneration Skill", {"subtask": subtask, "kwargs": kwargs}
        )
        if subtask == "consecutive":
            start = kwargs.get("start", 1)
            end = kwargs.get("end", 10)
            if start < end - 1:
                result = [start, start + 1]
            else:
                result = [end - 1, end]
        else:
            result = f"Unsupported subtask: {subtask}"
        logger.log(f"NumberGeneration Skill Result", {"result": result})
        return result
