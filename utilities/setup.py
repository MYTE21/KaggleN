import os
import uuid
from dotenv import load_dotenv
from IPython.display import Markdown

# Google ADK & GenAI Imports.
from google.genai import types
from google.adk.agents import Agent, LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import Runner, InMemoryRunner
from google.adk.sessions import InMemorySessionService


from google.adk.tools import google_search
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

from google.adk.apps.app import App, ResumabilityConfig
from google.adk.tools.function_tool import FunctionTool


# Load environment variables.
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


def get_kaggle_credentials() -> str | None:
    kaggle_api_key = os.getenv("KAGGLE_API_KEY")

    if not kaggle_api_key:
        print("⚠️ Authentication Error: 'KAGGLE_API_KEY' environment variable is missing.")
        return None

    try:
        os.environ["KAGGLE_API_KEY"] = kaggle_api_key
        print("✅ Kaggle API key setup complete.")
        return kaggle_api_key
    except Exception as e:
        print(f"⚠️ Error setting environment variables: {e}")


def get_notion_credentials() -> str | None:
    notion_api_key = os.getenv("NOTION_API_KEY")

    if not notion_api_key:
        print("⚠️ Authentication Error: 'NOTION_API_KEY' environment variable is missing.")
        return None

    try:
        os.environ["NOTION_API_KEY"] = notion_api_key
        print("✅ Notion API key setup complete.")
        return notion_api_key
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


if __name__ == "__main__":
    pass
