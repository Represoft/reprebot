

from enum import Enum
from typing import NamedTuple


class RetrieverEnum(Enum):
    EMPTY = 'EMPTY'
    FULL = 'FULL'


class EmbeddingsEnum(Enum):
    FAKE = 'FAKE'
    OPENAI = 'OPENAI'


class VectorStoreConfig(NamedTuple):
    retriever: RetrieverEnum
    embeddings: EmbeddingsEnum