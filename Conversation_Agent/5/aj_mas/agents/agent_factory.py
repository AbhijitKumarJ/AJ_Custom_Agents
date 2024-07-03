from ..utils import logger
from ..personas import load_personas
from .specialized_agents import TravelAgent, FinancialAdvisor, MedicalDoctor, LegalAdvisor, SoftwareEngineer

def create_agent(agent_type, skills, model_provider, document_store, config_path):
    personas = load_personas(config_path)
    persona = personas.get(agent_type)
    
    if not persona:
        logger.error(f"No persona found for agent type: {agent_type}")
        return None
    
    agent_classes = {
        "travel_agent": TravelAgent,
        "financial_advisor": FinancialAdvisor,
        "health_advisor": MedicalDoctor,
        "legal_advisor": LegalAdvisor,
        "software_engineer": SoftwareEngineer
    }
    
    agent_class = agent_classes.get(agent_type)
    if not agent_class:
        logger.error(f"No agent class found for agent type: {agent_type}")
        return None
    
    return agent_class(persona.name, skills, model_provider, document_store, persona)

def get_available_agent_types():
    return ["travel_agent", "financial_advisor", "health_advisor", "legal_advisor", "software_engineer"]