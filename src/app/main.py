import streamlit as st
import requests
import os
import uuid
from datetime import datetime

API_HOST = os.getenv("API_HOST", "localhost")

if "CONVERSATION_ID" not in st.session_state:
    st.session_state["CONVERSATION_ID"] = str(uuid.uuid4())

st.set_page_config(page_title="🤖 Reprebot")

with st.sidebar:
    st.markdown(
        """<div align="center">
        <h3>Welcome to 🤖 <b>Reprebot</b>!</h3>
        A chatbot to answer questions for the Faculty of Engineering community at the
        National University of Colombia.
        <br>
        <a href="https://github.com/Represoft/reprebot">Source code</a>
        """,
        unsafe_allow_html=True,
    )


st.title("🤖 Reprebot")


if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "¿Cómo puedo ayudarte?"},
    ]


for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Send query to chatbot api
    response = requests.get(
        f"http://{API_HOST}:8000/query", params={"q": prompt}, timeout=12000
    )
    if response.status_code == 200:
        result = response.json()
        msg = result["response"]
    else:
        msg = "Oops! Ha ocurrido un error :("

    # Render chatbot response
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

    # Render used sources
    sources = result["sources"]
    for i, source in enumerate(sources):
        with st.expander(f"Fuente {i+1}"):
            st.write(source["page_content"])
            st.write(f"FUENTE: {source['source']}")

    # Log conversation record
    payload = {
        "question": prompt,
        "answer": msg,
        "timestamp": datetime.now().isoformat(),
        "conversation_id": st.session_state["CONVERSATION_ID"],
    }

    requests.post(
        f"http://{API_HOST}:8000/conversation",
        json=payload,
        timeout=12000,
    )
