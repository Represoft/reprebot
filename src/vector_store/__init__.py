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
from src.vector_store.types import DocumentResponse, VectorStoreConfig
sys.path.append('../..')
from src.constants import VECTOR_DATABASE_PATH
from src.constants import DATABASE_PATH
from src.constants import CONTEXT_DATA_PATHS
from src.constants import CONTEXT_DATA_GROUPS
from src.constants import CONTEXT_DATA_PATH
from src.database import Database
from cryptography.hazmat.primitives import hashes


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
                "group_id": CONTEXT_DATA_GROUPS.index(group),
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


def _push_metadata(ids, metadata):
    database = Database(db_name=DATABASE_PATH)
    database.push(ids, metadata)


def start_vector_database(documents, embedding_function) -> Chroma:
    vector_db = Chroma(
        embedding_function=embedding_function,
        persist_directory=VECTOR_DATABASE_PATH,
    )
    ids = vector_db.add_documents(documents)
    metadata = [document.metadata for document in documents]
    _push_metadata(ids, metadata)
    vector_db.persist()
    return vector_db


def load_vector_database(embedding_function = None) -> Chroma:
    if embedding_function is None:
        vector_db = Chroma(
            persist_directory=VECTOR_DATABASE_PATH,
        )
    else:
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


def get_document_by_filename(filename: str) -> DocumentResponse:
    database = Database(db_name=DATABASE_PATH)
    _id = database.get_id_by_filename(filename)
    vector_db = load_vector_database()
    document = vector_db.get(_id)
    response = DocumentResponse(
        document_id=document["ids"][0],
        filename=document["metadatas"][0]["filename"],
        group_id=document["metadatas"][0]["group_id"],
        page_content=document["documents"][0],
    )
    return response


def get_document_by_id(document_id: str) -> DocumentResponse:
    vector_db = load_vector_database()
    document = vector_db.get(document_id)
    response = DocumentResponse(
        document_id=document["ids"][0],
        filename=document["metadatas"][0]["filename"],
        group_id=document["metadatas"][0]["group_id"],
        page_content=document["documents"][0],
    )
    return response


def delete_document(document_id: str) -> bool:
    vector_db = load_vector_database()
    # remove vector
    vector_db.delete([document_id])
    database = Database(db_name=DATABASE_PATH)
    # remove file
    filename = database.get_filename_by_id(document_id)
    group_id = database.get_group_id_by_id(document_id)
    group = CONTEXT_DATA_GROUPS[group_id]
    filepath = os.path.join(CONTEXT_DATA_PATH, group, filename)
    os.remove(filepath)
    # remove db record
    database.delete(document_id)
    return True


def _write_file(text: str, folder: str) -> str:
    digest = hashes.Hash(hashes.SHA256())
    digest.update(text.encode())
    file_name = digest.finalize().hex()
    with open(f"{folder}/{file_name}.txt", "w", encoding="utf-8") as file:
        file.write(text)
    return f"{file_name}.txt"


def update_document(document_id: str, document: Document, config: VectorStoreConfig) -> str:
    embedding_function = setup_embeddings(config)
    vector_db = load_vector_database(embedding_function=embedding_function)
    old_document = vector_db.get(document_id)
    document.metadata = old_document["metadatas"][0]
    vector_db.update_document(document_id, document)
    database = Database(db_name=DATABASE_PATH)
    # remove old file
    old_filename = database.get_filename_by_id(document_id)
    group_id = database.get_group_id_by_id(document_id)
    group = CONTEXT_DATA_GROUPS[group_id]
    folder = os.path.join(CONTEXT_DATA_PATH, group)
    old_filepath = os.path.join(folder, old_filename)
    os.remove(old_filepath)
    # create new file
    text = document.page_content
    filename = _write_file(text, folder)
    # update database record filename
    database.update_filename(document_id, filename)
    return filename


def add_document(document: Document, group_id: int, config: VectorStoreConfig) -> str:
    embedding_function = setup_embeddings(config)
    vector_db = load_vector_database(embedding_function=embedding_function)
    # generate file
    group = CONTEXT_DATA_GROUPS[group_id]
    folder = os.path.join(CONTEXT_DATA_PATH, group)
    text = document.page_content
    filename = _write_file(text, folder)
    metadata = {
        "filename": filename,
        "group_id": group_id,
    }
    document.metadata = metadata
    # insert vector
    ids = vector_db.add_documents([document])
    # create db record
    database = Database(db_name=DATABASE_PATH)
    database.push(ids, [metadata])
    document_id = ids[0]
    return document_id
