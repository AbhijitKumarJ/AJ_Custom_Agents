from ..base_tool import BaseTool
from utils.logger import logger
import requests
from bs4 import BeautifulSoup

class WebScraperTool(BaseTool):
    def __init__(self):
        super().__init__("Web Scraper", "Scrape content from web pages")

    def execute(self, url: str, selector: str):
        logger.log(f"Executing Web Scraper Tool")
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            elements = soup.select(selector)
            return [element.get_text().strip() for element in elements]
        except Exception as e:
            return f"Error scraping web page: {str(e)}"