import os
import pytest
from src.llm_client import LLMClient
from langchain.prompts import ChatPromptTemplate
from langchain.docstore.document import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import FakeEmbeddings
from langchain_core.runnables.base import RunnableSequence

class TestLLMClient:
    @pytest.fixture
    def llm_client(self):
        return LLMClient(model_type="gpt")

    def test_init(self, llm_client):
        assert llm_client.openai_api_key == os.environ.get("OPENAI_API_KEY")
        assert llm_client.model_type == "gpt"

    def test_setup_model(self, llm_client):
        temperature = 0.5
        model = llm_client.setup_model(temperature=temperature)
        assert model.temperature == temperature

    def test_setup_chain(self, llm_client):
        # Empty retriever for testing
        retriever = Chroma.from_documents(
            documents=[Document(page_content="")],
            embedding=FakeEmbeddings(size=1),
        ).as_retriever(search_kwargs={"k": 1})
        # Empty prompt for testing
        prompt = ChatPromptTemplate.from_messages([])
        # Default "gpt" model use in this test
        model = llm_client.setup_model()
        # RAG chain
        chain = llm_client.setup_chain(retriever=retriever, prompt=prompt, model=model)
        assert isinstance(chain, RunnableSequence)
