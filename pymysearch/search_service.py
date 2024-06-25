from duckduckgo_search import DDGS

from pymysearch import logger
from pymysearch.models import Result, Response
from pymysearch.utils import clean_text, html_to_markdown, parse_url


class BaseSearchService:
    def __init__(self):
        pass

    def search(self, query: str, max_results=5, **kwargs):
        pass


class DuckDuckGoSearchService(BaseSearchService):
    def __init__(self, *args, **kwargs):
        self.engine = DDGS(*args, **kwargs)

    def search(self, query, max_results=5, **kwargs):
        raw_results = self.engine.text(query, max_results=max_results, **kwargs)
        results = []
        for res in raw_results:
            logger.info(f"Found result: {res['href']}")
            url = res['href']
            html = parse_url(url)
            content = html_to_markdown(html)
            content = clean_text(content)
            results.append(Result(url=url, content=content, raw_content=html))
        return Response(results=results)
