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