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

def setup_model(model_type: str, temperature: float = 0):
    model = None
    if model_type == "gpt":
        model = ChatOpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
            model_name="gpt-3.5-turbo-0125",
            temperature=temperature
        )
    elif model_type == "fake":
        model = FakeListChatModel(responses=["Hello"])
    elif model_type == "hugging-face":
        llm = HuggingFaceEndpoint(
            repo_id="google/gemma-7b",
        )
        model = ChatHuggingFace(llm=llm)
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

def query(user_input: str, model_type: str):
    # Empty retriever for testing
    retriever = Chroma.from_documents(
        documents=[Document(page_content="")],
        embedding=FakeEmbeddings(size=1),
    ).as_retriever(search_kwargs={"k": 1})
    # Empty prompt for testing
    prompt = ChatPromptTemplate.from_messages([""])
    model = setup_model(model_type)
    chain = setup_chain(retriever=retriever, prompt=prompt, model=model)
    response = chain.invoke(user_input)
    return response