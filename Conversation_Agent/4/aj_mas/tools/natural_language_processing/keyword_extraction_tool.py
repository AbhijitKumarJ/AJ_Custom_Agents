from ..base_tool import BaseTool
from aj_mas.utils import logger
import yake

class KeywordExtractionTool(BaseTool):
    def __init__(self):
        super().__init__("Keyword Extraction", "Extract key phrases from text")
        self.kw_extractor = yake.KeywordExtractor()

    def execute(self, text: str, top_n: int = 5):
        logger.log(f"Executing Keyword Extraction Tool")
        try:
            keywords = self.kw_extractor.extract_keywords(text)
            return [kw for kw, _ in sorted(keywords, key=lambda x: x[1])[:top_n]]
        except Exception as e:
            return f"Error in keyword extraction: {str(e)}"