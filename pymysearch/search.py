from enum import Enum
from typing import Optional

from langchain_core.prompts import PromptTemplate
from langchain_core.language_models.chat_models import BaseLanguageModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import VectorStore

from pymysearch import logger
from pymysearch.retrievers import PyMySearchRetriever
from pymysearch.search_service import BaseSearchService, DuckDuckGoSearchService
from pymysearch.utils import format_docs


class SearchBackendType(Enum):
    DUCKDUCKGO = "duckduckgo"


class SearchClient:
    def __init__(
        self,
        search_service_name: Optional[str] = "duckduckgo",
        search_service: Optional[BaseSearchService] = None,
        llm: Optional[BaseLanguageModel] = None,
        text_splitter: Optional[object] = None,
        vectorstore: Optional[VectorStore] = None,
    ):
        self.search_service = search_service if search_service else self.init_search_service(search_service_name)
        self.llm = llm
        self.text_splitter = text_splitter
        self.vectorstore = vectorstore

    def init_search_service(self, search_backend):
        logger.info(f"Initializing search service with backend: {search_backend}")
        if search_backend == SearchBackendType.DUCKDUCKGO.value:
            return DuckDuckGoSearchService()
        else:
            raise ValueError("Search Backend is not valid.")

    def search(self, query, **kwargs):
        return self.search_service.search(query=query, **kwargs)

    def qna_search(self, query, prompt=None, max_results=5, **kwargs):
        assert self.llm is not None, "Language model is not provided."
        assert self.vectorstore is not None, "Vectorstore is not provided."
        assert self.text_splitter is not None, "Text splitter is not provided."

        retriever = PyMySearchRetriever(
            max_results=max_results, vectorstore=self.vectorstore, text_splitter=self.text_splitter
        )
        prompt = (
            prompt
            if prompt
            else PromptTemplate.from_template("""You are an assistant for question-answering tasks.
Use the following pieces of retrieved context to answer the question.
If you don't know the answer, just say that you don't know.
Keep the answer concise.

Question: {question}

Context:
{context}

Answer:""")
        )
        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
        answer = rag_chain.invoke(query, **kwargs)
        return answer
