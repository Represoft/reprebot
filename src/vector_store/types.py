from enum import Enum
from typing import NamedTuple, TypedDict


class RetrieverEnum(Enum):
    EMPTY = "EMPTY"
    FULL = "FULL"


class EmbeddingsEnum(Enum):
    FAKE = "FAKE"
    OPENAI = "OPENAI"


class VectorStoreConfig(NamedTuple):
    retriever: RetrieverEnum
    embeddings: EmbeddingsEnum


class DocumentResponse(TypedDict):
    document_id: str
    filename: str
    group_id: int
    page_content: str
