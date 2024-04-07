from pathlib import Path
import os

PROJECT_ROOT = str(Path(__file__).parent.parent.parent)


CONTEXT_DATA_GROUPS = [
    "faculty_secretary_faq",
]


CONTEXT_DATA_PATHS = {
    "faculty_secretary_faq": os.path.join(
        PROJECT_ROOT, "data/faculty_secretary_faq/"
    )
}


# might be useful for CRUD
CONTEXT_DATA_SOURCES = {
    "faculty_secretary_faq": "https://ingenieria.bogota.unal.edu.co/es/dependencias/secretaria-academica/preguntas-frecuentes.html"
}


VECTOR_DATABASE_PATH = os.path.join(PROJECT_ROOT, "vectordb/")
