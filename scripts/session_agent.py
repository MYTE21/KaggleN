# -- Imports --
# General Imports.
import os
from dotenv import load_dotenv
import asyncio

# Google ADK & GenAI Imports.
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
from google.genai import types
from google.adk.tools import google_search

# -- Setup --
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

APP_NAME = "agents"
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

        response_accumulator = []

        for query in user_queries:
            query = types.Content(role="user", parts=[types.Part(text=query)])

            async for event in runner_instance.run_async(
                user_id=USER_ID, session_id=session.id, new_message=query
            ):
                if event.content and event.content.parts:
                    parts_len = len(event.content.parts)
                    print(f"🦊 Event Content Part Length: {len(event.content.parts)}")
                    print(f"🎉 Event Content: {event.content}")
                    for i in range(parts_len):
                        chunk_text = event.content.parts[i].text
                        print(f"🐣 Chunk Text: {chunk_text}")
                        if (
                            event.content.parts[0].text != "None"
                            and event.content.parts[0].text
                        ):
                            response_accumulator.append(chunk_text)

        return "".join(response_accumulator)

    else:
        return None


# -- Agent Setup --
# Create the LLM Agent.
root_agent =LlmAgent(
    model=Gemini(model=MODEL_NAME, retry_options=retry_config),
    name="kagglen_agent",
    description="A text chatbot",
    tools=[google_search]
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


def run_chat_agent(message: str, session_name: str):
    response = asyncio.run(
        run_session(
            runner,
            [message],
            session_name,
        )
    )

    return response


if __name__ == "__main__":
    print(run_chat_agent("Generate a sample Python code.", "q"))
