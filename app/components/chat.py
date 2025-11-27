import os
import streamlit as st
from google.genai import types
from dotenv import load_dotenv
from google.adk.models.google_llm import Gemini
from google.adk.agents import Agent, LlmAgent
from google.adk.tools import google_search
from google.adk.runners import Runner, InMemoryRunner


load_dotenv()

def get_google_api_key(use_vertexai: bool = True) -> str | None:
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


if __name__ == "__main__":
    pass