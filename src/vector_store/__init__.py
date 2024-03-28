from typing import List
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain_community.vectorstores import Chroma
import os
from langchain_community.embeddings import FakeEmbeddings
from langchain_openai import OpenAIEmbeddings
import shutil
from langchain_core.vectorstores import VectorStoreRetriever
import sys
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
    for path in CONTEXT_DATA_PATHS.values():
        for filename in os.listdir(path):
            filepath = os.path.join(path, filename)
            documents.extend(load_documents_from_file(filepath))
    return documents


def chunk_documents(documents: List[Document]) -> List[Document]:
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunked_documents = text_splitter.split_documents(documents)
    if len(chunked_documents) == 0:
        chunked_documents = [Document(page_content="")]
    return chunked_documents


def start_vector_database(chunked_documents, embedding_function) -> Chroma:
    vector_db = Chroma.from_documents(
        documents=chunked_documents,
        embedding=embedding_function,
        persist_directory=VECTOR_DATABASE_PATH,
    )
    vector_db.persist(VECTOR_DATABASE_PATH)
    return vector_db


def load_vector_database(embedding_function) -> Chroma:
    vector_db = Chroma(
        persist_directory=VECTOR_DATABASE_PATH,
        embedding_function=embedding_function,
    )
    return vector_db


def setup_vector_database(chunked_documents, embedding_function) -> Chroma:
    vector_db = load_vector_database(embedding_function) \
        if os.path.exists(VECTOR_DATABASE_PATH) \
        else start_vector_database(chunked_documents, embedding_function)
    return vector_db


def setup_empty_retriever() -> VectorStoreRetriever:
    retriever = Chroma.from_documents(
        documents=[Document(page_content="")],
        embedding=FakeEmbeddings(size=1),
    ).as_retriever(search_kwargs={"k": 1})
    return retriever


def setup_retriever(config = None) -> VectorStoreRetriever:
    # load documents
    documents = load_documents_from_folders()
    # chunk documents
    chunked_documents = chunk_documents(documents)
    # set up vector db
    embedding_function = OpenAIEmbeddings()
    vector_db = setup_vector_database(chunked_documents, embedding_function)
    # generate retriever
    retriever = vector_db.as_retriever()
    return retriever, vector_db


# to be accessed from admin CRUD view at some point
def reset_vector_database() -> None:
    if os.path.exists(VECTOR_DATABASE_PATH):
        shutil.rmtree(VECTOR_DATABASE_PATH)
