import sys

sys.path.append("..")
from src.llm_client import query
from src.llm_client.types import GPTModelConfig
from src.vector_store.types import VectorStoreConfig

model_config = GPTModelConfig(
    model_name="gpt-3.5-turbo-0125",
)

vector_store_config = VectorStoreConfig(
    embeddings="OPENAI",
    retriever="FULL",
)

response = query(
    user_input="""
        ¿Hasta qué fecha se puede solicitar cancelación
        de asignaturas sin pérdida de créditos?
    """,
    model_config=model_config,
    vector_store_config=vector_store_config,
)

print(response, "\n")

response = query(
    user_input="""
        ¿Cómo se accede al beneficio de descuento electoral del 10 % aplicable
        sobre el valor de la matrícula?
    """,
    model_config=model_config,
    vector_store_config=vector_store_config,
)

print(response, "\n")


response = query(
    user_input="""
        ¿Cuándo puedo cancelar materias? Tienes enlaces relacionados con este proceso?
    """,
    model_config=model_config,
    vector_store_config=vector_store_config,
)

print(response, "\n")


response = query(
    user_input="""
        ¿Cuál es la diferencia entre práctica y pasantía?
    """,
    model_config=model_config,
    vector_store_config=vector_store_config,
)

print(response, "\n")
