from ..base_tool import BaseTool
from aj_mas.utils import logger

class SummarizationTool(BaseTool):
    def __init__(self, model_provider):
        super().__init__("Summarization", "Summarize a given text")
        self.model_provider = model_provider

    def execute(self, text: str, max_length: int = 100):
        logger.log(f"Executing Summarization Tool")
        prompt = f"Summarize the following text in {max_length} words: {text}"
        summary = self.model_provider.generate(prompt)
        return summary