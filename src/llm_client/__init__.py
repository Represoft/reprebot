import os
from langchain_openai import ChatOpenAI
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.docstore.document import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import FakeEmbeddings
from langchain.chat_models.fake import FakeListChatModel
from langchain_community.chat_models.huggingface import ChatHuggingFace
from langchain_community.llms.huggingface_endpoint import HuggingFaceEndpoint
from .types import (
    GPTModelConfig,
    FakeModelConfig,
    HuggingFaceModelConfig,
)

def setup_gpt_model(model_config: GPTModelConfig): # pragma: no cover
    model = ChatOpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        model_name=model_config.model_name,
        temperature=model_config.temperature
    )
    return model

def setup_fake_model(model_config: FakeModelConfig):
    model = FakeListChatModel(responses=model_config.responses)
    return model

def setup_hugging_face_model(model_config: HuggingFaceModelConfig):
    llm = HuggingFaceEndpoint(
        repo_id=model_config.repo_id,
        huggingfacehub_api_token=os.environ.get("HUGGINGFACEHUB_API_TOKEN"),
        temperature=model_config.temperature,
    )
    model = ChatHuggingFace(llm=llm)
    return model

def setup_model(
        model_config: GPTModelConfig | FakeModelConfig | HuggingFaceModelConfig
    ):
    model = None
    if model_config.model_type == "gpt": # pragma: no cover
        model = setup_gpt_model(model_config=model_config)
    elif model_config.model_type == "fake":
        model = setup_fake_model(model_config=model_config)
    elif model_config.model_type == "hugging-face":
        model = setup_hugging_face_model(model_config=model_config)
    return model

def setup_chain(retriever, prompt, model):
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

def setup_prompt(messages):
    prompt = ChatPromptTemplate.from_messages(messages)
    return prompt

def setup_retriever():
    # Empty retriever for testing
    retriever = Chroma.from_documents(
        documents=[Document(page_content="")],
        embedding=FakeEmbeddings(size=1),
    ).as_retriever(search_kwargs={"k": 1})
    return retriever

def query(
        user_input: str,
        model_config: GPTModelConfig | FakeModelConfig | HuggingFaceModelConfig
    ):
    retriever = setup_retriever()
    prompt = setup_prompt(messages=[""])
    model = setup_model(model_config=model_config)
    chain = setup_chain(retriever=retriever, prompt=prompt, model=model)
    response = chain.invoke(user_input)
    return response
