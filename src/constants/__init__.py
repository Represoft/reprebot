from pathlib import Path
import os

PROJECT_ROOT = str(Path(__file__).parent.parent)

CONTEXT_DATA_GROUPS = [
    "faculty_secretary_faq",
    "faculty_secretary_students_requests",
]

CONTEXT_DATA_PATHS = {
    "faculty_secretary_faq": os.path.join(PROJECT_ROOT, "data/faculty_secretary_faq/"),
    "faculty_secretary_students_requests": os.path.join(PROJECT_ROOT, "data/faculty_secretary_students_requests/"),
}

CONTEXT_DATA_SOURCES = {
    "faculty_secretary_faq": "https://ingenieria.bogota.unal.edu.co/es/dependencias/secretaria-academica/preguntas-frecuentes.html",
    "faculty_secretary_students_requests": "https://ingenieria.bogota.unal.edu.co/es/dependencias/secretaria-academica/solicitudes-estudiantiles.html",
}

VECTOR_DATABASE_PATH = os.path.join(PROJECT_ROOT, "vectordb/")
DATABASE_PATH = os.path.join(PROJECT_ROOT, "reprebot.db")
CONTEXT_DATA_PATH = os.path.join(PROJECT_ROOT, "data/")