import pytest
import tempfile
from datetime import datetime
from src.database import Database


@pytest.fixture
def db():
    db_file = tempfile.NamedTemporaryFile(delete=False)
    db = Database(db_file.name)
    yield db
    db.close()


def test_create_tables(db):
    db.cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='documents'"
    )
    assert db.cursor.fetchone() is not None

    db.cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='conversations'"
    )
    assert db.cursor.fetchone() is not None


def test_insert_and_get_document(db):
    doc_id = "doc1"
    filename = "file1.txt"
    group_id = 1
    db.push_documents([doc_id], [{"filename": filename, "group_id": group_id}])

    assert db.get_id_by_filename(filename) == doc_id
    assert db.get_filename_by_id(doc_id) == filename
    assert db.get_group_id_by_id(doc_id) == group_id


def test_update_document(db):
    doc_id = "doc1"
    filename = "file1.txt"
    group_id = 1
    db.push_documents([doc_id], [{"filename": filename, "group_id": group_id}])

    new_filename = "file2.txt"
    db.update_filename(doc_id, new_filename)

    assert db.get_filename_by_id(doc_id) == new_filename


def test_delete_document(db):
    doc_id = "doc1"
    filename = "file1.txt"
    group_id = 1
    db.push_documents([doc_id], [{"filename": filename, "group_id": group_id}])

    db.delete_document(doc_id)
    db.cursor.execute("SELECT * FROM documents WHERE id = ?", (doc_id,))
    assert db.cursor.fetchone() is None


def test_push_conversation_log_record(db):
    question = "What is the capital of France?"
    answer = "Paris"
    timestamp = datetime.now()
    conversation_id = "conv1"

    assert (
        db.push_conversation_log_record(question, answer, timestamp, conversation_id)
        is True
    )

    db.cursor.execute(
        "SELECT question, answer, timestamp, conversation_id FROM conversations WHERE conversation_id = ?",
        (conversation_id,),
    )
    result = db.cursor.fetchone()

    assert result is not None
    assert result[0] == question
    assert result[1] == answer
    assert datetime.fromisoformat(result[2]) == timestamp
    assert result[3] == conversation_id


def test_get_conversations_log(db):
    question = "What is the capital of France?"
    answer = "Paris"
    timestamp = datetime.now()
    conversation_id = "conv1"

    db.push_conversation_log_record(question, answer, timestamp, conversation_id)

    log = db.get_conversations_log()
    assert len(log) == 1
    log_entry = log[0]

    assert log_entry[1] == question
    assert log_entry[2] == answer
    assert log_entry[3] == timestamp
    assert log_entry[4] == conversation_id


def test_reset_documents(db):
    doc_id = "doc1"
    filename = "file1.txt"
    group_id = 1
    db.push_documents([doc_id], [{"filename": filename, "group_id": group_id}])

    db.reset_documents()
    db.cursor.execute("SELECT * FROM documents")
    assert db.cursor.fetchone() is None


def test_reset_conversations(db):
    question = "What is the capital of France?"
    answer = "Paris"
    timestamp = datetime.now()
    conversation_id = "conv1"

    db.push_conversation_log_record(question, answer, timestamp, conversation_id)

    db.reset_conversations()
    db.cursor.execute("SELECT * FROM conversations")
    assert db.cursor.fetchone() is None
