# -- IMPORTS --
# General Imports.
import os
import asyncio
from abc import ABC, abstractmethod

from dotenv import load_dotenv
import config
import nest_asyncio

# Google ADK Imports.
from google.adk.agents import LlmAgent
from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
from google.genai import types


load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# -- SHARED CONFIGURATIONS --
DB_URL = config.DB_URL

# Singleton pattern: initialize service once.
_session_service = DatabaseSessionService(db_url=DB_URL)

class BaseAgent(ABC):
    """
    Agents must inherit this, and this will handle the async logic and session management.
    """
    def __init__(self):
        self.app_name = "agents"
        self.user_id = "default"
        self.model_name = config.MODEL_NAME

        # Setup retry config.
        self.retry_config = types.HttpRetryOptions(
            attempts=5,
            exp_base=7,
            initial_delay=1,
            http_status_codes=[429, 500, 503, 504],
        )

        # Abstract: Initialize the specific Agent
        self.agent_definition = self._define_agent()

        # Create the Runner.
        self.runner = Runner(
            agent=self.agent_definition,
            app_name=self.app_name,
            session_service=_session_service
        )


    @abstractmethod
    def _define_agent(self) -> LlmAgent:
        """
        Child classes must implement this to define their name and tools.
        """
        pass

    async def _run_async_session(self, user_query: str, session_id: str):
        """
        Core async logic for response.
        """
        # Get or create a session.
        session = await _session_service.get_session(
            app_name=self.app_name,
            user_id=self.user_id,
            session_id=session_id
        )

        if not session:
            session = await _session_service.create_session(
                app_name=self.app_name,
                user_id=self.user_id,
                session_id=session_id
            )

        if not session:
            raise ValueError(f"Could not create or retrieve session '{session_id}'. Check DB connection.")

        # Prepare query.
        query_content = types.Content(
            role="user",
            parts=[types.Part(text=user_query)]
        )
        response_accumulator = []

        # Run the stream.
        async for event in self.runner.run_async(
            user_id=self.user_id,
            session_id=session.id,
            new_message=query_content
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        chunk_text = part.text
                        response_accumulator.append(chunk_text)
                        yield chunk_text

    def run(self, message: str, session_id: str):
        accumulated_text = ""
        print(f"⚠️ ⚠️ ⚠️ : {message}")

        async def _execute():
            nonlocal accumulated_text
            async for chunk in self._run_async_session(message, session_id):
                accumulated_text += chunk

        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                nest_asyncio.apply()
                loop.run_until_complete(_execute())
            else:
                asyncio.run(_execute())
        except RuntimeError as e:
            if "There is no current event loop" in str(e):
                asyncio.run(_execute())
            else:
                raise e

        print(f"🔥 🔥 🔥 : {accumulated_text}")

        return accumulated_text


    def run_generator(self, message: str, session_id: str):
        pass
