import random
import time
from typing import Generator, Any
import streamlit as st

# GOOGLE_API_KEY = setup.get_google_api_key(False)
# retry_config = setup.get_retry_config()


# -- Random Response --
def random_response() -> Generator[str, None, None]:
    response = random.choice([
        "The Amazon rainforest produces around 20% of the world’s oxygen; do you know that kind of massive ecosystem is still shrinking every year?",
        "Bananas are technically berries, but strawberries aren’t; do you know that kind of botanical twist comes from how the fruit develops?",
        "Your brain uses about 20% of your body’s energy; do you know that kind of demand is why thinking hard can actually feel tiring?"
    ])

    for word in response.split():
        yield word + " "
        time.sleep(0.05)

#
# # AI Agent
# async def gemini_agent(message: str) -> Any:
#     if "root_agent" not in st.session_state:
#         st.session_state.root_agent = Agent(
#             name="helpful_assistant",
#             model=Gemini(
#                 model="gemini-2.5-flash-lite",
#                 retry_options=retry_config
#             ),
#             description="A simple agent that can answer general questions.",
#             instruction="""
#                 You are a helpful and confident assistant.
#                 You are capable of searching Google for recent information using google_search tool.
#                 Use google_search for current information or if unsure.
#                 Whenever you reference information from Google Search, include the link in your answer.
#                 Create markdown formating, e.g., table, bulleted or numerical points, headings,
#                 and quotes if necessary. Also, consider creating a mermaid diagram if needed.
#                 """,
#             tools=[google_search]
#         )
#
#     runner = InMemoryRunner(agent=st.session_state.root_agent)
#
#     response = await runner.run_debug(message)
#     return response


if __name__ == "__main__":
    pass