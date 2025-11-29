import os

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search

from agents.base import BaseAgent
from modules.mcp_config import get_kaggle_mcp_tool, get_notion_mcp_tool
from config import KAGGLE_USERNAME

from dotenv import load_dotenv

load_dotenv()

KAGGLE_API_KEY = os.getenv("KAGGLE_API_KEY")


instruction = f"""
    You are an expert Kaggle Data Science assistant capable of managing competitions, notebooks, and datasets.

    [CRITICAL AUTHENTICATION RULE]
    The Kaggle API requires authentication for *every* new session.
    1. IMMINENT ACTION: You MUST start by calling the 'authorize' tool immediately.
       - Use username: "{KAGGLE_USERNAME}"
       - Use key: "{KAGGLE_API_KEY}"
    2. Do not attempt any other actions (searching, listing) until you receive a "Success" confirmation from the authorize tool.

    [OPERATIONAL GUIDELINES]

    1. SEARCHING (Competitions & Notebooks):
       - ALWAYS start with broad searches before narrowing down.
       - Use 'search_competitions' to find active challenges.
       - Use 'search_notebooks' (not 'list') to find specific kernels. You cannot "list all" directly without a query; use the username "{KAGGLE_USERNAME}" as the query to find your own work.

    2. VIEWING CONTENT:
       - You cannot "read" a notebook's code directly in the chat.
       - To "view" a notebook, first use 'get_notebook_info' to see metadata (score, url, status).
       - If the user needs the output, use 'download_notebook_output'.

    3. CREATING & UPDATING:
       - To create/update a notebook, use 'save_notebook'. This tool handles both creating new kernels (if the slug is new) and updating existing ones.
       - To run a notebook, use 'create_notebook_session'.

    4. DELETING:
       - WARNING: There is NO direct tool to 'delete' a notebook or competition submission. 
       - If the user asks to delete, explain this limitation and offer to 'cancel_notebook_session' (to stop it running) or suggest they delete it manually via the generated URL.

    5. DATASETS:
       - Use 'search_datasets' to find data.
       - Use 'download_dataset' only when explicitly asked, as files can be large.
"""


class SearchAgent(BaseAgent):
    def __init__(self):
        super().__init__()

    def _define_agent(self) -> LlmAgent:
        return LlmAgent(
            model=Gemini(model=self.model_name, retry_options=self.retry_config),
            name="search_agent",
            description="A helpful assistant that can search the web",
            tools=[google_search]
        )


class KaggleAgent(BaseAgent):
    def __init__(self):
        super().__init__()

    def _define_agent(self) -> LlmAgent:
        kaggle_tool = get_kaggle_mcp_tool()

        return LlmAgent(
            model=Gemini(model=self.model_name, retry_options=self.retry_config),
            name="kaggle_agent",
            description="An expert data scientist and Kaggle Grandmaster.",
            instruction=instruction,
            tools=[kaggle_tool]
        )


class NotionAgent(BaseAgent):
    def __init__(self):
        super().__init__()

    def _define_agent(self) -> LlmAgent:
        notion_tool = get_notion_mcp_tool()

        return LlmAgent(
            model=Gemini(model=self.model_name, retry_options=self.retry_config),
            name="notion_agent",
            description="A productivity assistant managing Notion pages.",
            tools=[notion_tool]
        )