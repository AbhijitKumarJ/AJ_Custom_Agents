from ..base_tool import BaseTool
from utils.logger import logger

class TranslationTool(BaseTool):
    def __init__(self, model_provider):
        super().__init__("Translation", "Translate text from one language to another")
        self.model_provider = model_provider

    def execute(self, text: str, source_language: str, target_language: str):
        logger.log(f"Executing Translation Tool")
        prompt = f"Translate the following {source_language} text to {target_language}: {text}"
        translated_text = self.model_provider.generate(prompt)
        return translated_text