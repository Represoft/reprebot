import streamlit as st
import requests


st.title("🤖 Reprebot")


if "messages" not in st.session_state:
    st.session_state["messages"] = [{
        "role": "assistant",
        "content": "¿Cómo puedo ayudarte?"},
    ]


for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    response = requests.get("http://localhost:8000/query", params={"q": prompt})
    if response.status_code == 200:
        msg = response.json()
    else:
        msg = "Oops! Ha ocurrido un error :("

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
