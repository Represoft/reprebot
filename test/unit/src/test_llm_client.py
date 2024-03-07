import os
import pytest
from src.llm_client import LLMClient

class TestLLMClient:
    @pytest.fixture
    def llm_client(self):
        return LLMClient()

    def test_init(self, llm_client):
        assert llm_client.api_key == os.environ["OPENAI_API_KEY"]
        assert llm_client.model_name == "gpt-3.5-turbo-0125"

    def test_setup_model(self, llm_client):
        temperature = 0.5
        model = llm_client.setup_model(temperature=temperature)
        assert model.temperature == temperature
