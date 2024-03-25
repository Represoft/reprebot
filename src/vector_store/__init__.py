from typing import List
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain_community.vectorstores import Chroma
import os
from langchain_community.embeddings import FakeEmbeddings
import shutil
from langchain_core.vectorstores import VectorStoreRetriever

def load_documents(path: str) -> List[Document]:
    loader = TextLoader()
    documents = loader.load(path)
    return documents


def chunk_documents(documents: List[Document]) -> List[Document]:
    splitter = CharacterTextSplitter()
    chunked_documents = [splitter.split(doc) for doc in documents]
    return chunked_documents


def setup_vector_database(path: str) -> Chroma:
    if not os.path.exists(path):
        documents = load_documents(path)
        chunked_documents = chunk_documents(documents)
        vector_db = Chroma.from_documents(chunked_documents, FakeEmbeddings())
        vector_db.persist(path)
    else:
        vector_db = Chroma(persist_directory=path, embeddings=FakeEmbeddings())
    return vector_db


def reset_vector_database(path: str) -> None:
    if os.path.exists(path):
        shutil.rmtree(path)


def setup_retriever(vector_db: Chroma) -> VectorStoreRetriever:
    retriever = vector_db.as_retriever()
    return retriever