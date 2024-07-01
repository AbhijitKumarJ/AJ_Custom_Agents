from typing import Dict, Type
from .base_tool import BaseTool

class ToolRegistry:
    tools: Dict[str, Type[BaseTool]] = {}

    @classmethod
    def register(cls, tool_class: Type[BaseTool]):
        cls.tools[tool_class.__name__] = tool_class

    @classmethod
    def get(cls, tool_name: str) -> Type[BaseTool]:
        return cls.tools.get(tool_name)

    @classmethod
    def list_tools(cls) -> list:
        return list(cls.tools.keys())