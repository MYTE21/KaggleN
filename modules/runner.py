import asyncio
from agents.factory import AgentFactory


def get_agent_response(agent_type: str, user_prompt: str, session_id: str):
    try:
        loop = asyncio.get_event_loop()
    except:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    agent = AgentFactory()
    return agent.run_dynamic_agent(agent_type, user_prompt, session_id)