from dataclasses import dataclass
from typing import List


@dataclass
class Result:
    url: str
    content: str


@dataclass
class Response:
    results: List[Result]
