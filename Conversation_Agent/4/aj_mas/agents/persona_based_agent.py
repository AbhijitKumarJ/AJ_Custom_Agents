from .base_agent import BaseAgent
from ..utils import logger, handle_error
from ..personas import SkillArea
import os

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
        return "\n".join([f"{doc[0]}: {doc[1]}" for doc in relevant_docs])

    def _execute_skill(self, skill_area, task, task_analysis, context):
        # Implement logic to select and execute the most appropriate skill
        # This is a placeholder implementation
        return f"Executed skill for {skill_area.value} with task: {task}"

    def _adjust_response_for_persona(self, skill_result, proficiency):
        prompt = f"""
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
        """
        return self.model_provider.generate(prompt)