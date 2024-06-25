from typing import List
from langchain_core.callbacks import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_core.vectorstores import VectorStore

from pymysearch import logger
from pymysearch.search_service import DuckDuckGoSearchService


class PyMySearchRetriever(BaseRetriever):
    text_splitter: object
    vectorstore: VectorStore
    max_results: int = 5

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        """Sync implementations for retriever."""
        search_service = DuckDuckGoSearchService()
        response = search_service.search(query, max_results=self.max_results)
        results = response.results

        docs = []

        for document in results:
            logger.info(f"Checking document with url: {document.url}")
            # check if document url is already in the vectorstore
            if self.vectorstore.get(where={'source': document.url}).get('ids'):
                logger.info("Already in vectorstore. Skipping.")
                continue
            doc = Document(page_content=document.content,
                           metadata={"source": document.url})
            docs.append(doc)

        all_splits = self.text_splitter.split_documents(docs)
        if all_splits:
            self.vectorstore.add_documents(all_splits)
        return self.vectorstore.as_retriever()._get_relevant_documents(query, run_manager=run_manager)
