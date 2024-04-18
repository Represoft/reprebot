from langchain.docstore.document import Document
import os
import shutil
import sys
from src.vector_store.types import DocumentResponse, VectorStoreConfig
sys.path.append('../../..')
from src.constants import VECTOR_DATABASE_PATH
from src.constants import DATABASE_PATH
from src.constants import CONTEXT_DATA_GROUPS
from src.constants import CONTEXT_DATA_PATH
from src.database import Database
from cryptography.hazmat.primitives import hashes
from src.vector_store import (
    load_vector_database,
    setup_embeddings,
)


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