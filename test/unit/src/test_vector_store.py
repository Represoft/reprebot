import pytest
import os
import tempfile

from langchain.docstore.document import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import FakeEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import VectorStoreRetriever

from src.constants import (
    CONTEXT_DATA_PATHS,
    CONTEXT_DATA_GROUPS,
)
from src.vector_store.types import VectorStoreConfig
from src.vector_store import (
    load_documents_from_file,
    load_documents_from_folders,
    chunk_documents,
    start_vector_database,
    load_vector_database,
    setup_vector_database,
    setup_empty_retriever,
    setup_full_retriever,
    setup_embeddings,
    setup_retriever,
)


@pytest.fixture
def sample_text_file(tmp_path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("This is a sample text file.")
    return str(file_path)


def test_load_documents_from_file(sample_text_file):
    documents = load_documents_from_file(sample_text_file)
    assert len(documents) == 1
    assert isinstance(documents[0], Document)
    assert documents[0].page_content == "This is a sample text file."


@pytest.fixture
def setup_test_directories(tmp_path):
    # Create a temporary directory structure
    for group in CONTEXT_DATA_GROUPS:
        group_dir = tmp_path / group
        group_dir.mkdir()
        # Create some test files
        (group_dir / f"{group}_file1.txt").write_text(f"Content for {group} file 1")
        (group_dir / f"{group}_file2.txt").write_text(f"Content for {group} file 2")

    # Temporarily modify CONTEXT_DATA_PATHS to use our test directories
    original_paths = CONTEXT_DATA_PATHS.copy()
    for group in CONTEXT_DATA_GROUPS:
        CONTEXT_DATA_PATHS[group] = str(tmp_path / group)

    yield

    # Restore original paths after the test
    CONTEXT_DATA_PATHS.clear()
    CONTEXT_DATA_PATHS.update(original_paths)


def test_load_documents_from_folders(setup_test_directories):
    documents = load_documents_from_folders()

    # Check if we have the correct number of documents
    expected_doc_count = len(CONTEXT_DATA_GROUPS) * 2  # 2 files per group
    assert len(documents) == expected_doc_count

    # Check if all documents are of type Document
    assert all(isinstance(doc, Document) for doc in documents)

    # Check if metadata is correctly set for each document
    for doc in documents:
        assert "filename" in doc.metadata
        assert "group_id" in doc.metadata
        assert doc.metadata["group_id"] in range(len(CONTEXT_DATA_GROUPS))

        # Check if the content matches the expected content
        group = CONTEXT_DATA_GROUPS[doc.metadata["group_id"]]
        expected_content = f"Content for {group} file "
        assert doc.page_content.startswith(expected_content)

    # Check if we have documents from all groups
    group_ids = set(doc.metadata["group_id"] for doc in documents)
    assert group_ids == set(range(len(CONTEXT_DATA_GROUPS)))


@pytest.fixture
def temp_db_path():
    db_file = tempfile.NamedTemporaryFile(delete=False)
    yield db_file.name
    db_file.close()
    os.remove(db_file.name)


@pytest.fixture
def temp_vector_db_path():
    vector_db_dir = tempfile.TemporaryDirectory()
    yield vector_db_dir.name
    vector_db_dir.cleanup()


def test_chunk_documents():
    documents = [Document(page_content="This is a test document.")]
    chunked_documents = chunk_documents(documents)
    assert len(chunked_documents) > 0


def test_start_vector_database(temp_db_path, temp_vector_db_path):
    documents = [
        Document(
            page_content="This is a test document.",
            metadata={
                "filename": "test_doc",
                "group_id": 1,
            },
        )
    ]
    embedding_function = FakeEmbeddings(size=1536)
    vector_db = start_vector_database(documents, embedding_function)

    assert isinstance(vector_db, Chroma)
    assert os.path.exists(temp_vector_db_path)


def test_load_vector_database(temp_vector_db_path):
    vector_db = load_vector_database()
    assert isinstance(vector_db, Chroma)


def test_setup_vector_database(temp_db_path, temp_vector_db_path):
    documents = [Document(page_content="This is a test document.")]
    embedding_function = FakeEmbeddings(size=1)
    vector_db = setup_vector_database(documents, embedding_function)
    assert isinstance(vector_db, Chroma)


def test_setup_empty_retriever(temp_db_path, temp_vector_db_path):
    embedding_function = FakeEmbeddings(size=1)
    retriever = setup_empty_retriever(embedding_function)
    assert isinstance(retriever, VectorStoreRetriever)


def test_setup_full_retriever(
    temp_db_path, temp_vector_db_path, setup_test_directories
):
    embedding_function = FakeEmbeddings(size=1)
    retriever = setup_full_retriever(embedding_function)
    assert isinstance(retriever, VectorStoreRetriever)


def test_setup_embeddings():
    config_fake = VectorStoreConfig(embeddings="FAKE", retriever="EMPTY")
    embeddings = setup_embeddings(config_fake)
    assert isinstance(embeddings, FakeEmbeddings)

    config_openai = VectorStoreConfig(embeddings="OPENAI", retriever="EMPTY")
    embeddings = setup_embeddings(config_openai)
    assert isinstance(embeddings, OpenAIEmbeddings)


def test_setup_retriever(temp_db_path, temp_vector_db_path, setup_test_directories):
    config_empty = VectorStoreConfig(embeddings="FAKE", retriever="EMPTY")
    retriever_empty = setup_retriever(config_empty)
    assert isinstance(retriever_empty, VectorStoreRetriever)

    config_full = VectorStoreConfig(embeddings="FAKE", retriever="FULL")
    retriever_full = setup_retriever(config_full)
    assert isinstance(retriever_full, VectorStoreRetriever)
