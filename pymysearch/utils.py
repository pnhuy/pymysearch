from markdownify import markdownify
import requests


def parse_url(url: str, **kwargs) -> str:
    response = requests.get(url, **kwargs)
    html = response.text
    return html


def html_to_markdown(html, strip=["a", "img"], convert=None):
    md = markdownify(html, strip=strip, convert=convert)
    return md
