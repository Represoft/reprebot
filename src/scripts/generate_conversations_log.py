import sys
import json
from datetime import datetime

sys.path.append("../..")
from src.database import Database
from src.constants import DATABASE_PATH


def generate_json_log(records, filename="conversations_log.json"):
    data = []
    for record in records:
        # Convert timestamp to string if it's a datetime object
        record = list(record)
        if isinstance(record[3], datetime):
            record[3] = record[3].isoformat()
        # Append the record as a dictionary
        data.append(
            {
                "ID": record[0],
                "Question": record[1],
                "Answer": record[2],
                "Timestamp": record[3],
                "Conversation ID": record[4],
            }
        )

    # Write data to JSON file
    with open(filename, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

    print(f"JSON log generated: {filename}")


database = Database(db_name=DATABASE_PATH)
records = database.get_conversations_log()
generate_json_log(records)

print(f"Total records: {len(records)}")
