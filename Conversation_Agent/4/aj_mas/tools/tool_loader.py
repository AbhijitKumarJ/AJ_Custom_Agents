import importlib
import os
from typing import Dict, Type
from .base_tool import BaseTool
from .tool_registry import ToolRegistry
from .tool_utils import getToolClassNameFromConfigName
from ..utils import logger
from ..config import config, load_config


def load_tools() -> Dict[str, BaseTool]:
    tools = {}
    tool_config = load_config(config["tool_config_path"])
    
    for tool_category, category_tools in tool_config.items():
        for tool_name, tool_info in category_tools.items():
            if tool_info.get('enabled', False):
                try:
                    module = importlib.import_module(f"aj_mas.tools.{tool_category}.{tool_name}")
                    tool_class = getattr(module, f"{getToolClassNameFromConfigName(tool_name)}")
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