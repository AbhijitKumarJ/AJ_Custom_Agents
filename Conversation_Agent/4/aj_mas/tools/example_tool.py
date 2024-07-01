from .base_tool import BaseTool
from .tool_loader import register_tool

@register_tool
class ExampleTool(BaseTool):
    def __init__(self):
        super().__init__("ExampleTool", "An example tool implementation")

    def execute(self, parameters: dict) -> dict:
        # Implement the tool's logic here
        result = {"message": f"Executed ExampleTool with parameters: {parameters}"}
        self.log_execution(parameters, result)
        return result