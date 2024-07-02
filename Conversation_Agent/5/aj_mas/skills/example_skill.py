from .base_skill import BaseSkill
from .skill_loader import register_skill

@register_skill
class ExampleSkill(BaseSkill):
    def __init__(self):
        super().__init__("ExampleSkill", "An example skill implementation")

    def execute(self, parameters: dict) -> dict:
        # Implement the skill's logic here
        result = {"message": f"Executed ExampleSkill with parameters: {parameters}"}
        self.log_execution(parameters, result)
        return result