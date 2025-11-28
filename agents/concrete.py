from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.tools import google_search

from agents.base import BaseAgent


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


class KaggleAgen(BaseAgent):
    def __init__(self):
        super().__init__()

    def _define_agent(self) -> LlmAgent:
        return LlmAgent(
            model=Gemini(model=self.model_name, retry_options=self.retry_config),
            name="kaggle_agent",
            description="An expert data scientist and Kaggle Grandmaster.",
            tools=[]
        )


class NotionAgent(BaseAgent):
    def __init__(self):
        super().__init__()

    def _define_agent(self) -> LlmAgent:
        return LlmAgent(
            model=Gemini(model=self.model_name, retry_options=self.retry_config),
            name="notion_agent",
            description="A productivity assistant managing Notion pages.",
            tools=[]
        )