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
    loader = TextLoader(path)
    documents = loader.load()
    return documents


def chunk_documents(documents: List[Document]) -> List[Document]:
    text_splitter = CharacterTextSplitter()
    chunked_documents = text_splitter.split_documents(documents)
    if len(chunked_documents) == 0:
        chunked_documents = [Document(page_content="")]
    return chunked_documents


def setup_vector_database(path: str) -> Chroma:
    vector_db = None
    vector_db_path = "vectordb/"
    if not os.path.exists(path):
        documents = load_documents(path)
        chunked_documents = chunk_documents(documents)
        vector_db = Chroma.from_documents(
            documents=chunked_documents,
            embedding=FakeEmbeddings(),
            persist_directory=vector_db_path,
        )
        vector_db.persist(vector_db_path)
    else:
        vector_db = Chroma(
            persist_directory=path,
            embedding_function=FakeEmbeddings(),
        )
    return vector_db


def reset_vector_database(path: str) -> None:
    if os.path.exists(path):
        shutil.rmtree(path)


def setup_retriever(vector_db: Chroma) -> VectorStoreRetriever:
    retriever = vector_db.as_retriever()
    return retriever