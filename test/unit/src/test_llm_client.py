import pytest
from src.llm_client import LLMClient
from langchain_contrib.llms.testing import FakeLLM

class TestFakeLLM:
    @pytest.fixture
    def llm_client(self):
        return LLMClient(model_type="fake")

    def test_init(self, llm_client):
        assert llm_client.model_type == "fake"

    def test_setup_model(self, llm_client):
        model = llm_client.setup_model()
        assert isinstance(model, FakeLLM)
