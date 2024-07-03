from enum import Enum
from typing import Dict, List

class SkillArea(Enum):
    TRAVEL = "TRAVEL"
    HEALTH = "HEALTH"
    GENERAL = "GENERAL"

class LanguageProficiency(Enum):
    NATIVE = 5
    FLUENT = 4
    ADVANCED = 3
    INTERMEDIATE = 2
    BASIC = 1

class AgentPersona:
    def __init__(self, name: str, gender: str, ethnicity: str, religious_inclination: str):
        self.name = name
        self.gender = gender
        self.ethnicity = ethnicity
        self.religious_inclination = religious_inclination
        self.skill_proficiencies: Dict[SkillArea, float] = {}
        self.tool_proficiencies: Dict[str, float] = {}
        self.language_proficiencies: Dict[str, LanguageProficiency] = {}
        self.personality_traits: List[str] = []
        self.communication_style: str = ""

    def set_skill_proficiency(self, skill_area: SkillArea, proficiency: float):
        if 0 <= proficiency <= 1:
            self.skill_proficiencies[skill_area] = proficiency
        else:
            raise ValueError("Proficiency must be between 0 and 1")

    def set_tool_proficiency(self, tool_name: str, proficiency: float):
        if 0 <= proficiency <= 1:
            self.tool_proficiencies[tool_name] = proficiency
        else:
            raise ValueError("Proficiency must be between 0 and 1")

    def set_language_proficiency(self, language: str, proficiency: LanguageProficiency):
        self.language_proficiencies[language] = proficiency

    def add_personality_trait(self, trait: str):
        self.personality_traits.append(trait)

    def set_communication_style(self, style: str):
        self.communication_style = style

    def __str__(self):
        return f"AgentPersona: {self.name} ({self.gender}, {self.ethnicity})"

    def to_dict(self):
        return {
            "name": self.name,
            "gender": self.gender,
            "ethnicity": self.ethnicity,
            "religious_inclination": self.religious_inclination,
            "skill_proficiencies": {k.value: v for k, v in self.skill_proficiencies.items()},
            "tool_proficiencies": self.tool_proficiencies,
            "language_proficiencies": {k: v.value for k, v in self.language_proficiencies.items()},
            "personality_traits": self.personality_traits,
            "communication_style": self.communication_style
        }

    @classmethod
    def from_dict(cls, data):
        persona = cls(
            data["name"],
            data["gender"],
            data["ethnicity"],
            data["religious_inclination"]
        )
        for skill, prof in data["skill_proficiencies"].items():
            persona.set_skill_proficiency(SkillArea(skill), prof)
        for tool, prof in data["tool_proficiencies"].items():
            persona.set_tool_proficiency(tool, prof)
        for lang, prof in data["language_proficiencies"].items():
            persona.set_language_proficiency(lang, LanguageProficiency(prof))
        for trait in data["personality_traits"]:
            persona.add_personality_trait(trait)
        persona.set_communication_style(data["communication_style"])
        return persona
