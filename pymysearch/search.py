from enum import Enum
from typing import Optional

from pymysearch.search_service import BaseSearchService, DuckDuckGoSearchService


class SearchBackendType(Enum):
    DUCKDUCKGO = "duckduckgo"


class SearchClient:
    def __init__(
        self,
        search_backend: SearchBackendType = SearchBackendType.DUCKDUCKGO,
        search_service: Optional[BaseSearchService] = None,
    ):
        self.search_backend = search_backend
        self.search_service = (
            search_service
            if search_service
            else self.init_search_service(search_backend)
        )

    def init_search_service(self, search_backend):
        if search_backend == SearchBackendType.DUCKDUCKGO:
            return DuckDuckGoSearchService()
        else:
            raise ValueError("Search Backend is not valid.")

    def search(self, query, **kwargs):
        return self.search_service.search(query=query, **kwargs)

    def qna_search(self, query, **kwargs):
        raise NotImplementedError
