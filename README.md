# PyMySearch

My low-key LLM-friendly wrapper for search engines.

## Installation
```bash
pip install git+https://github.com/pnhuy/pymysearch
```

## Usage

```python
from pymysearch.search import SearchClient
client = SearchClient('duckduckgo')
response = client.search('langchain', max_results=5)
results = response.results
for res in results:
    print(res.url)
    print(res.content[:10])
```
