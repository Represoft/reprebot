import os
from langchain_openai import ChatOpenAI

class LLMClient:
    def __init__(self, model_name="gpt-3.5-turbo-0125"):
        self.api_key = os.environ["OPENAI_API_KEY"]
        self.model_name = model_name
        self.model = self.setup_model()

    def setup_model(self, temperature=0):
        model = ChatOpenAI(
            api_key=self.api_key,
            model_name=self.model_name,
            temperature=temperature
        )
        return model
