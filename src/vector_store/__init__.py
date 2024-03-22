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
    # use TextLoader
    # return documents
    pass


def chunk_documents(documents: List[Document]) -> List[Document]:
    # use CharacterTextSplitter
    # return chunked_documents
    pass


def setup_vector_database(path: str) -> Chroma:
    # if not os.path.exists(path):
        # load documents
        # chunk documents
        # use Chroma.from_documents to generate vector db
        # persist db with .persist() method
    # else:
        # use Chroma(persist_directory=path, ...)
    # use FakeEmbeddings when instantiating the vector db
    # return vector_db
    pass


def reset_vector_database(path: str) -> None:
    # if os.path.exists(path):
        # shutil.rmtree(path)
    pass


def setup_retriever(vector_db: Chroma) -> VectorStoreRetriever:
    # use as_retriever() method
    # return retriever
    pass
