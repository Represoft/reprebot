from datetime import datetime
from src.database import Database
from src.constants import DATABASE_PATH


def log_conversation(
    question: str, answer: str, timestamp: datetime, conversation_id: str
) -> bool:

    database = Database(db_name=DATABASE_PATH)
    result = database.push_conversation_log_record(
        question=question,
        answer=answer,
        timestamp=timestamp,
        conversation_id=conversation_id,
    )

    return result
