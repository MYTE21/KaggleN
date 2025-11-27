import os
import streamlit as st
from components import title, chat
import asyncio


# -- Setup --
LOGO_PATH = os.path.join(os.getcwd(), "assets/icon.png")

st.set_page_config(
    page_title="KaggleN",
    page_icon=LOGO_PATH
)

# -- Title --
with st.sidebar:
    title.get_title_with_icon("KaggleN", LOGO_PATH)
    st.badge("Partner of your Kaggle journey.", icon=":material/star:", color="violet")

title.get_title_with_icon("Chat", LOGO_PATH)


# -- AI Agent --
# Initialize chat history.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input.
if prompt := st.chat_input("Ask me anything..."):

    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        # response = st.write_stream(chat.random_response())
        response = st.write(asyncio.run(chat.gemini_agent(prompt)))

    st.session_state.messages.append({"role": "assistant", "content": response})