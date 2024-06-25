import re
from markdownify import markdownify
import requests


def parse_url(url: str, **kwargs) -> str:
    response = requests.get(url, **kwargs)
    html = response.text
    return html


def html_to_markdown(html: str, strip=["a", "img"], convert=None) -> str:
    md = markdownify(
        html,
        strip=strip,
        convert=convert,
        heading_style="ATX"
    )
    return md


def clean_text(text: str) -> str:
    # Remove repeated spaces
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove non-ASCII characters
    text = re.sub(r"[^\x00-\x7F]+", "", text)

    return text


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)
