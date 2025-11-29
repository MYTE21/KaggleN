import asyncio
import os
from dotenv import load_dotenv

from google.genai import types
from google.adk.agents import Agent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner


from google.adk.tools import google_search

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
retry_config = types.HttpRetryOptions(
        attempts=5,
        exp_base=7,
        initial_delay=1,
        http_status_codes=[429, 500, 503, 504]
    )

root_agent = Agent(
    name="helpful_agent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="A simple agent that can answer general questions.",
    instruction="""
        You are a helpful and confident assistant. You are capable of searching Google for recent information using google_search tool. Use google_search for current information or if unsure. Whenever you reference information from Google Search, include the link in your answer. Create markdown formating, e.g., table, bulleted or numerical points, headings, and quotes if necessary. Also, consider creating a mermaid diagram if needed.
    """,
    tools=[google_search],
)

print("✅ Root Agent defined.")

runner = InMemoryRunner(app_name="agents", agent=root_agent)

print("✅ Runner created.")

response = asyncio.run(runner.run_debug("""What are the recent Kaggle competitions that are active, and rank them by price pool?"""))