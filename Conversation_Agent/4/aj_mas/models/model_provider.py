from abc import ABC, abstractmethod

class ModelProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, max_length: int = 100, temperature: float = 0.7) -> str:
        pass

    @abstractmethod
    def analyze_task(self, task: str, user_id: str) -> dict:
        pass