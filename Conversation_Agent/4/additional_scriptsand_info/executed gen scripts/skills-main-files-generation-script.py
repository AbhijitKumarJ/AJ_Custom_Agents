import os

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def write_file(path, content):
    with open(path, 'w') as f:
        f.write(content)
    print(f"Created file: {path}")

def create_skills_main_files():
    skills_dir = "aj_mas/skills"
    create_directory(skills_dir)

    # __init__.py
    init_content = """
from .base_skill import BaseSkill
from .skill_loader import load_skills, register_skill
from .skill_registry import SkillRegistry
"""
    write_file(os.path.join(skills_dir, "__init__.py"), init_content.strip())

    # base_skill.py
    base_skill_content = """
from abc import ABC, abstractmethod
from aj_mas.utils import logger

class BaseSkill(ABC):
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
    write_file(os.path.join(skills_dir, "base_skill.py"), base_skill_content.strip())

    # skill_loader.py
    skill_loader_content = """
import importlib
import os
from typing import Dict, Type
from .base_skill import BaseSkill
from .skill_registry import SkillRegistry
from aj_mas.utils import logger, load_config

def load_skills() -> Dict[str, BaseSkill]:
    skills = {}
    skill_config = load_config()['skills']
    
    for skill_name, skill_info in skill_config.items():
        if skill_info.get('enabled', False):
            try:
                module = importlib.import_module(f"aj_mas.skills.{skill_name}")
                skill_class = getattr(module, f"{skill_name.capitalize()}Skill")
                skills[skill_name] = skill_class()
                logger.log(f"Loaded skill: {skill_name}")
            except (ImportError, AttributeError) as e:
                logger.error(f"Failed to load skill: {skill_name}", {"error": str(e)})
    
    return skills

def register_skill(skill_class: Type[BaseSkill]):
    SkillRegistry.register(skill_class)
    logger.log(f"Registered skill: {skill_class.__name__}")

def get_skill(skill_name: str) -> BaseSkill:
    return SkillRegistry.get(skill_name)

def list_available_skills() -> list:
    return list(SkillRegistry.skills.keys())
"""
    write_file(os.path.join(skills_dir, "skill_loader.py"), skill_loader_content.strip())

    # skill_registry.py
    skill_registry_content = """
from typing import Dict, Type
from .base_skill import BaseSkill

class SkillRegistry:
    skills: Dict[str, Type[BaseSkill]] = {}

    @classmethod
    def register(cls, skill_class: Type[BaseSkill]):
        cls.skills[skill_class.__name__] = skill_class

    @classmethod
    def get(cls, skill_name: str) -> Type[BaseSkill]:
        return cls.skills.get(skill_name)

    @classmethod
    def list_skills(cls) -> list:
        return list(cls.skills.keys())
"""
    write_file(os.path.join(skills_dir, "skill_registry.py"), skill_registry_content.strip())

    # example_skill.py
    example_skill_content = """
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
"""
    write_file(os.path.join(skills_dir, "example_skill.py"), example_skill_content.strip())

if __name__ == "__main__":
    create_skills_main_files()
    print("AJ_MAS skills main files created successfully!")
