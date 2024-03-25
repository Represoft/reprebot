from fastapi import FastAPI
import sys
sys.path.append('../..')
from src.llm_client import query as _query
from src.llm_client.types import GPTModelConfig


app = FastAPI()

model_config = GPTModelConfig(
    model_name="gpt-3.5-turbo-0125",
)

@app.get("/{query}")
async def query(query):
    response = _query(
        user_input=query,
        model_config=model_config
    )
    return response