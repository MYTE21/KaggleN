import nest_asyncio
import streamlit as st

# Import modules.
from config import LOGO_PATH
from components import title
from components.sidebar import render_sidebar
from components.welcome import render_welcome_screen
from modules.display import handle_response_display
from modules.history import HistoryManager
from modules.runner import get_agent_response

# Apply the asyncio patch: This allows the event loop to be reused across Streamlit reruns.
nest_asyncio.apply()

# -- Setup --
st.set_page_config(
    page_title="KaggleN",
    page_icon=LOGO_PATH,
    layout="wide"
)

def main():
    # Render sidebar and get selection
    selected_agent = render_sidebar()

    # Title.
    # title.get_title_with_icon("Chat", LOGO_PATH)

    # Load history.
    if "messages" not in st.session_state:
        st.session_state.messages = HistoryManager.load()

    # Display chat.
    if len(st.session_state.messages) == 0:
        render_welcome_screen()
    else:
        title.get_title_with_icon("KaggleN", LOGO_PATH)
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Input loop.
    if prompt := st.chat_input("Ask me anything..."):
        # User step.
        st.session_state.messages.append({"role": "user", "content": prompt})
        HistoryManager.save(st.session_state.messages)
        with st.chat_message("user"):
            st.markdown(prompt)

        # Agent step.
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Thinking... ⏳")
            full_response = ""

            try:
                # Run the agent.
                response = get_agent_response(selected_agent, prompt, "test")
                full_response = handle_response_display(response, message_placeholder)
            except Exception as e:
                st.error(f"Error: {e}")
                full_response = "I encountered an error processing your request."

        # Save step.
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        HistoryManager.save(st.session_state.messages)
        st.rerun()


if __name__ == "__main__":
    main()
