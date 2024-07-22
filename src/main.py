"""
This is a demo script to test the `OPENAI_API_KEY` with four demo questions.
"""

import sys

sys.path.append("..")
from src.llm_client import query
from src.llm_client.types import GPTModelConfig
from src.vector_store.types import VectorStoreConfig

model_config = GPTModelConfig(
    model_name="gpt-4o-mini",
)

vector_store_config = VectorStoreConfig(
    embeddings="OPENAI",
    retriever="FULL",
)

question_1 = """
    ¿Hasta qué fecha se puede solicitar cancelación
    de asignaturas sin pérdida de créditos?
"""

response_1 = query(
    user_input=question_1,
    model_config=model_config,
    vector_store_config=vector_store_config,
)

print("QUESTION 1:", question_1, "\n")
print("RESPONSE 1:", response_1, "\n\n")

question_2 = """
    ¿Cómo se accede al beneficio de descuento electoral del 10 % aplicable
    sobre el valor de la matrícula?
"""

response_2 = query(
    user_input=question_2,
    model_config=model_config,
    vector_store_config=vector_store_config,
)

print("QUESTION 2:", question_2, "\n")
print("RESPONSE 2:", response_2, "\n\n")

question_3 = """
    ¿Cuándo puedo cancelar materias? Tienes enlaces relacionados con este proceso?
"""

response_3 = query(
    user_input=question_3,
    model_config=model_config,
    vector_store_config=vector_store_config,
)

print("QUESTION 3:", question_3, "\n")
print("RESPONSE 3:", response_3, "\n\n")

question_4 = """
    ¿Cuál es la diferencia entre práctica y pasantía?
"""

response_4 = query(
    user_input=question_4,
    model_config=model_config,
    vector_store_config=vector_store_config,
)

print("QUESTION 4:", question_4, "\n")
print("RESPONSE 4:", response_4, "\n\n")
