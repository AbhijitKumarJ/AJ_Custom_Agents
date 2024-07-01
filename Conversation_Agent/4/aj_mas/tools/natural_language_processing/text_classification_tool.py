from ..base_tool import BaseTool
from utils.logger import logger
from transformers import pipeline

class TextClassificationTool(BaseTool):
    def __init__(self):
        super().__init__("Text Classification", "Classify text into predefined categories")
        self.classifier = pipeline("text-classification")

    def execute(self, text: str):
        logger.log(f"Executing Text Classification Tool")
        try:
            result = self.classifier(text)
            return result[0]
        except Exception as e:
            return f"Error in text classification: {str(e)}"