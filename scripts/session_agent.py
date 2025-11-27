# -- Imports --
# General Imports.
import os
from dotenv import load_dotenv
from typing import Any, Dict
import asyncio

# Google ADK & GenAI Imports.
from google.adk.agents import Agent, LlmAgent
from google.adk.apps.app import App, EventsCompactionConfig
from google.adk.models.google_llm import Gemini
from google.adk.sessions import DatabaseSessionService
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.tools.tool_context import ToolContext
from google.genai import types
from streamlit import session_state

# -- Setup --
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

APP_NAME = "default"
USER_ID = "default"
SESSION = "default"

MODEL_NAME = "gemini-2.5-flash-lite"

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

# -- Helper Function --
async def run_session(runner_instance: Runner, user_queries: list[str] | str = None, session_name: str = "default",):
    print(f"\n ### Session: {session_name}")

    app_name = runner_instance.app_name

    try:
        session = await session_service.create_session(
            app_name=app_name, user_id=USER_ID, session_id=session_name
        )
    except:
        session = await session_service.get_session(
            app_name=app_name, user_id=USER_ID, session_id=session_name
        )

    if user_queries:
        if type(user_queries) == str:
            user_queries = [user_queries]

        for query in user_queries:
            print(f"\nUser > {query}")

            query = types.Content(role="user", parts=[types.Part(text=query)])

            async for event in runner_instance.run_async(
                user_id=USER_ID, session_id=session.id, new_message=query
            ):
                if event.content and event.content.parts:
                    if (
                        event.content.parts[0].text != "None"
                        and event.content.parts[0].text
                    ):
                        print(f"{MODEL_NAME} > ", event.content.parts[0].text)
    else:
        print("No queries!")


# -- Agent Setup --
# Create the LLM Agent.
root_agent =LlmAgent(
    model=Gemini(model=MODEL_NAME, retry_options=retry_config),
    name="kagglen_agent",
    description="A text chatbot",
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_DIR, "../data")
os.makedirs(DATA_FOLDER, exist_ok=True)
DB_PATH = os.path.join(DATA_FOLDER, "my_agent_data.db")

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DB_PATH = os.path.join(BASE_DIR, "my_agent_data.db")
db_url = f"sqlite+aiosqlite:///{DB_PATH}"

session_service = DatabaseSessionService(db_url=db_url)

runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service
)


def run_chat_agent(message: str):
    asyncio.run(
        run_session(
            runner,
            [message],
            "session-1",
        )
    )


if __name__ == "__main__":
    run_chat_agent("What did I ask you about earlier?")
