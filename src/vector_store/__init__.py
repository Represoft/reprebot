from typing import List
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_community.vectorstores import Chroma
import os
from langchain_community.embeddings import FakeEmbeddings
from langchain_openai import OpenAIEmbeddings
import shutil
from langchain_core.vectorstores import VectorStoreRetriever
import sys
from src.vector_store.types import VectorStoreConfig
sys.path.append('../..')
from src.constants import VECTOR_DATABASE_PATH
from src.constants import CONTEXT_DATA_PATHS


def load_documents_from_file(filepath: str) -> List[Document]:
    loader = TextLoader(filepath, encoding="utf8")
    documents = loader.load()
    # one file could generate multiple documents
    return documents


def load_documents_from_folders() -> List[Document]:
    documents = []
    metadata = []
    for group, path in CONTEXT_DATA_PATHS.items():
        for filename in os.listdir(path):
            filepath = os.path.join(path, filename)
            documents.extend(load_documents_from_file(filepath))
            metadata.append({
                "filename": filename,
                "group": group,
            })
    # set metadata to documents
    for document, _metadata in zip(documents, metadata):
        document.metadata = _metadata
    return documents


def chunk_documents(documents: List[Document]) -> List[Document]: # pragma: no cover
    # we won't be using chunking anymore because it would conflict with CRUD idea
    text_splitter = RecursiveCharacterTextSplitter()
    chunked_documents = text_splitter.split_documents(documents)
    if len(chunked_documents) == 0:
        chunked_documents = [Document(page_content="")]
    return chunked_documents


def start_vector_database(documents, embedding_function) -> Chroma:
    vector_db = Chroma(
        embedding_function=embedding_function,
        persist_directory=VECTOR_DATABASE_PATH,
    )
    ids = vector_db.add_documents(documents)
    # ids will be stored in a database to later implement a CRUD for vectors
    vector_db.persist()
    return vector_db


def load_vector_database(embedding_function) -> Chroma:
    vector_db = Chroma(
        persist_directory=VECTOR_DATABASE_PATH,
        embedding_function=embedding_function,
    )
    return vector_db


def setup_vector_database(documents, embedding_function) -> Chroma:
    vector_db = load_vector_database(embedding_function) \
        if os.path.exists(VECTOR_DATABASE_PATH) \
        else start_vector_database(documents, embedding_function)
    return vector_db


def setup_empty_retriever(embedding_function) -> VectorStoreRetriever:
    vector_db = Chroma.from_documents(
        documents=[Document(page_content="")],
        embedding=embedding_function,
    )
    retriever = vector_db.as_retriever(search_kwargs={"k": 1})
    return retriever


def setup_full_retriever(embedding_function) -> VectorStoreRetriever:
    # load documents
    documents = load_documents_from_folders()
    # chunk documents
    # chunked_documents = chunk_documents(documents)
    # set up vector db
    vector_db = setup_vector_database(documents, embedding_function)
    # generate retriever
    retriever = vector_db.as_retriever()
    return retriever


def setup_embeddings(config: VectorStoreConfig):
    if config.embeddings == "FAKE":
        return FakeEmbeddings(size=1)
    if config.embeddings == "OPENAI":
        return OpenAIEmbeddings()


def setup_retriever(config: VectorStoreConfig) -> VectorStoreRetriever:
    embedding_function = setup_embeddings(config)
    if config.retriever == "EMPTY":
        return setup_empty_retriever(embedding_function)
    if config.retriever == "FULL":
        return setup_full_retriever(embedding_function)


# to be accessed from admin CRUD view at some point
def reset_vector_database() -> None:
    if os.path.exists(VECTOR_DATABASE_PATH):
        shutil.rmtree(VECTOR_DATABASE_PATH)
