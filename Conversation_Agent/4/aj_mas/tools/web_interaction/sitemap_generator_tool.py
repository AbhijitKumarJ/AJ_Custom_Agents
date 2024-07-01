from ..base_tool import BaseTool
from utils.logger import logger
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

class SitemapGeneratorTool(BaseTool):
    def __init__(self):
        super().__init__("Sitemap Generator", "Generate a sitemap for a given website")

    def execute(self, base_url: str, max_depth: int = 3):
        logger.log(f"Executing Sitemap Generator Tool")
        try:
            visited = set()
            sitemap = []

            def crawl(url, depth):
                if depth > max_depth or url in visited:
                    return
                visited.add(url)
                
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    sitemap.append(url)
                    
                    for link in soup.find_all('a'):
                        href = link.get('href')
                        if href and not href.startswith('#'):
                            full_url = urljoin(url, href)
                            if urlparse(full_url).netloc == urlparse(base_url).netloc:
                                crawl(full_url, depth + 1)
                except Exception as e:
                    logger.log(f"Error crawling {url}: {str(e)}")

            crawl(base_url, 1)
            return sitemap
        except Exception as e:
            return f"Error generating sitemap: {str(e)}"