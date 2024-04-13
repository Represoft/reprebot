from fastapi import FastAPI, Query
import sys
sys.path.append('../..')
from src.llm_client import query as _query
from src.llm_client.types import GPTModelConfig
from src.vector_store.types import VectorStoreConfig
from src.vector_store import get_document_by_filename as _get_document_by_filename
from src.vector_store import get_document_by_id as _get_document_by_id


app = FastAPI()


model_config = GPTModelConfig(
    model_name="gpt-3.5-turbo-0125",
)


vector_store_config = VectorStoreConfig(
    embeddings="OPENAI",
    retriever="FULL",
)


@app.get("/query")
async def query(q: str = Query(None)):
    if q:
        response = _query(
            user_input=q,
            model_config=model_config,
            vector_store_config=vector_store_config
        )
    else:
        response = {
            "error": "'query' parameter must be provided."
        }
    return response


@app.get("/document")
async def document(filename: str = Query(None), document_id: str = Query(None)):
    if filename:
        response = _get_document_by_filename(filename)
    elif document_id:
        response = _get_document_by_id(document_id)
    else:
        response = {
            "error": "Either 'filename' or 'document_id' query parameter must be provided."
        }
    return response
