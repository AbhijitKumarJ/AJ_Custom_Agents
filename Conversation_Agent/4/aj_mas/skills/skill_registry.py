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