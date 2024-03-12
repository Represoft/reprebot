import os
import pytest
from src.llm_client import LLMClient

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