from abc import ABC, abstractmethod
from ..utils.logger import logger
from ..utils.task_analyzer import TaskAnalyzer
from ..utils.memory_system import memory_system
from ..utils.document_store import document_store
from transformers import pipeline


class BaseAgent(ABC):
    def __init__(self, name, skills):
        self.name = name
        self.skills = {skill.name: skill for skill in skills}
        self.classifier = pipeline(
            "zero-shot-classification", model="facebook/bart-large-mnli"
        )
        self.task_analyzer = TaskAnalyzer()
        self.memory = memory_system
        self.document_store = document_store
        logger.log(
            f"Initialized {self.__class__.__name__}",
            {"name": name, "skills": list(self.skills.keys())},
        )

    @abstractmethod
    def perform_task(self, task, **kwargs):
        pass

    def analyze_task(self, task):
        logger.log(f"Analyzing task", {"agent": self.name, "task": task})
        skill_names = list(self.skills.keys())
        result = self.classifier(task, skill_names, multi_label=True)
        analysis = list(zip(result["labels"], result["scores"]))
        logger.log(f"Task analysis result", {"analysis": analysis})
        return analysis

    def add_to_memory(self, entry):
        self.memory.add_to_current_session(entry)

    def get_current_session(self):
        return self.memory.get_current_session()

    def get_user_history(self, user_id, n_sessions=None):
        if n_sessions:
            return self.memory.get_last_n_sessions(user_id, n_sessions)
        return self.memory.get_user_sessions(user_id)

    def retrieve_relevant_documents(self, query):
        return self.document_store.retrieve_relevant_content(query)
