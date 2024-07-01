import os

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def write_file(path, content):
    with open(path, 'w') as f:
        f.write(content)
    print(f"Created file: {path}")

def create_personas_files():
    personas_dir = "aj_mas/personas"
    create_directory(personas_dir)

    # __init__.py
    init_content = """
from .persona import AgentPersona, SkillArea, LanguageProficiency
from .persona_loader import load_personas
"""
    write_file(os.path.join(personas_dir, "__init__.py"), init_content.strip())

    # persona.py
    persona_content = """
from enum import Enum
from typing import Dict, List

class SkillArea(Enum):
    TRAVEL = "Travel"
    ENTERTAINMENT = "Entertainment"
    SPORTS = "Sports"
    EDUCATION = "Education"
    BUSINESS = "Business"
    TECHNOLOGY = "Technology"
    HEALTH = "Health"
    FINANCE = "Finance"
    ARTS = "Arts"
    SCIENCE = "Science"
    LAW = "Law"
    MATHEMATICS = "Mathematics"

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
"""
    write_file(os.path.join(personas_dir, "persona.py"), persona_content.strip())

    # persona_loader.py
    persona_loader_content = """
import json
from typing import Dict
from .persona import AgentPersona

def load_personas(config_path: str) -> Dict[str, AgentPersona]:
    with open(config_path, 'r') as f:
        config_data = json.load(f)
    
    personas = {}
    for agent_type, persona_data in config_data.items():
        personas[agent_type] = AgentPersona.from_dict(persona_data)
    
    return personas

def save_personas(personas: Dict[str, AgentPersona], config_path: str):
    config_data = {agent_type: persona.to_dict() for agent_type, persona in personas.items()}
    with open(config_path, 'w') as f:
        json.dump(config_data, f, indent=2)

# Example usage:
# personas = load_personas("path/to/agent_config.json")
# travel_agent_persona = personas["travel_agent"]
# 
# # Modify persona if needed
# travel_agent_persona.add_personality_trait("Adventurous")
# 
# # Save updated personas
# save_personas(personas, "path/to/agent_config.json")
"""
    write_file(os.path.join(personas_dir, "persona_loader.py"), persona_loader_content.strip())

if __name__ == "__main__":
    create_personas_files()
    print("AJ_MAS personas files created successfully!")
