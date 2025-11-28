import os
import asyncio
import json
import nest_asyncio
import streamlit as st
from components import title
from scripts import session_agent
from utilities import streamed_response as sr

# Apply the asyncio patch: This allows the event loop to be reused across Streamlit reruns.
nest_asyncio.apply()

# -- Setup --
LOGO_PATH = os.path.join(os.getcwd(), "assets/icon.png")
HISTORY_PATH = os.path.join(os.getcwd(), "sessions/history.json")

st.set_page_config(
    page_title="KaggleN",
    page_icon=LOGO_PATH
)

# -- History --
def load_chat_history():
    if os.path.exists(HISTORY_PATH):
        try:
            with open(HISTORY_PATH, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_chat_history(messages):
    with open(HISTORY_PATH, "w") as f:
        json.dump(messages, f)


# -- Title --
with st.sidebar:
    title.get_title_with_icon("KaggleN", LOGO_PATH)
    st.badge("Partner of your Kaggle journey.", icon=":material/star:", color="violet")

    if st.button("Clear Chat History", type="primary"):
        st.session_state.messages = []
        save_chat_history([])
        st.rerun()

title.get_title_with_icon("Chat", LOGO_PATH)

# -- AI Agent --
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    save_chat_history(st.session_state.messages)

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            # Run the agent.
            response_obj = session_agent.run_chat_agent(prompt, session_name="test")

            # Handle response (String vs Generator).
            if hasattr(response_obj, "__iter__") and not isinstance(response_obj, str):
                for chunk in response_obj:
                    full_response += chunk
                    if full_response.count("```") % 2 == 0:
                        message_placeholder.markdown(full_response + "▌")  # Add cursor
                    else:
                        message_placeholder.markdown(full_response)
                message_placeholder = st.write_stream(sr.response_generator(full_response))
            else:
                full_response = str(response_obj)
                message_placeholder = st.write_stream(sr.response_generator(full_response))

        except Exception as e:
            st.error(f"Error: {e}")
            full_response = "I encountered an error processing your request."

    st.session_state.messages.append({"role": "assistant", "content": full_response})

    save_chat_history(st.session_state.messages)

if __name__ == "__main__":
    pass