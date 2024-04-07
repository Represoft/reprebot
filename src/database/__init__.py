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


    def _insert(self, data: list[tuple[str, str, str]]) -> None:
        self.cursor.executemany(
            "INSERT INTO documents VALUES (?, ?, ?)",
            data
        )
        self.connector.commit()


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