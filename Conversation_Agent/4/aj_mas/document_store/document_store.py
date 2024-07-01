from abc import ABC, abstractmethod
from typing import List, Tuple

class DocumentStore(ABC):
    @abstractmethod
    def add_document(self, filename: str, content: str):
        pass

    @abstractmethod
    def retrieve_relevant_content(self, query: str, top_k: int = 3) -> List[Tuple[str, str]]:
        pass