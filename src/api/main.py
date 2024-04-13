from fastapi import FastAPI, Query
import sys
sys.path.append('../..')
from src.llm_client import query
from src.llm_client.types import GPTModelConfig
from src.vector_store.types import VectorStoreConfig
from src.vector_store import get_document_by_filename
from src.vector_store import get_document_by_id
from src.vector_store import delete_document
from src.vector_store import update_document
from langchain.docstore.document import Document


app = FastAPI()


model_config = GPTModelConfig(
    model_name="gpt-3.5-turbo-0125",
)


vector_store_config = VectorStoreConfig(
    embeddings="OPENAI",
    retriever="FULL",
)


@app.get("/query")
async def query_get(q: str = Query(None)):
    if q:
        response = query(
            user_input=q,
            model_config=model_config,
            vector_store_config=vector_store_config
        )
    else:
        response = {
            "error": "'query' parameter must be provided.",
        }
    return response


@app.get("/document")
async def document_get(filename: str = Query(None), document_id: str = Query(None)):
    if filename:
        response = get_document_by_filename(filename)
    elif document_id:
        response = get_document_by_id(document_id)
    else:
        response = {
            "error": "Either 'filename' or 'document_id' parameter must be provided.",
        }
    return response


@app.delete("/document")
async def document_delete(document_id: str = Query(None)):
    if document_id:
        delete_document(document_id)
        response = {
            "success": document_id,
        }
    else:
        response = {
            "error": "'document_id' parameter must be provided.",
        }
    return response


@app.put("/document")
async def document_put(document_id: str = Query(None), page_content: str = Query(None)):
    if document_id and page_content:
        document = Document(page_content=page_content)
        update_document(document_id, document, vector_store_config)
        response = {
            "success": document_id,
        }
    else:
        response = {
            "error": "'document_id' and 'page_content' parameters must be provided.",
        }
    return response
