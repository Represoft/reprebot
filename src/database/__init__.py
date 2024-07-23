import sqlite3
from datetime import datetime
from typing import List, Tuple

class Database:
    def __init__(self, db_name: str) -> None:
        self.connector = None
        self.cursor = None
        self.db_name = db_name
        self._connect()
        self._create_tables()

    def _connect(self) -> None:
        self.connector = sqlite3.connect(self.db_name)
        self.cursor = self.connector.cursor()

    def _create_documents_table(self) -> None:
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS documents(
                id TEXT,
                filename TEXT,
                group_id INTEGER
            )
            """
        )
        self.connector.commit()

    def _create_conversations_table(self) -> None:
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                conversation_id TEXT NOT NULL
            )
            """
        )
        self.connector.commit()

    def _create_tables(self) -> None:
        self._create_documents_table()
        self._create_conversations_table()

    def _insert_documents(self, data: list[tuple[str, str, int]]) -> None:
        self.cursor.executemany("INSERT INTO documents VALUES (?, ?, ?)", data)
        self.connector.commit()

    def delete_document(self, document_id: str) -> None:
        self.cursor.execute(
            "DELETE FROM documents WHERE id = ?", (document_id,)
        )
        self.connector.commit()

    def update_filename(self, document_id: str, filename: str) -> None:
        self.cursor.execute(
            "UPDATE documents SET filename = ? WHERE id = ?",
            (
                filename,
                document_id,
            ),
        )
        self.connector.commit()

    def get_id_by_filename(self, filename: str) -> str:
        self.cursor.execute(
            "SELECT id FROM documents WHERE filename = ?", (filename,)
        )
        result = self.cursor.fetchone()
        _id = result[0]
        return _id

    def get_filename_by_id(self, document_id: str) -> str:
        self.cursor.execute(
            "SELECT filename FROM documents WHERE id = ?", (document_id,)
        )
        result = self.cursor.fetchone()
        filename = result[0]
        return filename

    def get_group_id_by_id(self, document_id: str) -> str:
        self.cursor.execute(
            "SELECT group_id FROM documents WHERE id = ?", (document_id,)
        )
        result = self.cursor.fetchone()
        group_id = result[0]
        return group_id

    def push_documents(self, ids, metadata) -> None:
        data = [
            (_id, _metadata["filename"], _metadata["group_id"])
            for _id, _metadata in zip(ids, metadata)
        ]
        self._insert_documents(data)

    def push_conversation_log_record(
        self,
        question: str,
        answer: str,
        timestamp: datetime,
        conversation_id: str,
    ) -> bool:
        try:
            query = """
            INSERT INTO conversations (question, answer, timestamp, conversation_id)
            VALUES (?, ?, ?, ?)
            """
            self.cursor.execute(query, (question, answer, timestamp.isoformat(), conversation_id))
            self.connector.commit()
            return True
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            self.connector.rollback()
            raise

    def get_conversations_log(self) -> List[Tuple[int, str, str, datetime, str]]:
        try:
            query = "SELECT id, question, answer, timestamp, conversation_id FROM conversations"
            self.cursor.execute(query)

            # Fetch all records
            records = self.cursor.fetchall()

            # Convert timestamp strings back to datetime objects
            converted_records = []
            for record in records:
                _id, question, answer, timestamp_str, conversation_id = record
                timestamp = datetime.fromisoformat(timestamp_str)
                converted_records.append((_id, question, answer, timestamp, conversation_id))

            return converted_records
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            raise

    def _delete_documents_table(self) -> None:
        self.cursor.execute("DROP TABLE IF EXISTS documents")
        self.connector.commit()

    def _delete_conversations_table(self) -> None:
        self.cursor.execute("DROP TABLE IF EXISTS conversations")
        self.connector.commit()

    def reset_documents(self) -> None:
        self._delete_documents_table()
        self._create_documents_table()

    def reset_conversations(self) -> None:
        self._delete_conversations_table()
        self._create_conversations_table()

    def reset(self) -> None:
        self.delete_tables()
        self.create_tables()

    def close(self) -> None:
        self.connector.close()
