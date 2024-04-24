import sqlite3


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

    def _create_tables(self) -> None:
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

    def _insert(self, data: list[tuple[str, str, int]]) -> None:
        self.cursor.executemany("INSERT INTO documents VALUES (?, ?, ?)", data)
        self.connector.commit()

    def delete(self, document_id: str) -> None:
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

    def push(self, ids, metadata) -> None:
        data = [
            (_id, _metadata["filename"], _metadata["group_id"])
            for _id, _metadata in zip(ids, metadata)
        ]
        self._insert(data)

    def reset(self) -> None:
        self.cursor.execute("DROP TABLE IF EXISTS documents")
        self._create_tables()

    def close(self) -> None:
        self.connector.close()
