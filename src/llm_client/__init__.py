import os
from langchain_openai import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.docstore.document import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import FakeEmbeddings

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

    def setup_chain(self, retriever, prompt, model):
        chain = (
            {
                "input": RunnablePassthrough(),
                "context": retriever,
            }
            | prompt
            | model
            | StrOutputParser()
        )
        return chain

    def query(self, user_input: str):
        # Empty retriever for testing
        retriever = Chroma.from_documents(
            documents=[Document(page_content="")],
            embedding=FakeEmbeddings(size=1),
        ).as_retriever(search_kwargs={"k": 1})
        # Empty prompt for testing
        prompt = ChatPromptTemplate.from_messages([""])
        chain = self.setup_chain(
            retriever=retriever,
            prompt=prompt,
            model=self.model
        )
        response = chain.invoke(user_input)
        return response