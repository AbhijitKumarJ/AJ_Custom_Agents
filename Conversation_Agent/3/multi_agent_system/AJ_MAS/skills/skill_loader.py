import os
import importlib
from .base_skill import BaseSkill


def load_skills():
    skills = {}
    skills_dir = os.path.dirname(__file__)
    for filename in os.listdir(skills_dir):
        if filename.endswith("_skill.py") and filename != "base_skill.py":
            module_name = filename[:-3]  # Remove .py extension
            module = importlib.import_module(f"AJ_MAS.skills.{module_name}")
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (
                    isinstance(attr, type)
                    and issubclass(attr, BaseSkill)
                    and attr != BaseSkill
                ):
                    skill_name = attr_name.replace("Skill", "").lower()
                    skills[skill_name] = attr
    return skills


ALL_SKILLS = load_skills()
