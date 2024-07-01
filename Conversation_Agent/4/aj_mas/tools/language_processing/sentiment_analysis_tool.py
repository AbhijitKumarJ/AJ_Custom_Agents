from ..base_tool import BaseTool
from utils.logger import logger

class SentimentAnalysisTool(BaseTool):
    def __init__(self, model_provider):
        super().__init__("Sentiment Analysis", "Analyze the sentiment of a given text")
        self.model_provider = model_provider

    def execute(self, text: str):
        logger.log(f"Executing Sentiment Analysis Tool")
        prompt = f"Analyze the sentiment of the following text and respond with either 'positive', 'negative', or 'neutral': {text}"
        sentiment = self.model_provider.generate(prompt)
        return sentiment.strip().lower()