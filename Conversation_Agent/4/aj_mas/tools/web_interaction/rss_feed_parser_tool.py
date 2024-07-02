from ..base_tool import BaseTool
from aj_mas.utils import logger
import feedparser

class RSSFeedParserTool(BaseTool):
    def __init__(self):
        super().__init__("RSS Feed Parser", "Parse RSS feeds and extract information")

    def execute(self, feed_url: str):
        logger.log(f"Executing RSS Feed Parser Tool")
        try:
            feed = feedparser.parse(feed_url)
            
            parsed_entries = []
            for entry in feed.entries:
                parsed_entries.append({
                    'title': entry.get('title', 'No title'),
                    'link': entry.get('link', 'No link'),
                    'published': entry.get('published', 'No publish date'),
                    'summary': entry.get('summary', 'No summary')
                })
            
            return {
                'feed_title': feed.feed.get('title', 'No feed title'),
                'feed_link': feed.feed.get('link', 'No feed link'),
                'feed_description': feed.feed.get('description', 'No feed description'),
                'entries': parsed_entries
            }
        except Exception as e:
            return f"Error parsing RSS feed: {str(e)}"