
from typing import List, TypedDict


class GPTModelConfig: # pragma: no cover
    def __init__(self, model_name: str, temperature: float = 0.00):
        self.model_type: str = "gpt"
        self.model_name = model_name
        self.temperature = temperature

class FakeModelConfig:
    def __init__(self, responses: list[str]):
        self.model_type: str = "fake"
        self.responses = responses

class HuggingFaceModelConfig:
    def __init__(self, repo_id: str, temperature: float = 0.01):
        self.model_type: str = "hugging-face"
        self.repo_id = repo_id
        self.temperature = temperature


class Source(TypedDict):
    page_content: str
    source: str


class QueryResponse(TypedDict):
    response: str
    sources: List[Source]
