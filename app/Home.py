import os
import streamlit as st
from components import title, chat
import asyncio
from google.genai import types
from dotenv import load_dotenv
from google.adk.models.google_llm import Gemini
from google.adk.agents import Agent, LlmAgent
from google.adk.tools import google_search
from google.adk.runners import Runner, InMemoryRunner


load_dotenv()


def get_google_api_key(use_vertexai: bool = True) -> str | None:
    """
    Configures the environment for Google Gen AI authentication.

    This function loads environment variables, ensures the Google API key is present,
    and configures the backend mode (Vertex AI vs. Gemini Developer API/AI Studio)
    by manipulating the 'GOOGLE_GENAI_USE_VERTEXAI'
    environment variable.

    Parameters:
        use_vertexai (bool): Determines the backend configuration.
            - If False: Explicitly sets 'GOOGLE_GENAI_USE_VERTEXAI' to "FALSE" to force the usage of the Gemini
            Developer API (AI Studio).
            - If True (Default): Removes 'GOOGLE_GENAI_USE_VERTEXAI' from the environment,
            if it exists, allowing the SDK to revert to its default behavior or pick up Vertex AI credentials.

    Returns:
        str | None: The loaded Google API Key if successful, or None if the key is missing from the environment.
    """
    google_api_key = os.getenv("GOOGLE_API_KEY")

    if not google_api_key:
        print("⚠️ Authentication Error: 'GOOGLE_API_KEY' environment variable is missing.")
        return None

    try:
        os.environ["GOOGLE_API_KEY"] = google_api_key
        if not use_vertexai:
            os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"
        else:
            os.environ.pop("GOOGLE_GENAI_USE_VERTEXAI", None)

        print("✅ Gemini API key setup complete.")
        return google_api_key
    except Exception as e:
        print(f"⚠️ Error setting environment variables: {e}")


def get_retry_config() -> types.HttpRetryOptions:
    """
    Creates a retry configuration for the Google Gen AI Client.
    """
    retry_config = types.HttpRetryOptions(
        attempts=5,
        exp_base=7,
        initial_delay=1,
        http_status_codes=[429, 500, 503, 504]
    )

    return retry_config


async def gemini_agent(message: str):
    if "root_agent" not in st.session_state:
        st.session_state.root_agent = Agent(
            name="helpful_assistant",
            model=Gemini(
                model="gemini-2.5-flash-lite",
                retry_options=get_retry_config()
            ),
            description="A simple agent that can answer general questions.",
            instruction="""
                You are a helpful and confident assistant. 
                You are capable of searching Google for recent information using google_search tool. 
                Use google_search for current information or if unsure. 
                Whenever you reference information from Google Search, include the link in your answer. 
                Create markdown formating, e.g., table, bulleted or numerical points, headings, 
                and quotes if necessary. Also, consider creating a mermaid diagram if needed.
                """,
            tools=[google_search]
        )

    runner = InMemoryRunner(agent=st.session_state.root_agent)

    response = await runner.run_debug(message)
    return response[0].content.parts[0].text


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
        response = st.write(asyncio.run(gemini_agent(prompt)))

    st.session_state.messages.append({"role": "assistant", "content": response})