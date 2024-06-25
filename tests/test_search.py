
from pymysearch.search import SearchClient


def test_search():
    client = SearchClient('duckduckgo')
    response = client.search('langchain', max_results=5)
    results = response.results
    urls = [res.url for res in results]

    assert len(urls) == 5
    assert urls[0] == 'https://www.langchain.com/'
