import os
from langchain_openai import ChatOpenAI

class LLMClient:
    def __init__(self, model_type: str):
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        self.huggingfacehub_api_token = os.environ.get("HUGGINGFACEHUB_API_TOKEN")
        self.model_type = model_type
        self.model = self.setup_model()

    def setup_model(self, temperature=0):
        model = None
        if self.model_type == "gpt":
            model = ChatOpenAI(
                api_key=self.openai_api_key,
                model_name="gpt-3.5-turbo-0125",
                temperature=temperature
            )
        """
        elif self.model_type == "hugging-face":
            llm = HuggingFaceEndpoint(
                repo_id="google/gemma-7b",
            )
            model = ChatHuggingFace(llm=llm)
        """
        # https://github.com/langchain-ai/langchain/issues/18639
        return model
