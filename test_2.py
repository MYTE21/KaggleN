import asyncio
import os
from dotenv import load_dotenv

from google.genai import types
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search

# Assuming utilities.setup loads env vars or returns a dict
from utilities.setup import *
from modules import mcp_config

# 1. Ensure credentials are valid and accessible
# (This setup function likely sets os.environ['KAGGLE_USERNAME'] and 'KAGGLE_KEY')
get_google_api_key()
get_kaggle_credentials()
retry_config = get_retry_config()

# Retrieve credentials to pass to the agent
# k_username = os.environ.get("KAGGLE_USERNAME")
k_key = get_kaggle_credentials()
username = "machinelearning557"

if not k_key:
    raise ValueError("KAGGLE_USERNAME and KAGGLE_KEY environment variables must be set.")

mcp_kaggle_server = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command='npx',
            args=[
                '-y',
                'mcp-remote',
                'https://www.kaggle.com/mcp',
                "--header",
                f"Authorization: Bearer {k_key}"
            ],
            tool_filter=mcp_config.kaggle_tools
        ),
        timeout=30,
    )
)

print("✅ MCP Kaggle Toolset defined.")

instruction = f"""
    You are a Kaggle Data Science assistant. 

    CRITICAL AUTHENTICATION:
    1. Call 'authorize' immediately with username: "{username}" and key: "{k_key}".

    TO FIND USER NOTEBOOKS:
    The tool 'search_notebooks' is the only way to find notebooks. 
    To find the user's notebooks, you must call 'search_notebooks' with the search query set strictly to the username: "{username}".

    LIMITATIONS:
    - You might only see PUBLIC notebooks. If you cannot determine private status, state that clearly.
    - If the list returns exactly 20 items, tell the user there might be more due to pagination limits.

    Do not guess numbers. Count exactly what is returned in the tool output.
"""

root_agent = LlmAgent(
    name="helpful_agent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="A simple agent that can answer general questions.",
    # 3. FIX: Instruct the agent to authorize using the injected credentials
    instruction=instruction,
    tools=[mcp_kaggle_server],
)

print("✅ Root Agent defined.")

runner = InMemoryRunner(app_name="agents", agent=root_agent)

print("✅ Runner created.")

# The agent will now see the instruction to authorize first, then run the user query.
# response = asyncio.run(runner.run_debug("""What are the recent Kaggle competitions that are active?""", verbose=True))
# response = asyncio.run(runner.run_debug("""How many Kaggle notebooks have I created? List them.  """, verbose=True))
# response = asyncio.run(runner.run_debug("""I have provided the user name and key in the instruction. Can you tell me how many kaggle notebooks have i created. and how many are private and public?""", verbose=True))
# response = asyncio.run(runner.run_debug(""" me details about the notebook: "MYTE 21 Pandas Practice". Link: https://www.kaggle.com/code/machinelearning557/myte-21-pandas-practice""", verbose=True))
# response = asyncio.run(runner.run_debug("""Can you talk about this user: machinelearning557""", verbose=True))
response = asyncio.run(runner.run_debug("""Can you tell me the user names of the top in the leaderboard of "AI Mathematical Olympiad - Progress Prize 3" competition?""", verbose=True))