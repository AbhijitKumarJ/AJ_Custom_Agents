import os

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def write_file(path, content):
    with open(path, 'w') as f:
        f.write(content)
    print(f"Created file: {path}")

def create_tools_main_files():
    tools_dir = "aj_mas/tools"
    create_directory(tools_dir)

    # __init__.py
    init_content = """
from .base_tool import BaseTool
from .tool_loader import load_tools, register_tool
from .tool_registry import ToolRegistry
"""
    write_file(os.path.join(tools_dir, "__init__.py"), init_content.strip())

    # base_tool.py
    base_tool_content = """
from abc import ABC, abstractmethod
from aj_mas.utils import logger

class BaseTool(ABC):
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
"""
    write_file(os.path.join(tools_dir, "base_tool.py"), base_tool_content.strip())

    # tool_loader.py
    tool_loader_content = """
import importlib
import os
from typing import Dict, Type
from .base_tool import BaseTool
from .tool_registry import ToolRegistry
from aj_mas.utils import logger, load_config

def load_tools() -> Dict[str, BaseTool]:
    tools = {}
    tool_config = load_config()['tools']
    
    for tool_name, tool_info in tool_config.items():
        if tool_info.get('enabled', False):
            try:
                module = importlib.import_module(f"aj_mas.tools.{tool_name}")
                tool_class = getattr(module, f"{tool_name.capitalize()}Tool")
                tools[tool_name] = tool_class()
                logger.log(f"Loaded tool: {tool_name}")
            except (ImportError, AttributeError) as e:
                logger.error(f"Failed to load tool: {tool_name}", {"error": str(e)})
    
    return tools

def register_tool(tool_class: Type[BaseTool]):
    ToolRegistry.register(tool_class)
    logger.log(f"Registered tool: {tool_class.__name__}")

def get_tool(tool_name: str) -> BaseTool:
    return ToolRegistry.get(tool_name)

def list_available_tools() -> list:
    return list(ToolRegistry.tools.keys())
"""
    write_file(os.path.join(tools_dir, "tool_loader.py"), tool_loader_content.strip())

    # tool_registry.py
    tool_registry_content = """
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
"""
    write_file(os.path.join(tools_dir, "tool_registry.py"), tool_registry_content.strip())

    # example_tool.py
    example_tool_content = """
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
"""
    write_file(os.path.join(tools_dir, "example_tool.py"), example_tool_content.strip())

    # tool_utils.py
    tool_utils_content = """
from typing import List
from .base_tool import BaseTool

def chain_tools(tools: List[BaseTool], initial_input: dict) -> dict:
    result = initial_input
    for tool in tools:
        result = tool.execute(result)
    return result

def parallel_execute(tools: List[BaseTool], input_data: dict) -> List[dict]:
    return [tool.execute(input_data) for tool in tools]

def validate_tool_parameters(tool: BaseTool, parameters: dict) -> bool:
    # Implement parameter validation logic here
    # This is a placeholder implementation
    return True
"""
    write_file(os.path.join(tools_dir, "tool_utils.py"), tool_utils_content.strip())

if __name__ == "__main__":
    create_tools_main_files()
    print("AJ_MAS tools main files created successfully!")
