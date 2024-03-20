from src.llm_client import setup_model, setup_chain, query
from langchain.prompts import ChatPromptTemplate
from langchain.docstore.document import Document
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import FakeEmbeddings
from langchain_core.runnables.base import RunnableSequence
from langchain.chat_models.fake import FakeListChatModel
from langchain_community.chat_models.huggingface import ChatHuggingFace

def test_setup_model_fake():
    model = setup_model("fake")
    assert isinstance(model, FakeListChatModel)

def test_setup_model_hugging_face():
    model = setup_model("hugging-face")
    assert isinstance(model, ChatHuggingFace)

def test_setup_chain_fake():
    retriever = Chroma.from_documents(
        documents=[Document(page_content="")],
        embedding=FakeEmbeddings(size=1),
    ).as_retriever(search_kwargs={"k": 1})
    prompt = ChatPromptTemplate.from_messages([""])
    model = setup_model("fake")
    chain = setup_chain(retriever=retriever, prompt=prompt, model=model)
    assert isinstance(chain, RunnableSequence)

def test_setup_chain_hugging_face():
    retriever = Chroma.from_documents(
        documents=[Document(page_content="")],
        embedding=FakeEmbeddings(size=1),
    ).as_retriever(search_kwargs={"k": 1})
    prompt = ChatPromptTemplate.from_messages([""])
    model = setup_model("hugging-face")
    chain = setup_chain(retriever=retriever, prompt=prompt, model=model)
    assert isinstance(chain, RunnableSequence)

def test_query_fake():
    response = query(user_input="", model_type="fake")
    assert isinstance(response, str)
    assert response == "Hello"

def test_query_hugging_face():
    response = query(user_input="", model_type="hugging-face")
    assert isinstance(response, str)
