import os
import pytest
from src.llm_client import LLMClient
from langchain.prompts import ChatPromptTemplate
from langchain.docstore.document import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import FakeEmbeddings
from langchain_core.runnables.base import RunnableSequence
from langchain.chat_models.fake import FakeListChatModel


class TestFakeLLMClient:
    @pytest.fixture
    def llm_client(self):
        return LLMClient(model_type="fake")

    def test_init(self, llm_client):
        assert llm_client.model_type == "fake"

    def test_setup_model(self, llm_client):
        model = llm_client.setup_model()
        assert isinstance(model, FakeListChatModel)

    def test_setup_chain(self, llm_client):
        # Empty retriever for testing
        retriever = Chroma.from_documents(
            documents=[Document(page_content="")],
            embedding=FakeEmbeddings(size=1),
        ).as_retriever(search_kwargs={"k": 1})
        # Empty prompt for testing
        prompt = ChatPromptTemplate.from_messages([""])
        # Default "fake" model use in this test
        model = llm_client.setup_model()
        # RAG chain
        chain = llm_client.setup_chain(retriever=retriever, prompt=prompt, model=model)
        assert isinstance(chain, RunnableSequence)

    def test_query(self, llm_client):
        response = llm_client.query(user_input="")
        assert isinstance(response, str)
        assert response == "Hello"