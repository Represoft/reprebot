from pathlib import Path
import os

PROJECT_ROOT = str(Path(__file__).parent.parent.parent)


CONTEXT_DATA_PATHS = {
    "faculty_secretary_faq": os.path.join(
        PROJECT_ROOT, "data/faculty_secretary_faq/"
    )
}


VECTOR_DATABASE_PATH = os.path.join(PROJECT_ROOT, "vectordb/")
