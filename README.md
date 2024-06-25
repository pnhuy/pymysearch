# PyMySearch

My low-key LLM-friendly wrapper for search engines.

## Installation
```bash
pip install git+https://github.com/pnhuy/pymysearch
```

## Usage

## Search

```python
from pymysearch.search import SearchClient
client = SearchClient('duckduckgo')
response = client.search('langchain', max_results=5)
results = response.results
for res in results:
    print(res.url)
    print(res.content[:10])
```

## Q&A with Search

Give a quick answer based on search results:

```python
# pip install langchain-text-splitters langchain-chroma langchain-openai langchain-huggingface

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pymysearch.search import SearchClient

client = SearchClient(
    llm=llm,
    text_splitter=RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=500),
    vectorstore=Chroma(
        persist_directory="./chroma_db",
        embedding_function=HuggingFaceEmbeddings(),
    ),
)

print(client.qna_search("What is the capital of Vietnam?"))
# => The capital of Vietnam is Hanoi.
```

You might want to custom the prompt to change the output:

```python
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template("""You are an assistant for question-answering tasks.
Use the following pieces of retrieved context to answer the question.
If you don't know the answer, just say that you don't know.
Make the answer informative and detailed.

Question: {question}

Context:
{context}

Answer:""")
print(client.qna_search("What is the capital of Vietnam?", prompt=prompt))
# => The capital of Vietnam is Hanoi. Hanoi is the second-largest city in Vietnam by population...
```