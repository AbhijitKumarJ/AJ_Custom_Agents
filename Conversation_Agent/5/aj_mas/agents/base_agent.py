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