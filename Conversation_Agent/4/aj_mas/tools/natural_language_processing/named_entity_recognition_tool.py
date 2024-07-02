from ..base_tool import BaseTool
from aj_mas.utils import logger
import spacy

class NamedEntityRecognitionTool(BaseTool):
    def __init__(self):
        super().__init__("Named Entity Recognition", "Identify and classify named entities in text")
        self.nlp = spacy.load("en_core_web_sm")

    def execute(self, text: str):
        logger.log(f"Executing Named Entity Recognition Tool")
        try:
            doc = self.nlp(text)
            entities = [(ent.text, ent.label_) for ent in doc.ents]
            return entities
        except Exception as e:
            return f"Error in named entity recognition: {str(e)}"