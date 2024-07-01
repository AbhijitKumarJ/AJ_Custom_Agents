from ..base_tool import BaseTool
from utils.logger import logger
from bs4 import BeautifulSoup

class HTMLParserTool(BaseTool):
    def __init__(self):
        super().__init__("HTML Parser", "Parse and extract information from HTML content")

    def execute(self, html_content: str, parser: str = 'html.parser'):
        logger.log(f"Executing HTML Parser Tool")
        try:
            soup = BeautifulSoup(html_content, parser)
            
            # Extract basic information
            title = soup.title.string if soup.title else "No title found"
            headings = [h.text for h in soup.find_all(['h1', 'h2', 'h3'])]
            paragraphs = [p.text for p in soup.find_all('p')]
            links = [{'text': a.text, 'href': a.get('href')} for a in soup.find_all('a')]
            
            return {
                'title': title,
                'headings': headings,
                'paragraphs': paragraphs,
                'links': links
            }
        except Exception as e:
            return f"Error parsing HTML: {str(e)}"