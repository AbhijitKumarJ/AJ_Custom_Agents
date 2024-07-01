import importlib
import os
from typing import Dict, Type
from .base_skill import BaseSkill
from .skill_registry import SkillRegistry
from ..utils import logger
from ..config import config, load_config

def load_skills() -> Dict[str, BaseSkill]:
    skills = {}
    skill_config = load_config(config["skill_config_path"])
    
    for skill_category, category_skills in skill_config.items():
        for skill_name, skill_info in category_skills.items():
            if skill_info.get('enabled', False):
                try:
                    module = importlib.import_module(f"aj_mas.skills.{skill_category}.{skill_name}")
                    skill_class = getattr(module, f"{skill_name.replace("_", "").capitalize()}Skill")
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