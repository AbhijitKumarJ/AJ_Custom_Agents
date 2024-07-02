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


def getToolClassNameFromConfigName(tool_config_name: str) -> str:
    return "".join(
        [name_part.capitalize() for name_part in tool_config_name.split("_")]
    )
