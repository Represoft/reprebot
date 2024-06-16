import sys

sys.path.append("../..")
from src.vector_store.types import VectorStoreConfig
from src.vector_store import (
    setup_embeddings,
    load_documents_from_folders,
    setup_vector_database,
)

config = VectorStoreConfig(
    embeddings="OPENAI",
    retriever=None, # not needed
)

embedding_function = setup_embeddings(config)
documents = load_documents_from_folders()
setup_vector_database(documents, embedding_function)
