import pytest
import os
from src.llm_client import (
    query,
)
from src.llm_client.types import (
    GPTModelConfig,
    FakeModelConfig,
    HuggingFaceModelConfig,
)


@pytest.mark.skip(reason="can't use empty retriever yet")
@pytest.mark.parametrize(
    ("user_input", "responses"),
    [
        ("Hello", ["Hello"]),
        ("Hi", ["Bye"]),
        ("Thank you", ["Welcome", "Thanks"]),
    ],
)
def test_query_fake(user_input: str, responses: list[str]):
    model_config = FakeModelConfig(
        responses=responses,
    )
    response = query(user_input=user_input, model_config=model_config)
    assert isinstance(response, str)
    assert response in responses


@pytest.mark.skip(reason="can't use empty retriever yet")
@pytest.mark.skipif(
    os.environ.get("HUGGINGFACEHUB_API_TOKEN") is None,
    reason="HUGGINGFACEHUB_API_TOKEN is not available"
)
@pytest.mark.parametrize(
    ("user_input", "repo_id"),
    [
        ("Hello", "google/gemma-7b"),
    ],
)
def test_query_hugging_face(user_input: str, repo_id: str):
    model_config = HuggingFaceModelConfig(
        repo_id=repo_id,
    )
    response = query(user_input=user_input, model_config=model_config)
    assert isinstance(response, str)


# comment next line if you want to run this test
@pytest.mark.skip()
@pytest.mark.skipif(
    os.environ.get("OPENAI_API_KEY") is None,
    reason="OPENAI_API_KEY is not available"
)
@pytest.mark.parametrize(
    ("user_input", "_word_to_check"),
    [
        ("Say 'Hello'", "Hello"),
    ],
)
def test_query_gpt(user_input: str, _word_to_check: str):
    model_config = GPTModelConfig(
        model_name="gpt-3.5-turbo-0125",
    )
    response = query(user_input=user_input, model_config=model_config)
    assert isinstance(response, str)
    assert _word_to_check in response
