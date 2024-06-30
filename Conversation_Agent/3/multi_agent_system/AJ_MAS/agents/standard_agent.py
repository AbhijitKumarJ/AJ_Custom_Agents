from .base_agent import BaseAgent
from ..utils.logger import logger


class StandardAgent(BaseAgent):
    def perform_task(self, task, **kwargs):
        logger.log(
            f"Performing task", {"agent": self.name, "task": task, "kwargs": kwargs}
        )
        skill_scores = self.analyze_task(task)
        best_skill = max(skill_scores, key=lambda x: x[1])[0]
        try:
            task_info = self.task_analyzer.extract_parameters(task)
            subtasks = task_info["subtasks"]
            parameters = task_info["parameters"]

            parameters.update(kwargs)

            if subtasks:
                results = []
                for subtask in subtasks:
                    result = self.skills[best_skill].execute(
                        subtask=subtask, **parameters
                    )
                    results.append(result)
                result = results
            else:
                result = self.skills[best_skill].execute(
                    subtask="default", **parameters
                )

            logger.log(f"Task result", {"agent": self.name, "result": result})
            return result
        except Exception as e:
            error_msg = f"Error: {str(e)}. Please provide the necessary arguments for the {best_skill} skill."
            logger.log(f"Task error", {"agent": self.name, "error": error_msg})
            return error_msg
