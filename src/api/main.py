from fastapi import FastAPI
import sys
sys.path.append('../..')
from src.llm_client import query as _query
from src.llm_client.types import GPTModelConfig
from src.vector_store.types import VectorStoreConfig

app = FastAPI()

model_config = GPTModelConfig(
    model_name="gpt-3.5-turbo-0125",
)

vector_store_config = VectorStoreConfig(
    embeddings="OPENAI",
    retriever="FULL",
)

@app.get("/{query}")
async def query(query):
    response = _query(
        user_input=query,
        model_config=model_config,
        vector_store_config=vector_store_config
    )
    print(response)
    return response