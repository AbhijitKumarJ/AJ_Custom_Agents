import os

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def write_file(path, content):
    with open(path, 'w') as f:
        f.write(content)
    print(f"Created file: {path}")

def create_agents_files():
    agents_dir = "aj_mas/agents"
    create_directory(agents_dir)

    # __init__.py
    init_content = """
from .base_agent import BaseAgent
from .persona_based_agent import PersonaBasedAgent
from .specialized_agents import TravelAgent, FinancialAdvisor, MedicalDoctor, LegalAdvisor, SoftwareEngineer
from .agent_factory import create_agent
"""
    write_file(os.path.join(agents_dir, "__init__.py"), init_content.strip())

    # base_agent.py
    base_agent_content = """
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, name, skills, model_provider, document_store):
        self.name = name
        self.skills = skills
        self.model_provider = model_provider
        self.document_store = document_store

    @abstractmethod
    def perform_task(self, task):
        pass

    @abstractmethod
    def start_session(self, user_id):
        pass

    @abstractmethod
    def end_session(self):
        pass

    @abstractmethod
    def add_document(self, file_path):
        pass
"""
    write_file(os.path.join(agents_dir, "base_agent.py"), base_agent_content.strip())

    # persona_based_agent.py
    persona_based_agent_content = """
from .base_agent import BaseAgent
from aj_mas.utils import logger, handle_error
from aj_mas.personas import SkillArea

class PersonaBasedAgent(BaseAgent):
    def __init__(self, name, skills, model_provider, document_store, persona):
        super().__init__(name, skills, model_provider, document_store)
        self.persona = persona
        self.current_user_id = None

    @handle_error
    def perform_task(self, task):
        logger.log(f"Agent {self.name} performing task: {task}")
        task_analysis = self.model_provider.analyze_task(task, self.current_user_id)
        skill_area = self._determine_skill_area(task_analysis)
        
        proficiency = self.persona.skill_proficiencies.get(skill_area, 0)
        if proficiency < 0.3:
            return self._generate_low_proficiency_response(skill_area, task)
        
        relevant_docs = self.document_store.retrieve_relevant_content(task)
        context = self._prepare_context(relevant_docs)
        
        skill_result = self._execute_skill(skill_area, task, task_analysis, context)
        adjusted_response = self._adjust_response_for_persona(skill_result, proficiency)
        
        return adjusted_response

    def start_session(self, user_id):
        self.current_user_id = user_id
        logger.log(f"Agent {self.name} started session for user: {user_id}")

    def end_session(self):
        logger.log(f"Agent {self.name} ended session for user: {self.current_user_id}")
        self.current_user_id = None

    def add_document(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            filename = os.path.basename(file_path)
            self.document_store.add_document(filename, content)
            return f"Document added: {filename}"
        except Exception as e:
            logger.error(f"Error adding document: {str(e)}")
            return f"Error adding document: {str(e)}"

    def _determine_skill_area(self, task_analysis):
        # Implement logic to determine the most relevant skill area based on task analysis
        # This is a placeholder implementation
        return SkillArea.GENERAL

    def _generate_low_proficiency_response(self, skill_area, task):
        prompt = f"Generate a response for an agent with low proficiency in {skill_area.value} when asked about the task: {task}. The agent should politely express limited knowledge and suggest seeking information from a more qualified source."
        return self.model_provider.generate(prompt)

    def _prepare_context(self, relevant_docs):
        return "\\n".join([f"{doc[0]}: {doc[1]}" for doc in relevant_docs])

    def _execute_skill(self, skill_area, task, task_analysis, context):
        # Implement logic to select and execute the most appropriate skill
        # This is a placeholder implementation
        return f"Executed skill for {skill_area.value} with task: {task}"

    def _adjust_response_for_persona(self, skill_result, proficiency):
        prompt = f""""""
        Adjust the following skill execution result:
        '{skill_result}'
        
        Consider these persona characteristics:
        - Name: {self.persona.name}
        - Gender: {self.persona.gender}
        - Ethnicity: {self.persona.ethnicity}
        - Religious inclination: {self.persona.religious_inclination}
        - Personality traits: {', '.join(self.persona.personality_traits)}
        - Communication style: {self.persona.communication_style}
        - Proficiency level: {proficiency}

        Rewrite the response to reflect these characteristics and the proficiency level.
        """"""
        return self.model_provider.generate(prompt)
"""
    write_file(os.path.join(agents_dir, "persona_based_agent.py"), persona_based_agent_content.strip())

    # specialized_agents.py
    specialized_agents_content = """
from .persona_based_agent import PersonaBasedAgent
from aj_mas.personas import SkillArea

class TravelAgent(PersonaBasedAgent):
    def __init__(self, name, skills, model_provider, document_store, persona):
        super().__init__(name, skills, model_provider, document_store, persona)
    
    def _determine_skill_area(self, task_analysis):
        # Implement travel-specific skill area determination
        return SkillArea.TRAVEL

class FinancialAdvisor(PersonaBasedAgent):
    def __init__(self, name, skills, model_provider, document_store, persona):
        super().__init__(name, skills, model_provider, document_store, persona)
    
    def _determine_skill_area(self, task_analysis):
        # Implement finance-specific skill area determination
        return SkillArea.FINANCE

class MedicalDoctor(PersonaBasedAgent):
    def __init__(self, name, skills, model_provider, document_store, persona):
        super().__init__(name, skills, model_provider, document_store, persona)
    
    def _determine_skill_area(self, task_analysis):
        # Implement medical-specific skill area determination
        return SkillArea.HEALTH

class LegalAdvisor(PersonaBasedAgent):
    def __init__(self, name, skills, model_provider, document_store, persona):
        super().__init__(name, skills, model_provider, document_store, persona)
    
    def _determine_skill_area(self, task_analysis):
        # Implement legal-specific skill area determination
        return SkillArea.LAW

class SoftwareEngineer(PersonaBasedAgent):
    def __init__(self, name, skills, model_provider, document_store, persona):
        super().__init__(name, skills, model_provider, document_store, persona)
    
    def _determine_skill_area(self, task_analysis):
        # Implement software engineering-specific skill area determination
        return SkillArea.TECHNOLOGY
"""
    write_file(os.path.join(agents_dir, "specialized_agents.py"), specialized_agents_content.strip())

    # agent_factory.py
    agent_factory_content = """
from aj_mas.utils import logger
from aj_mas.personas import load_personas
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
        "medical_doctor": MedicalDoctor,
        "legal_advisor": LegalAdvisor,
        "software_engineer": SoftwareEngineer
    }
    
    agent_class = agent_classes.get(agent_type)
    if not agent_class:
        logger.error(f"No agent class found for agent type: {agent_type}")
        return None
    
    return agent_class(persona.name, skills, model_provider, document_store, persona)

def get_available_agent_types():
    return ["travel_agent", "financial_advisor", "medical_doctor", "legal_advisor", "software_engineer"]
"""
    write_file(os.path.join(agents_dir, "agent_factory.py"), agent_factory_content.strip())

if __name__ == "__main__":
    create_agents_files()
    print("AJ_MAS agents files created successfully!")
